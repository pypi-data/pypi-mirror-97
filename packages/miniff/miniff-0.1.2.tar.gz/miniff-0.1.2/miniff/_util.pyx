import numpy as np
cimport numpy as np
from libc.math cimport sqrt


def calc_sparse_distances(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, dim
    cdef int ptr, ptr_fr, ptr_to

    # Vars: coordinates and distances
    cdef double x, y, z

    # Vars: result
    result = np.empty(len(r_indices), dtype=float)
    cdef double[::1] result_mv = result

    for row in range(nrows):
        ptr_fr = r_indptr[row]
        ptr_to = r_indptr[row + 1]
        for ptr in range(ptr_fr, ptr_to):
            col = r_indices[ptr]
            result_mv[ptr] = 0
            for dim in range(3):
                result_mv[ptr] += (cartesian_col[col, dim] - cartesian_row[row, dim]) * (cartesian_col[col, dim] - cartesian_row[row, dim])
            result_mv[ptr] = sqrt(result_mv[ptr])

    return result
