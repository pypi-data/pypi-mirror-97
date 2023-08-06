#!/usr/bin/env python3
"""Routines related to MPI usage."""
import logging
import os

try:
    from mpi4py import MPI
    from mpi4py.futures import MPIPoolExecutor

    MPI4PY_IMPORT_ERROR = None
except ImportError as err:
    MPI4PY_IMPORT_ERROR = err
from .logs import logcolor

logger = logging.getLogger(__name__)


def mpi_parallel(fun, iterable):
    """Run function "fun" in parallel over "iterable" using MPI."""
    if MPI4PY_IMPORT_ERROR is not None:
        msg = "%s. %s%s%s" % (
            MPI4PY_IMPORT_ERROR,
            logcolor.red,
            "Support to MPI is unavailable!",
            logcolor.reset,
        )
        raise ImportError(msg) from MPI4PY_IMPORT_ERROR

    # Prevent using mpiexec with n>1
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    if size > 1:
        if rank == 0:
            raise ValueError(
                "Received '-n %d' from the MPI runner. Please " % (size)
                + "use '-n 1' when running this application with MPI, "
                + "and then select the maximum number N of parallel "
                + "MPI tasks by passing '-usize N'"
            )

    # Establish max #workers that will be dynamically spawn
    # (i.a) Check if universe size passed explicitly (e.g., via "-usize")
    univ_size = comm.Get_attr(MPI.UNIVERSE_SIZE)
    # (i.b) If not (i.a), check if we can guess from the scheduler's env
    if univ_size is None:
        univ_size = os.getenv("SLURM_NTASKS", os.getenv("PBS_NP", None))
    # (i.c) If not (i.b), assume it's a local run
    if univ_size is None:
        univ_size = int(os.getenv("NETATMOQC_MAX_PYTHON_PROCS", "1"))
    # (ii) Check how many tasks will actually be performed
    max_workers = min(len(iterable), int(univ_size))

    # Spawn workers and perform tasks
    with MPIPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(fun, iterable)
    return list(results)
