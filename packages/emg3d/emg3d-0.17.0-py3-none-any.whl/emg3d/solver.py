"""
The actual multigrid solver routines. The most computationally intensive parts,
however, are in the :mod:`emg3d.core` as numba-jitted functions.
"""
# Copyright 2018-2021 The emg3d Developers.
#
# This file is part of emg3d.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.  You may obtain a copy
# of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations under
# the License.

import itertools
from dataclasses import dataclass

import numpy as np
import scipy.linalg as sl
import scipy.sparse.linalg as ssl

from emg3d import core, meshes, models, fields, utils

__all__ = ['solve', 'multigrid', 'smoothing', 'restriction', 'prolongation',
           'residual', 'krylov', 'MGParameters', 'RegularGridProlongator']


# MAIN USER-FACING FUNCTION
def solve(grid, model, sfield, efield=None, cycle='F', sslsolver=False,
          semicoarsening=False, linerelaxation=False, verb=1, **kwargs):
    r"""Solver for 3D CSEM data with tri-axial electrical anisotropy.

    The principal solver of `emg3d` is using the multigrid method as presented
    in [Muld06]_. Multigrid can be used as a standalone solver, or as a
    preconditioner for an iterative solver from the
    :mod:`scipy.sparse.linalg`-library, e.g.,
    :func:`scipy.sparse.linalg.bicgstab`. Alternatively, these Krylov subspace
    solvers can also be used without multigrid at all. See the `cycle` and
    `sslsolver` parameters.

    Implemented are the `F`-, `V`-, and `W`-cycle schemes for multigrid
    (`cycle` parameter), and the amount of smoothing steps (initial smoothing,
    pre-smoothing, coarsest-grid smoothing, and post-smoothing) can be set
    individually (`nu_init`, `nu_pre`, `nu_coarse`, and `nu_post`,
    respectively). The maximum level of coarsening can be restricted with the
    `clevel` parameter.

    Semicoarsening and line relaxation, as presented in [Muld07]_, are
    implemented, see the `semicoarsening` and `linerelaxation` parameters.
    Using the BiCGSTAB solver together with multigrid preconditioning with
    semicoarsening and line relaxation is slow but generally the most robust.
    Not using BiCGSTAB nor semicoarsening nor line relaxation is fast but may
    fail on stretched grids.


    Parameters
    ----------
    grid : :class:`emg3d.meshes.TensorMesh`
        The grid. See :class:`emg3d.meshes.TensorMesh`.

    model : :class:`emg3d.models.Model`
        The model. See :class:`emg3d.models.Model`.

    sfield : :class:`emg3d.fields.SourceField`
        The source field. See :func:`emg3d.fields.get_source_field`.

    efield : :class:`emg3d.fields.Field`, optional
        Initial electric field. It is initiated with zeroes if not provided. A
        provided efield MUST have frequency information (initiated with
        ``emg3d.fields.Field(..., freq)``).

        If an initial efield is provided nothing is returned, but the final
        efield is directly put into the provided efield.

        If an initial field is provided and a sslsolver is used, then it first
        carries out one multigrid cycle without semicoarsening nor line
        relaxation. The sslsolver is at times unstable with an initial guess,
        carrying out one MG cycle helps to stabilize it.

    cycle : str; optional.
        Type of multigrid cycle. Default is 'F'.

        - 'V': V-cycle, simplest version;
        - 'W': W-cycle, most expensive version;
        - 'F': F-cycle, sort of a compromise between 'V' and 'W';
        - None: Does not use multigrid, only `sslsolver`.

        If None, `sslsolver` must be provided, and the `sslsolver` will be used
        without multigrid pre-conditioning.

        Comparison of V (left), F (middle), and W (right) cycles for the case
        of four grids (three relaxation and prolongation steps)::

            h_
           2h_   \    /   \          /   \            /
           4h_    \  /     \    /\  /     \    /\    /
           8h_     \/       \/\/  \/       \/\/  \/\/


    sslsolver : str, optional
        A :mod:`scipy.sparse.linalg`-solver, to use with MG as pre-conditioner
        or on its own (if ``cycle=None``). Default is False.

        Current possibilities:

            - True or 'bicgstab': BIConjugate Gradient STABilized
              :func:`scipy.sparse.linalg.bicgstab`;
            - 'cgs': Conjugate Gradient Squared
              :func:`scipy.sparse.linalg.cgs`;
            - 'gcrotmk': GCROT: Generalized Conjugate Residual with inner
              Orthogonalization and Outer Truncation
              :func:`scipy.sparse.linalg.gcrotmk`.

        It does currently not work with 'cg', 'bicg', 'qmr', and 'minres' for
        various reasons (e.g., some require `rmatvec` in addition to `matvec`).

    semicoarsening : int; optional
        Semicoarsening. Default is False.

        - True: Cycling over 1, 2, 3.
        - 0 or False: No semicoarsening.
        - 1: Semicoarsening in x direction.
        - 2: Semicoarsening in y direction.
        - 3: Semicoarsening in z direction.
        - Multi-digit number containing digits from 0 to 3. Multigrid will
          cycle over these values, e.g., ``semicoarsening=1213`` will cycle
          over [1, 2, 1, 3].

    linerelaxation : int; optional
        Line relaxation. Default is False.

        This parameter is not respected on the coarsest grid, except if it is
        set to 0. If it is bigger than zero line relaxation on the coarsest
        grid is carried out along all dimensions which have more than 2 cells.

        - True: Cycling over [4, 5, 6].
        - 0 or False: No line relaxation.
        - 1: line relaxation in x direction.
        - 2: line relaxation in y direction.
        - 3: line relaxation in z direction.
        - 4: line relaxation in y and z directions.
        - 5: line relaxation in x and z directions.
        - 6: line relaxation in x and y directions.
        - 7: line relaxation in x, y, and z directions.
        - Multi-digit number containing digits from 0 to 7. Multigrid will
          cycle over these values, e.g., ``linerelaxation=1213`` will cycle
          over [1, 2, 1, 3].

        Note: Smoothing is generally done in lexicographical order, except for
        line relaxation in y direction; the reason is speed (memory access).

    verb : int; optional
        Level of verbosity (the higher the more verbose). Default is 1.

        - 0: Nothing.
        - 1: Warnings.
        - 2: One-liner at the end.
        - 3: Runtime and information about the method.
        - 4: Additional information for each MG-cycle.
        - 5: Everything (slower due to additional error computations).
        - -1: One-liner (dynamically updated).

    tol : float
        Convergence tolerance. Default is 1e-6.

        Iterations stop as soon as the norm of the residual has decreased by
        this factor, relative to the residual norm obtained for a zero
        electric field.

    maxit : int
        Maximum number of multigrid iterations. Default is 50.

        If `sslsolver` is used, this applies to the `sslsolver`.

        In the case that multigrid is used as a pre-conditioner for the
        `sslsolver`, the maximum iteration for multigrid is defined by the
        maximum length of the `linerelaxation` and `semicoarsening`-cycles.

    nu_init : int
        Number of initial smoothing steps, before MG cycle. Default is 0.

    nu_pre : int
        Number of pre-smoothing steps. Default is 2.

    nu_coarse : int
        Number of smoothing steps on coarsest grid. Default is 1.

    nu_post : int
        Number of post-smoothing steps. Default is 2.

    clevel : int
        The maximum coarsening level can be different for each dimension and
        is, by default, automatically determined (``clevel=-1``). The
        parameter `clevel` can be used to restrict the maximum coarsening
        level in any direction by its value.
        Default is -1.

    return_info : bool
        If True, a dictionary is returned with runtime info (final norm and
        number of iterations of MG and the sslsolver).

    log : int
        Only relevant if ``return_info=True``. Default is 1.

        - -1: LOG ONLY: Only store info in log, do not print on screen.
        - 0: SCREEN only: Only print info to screen, do not store in log.
        - 1: BOTH: Store info in log and print on screen.


    Returns
    -------
    efield : :class:`emg3d.fields.Field`
        Resulting electric field. Is not returned but replaced in-place if an
        initial efield was provided.

    info_dict : dict
        Dictionary with runtime info; only if ``return_info=True``.

        Keys:

        - `exit`: Exit status, 0=Success, 1=Failure;
        - `exit_message`: Exit message, check this if ``exit=1``;
        - `abs_error`: Absolute error;
        - `rel_error`: Relative error;
        - `ref_error`: Reference error [norm(sfield)];
        - `tol`: Tolerance (abs_error<ref_error*tol);
        - `it_mg`: Number of multigrid iterations;
        - `it_ssl`: Number of SSL iterations;
        - `time`: Runtime (s).
        - `runtime_at_cycle`: Runtime after each cycle (s).
        - `error_at_cycle`: Absolute error after each cycle.
        - `log`: Stored log.


    Examples
    --------
    >>> import emg3d
    >>> import numpy as np
    >>> # Create a simple grid, 8 cells of length 1 in each direction,
    >>> # starting at the origin.
    >>> grid = emg3d.TensorMesh(
    >>>         [np.ones(8), np.ones(8), np.ones(8)],
    >>>         origin=np.array([0, 0, 0]))
    >>> # The model is a fullspace with tri-axial anisotropy.
    >>> model = emg3d.Model(grid, property_x=1.5, property_y=1.8,
    >>>                     property_z=3.3, mapping='Resistivity')
    >>> # The source is a x-directed, horizontal dipole at (4, 4, 4)
    >>> # with a frequency of 10 Hz.
    >>> sfield = emg3d.fields.get_source_field(
    >>>         grid, src=[4, 4, 4, 0, 0], freq=10)
    >>> # Compute the electric signal.
    >>> efield = emg3d.solve(grid, model, sfield, verb=4)
    >>> # Get the corresponding magnetic signal.
    >>> hfield = emg3d.fields.get_h_field(grid, model, efield)
    .
    :: emg3d START :: 10:27:25 :: v0.9.1
    .
       MG-cycle       : 'F'                 sslsolver : False
       semicoarsening : False [0]           tol       : 1e-06
       linerelaxation : False [0]           maxit     : 50
       nu_{i,1,c,2}   : 0, 2, 1, 2          verb      : 4
       Original grid  :   8 x   8 x   8     => 512 cells
       Coarsest grid  :   2 x   2 x   2     => 8 cells
       Coarsest level :   2 ;   2 ;   2
    .
       [hh:mm:ss]  rel. error                  [abs. error, last/prev]   l s
    .
           h_
          2h_ \    /
          4h_  \/\/
    .
       [10:27:25]   2.284e-02  after   1 F-cycles   [1.275e-06, 0.023]   0 0
       [10:27:25]   1.565e-03  after   2 F-cycles   [8.739e-08, 0.069]   0 0
       [10:27:25]   1.295e-04  after   3 F-cycles   [7.232e-09, 0.083]   0 0
       [10:27:25]   1.197e-05  after   4 F-cycles   [6.685e-10, 0.092]   0 0
       [10:27:25]   1.233e-06  after   5 F-cycles   [6.886e-11, 0.103]   0 0
       [10:27:25]   1.415e-07  after   6 F-cycles   [7.899e-12, 0.115]   0 0
    .
       > CONVERGED
       > MG cycles        : 6
       > Final rel. error : 1.415e-07
    .
    :: emg3d END   :: 10:27:25 :: runtime = 0:00:00

    """

    # Solver settings; get from kwargs or set to default values.
    var = MGParameters(
            cycle=cycle, sslsolver=sslsolver, semicoarsening=semicoarsening,
            linerelaxation=linerelaxation, vnC=grid.vnC, verb=verb, **kwargs
    )

    # Start logging and print all parameters.
    var.cprint(f"\n:: emg3d START :: {var.time.now} :: "
               f"v{utils.__version__}\n", 2)
    var.cprint(var, 2)

    # Compute reference error for tolerance.
    var.l2_refe = sl.norm(sfield, check_finite=False)
    var.error_at_cycle[0] = var.l2_refe

    # Check sfield.
    if sfield.freq is None:
        raise ValueError(
                "Source field is missing frequency information;\n"
                "Create it with `emg3d.fields.get_source_field`, or\n"
                "initiate it with `emg3d.fields.SourceField`.")

    # Get volume-averaged model values.
    vmodel = models.VolumeModel(grid, model, sfield)

    # Get efield.
    if efield is None:
        # If not provided, initiate an empty one.
        efield = fields.Field(grid, dtype=sfield.dtype, freq=sfield._freq)

        # Set flag to return the field.
        var.do_return = True
    else:

        # Ensure efield has same data type as sfield.
        if sfield.dtype != efield.dtype:
            raise ValueError(
                    "Source field and electric field must have the\n same "
                    "dtype; complex (f-domain) or real (s-domain).\n Provided:"
                    f"sfield: {sfield.dtype}; efield: {efield.dtype}.")

        # If provided efield is missing frequency information, add it from the
        # source field.
        if efield.freq is None:
            efield._freq = sfield._freq

        # Set flag to NOT return the field.
        var.do_return = False

        # If efield is provided, check if it is already sufficiently good.
        var.l2 = residual(grid, vmodel, sfield, efield, True)
        if var.l2 < var.tol*var.l2_refe:

            # Switch-off both sslsolver and multigrid.
            var.sslsolver = None
            var.cycle = None

            # Start final info.
            var.exit_message = "CONVERGED"
            info = "   > NOTHING DONE (provided efield already good enough)\n"

    # Check if sfield is zero.
    if var.l2_refe < 100*np.finfo(float).tiny:

        # To avoid division by zero for the log.
        var.l2_refe = np.nan

        # Switch-off both sslsolver and multigrid.
        var.sslsolver = None
        var.cycle = None

        # Start final info.
        var.exit_message = "CONVERGED"
        info = "   > RETURN ZERO E-FIELD (provided sfield is zero)\n"

        # Zero-source means zero e-field.
        efield = fields.Field(grid, dtype=sfield.dtype, freq=sfield._freq)

    # Print header for iteration log.
    header = f"   [hh:mm:ss]  {'rel. error':<22}"
    if var.sslsolver:
        header += f"{'solver':<20}"
        if var.cycle:
            header += f"{'MG':<11} l s"
        var.cprint(header+"\n", 3)
    elif var.cycle:
        var.cprint(header+f"{'[abs. error, last/prev]':>29}   l s\n", 3)

    # Solve the system with...
    if var.sslsolver:  # ... sslsolver.
        krylov(grid, vmodel, sfield, efield, var)
    elif var.cycle:    # ... multigrid.
        multigrid(grid, vmodel, sfield, efield, var)

    # Get exit status.
    exit_status = int(var.exit_message != 'CONVERGED')

    # Print runtime information.
    if var.verb < 0 or var.verb == 2:
        var.one_liner(var.l2, True)
    elif var.verb > 2:
        if var.sslsolver:  # sslsolver-specific info.
            info = f"   > Solver steps     : {var._ssl_it}\n"
            if var.cycle:
                info += f"   > MG prec. steps   : {var.it}\n"
        elif var.cycle:    # multigrid-specific info.
            info = f"   > MG cycles        : {var.it}\n"
        info += f"   > Final rel. error : {var.l2/var.l2_refe:.3e}\n\n"
        info += f":: emg3d END   :: {var.time.now} :: "
        info += f"runtime = {var.time.runtime}\n"
        var.cprint(info, 2)
    elif var.verb == 1 and exit_status == 1:
        var.cprint(f"* WARNING :: {var.exit_message}", 0)

    # Assemble the info_dict if return_info
    if var.return_info:
        info_dict = {
            'exit': exit_status,               # Exit status.
            'exit_message': var.exit_message,  # Exit message.
            'abs_error': var.l2,               # Absolute error.
            'rel_error': var.l2/var.l2_refe,   # Relative error.
            'ref_error': var.l2_refe,    # Reference error [norm(sfield)].
            'tol': var.tol,              # Tolerance (abs_error<ref_error*tol).
            'it_mg': var.it,             # Multigrid iterations.
            'it_ssl': var._ssl_it,       # SSL iterations.
            'time': var.runtime_at_cycle[-1],          # Runtime (s).
            'runtime_at_cycle': var.runtime_at_cycle,  # Runtime at cycle (s).
            'error_at_cycle': var.error_at_cycle,      # Abs. error at cycle.
            'log': var.log_message,                    # Log.
        }

    # Return depending on input arguments; or nothing.
    if var.do_return and var.return_info:  # efield and info.
        return efield, info_dict
    elif var.do_return:                    # efield.
        return efield
    elif var.return_info:                  # info.
        return info_dict


# SOLVERS
def multigrid(grid, model, sfield, efield, var, **kwargs):
    """Multigrid solver for 3D controlled-source electromagnetic (CSEM) data.

    Multigrid solver as presented in [Muld06]_, including semicoarsening and
    line relaxation as presented in and [Muld07]_.

    - The electric field is stored in-place in `efield`.
    - The number of multigrid cycles is stored in `var.it`.
    - The current error (l2-norm) is stored in `var.l2`.
    - The reference error (l2-norm of sfield) is stored in `var.l2_refe`.

    This function is called by :func:`solve`.


    Parameters
    ----------
    grid : :class:`emg3d.meshes.TensorMesh`
        The grid. See :class:`emg3d.meshes.TensorMesh`.

    model : :class:`emg3d.models.VolumeModel`
        The Model. See :class:`emg3d.models.VolumeModel`.

    sfield : :class:`emg3d.fields.SourceField`
        The source field. See :func:`emg3d.fields.get_source_field`.

    efield : :class:`emg3d.fields.Field`
        The electric field. See :class:`emg3d.fields.Field`.

    var : :class:`MGParameters` instance
        As returned by :func:`multigrid`.

    **kwargs : Recursion parameters.
        Do not use; only used internally by recursion; `level` (current
        coarsening level) and `new_cycmax` (new maximum of MG cycles, takes
        care of V/W/F-cycling).

    """
    # Get recursion parameters.
    level = kwargs.get('level', 0)
    new_cycmax = kwargs.get('new_cycmax', 0)

    # Initiate iteration count.
    it = 0

    # Get cycmax (depends on cycle and on level [as a fct of sc_dir]).
    # This defines the V, W, and F-cycle scheme.
    if level == var.clevel[var.sc_dir]:
        cycmax = 1
    elif new_cycmax == 0 or var.cycle != 'F':
        cycmax = var.cycmax
    else:
        cycmax = new_cycmax
    cyc = 0  # Initiate cycle count.

    # Compute current error (l2-norms).
    l2_last = residual(grid, model, sfield, efield, True)

    # Initiate the error-array to check for stagnation.
    l2_stag = np.ones(var._maxcycle)*l2_last

    # Keep track on the levels during the first cycle, for QC.
    if var._first_cycle and var.verb > 3:
        var._level_all.append(level)

    # Print initial call info.
    if level == 0:
        var.cprint("     it cycmax               error", 4)
        var.cprint("      level [  dimension  ]            info\n", 4)
        if var.verb > 4:
            info = _print_gs_info(it, level, cycmax, grid, l2_last)
            var.cprint(info + "initial error", 4)

    # Initial smoothing (nu_init).
    if level == 0 and var.nu_init > 0:
        # Smooth and re-compute error.
        smoothing(grid, model, sfield, efield, var.nu_init, var.lr_dir)

        # Print initial smoothing info.
        if var.verb > 4:
            norm = residual(grid, model, sfield, efield, True)
            info = _print_gs_info(it, level, cycmax, grid, norm)
            var.cprint(info + "initial smoothing", 4)

    # Start the actual (recursive) multigrid cycle.
    while level == 0 or (level > 0 and it < cycmax):

        # Store errors for comparisons (previous and previous of same cycle).
        l2_prev = l2_last
        l2_stag[(it-1) % var._maxcycle] = l2_last

        if level == var.clevel[var.sc_dir]:  # (A) Coarsest grid, solve system.
            # Note that coarsest grid depends on semicoarsening (sc_dir). If
            # semicoarsening is carried out along the biggest dimension it
            # reduces the number of coarsening levels.

            # Gauss-Seidel on the coarsest grid.
            smoothing(grid, model, sfield, efield, var.nu_coarse, var.lr_dir)

            # Print coarsest grid smoothing info.
            if var.verb > 4:
                norm = residual(grid, model, sfield, efield, True)
                info = _print_gs_info(it, level, cycmax, grid, norm)
                var.cprint(info + "coarsest level", 4)

        else:                   # (B) Not yet on coarsest grid.

            # (B.1) Pre-smoothing (nu_pre).
            if var.nu_pre > 0:
                smoothing(grid, model, sfield, efield, var.nu_pre, var.lr_dir)

                # Print pre-smoothing info.
                if var.verb > 4:
                    norm = residual(grid, model, sfield, efield, True)
                    info = _print_gs_info(it, level, cycmax, grid, norm)
                    var.cprint(info + "pre-smoothing", 4)

            # Get sc_dir for this grid.
            sc_dir = _current_sc_dir(var.sc_dir, grid)

            # (B.2) Restrict grid, model, and fields from fine to coarse grid.
            res = residual(grid, model, sfield, efield)  # Get residual.
            cgrid, cmodel, csfield, cefield = restriction(
                    grid, model, sfield, res, sc_dir)

            # (B.3) Recursive call for coarse-grid correction.
            multigrid(cgrid, cmodel, csfield, cefield, var, level=level+1,
                      new_cycmax=cycmax-cyc)

            # (B.4) Add coarse field residual to fine grid field.
            prolongation(grid, efield, cgrid, cefield, sc_dir)

            # Append current prolongation level for QC.
            if var._first_cycle and var.verb > 3:
                var._level_all.append(level)

            # (B.5) Post-smoothing (nu_post).
            if var.nu_post > 0:
                smoothing(grid, model, sfield, efield, var.nu_post, var.lr_dir)

                # Print post-smoothing info.
                if var.verb > 4:
                    norm = residual(grid, model, sfield, efield, True)
                    info = _print_gs_info(it, level, cycmax, grid, norm)
                    var.cprint(info + "post-smoothing", 4)

        # Update iterator counts.
        it += 1         # Local iterator.
        if level == 0:  # Global iterator (works also when preconditioner.)
            var.it += 1

        # End loop depending if we are on the original grid or not.
        if level > 0:  # Update cyc if on a coarse grid.
            cyc += 1

        else:          # Original grid reached, check termination criteria.

            # Get current error (l2-norm).
            l2_last = residual(grid, model, sfield, efield, True)

            # Print end-of-cycle info.
            _print_cycle_info(var, l2_last, l2_prev)

            # Adjust semicoarsening and line relaxation if they cycle.
            if var.sc_cycle:
                var.sc_dir = next(var.sc_cycle)
            if var.lr_cycle:
                var.lr_dir = next(var.lr_cycle)

            # Check if any termination criteria is fulfilled.
            if _terminate(var, l2_last, l2_stag[(it-1) % var._maxcycle], it):
                break

    # Store final error (l2-norm).
    var.l2 = l2_last


def krylov(grid, model, sfield, efield, var):
    """Krylov Subspace iterative solver for 3D CSEM data.

    Using a Krylov subspace iterative solver (defined in `var.sslsolver`)
    implemented in SciPy with or without multigrid as a pre-conditioner
    ([Muld06]_).

    - The electric field is stored in-place in `efield`.
    - The current error (l2-norm) is stored in `var.l2`.
    - The reference error (l2-norm of sfield) is stored in `var.l2_refe`.

    This function is called by :func:`solve`.


    Parameters
    ----------
    grid : :class:`emg3d.meshes.TensorMesh`
        The grid. See :class:`emg3d.meshes.TensorMesh`.

    model : :class:`emg3d.models.VolumeModel`
        The Model. See :class:`emg3d.models.VolumeModel`.

    sfield : :class:`emg3d.fields.SourceField`
        The source field. See :func:`emg3d.fields.get_source_field`.

    efield : :class:`emg3d.fields.Field`
        The electric field. See :class:`emg3d.fields.Field`.

    var : :class:`MGParameters` instance
        As returned by :func:`multigrid`.

    """
    # Get frequency
    freq = sfield._freq

    # Define matrix operation A x as LinearOperator.
    def amatvec(efield):
        """Compute A x for solver; residual is b-Ax = src-amatvec."""

        # Cast current efield to Field instance.
        efield = fields.Field(grid, efield)

        # Compute A x.
        rfield = fields.Field(grid, dtype=efield.dtype, freq=freq)
        core.amat_x(
                rfield.fx, rfield.fy, rfield.fz,
                efield.fx, efield.fy, efield.fz, model.eta_x, model.eta_y,
                model.eta_z, model.zeta, grid.h[0], grid.h[1], grid.h[2])

        # Return Field instance.
        return -rfield

    # Initiate LinearOperator A x.
    A = ssl.LinearOperator(
            shape=(grid.nE, grid.nE), dtype=sfield.dtype, matvec=amatvec)

    # Define MG pre-conditioner as LinearOperator, if `var.cycle`.
    def mg_matvec(sfield):
        """Use multigrid as pre-conditioner."""

        # Cast current fields to Field instances.
        sfield = fields.Field(grid, sfield, freq=freq)
        efield = fields.Field(grid, dtype=sfield.dtype, freq=freq)

        # Solve for these fields.
        multigrid(grid, model, sfield, efield, var)

        return efield

    # Initiate LinearOperator M.
    M = None
    if var.cycle:
        M = ssl.LinearOperator(
                shape=(grid.nE, grid.nE), dtype=sfield.dtype, matvec=mg_matvec)

    # Define callback to keep track of sslsolver-iterations.
    def callback(x):
        """Solver iteration count and error (l2-norm)."""
        # Update iteration count.
        var._ssl_it += 1

        # Add current runtime and error to var.
        var.runtime_at_cycle = np.r_[var.runtime_at_cycle, var.time.elapsed]
        var.l2 = residual(grid, model, sfield, fields.Field(grid, x), True)
        var.error_at_cycle = np.r_[var.error_at_cycle, var.l2]

        # Print error (only if verbose).
        if var.verb > 3:

            log = f"   [{var.time.now}]   {var.l2/var.l2_refe:.3e} "
            log += f" after {var._ssl_it:3} {var.sslsolver}-cycles"

            # For those solvers who run an iteration before the first
            # preconditioner run ['gcrotmk'].
            if var._ssl_it == 1 and var.it == 0 and var.cycle is not None:
                log += "\n"

            var.cprint(log, 3)

        elif var.verb < 0:

            var.one_liner(var.l2)

    # Solve the system with sslsolver.
    # The ssl solvers do not abort if the norm diverges or is not finite. We
    # therefore throw an exception in `_terminate`, and catch it here.
    try:
        efield.field, i = getattr(ssl, var.sslsolver)(
                A=A, b=sfield, x0=efield, tol=var.tol, maxiter=var.ssl_maxit,
                atol=1e-30, M=M, callback=callback)
    except _ConvergenceError:
        i = -1  # Mark it as error; returned field is all zero.
        var.exit_message += " (returned field is zero)"

    # Convergence-checks for sslsolver.
    pre = "\n   > "
    if i < 0:
        if var.exit_message == '':
            var.exit_message = f"Error in {var.sslsolver} ({i})"
        pre = "\n* ERROR   :: "
    elif i > 0:
        var.exit_message = "MAX. ITERATION REACHED, NOT CONVERGED"
    else:
        var.exit_message = "CONVERGED"
    var.cprint(pre+var.exit_message, 2)


# MULTIGRID SUB-ROUTINES
def smoothing(grid, model, sfield, efield, nu, lr_dir):
    """Reducing high-frequency error by smoothing.

    Solves the linear equation system :math:`A x = b` iteratively using the
    Gauss-Seidel method. This acts as smoother or, on the coarsest grid, as a
    direct solver.


    This is a simple wrapper for the jitted computation in
    :func:`emg3d.core.gauss_seidel`, :func:`emg3d.core.gauss_seidel_x`,
    :func:`emg3d.core.gauss_seidel_y`, and
    :func:`emg3d.core.gauss_seidel_z` (`@njit` can not [yet] access class
    attributes). See these functions for more details and corresponding theory.

    The electric fields are updated in-place.

    This function is called by :func:`multigrid`.


    Parameters
    ----------
    grid : :class:`emg3d.meshes.TensorMesh`
        Input grid.

    model : :class:`emg3d.models.VolumeModel`
        Input model.

    sfield : :class:`emg3d.fields.SourceField`
        Input source field.

    efield : :class:`emg3d.fields.Field`
        Input electric field.

    nu : int
        Number of Gauss-Seidel steps; odd numbers are forward, even numbers are
        reversed. E.g., ``nu=2`` is one symmetric Gauss-Seidel iteration, with
        a forward and a backward step.

    lr_dir : int
        Direction of line relaxation {0, 1, 2, 3, 4, 5, 6, 7}.

    """

    # Collect Gauss-Seidel input (same for all routines)
    inp = (sfield.fx, sfield.fy, sfield.fz, model.eta_x, model.eta_y,
           model.eta_z, model.zeta, grid.h[0], grid.h[1], grid.h[2], nu)

    # Avoid line relaxation in a direction where there are only two cells.
    lr_dir = _current_lr_dir(lr_dir, grid)

    # Compute and store fields (in-place)
    if lr_dir == 0:             # Standard MG
        core.gauss_seidel(efield.fx, efield.fy, efield.fz, *inp)

    if lr_dir in [1, 5, 6, 7]:  # Line relaxation in x-direction
        core.gauss_seidel_x(efield.fx, efield.fy, efield.fz, *inp)

    if lr_dir in [2, 4, 6, 7]:  # Line relaxation in y-direction
        core.gauss_seidel_y(efield.fx, efield.fy, efield.fz, *inp)

    if lr_dir in [3, 4, 5, 7]:  # Line relaxation in z-direction
        core.gauss_seidel_z(efield.fx, efield.fy, efield.fz, *inp)


def restriction(grid, model, sfield, residual, sc_dir):
    """Downsampling of grid, model, and fields to a coarser grid.

    The restriction of the residual is used as source term for the coarse grid.

    Corresponds to Equations 8 and 9 in [Muld06]_ and surrounding text. In the
    case of the restriction of the residual, this function is a wrapper for the
    jitted functions :func:`emg3d.core.restrict_weights` and
    :func:`emg3d.core.restrict` (`@njit` can not [yet] access class
    attributes). See these functions for more details and corresponding theory.

    This function is called by :func:`multigrid`.


    Parameters
    ----------
    grid : :class:`emg3d.meshes.TensorMesh`
        Input grid.

    model : :class:`emg3d.models.VolumeModel`
        Input model.

    sfield : :class:`emg3d.fields.SourceField`
        Input source field.

    sc_dir : int
        Direction of semicoarsening (0, 1, 2, or 3).


    Returns
    -------
    cgrid : :class:`emg3d.meshes.TensorMesh`
        Coarse grid.

    cmodel : :class:`emg3d.models.VolumeModel`
        Coarse model.

    csfield : :class:`emg3d.fields.SourceField`
        Coarse source field. Corresponds to restriction of fine-grid residual.

    cefield : :class:`emg3d.fields.Field`
        Coarse electric field, complex zeroes.

    """

    # 1. RESTRICT GRID

    # We take every second element for the direction(s) of coarsening.
    rx, ry, rz = 2, 2, 2
    if sc_dir in [1, 5, 6]:  # No coarsening in x-direction.
        rx = 1
    if sc_dir in [2, 4, 6]:  # No coarsening in y-direction.
        ry = 1
    if sc_dir in [3, 4, 5]:  # No coarsening in z-direction.
        rz = 1

    # Compute distances of coarse grid.
    ch = [np.diff(grid.nodes_x[::rx]),
          np.diff(grid.nodes_y[::ry]),
          np.diff(grid.nodes_z[::rz])]

    # Create new `TensorMesh` instance for coarse grid
    cgrid = meshes._TensorMesh(ch, grid.origin)

    # 2. RESTRICT MODEL

    class VolumeModel:
        """Dummy class to create coarse-grid model."""
        def __init__(self, case):
            """Initialize with case."""
            self.case = case

    cmodel = VolumeModel(model.case)
    cmodel.eta_x = _restrict_model_parameters(model.eta_x, sc_dir)
    if model.case in [1, 3]:  # HTI or tri-axial.
        cmodel.eta_y = _restrict_model_parameters(model.eta_y, sc_dir)
    else:
        cmodel.eta_y = cmodel.eta_x
    if model.case in [2, 3]:  # VTI or tri-axial.
        cmodel.eta_z = _restrict_model_parameters(model.eta_z, sc_dir)
    else:
        cmodel.eta_z = cmodel.eta_x
    cmodel.zeta = _restrict_model_parameters(model.zeta, sc_dir)

    # 3. RESTRICT FIELDS

    # Get the weights (Equation 9 of [Muld06]_).
    wx, wy, wz = _get_restriction_weights(grid, cgrid, sc_dir)

    # Compute the source terms (Equation 8 in [Muld06]_).
    # Initiate zero field.
    csfield = fields.Field(cgrid, dtype=sfield.dtype, freq=sfield._freq)
    core.restrict(csfield.fx, csfield.fy, csfield.fz, residual.fx,
                  residual.fy, residual.fz, wx, wy, wz, sc_dir)

    # Ensure PEC and initiate empty e-field.
    csfield.ensure_pec
    cefield = fields.Field(cgrid, dtype=sfield.dtype, freq=sfield._freq)

    return cgrid, cmodel, csfield, cefield


def prolongation(grid, efield, cgrid, cefield, sc_dir):
    """Interpolating the electric field from coarse grid to fine grid.

    The prolongation from a coarser to a finer grid is the inverse process of
    the restriction (:func:`restriction`) from a finer to a coarser grid. The
    interpolated values of the coarse grid electric field are added to the fine
    grid electric field, in-place. Piecewise constant interpolation is used in
    the direction of the field, and bilinear interpolation in the other two
    directions.

    See Equation 10 in [Muld06]_ and surrounding text.

    This function is called by :func:`multigrid`.


    Parameters
    ----------
    grid, cgrid : :class:`emg3d.meshes.TensorMesh`
        Fine and coarse grids.

    efield, cefield : :class:`emg3d.fields.Field`
        Fine and coarse grid electric fields.

    sc_dir : int
        Direction of semicoarsening (0, 1, 2, or 3).

    """

    # Interpolate ex in y-z-slices.
    yz_points = _get_prolongation_coordinates(grid, 'y', 'z')
    fn = RegularGridProlongator(cgrid.nodes_y, cgrid.nodes_z, yz_points)
    for ixc in range(cgrid.vnC[0]):
        # Bilinear interpolation in the y-z plane
        hh = fn(cefield.fx[ixc, :, :]).reshape(grid.vnEx[1:], order='F')

        # Piecewise constant interpolation in x-direction
        if sc_dir not in [1, 5, 6]:
            efield.fx[2*ixc, :, :] += hh
            efield.fx[2*ixc+1, :, :] += hh
        else:
            efield.fx[ixc, :, :] += hh

    # Interpolate ey in x-z-slices.
    xz_points = _get_prolongation_coordinates(grid, 'x', 'z')
    fn = RegularGridProlongator(cgrid.nodes_x, cgrid.nodes_z, xz_points)
    for iyc in range(cgrid.vnC[1]):

        # Bilinear interpolation in the x-z plane
        hh = fn(cefield.fy[:, iyc, :]).reshape(grid.vnEy[::2], order='F')

        # Piecewise constant interpolation in y-direction
        if sc_dir not in [2, 4, 6]:
            efield.fy[:, 2*iyc, :] += hh
            efield.fy[:, 2*iyc+1, :] += hh
        else:
            efield.fy[:, iyc, :] += hh

    # Interpolate ez in x-y-slices.
    xy_points = _get_prolongation_coordinates(grid, 'x', 'y')
    fn = RegularGridProlongator(cgrid.nodes_x, cgrid.nodes_y, xy_points)
    for izc in range(cgrid.vnC[2]):

        # Bilinear interpolation in the x-y plane
        hh = fn(cefield.fz[:, :, izc]).reshape(grid.vnEz[:-1], order='F')

        # Piecewise constant interpolation in z-direction
        if sc_dir not in [3, 4, 5]:
            efield.fz[:, :, 2*izc] += hh
            efield.fz[:, :, 2*izc+1] += hh
        else:
            efield.fz[:, :, izc] += hh

    # Ensure PEC boundaries
    efield.ensure_pec


def residual(grid, model, sfield, efield, norm=False):
    r"""Computing the residual.

    Returns the complete residual as given in [Muld06]_, page 636, middle of
    the right column:

    .. math::

        \mathbf{r} = V \left( \mathrm{i}\omega\mu_0\mathbf{J_s}
                     + \mathrm{i}\omega\mu_0 \tilde{\sigma} \mathbf{E}
                     - \nabla \times \mu_\mathrm{r}^{-1} \nabla \times
                       \mathbf{E} \right) .

    This is a simple wrapper for the jitted computation in
    :func:`emg3d.core.amat_x` (`@njit` can not [yet] access class
    attributes). See :func:`emg3d.core.amat_x` for more details and
    corresponding theory.

    This function is called by :func:`multigrid`.


    Parameters
    ----------
    grid : :class:`emg3d.meshes.TensorMesh`
        Input grid.

    model : :class:`emg3d.models.VolumeModel`
        Input model.

    sfield : :class:`emg3d.fields.SourceField`
        Input source field.

    efield : :class:`emg3d.fields.Field`
        Input electric field.

    norm : bool
        If True, the error (l2-norm) of the residual is returned, not the
        residual.


    Returns
    -------
    residual : Field
        Returned if ``norm=False``. The residual field;
        :class:`emg3d.fields.Field` instance.

    norm : float
        Returned if ``norm=True``. The error (l2-norm) of the residual

    """
    # Get residual.
    rfield = sfield.copy()
    core.amat_x(rfield.fx, rfield.fy, rfield.fz, efield.fx, efield.fy,
                efield.fz, model.eta_x, model.eta_y, model.eta_z, model.zeta,
                grid.h[0], grid.h[1], grid.h[2])

    if norm:  # Return its error.
        return sl.norm(rfield, check_finite=False)
    else:     # Return residual.
        return rfield


# VARIABLE DATACLASS
@dataclass
class MGParameters:
    """Collect multigrid solver settings.

    This dataclass is used by the main :func:`solve`-routine. See
    :func:`solve` for a description of the mandatory and optional input
    parameters and more information .

    Returns
    -------
    var : class:`MGParameters`
        As required by :func:`multigrid`.

    """

    # (A) Parameters without default values (mandatory).
    verb: int
    cycle: str
    sslsolver: str
    linerelaxation: int
    semicoarsening: int
    vnC: tuple  # Finest grid dimension

    # (B) Parameters with default values
    # Convergence tolerance.
    tol: float = 1e-6
    # Maximum iteration.
    maxit: int = 50
    # Initial fine-grid smoothing steps before first iteration.
    nu_init: int = 0
    # Pre-smoothing steps.
    nu_pre: int = 2
    # Smoothing steps on coarsest grid.
    nu_coarse: int = 1
    # Post-smoothing steps.
    nu_post: int = 2
    # Coarsest level; automatically determined if a negative number is given.
    clevel: int = -1

    # Whether or not to return info.
    return_info: bool = False
    # Log verbosity.
    log: int = 1
    log_message: str = ''

    def __post_init__(self):
        """Set and check some of the parameters."""

        # 0. Set some additional variables.
        self._level_all = list()   # To keep track of the levels for QC-figure.
        self._first_cycle = True   # Flag if in first cycle for QC-figure.
        self.it = 0                # To store MG cycle count.
        self._ssl_it = 0           # To store solver iteration count.
        self.l2 = 1.0              # To store current error.
        self.l2_refe = 1.0         # To store reference error.
        self.exit_message = ''     # For convergence status.

        self.time = utils.Time()   # Timer.
        self.runtime_at_cycle = np.array([0.])  # Store runtime per cycle.
        self.error_at_cycle = np.array([0.])    # Store error per cycle.
        self.do_return = True      # Whether or not to return the efield.

        # 1. Set everything related to semicoarsening and line relaxation.
        self._semicoarsening()
        self._linerelaxation()

        # 2. Set everything to used solver and MG-cycle.
        self._solver_and_cycle()

        # 3. Check max coarsening level.
        self.max_level

    def __repr__(self):
        """Print all relevant parameters."""

        outstring = (
            f"   MG-cycle       : {self.cycle!r:17}"
            f"   sslsolver : {self.sslsolver!r}\n"
            f"   semicoarsening : {self._p_sc_dir:17}"
            f"   tol       : {self.tol}\n"
            f"   linerelaxation : {self._p_lr_dir:17}"
            f"   maxit     : {self._maxit}\n"
            f"   nu_{{i,1,c,2}}   : {self.nu_init}, {self.nu_pre}"
            f", {self.nu_coarse}, {self.nu_post}       "
            f"   verb      : {self.verb}\n"
            f"   Original grid  "
            f": {self.vnC[0]:3} x {self.vnC[1]:3} x {self.vnC[2]:3}  "
            f"   => {self.vnC[0]*self.vnC[1]*self.vnC[2]:,} cells\n"
            f"   Coarsest grid  : {self.pclevel['vnC'][0]:3} "
            f"x {self.pclevel['vnC'][1]:3} x {self.pclevel['vnC'][2]:3}  "
            f"   => {self.pclevel['nC']:,} cells\n"
            f"   Coarsest level : {self.pclevel['clevel'][0]:3} "
            f"; {self.pclevel['clevel'][1]:3} ;{self.pclevel['clevel'][2]:4} "
            f"  {self.pclevel['message']}"
            f"\n"
        )

        return outstring

    @property
    def max_level(self):
        r"""Sets dimension-dependent level variable `clevel`.

        Requires at least two cells in each direction (for `nCx`, `nCy`, and
        `nCz`).
        """
        # Store input clevel for checks.
        inp_clevel = np.inf if self.clevel < 0 else self.clevel

        # Store maximum division-by-two level for each dimension.
        # After that, clevel = [nx, ny, nz], where nx, ny, and nz are the
        # number of times you can divide by two in this dimension.
        clevel = np.zeros(3, dtype=np.int_)
        for i in range(3):
            n = self.vnC[i]
            while n % 2 == 0 and n > 2:
                clevel[i] += 1
                n /= 2

        # Restrict to max coarsening level provided by user.
        for i in range(3):
            if self.clevel > -1 and self.clevel < clevel[i]:
                clevel[i] = self.clevel

        # Set overall clevel and store.
        self.clevel = np.array(
            [max(clevel[0], clevel[1], clevel[2]),  # Max-level if sc_dir=0
             max(clevel[1], clevel[2]),             # Max-level if sc_dir=1
             max(clevel[0], clevel[2]),             # Max-level if sc_dir=2
             max(clevel[0], clevel[1])]             # Max-level if sc_dir=3
        )

        # Store coarsest nr of cells on coarsest grid and dimension for the
        # log-printing.
        sx = int(self.vnC[0]/2**clevel[0])
        sy = int(self.vnC[1]/2**clevel[1])
        sz = int(self.vnC[2]/2**clevel[2])
        self.pclevel = {'nC': sx*sy*sz, 'vnC': (sx, sy, sz), 'clevel': clevel}

        # Check some grid characteristics. Good values up to 1024 are:
        # - 2*2^{2, ..., 9}: 8, 16,  32,  64, 128, 256, 512, 1024,
        # - 3*2^{2, ..., 8}: 12, 24,  48,  96, 192, 384, 768,
        # - 5*2^{2, ..., 7}: 20, 40,  80, 160, 320, 640,
        # - 7*2^{2, ..., 7}: 28, 56, 112, 224, 448, 896,
        # and preference decreases from top to bottom row.

        # Check if number on coarsest grid is bigger than 7.
        # Ignore if clevel was provided and also reached (user wants it).
        check_inp = zip(clevel, [sx, sy, sz])
        low_prime = any([cl < inp_clevel and sl > 7 for cl, sl in check_inp])
        # Check if it can be at least 3 (or inp_clevel) times coarsened.
        min_div = any(clevel < min(inp_clevel, 3))
        # Raise warning if necessary.
        if low_prime or min_div:
            self.pclevel['message'] = "  :: Grid not optimal for MG solver ::"
        else:
            self.pclevel['message'] = ""

        # Check at least two cells in each direction
        if np.any(np.array(self.vnC) < 2):
            raise ValueError(
                    "Nr. of cells must be at least two in each direction\n"
                    "Provided shape: "
                    f"({self.vnC[0]}, {self.vnC[1]}, {self.vnC[2]}).")

    def cprint(self, info, verbosity, **kwargs):
        """Conditional printing.

        Prints `info` if `self.verb` > `verbosity`.

        Parameters
        ----------
        info : str
            String to be printed.

        verbosity : int
            Verbosity of info.

        kwargs : optional
            Arguments passed to `print`.

        """
        if self.verb > verbosity:
            if self.log != 0:
                self.log_message += str(info)+'\n'
            if self.log >= 0:
                print(info, **kwargs)

    def one_liner(self, l2_last, last=False):
        """Print continuously updated one-liner.

        Parameters
        ----------
        l2_last : float
            Current error.

        last : bool
            If True, adds `exit_message` and finishes line.

        """
        # Collect info.
        info = f":: emg3d :: {l2_last/self.l2_refe:.1e}; "  # Absolute error.
        if self.sslsolver:  # For multigrid as preconditioner.
            info += f"{self._ssl_it}({self.it}); "
        else:               # Stand-alone multigrid.
            info += f"{self.it}; "
        info += f"{self.time.runtime}"  # Runtime

        # Print depending on `exit`.
        if last:
            self.cprint(info+f"; {self.exit_message}", -100)
        else:
            self.cprint(info, -100, end='\r')

    def _semicoarsening(self):
        """Set everything related to semicoarsening."""

        # Check input.
        if self.semicoarsening is True:            # If True, cycle [1, 2, 3].
            sc_cycle = np.array([1, 2, 3])
            self.sc_cycle = itertools.cycle(sc_cycle)
        elif self.semicoarsening in np.arange(4):  # If 0-4, use this.
            sc_cycle = np.array([int(self.semicoarsening)])
            self.sc_cycle = False
        else:                                      # Else, use numbers.
            sc_cycle = np.array([int(x) for x in
                                 str(abs(self.semicoarsening))])
            self.sc_cycle = itertools.cycle(sc_cycle)

            # Ensure numbers are within 0 <= sc_dir <= 3
            if np.any(sc_cycle < 0) or np.any(sc_cycle > 3):
                raise ValueError(
                        "`semicoarsening` must be one of "
                        "(False, True, 0, 1, 2, 3).\n"
                        f"{' ':>13} Or a combination of (0, 1, 2, 3) to cycle,"
                        f" e.g. 1213.\n{'Provided:':>23} "
                        f"semicoarsening={self.semicoarsening}.")

        # Get first (or only) direction.
        if self.sc_cycle:
            self.sc_dir = next(self.sc_cycle)
        else:
            self.sc_dir = sc_cycle[0]

        # Set semicoarsening to True/False; print statement
        self.semicoarsening = self.sc_dir != 0
        self._p_sc_dir = f"{self.semicoarsening} {sc_cycle}"
        self._raw_sc_cycle = sc_cycle

    def _linerelaxation(self):
        """Set everything related to line relaxation."""

        # Check input.
        if self.linerelaxation is True:            # If True, cycle [1, 2, 3].
            lr_cycle = np.array([4, 5, 6])
            self.lr_cycle = itertools.cycle(lr_cycle)
        elif self.linerelaxation in np.arange(8):  # If 0-7, use this.
            lr_cycle = np.array([int(self.linerelaxation)])
            self.lr_cycle = False
        else:                                      # Else, use numbers.
            lr_cycle = np.array([int(x) for x in
                                 str(abs(self.linerelaxation))])
            self.lr_cycle = itertools.cycle(lr_cycle)

            # Ensure numbers are within 0 <= lr_dir <= 7
            if np.any(lr_cycle < 0) or np.any(lr_cycle > 7):
                raise ValueError(
                        "`linerelaxation` must be one of "
                        f"(False, True, 0, 1, 2, 3, 4, 5, 6, 7).\n"
                        f"{' ':>13} Or a combination of (1, 2, 3, 4, 5, 6, 7) "
                        f"to cycle, e.g. 1213.\n{'Provided:':>23} "
                        f"linerelaxation={self.linerelaxation}.")

        # Get first (only) direction
        if self.lr_cycle:
            self.lr_dir = next(self.lr_cycle)
        else:
            self.lr_dir = lr_cycle[0]

        # Set linerelaxation to True/False; print statement
        self.linerelaxation = self.lr_dir != 0
        self._p_lr_dir = f"{self.linerelaxation} {lr_cycle}"
        self._raw_lr_cycle = lr_cycle

    def _solver_and_cycle(self):
        """Set everything related to solver and MG-cycle."""

        # sslsolver.
        solvers = ['bicgstab', 'cgs', 'gcrotmk']
        if self.sslsolver is True:
            self.sslsolver = 'bicgstab'
        elif self.sslsolver is not False and self.sslsolver not in solvers:
            raise ValueError(
                    f"`sslsolver` must be True, False, or one of {solvers}.\n"
                    f"Provided: sslsolver={self.sslsolver!r}.")

        if self.cycle not in ['F', 'V', 'W', None]:
            raise ValueError(
                    "`cycle` must be one of {'F', 'V', 'W', None}.\n"
                    f"Provided: cycle={self.cycle}.")

        # Add maximum MG cycles depending on cycle
        if self.cycle in ['F', 'W']:
            self.cycmax = 2
        else:
            self.cycmax = 1

        # Ensure at least cycle or sslsolver is set
        if not self.sslsolver and not self.cycle:
            raise ValueError(
                    "At least `cycle` or `sslsolver` is required.\nProvided"
                    f"input: cycle={self.cycle}; sslsolver={self.sslsolver}.")

        # Store maxit in ssl_maxit and adjust maxit if sslsolver.
        self.ssl_maxit = 0             # Maximum iteration
        self._maxit = f"{self.maxit}"  # For printing
        self._maxcycle = max(len(self._raw_sc_cycle), len(self._raw_lr_cycle))
        if self.sslsolver:
            self.ssl_maxit = self.maxit
            if self.cycle is not None:  # Only if MG is used
                self.maxit = self._maxcycle
                self._maxit += f" ({self.maxit})"  # For printing


# INTERPOLATION DATACLASS
class RegularGridProlongator:
    """Prolongate field from coarse to fine grid.

    This is a heavily modified and adapted version of
    :class:`scipy.interpolate.RegularGridInterpolator`.

    The main difference (besides the pre-sets) is that this version allows to
    initiate an instance with the coarse and fine grids. This initialize will
    compute the required weights, and it has therefore only to be done once.

    After this, interpolating values from the coarse to the fine grid can be
    carried out much faster.

    Simplifications in comparison to
    :class:`scipy.interpolate.RegularGridInterpolator`:

    - No sanity checks what-so-ever.
    - Only 2D data;
    - ``method='linear'``;
    - ``bounds_error=False``;
    - ``fill_value=None``.

    It results in a speed-up factor of about 2, independent of grid size, for
    this particular case. The prolongation is the second-most expensive part of
    multigrid after the smoothing. Trying to improve this further might
    therefore be useful.

    Parameters
    ----------
    x, y : ndarray
        The x/y-coordinates defining the coarse grid.

    cxy : ndarray of shape (..., 2)
        The ([[x], [y]]).T-coordinates defining the fine grid.

    """

    def __init__(self, x, y, cxy):
        self.size = cxy.shape[0]
        self._set_edges_and_weights((x, y), cxy)

    def __call__(self, values):
        """Return values of coarse grid on fine grid locations.

        Parameters
        ----------
        values : ndarray
            Values corresponding to x/y-coordinates.

        Returns
        -------
        result : ndarray
            Values corresponding to cxy-coordinates.

        """
        # Initiate result.
        result = 0.

        # Find relevant values.
        for n, edge_indices in enumerate(self._get_edges_copy()):
            result += np.asarray(values[edge_indices]) * self.weight[n, :]

        return result

    def _set_edges_and_weights(self, xy, cxy):
        """Compute weights to go from xy- to cxy-coordinates."""

        # Find relevant edges between which cxy are situated.
        indices = []

        # Compute distance to lower edge in unity units.
        norm_distances = []

        # Iterate through dimensions.
        for x, grid in zip(cxy.T, xy):
            i = np.searchsorted(grid, x) - 1
            i[i < 0] = 0
            i[i > grid.size - 2] = grid.size - 2
            indices.append(i)
            norm_distances.append((x - grid[i]) / (grid[i + 1] - grid[i]))

        # Find relevant values; each i and i+1 represents a edge.
        self.edges = itertools.product(*[[i, i + 1] for i in indices])

        # Compute weights.
        self.weight = np.ones((4, self.size))
        for n, edge_indices in enumerate(self._get_edges_copy()):
            partial_weight = 1.
            for ei, i, yi in zip(edge_indices, indices, norm_distances):
                partial_weight *= np.where(ei == i, 1 - yi, yi)
            self.weight[n, :] = partial_weight

    def _get_edges_copy(self):
        """Return a copy of the edges-iterator."""
        self.edges, edges = itertools.tee(self.edges)
        return edges


# MG HELPER ROUTINES
def _current_sc_dir(sc_dir, grid):
    """Return current direction(s) for semicoarsening.

    Semicoarsening is defined in `self.sc_dir`. Here `self.sc_dir` is checked
    with which directions can actually still be halved, and depending on that,
    an adjusted `sc_dir` is returned for this particular grid.


    Parameters
    ----------
    grid : :class:`emg3d.meshes.TensorMesh`
        Input grid.

    sc_dir : int
        Direction of semicoarsening.

    Returns
    -------
    c_sc_dir : int
        Current direction of semicoarsening.

    """
    # Find out in which direction we want to half the number of cells.
    # This depends on an (optional) direction of semicoarsening, and
    # if the number of cells in a direction can still be halved.
    xsc_dir = grid.vnC[0] % 2 != 0 or grid.vnC[0] < 3 or sc_dir == 1
    ysc_dir = grid.vnC[1] % 2 != 0 or grid.vnC[1] < 3 or sc_dir == 2
    zsc_dir = grid.vnC[2] % 2 != 0 or grid.vnC[2] < 3 or sc_dir == 3

    # Set current sc_dir depending on the above outcome.
    if xsc_dir:
        if ysc_dir:
            c_sc_dir = 6  # Only coarsen in z-direction.
        elif zsc_dir:
            c_sc_dir = 5  # Only coarsen in y-direction.
        else:
            c_sc_dir = 1  # Coarsen in y- and z-directions.
    elif ysc_dir:
        if zsc_dir:
            c_sc_dir = 4  # Only coarsen in x-direction.
        else:
            c_sc_dir = 2  # Coarsen in x- and z-directions.
    elif zsc_dir:
        c_sc_dir = 3  # Coarsen in x- and y-directions.
    else:
        c_sc_dir = 0  # Coarsen in all directions.

    return c_sc_dir


def _current_lr_dir(lr_dir, grid):
    """Return current direction(s) for line relaxation.

    Line relaxation is defined in `self.lr_dir`. Here `self.lr_dir` is checked
    with the dimension of the grid, to avoid line relaxation in a direction
    where there are only two cells.


    Parameters
    ----------
    grid : :class:`emg3d.meshes.TensorMesh`
        Input grid.

    lr_dir : int
        Direction of line relaxation {0, 1, 2, 3, 4, 5, 6, 7}.


    Returns
    -------
    lr_dir : int
        Current direction of line relaxation.

    """
    lr_dir = np.copy(lr_dir)

    if grid.vnC[0] == 2:  # Check x-direction.
        if lr_dir == 1:
            lr_dir = 0
        elif lr_dir == 5:
            lr_dir = 3
        elif lr_dir == 6:
            lr_dir = 2
        elif lr_dir == 7:
            lr_dir = 4

    if grid.vnC[1] == 2:  # Check y-direction.
        if lr_dir == 2:
            lr_dir = 0
        elif lr_dir == 4:
            lr_dir = 3
        elif lr_dir == 6:
            lr_dir = 1
        elif lr_dir == 7:
            lr_dir = 5

    if grid.vnC[2] == 2:  # Check z-direction.
        if lr_dir == 3:
            lr_dir = 0
        elif lr_dir == 4:
            lr_dir = 2
        elif lr_dir == 5:
            lr_dir = 1
        elif lr_dir == 7:
            lr_dir = 6

    return lr_dir


def _print_cycle_info(var, l2_last, l2_prev):
    """Print cycle info to log.

    Parameters
    ----------
    var : `MGParameters` instance
        As returned by :func:`multigrid`.

    l2_last, l2_prev : float
        Last and previous errors (l2-norms).

    """
    # Add current runtime to var.
    var.runtime_at_cycle = np.r_[var.runtime_at_cycle, var.time.elapsed]
    var.error_at_cycle = np.r_[var.error_at_cycle, l2_last]

    # Start info string, return if not enough verbose.
    if var.verb < 0:  # One-liner
        var.one_liner(l2_last)
        return
    elif var.verb < 4:
        # Set first_cycle to False, to stop logging.
        return
    elif var.verb > 4:
        info = "\n"
    else:
        info = ""

    # Add multigrid-cycle visual QC on first cycle.
    if var._first_cycle:

        # Cast levels into array, get maximum.
        _lvl_all = np.array(var._level_all, dtype=np.int_)
        lvl_max = np.max(_lvl_all)

        # Get levels, multiply by difference to get +/-.
        lvl = (_lvl_all[1:] + _lvl_all[:-1])//2+1
        lvl *= _lvl_all[1:] - _lvl_all[:-1]

        # Create info string.
        out = ["       h_\n"]
        slen = min(len(lvl), 70)
        for cl in range(lvl_max):
            out += f"   {2**(cl+1):4}h_ "
            out += [" " if abs(lvl[v]) != cl+1 else "\\" if
                    lvl[v] > 0 else "/" for v in range(slen)]
            if cl < lvl_max-1:
                out.append("\n")

        # Add the cycle to inf.
        info += "".join(out)
        info += "\n\n"
        if len(lvl) > 70:
            info += "  (Cycle-QC restricted to first 70 steps of "
            info += f"{len(lvl)} steps.)\n"

        # Set first_cycle to False, to reduce verbosity from now on.
        var._first_cycle = False

    # Add iteration log.
    info += f"   [{var.time.now}]   {l2_last/var.l2_refe:.3e}  "
    if var.sslsolver:  # For multigrid as preconditioner.
        info += f"after {19*' '} {var.it:3} {var.cycle}-cycles "

    else:              # For multigrid as solver.
        info += f"after {var.it:3} {var.cycle}-cycles   "
        info += f"[{l2_last:.3e}, {l2_last/l2_prev:.3f}]"
    info += f"   {var.lr_dir} {var.sc_dir}"

    if var.verb > 4:
        info += "\n"

    # Print the info.
    var.cprint(info, 3)


def _print_gs_info(it, level, cycmax, grid, norm):
    """Return info-string to log after each Gauss-Seidel smoothing step.

    Parameters
    ----------
    it : int
        Iteration number.

    level : int
        Current coarsening level.

    cycmax : int
        Maximum MG cycles.

    grid : :class:`emg3d.meshes.TensorMesh`
        Input grid.

    norm : float
        Current error (l2-norm).


    Returns
    -------
    info : str
        Info string.

    """
    info = f"     {it:2} {level} {cycmax} [{grid.vnC[0]:3}, {grid.vnC[1]:3}, "
    return info + f"{grid.vnC[2]:3}]: {norm:.3e} "


def _terminate(var, l2_last, l2_stag, it):
    """Return multigrid termination flag.

    Checks all termination criteria and returns True if at least one is
    fulfilled.


    Parameters
    ----------
    var : `MGParameters` instance
        As returned by :func:`multigrid`.

    l2_last, l2_stag : float
        Last error and error for stagnation comparison (l2-norms).

    it : int
        Iteration number.


    Returns
    -------
    finished : bool
        Boolean indicating if multigrid is finished.

    """

    finished = False
    sslabort = False

    if l2_last < var.tol*var.l2_refe:    # Converged.
        var.exit_message = "CONVERGED"
        finished = True

    elif l2_last > 10*var.l2_refe or not np.isfinite(l2_last):  # Diverged.
        var.exit_message = "DIVERGED"
        finished = True
        sslabort = True  # Force abort if sslsolver.

    elif it > 2 and l2_last >= l2_stag:  # Stagnated.
        var.exit_message = "STAGNATED"
        finished = True
        sslabort = True  # Force abort if sslsolver.
        # Note: SSL will not fall into this, as it compares to the last value
        #       of the same cycle type. However, if used as preconditioner each
        #       cycle-type is only run once, before returning to the SSL.

    elif it == var.maxit:                # Maximum iterations reached.
        if not var.sslsolver:
            var.exit_message = "MAX. ITERATION REACHED, NOT CONVERGED"
        finished = True

    # Force abort (ssl solver) or print info.
    if finished:
        if var.sslsolver and sslabort:  # Force abortion of SSL solver.
            raise _ConvergenceError
        elif not var.sslsolver:  # Print info (if not preconditioner).
            if var.verb < 5:
                add = "\n"
            else:
                add = ""
            var.cprint(add+"   > "+var.exit_message, 2)

    return finished


def _restrict_model_parameters(param, sc_dir):
    """Restrict model parameters.

    Parameters
    ----------
    param : ndarray
        Model parameter to restrict.

    sc_dir : int
        Direction of semicoarsening.

    Returns
    -------
    out : ndarray
        Restricted model parameter.

    """
    if sc_dir == 1:    # Only sum the four cells in y-z-plane
        out = param[:, :-1:2, :-1:2] + param[:, 1::2, :-1:2]
        out += param[:, :-1:2, 1::2] + param[:, 1::2, 1::2]
    elif sc_dir == 2:  # Only sum the four cells in x-z-plane
        out = param[:-1:2, :, :-1:2] + param[1::2, :, :-1:2]
        out += param[:-1:2, :, 1::2] + param[1::2, :, 1::2]
    elif sc_dir == 3:  # Only sum the four cells in x-y-plane
        out = param[:-1:2, :-1:2, :] + param[1::2, :-1:2, :]
        out += param[:-1:2, 1::2, :] + param[1::2, 1::2, :]
    elif sc_dir == 4:  # Only sum the two cells in x-direction
        out = param[:-1:2, :, :] + param[1::2, :, :]
    elif sc_dir == 5:  # Only sum the two cells y-direction
        out = param[:, :-1:2, :] + param[:, 1::2, :]
    elif sc_dir == 6:  # Only sum the two cells z-direction
        out = param[:, :, :-1:2] + param[:, :, 1::2]
    else:            # Standard: Sum all 8 cells.
        out = param[:-1:2, :-1:2, :-1:2] + param[1::2, :-1:2, :-1:2]
        out += param[:-1:2, :-1:2, 1::2] + param[1::2, :-1:2, 1::2]
        out += param[:-1:2, 1::2, :-1:2] + param[1::2, 1::2, :-1:2]
        out += param[:-1:2, 1::2, 1::2] + param[1::2, 1::2, 1::2]
    return out


def _get_restriction_weights(grid, cgrid, sc_dir):
    """Return restriction weights.

    Return the weights (Equation 9 of [Muld06]_). The corresponding weights are
    not actually used in the case of semicoarsening. We still have to provide
    arrays of the correct format though, otherwise numba will complain in the
    jitted functions.


    Parameters
    ----------
    grid, cgrid : :class:`emg3d.meshes.TensorMesh`
        Fine and coarse grids.

    sc_dir : int
        Direction of semicoarsening.


    Returns
    -------
    wx, wy, wz : ndarray
        Restriction weights.

    """
    if sc_dir not in [1, 5, 6]:
        wx = core.restrict_weights(
                grid.nodes_x, grid.cell_centers_x, grid.h[0], cgrid.nodes_x,
                cgrid.cell_centers_x, cgrid.h[0])
    else:
        wxlr = np.zeros(grid.vnN[0], dtype=np.float64)
        wx0 = np.ones(grid.vnN[0], dtype=np.float64)
        wx = (wxlr, wx0, wxlr)

    if sc_dir not in [2, 4, 6]:
        wy = core.restrict_weights(
                grid.nodes_y, grid.cell_centers_y, grid.h[1], cgrid.nodes_y,
                cgrid.cell_centers_y, cgrid.h[1])
    else:
        wylr = np.zeros(grid.vnN[1], dtype=np.float64)
        wy0 = np.ones(grid.vnN[1], dtype=np.float64)
        wy = (wylr, wy0, wylr)

    if sc_dir not in [3, 4, 5]:
        wz = core.restrict_weights(
                grid.nodes_z, grid.cell_centers_z, grid.h[2], cgrid.nodes_z,
                cgrid.cell_centers_z, cgrid.h[2])
    else:
        wzlr = np.zeros(grid.vnN[2], dtype=np.float64)
        wz0 = np.ones(grid.vnN[2], dtype=np.float64)
        wz = (wzlr, wz0, wzlr)

    return wx, wy, wz


def _get_prolongation_coordinates(grid, d1, d2):
    """Compute required coordinates of finer grid for prolongation."""
    D2, D1 = np.broadcast_arrays(
            getattr(grid, 'nodes_'+d2), getattr(grid, 'nodes_'+d1)[:, None])
    return np.r_[D1.ravel('F'), D2.ravel('F')].reshape(-1, 2, order='F')


class _ConvergenceError(Exception):
    """Custom exception for convergence issues with SSL solvers."""
    pass
