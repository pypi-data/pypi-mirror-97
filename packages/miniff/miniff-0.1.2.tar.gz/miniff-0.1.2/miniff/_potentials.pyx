# cython: language_level=2
import numpy as np
cimport numpy as np
cimport cython
from libc.math cimport exp, cos, sin, pi, pow, sqrt
from cython.parallel import prange

# Template potential-2.pyx
# A two-point potential: depends on the distance between pairs of atoms

def kernel_general_2(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, f, df_dr,
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r
    cdef int row_mask_, col_mask_, reverse

    # --- preamble ---
    # (no 'preamble' statements)
    # ----------------

    for row in range(nrows,):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if species_row[col_] == col_mask:
                    r = r_data[ptr]
                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # --- kernel ---
                        out[row] += f(r)


# Template potential-2-g.pyx
# A two-point potential: depends on the distance between pairs of atoms

def kernel_g_general_2(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, f, df_dr,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_, dim
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r, function_value, g, x

    # --- preamble ---
    # (no 'preamble' statements)
    # (no 'preamble_grad' statements)
    # ----------------

    for row in range(nrows,):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if species_row[col_] == col_mask:
                    r = r_data[ptr]

                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # (no 'before_grad' statements)
                        # --- kernel ---
                        function_value = f(r)
                        # ---  grad  ---
                        g = df_dr(r)
                        # --------------
                        for dim in range(3):
                            x = (cartesian_row[row, dim] - cartesian_col[col, dim]) / r * g
                            out[row, row, dim] += x   # df_self / dr_self
                            out[row, col_, dim] -= x  # df_self / dr_neighbor


# Template potential-3.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed

def kernel_general_3(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, f, df_dr1, df_dr2, df_dt,
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col1, col2, dim
    cdef int ptr1, ptr2, ptr_fr, ptr_to, _ptr_fr
    cdef int row_mask = species_mask[0]
    cdef int col1_mask = species_mask[1]
    cdef int col2_mask = species_mask[2]

    cdef int r12_symmetry_allowed = 0 and col1_mask == col2_mask

    cdef double r1, r2, r12_cos

    # --- preamble ---
    # (no 'preamble' statements)
    # ----------------

    for row in range(nrows,):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                if species_row[cython.cmod(col1, nrows)] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        # (no 'before1' statements)
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                if species_row[cython.cmod(col2, nrows)] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)
                                        # --- before ---
                                        # (no 'before' statements)
                                        if True:
                                            # --- before ---
                                            # (no 'before_inner' statements)
                                            # --- kernel ---
                                            out[row] += (1 + r12_symmetry_allowed * (ptr1 != ptr2)) * (f(r1, r2, r12_cos))


# Template potential-3-g.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed

def kernel_g_general_3(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, f, df_dr1, df_dr2, df_dt,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col1, col1_, col2, col2_, dim
    cdef int ptr1, ptr2, ptr_fr, ptr_to, _ptr_fr
    cdef int row_mask = species_mask[0]
    cdef int col1_mask = species_mask[1]
    cdef int col2_mask = species_mask[2]

    cdef double r1, r2, r12_cos, function_value, dfunc_dr1, dfunc_dr2, dfunc_dct
    cdef double nx1, nx2, cx1, cx2

    cdef int r12_symmetry_allowed = 0 and col1_mask == col2_mask

    # --- preamble ---
    # (no 'preamble' statements)
    # (no 'preamble_grad' statements)
    # ----------------

    for row in range(nrows,):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                col1_ = cython.cmod(col1, nrows)
                if species_row[col1_] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        # (no 'before1' statements)
                        # (no 'before1_grad' statements)
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                col2_ = cython.cmod(col2, nrows)
                                if species_row[col2_] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)

                                        # --- before ---
                                        # (no 'before' statements)
                                        # (no 'before_grad' statements)
                                        if True:
                                            # --- before ---
                                            # (no 'before_inner' statements)
                                            # (no 'before_inner_grad' statements)
                                            # --- kernel ---
                                            function_value = f(r1, r2, r12_cos)
                                            # ---  grad  ---
                                            dfunc_dr1 = df_dr1(r1, r2, r12_cos)
                                            dfunc_dr2 = df_dr2(r1, r2, r12_cos)
                                            dfunc_dct = df_dt(r1, r2, r12_cos)
                                            if r12_symmetry_allowed and ptr1 != ptr2:
                                                dfunc_dr1 = dfunc_dr1 * 2
                                                dfunc_dr2 = dfunc_dr2 * 2
                                                dfunc_dct = dfunc_dct * 2

                                            # Derivatives

                                            for dim in range(3):
                                                nx1 = (cartesian_row[row, dim] - cartesian_col[col1, dim]) / r1
                                                nx2 = (cartesian_row[row, dim] - cartesian_col[col2, dim]) / r2
                                                # d(cos θ) / dr = 1/r (n_s - n_r cos θ)
                                                cx1 = (nx2 - nx1 * r12_cos) / r1
                                                cx2 = (nx1 - nx2 * r12_cos) / r2

                                                out[row, row, dim] += nx1 * dfunc_dr1 + cx1 * dfunc_dct + nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_self
                                                out[row, col1_, dim] -= nx1 * dfunc_dr1 + cx1 * dfunc_dct  # df_self / dr_n1
                                                out[row, col2_, dim] -= nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_n2


# Template potential-2.pyx
# A two-point potential: depends on the distance between pairs of atoms

def kernel_harmonic_repulsion(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double epsilon,
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r
    cdef int row_mask_, col_mask_, reverse

    # --- preamble ---
    # (no 'preamble' statements)
    # ----------------

    for row in range(nrows,):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if species_row[col_] == col_mask:
                    r = r_data[ptr]
                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # --- kernel ---
                        out[row] += epsilon * (r - a) * (r - a) / a / a / 2


# Template potential-2-g.pyx
# A two-point potential: depends on the distance between pairs of atoms

def kernel_g_harmonic_repulsion(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double epsilon,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_, dim
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r, function_value, g, x

    # --- preamble ---
    # (no 'preamble' statements)
    # (no 'preamble_grad' statements)
    # ----------------

    for row in range(nrows,):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if species_row[col_] == col_mask:
                    r = r_data[ptr]

                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # (no 'before_grad' statements)
                        # --- kernel ---
                        function_value = epsilon * (r - a) * (r - a) / a / a / 2
                        # ---  grad  ---
                        g = epsilon * (r - a) / a / a
                        # --------------
                        for dim in range(3):
                            x = (cartesian_row[row, dim] - cartesian_col[col, dim]) / r * g
                            out[row, row, dim] += x   # df_self / dr_self
                            out[row, col_, dim] -= x  # df_self / dr_neighbor


# Template potential-2.pyx
# A two-point potential: depends on the distance between pairs of atoms
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_harmonic_repulsion(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double epsilon,
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r
    cdef int row_mask_, col_mask_, reverse

    # --- preamble ---
    # (no 'preamble' statements)
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if species_row[col_] == col_mask:
                    r = r_data[ptr]
                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # --- kernel ---
                        out[row] += epsilon * (r - a) * (r - a) / a / a / 2


# Template potential-2-g.pyx
# A two-point potential: depends on the distance between pairs of atoms
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_g_harmonic_repulsion(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double epsilon,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_, dim
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r, function_value, g, x

    # --- preamble ---
    # (no 'preamble' statements)
    # (no 'preamble_grad' statements)
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if species_row[col_] == col_mask:
                    r = r_data[ptr]

                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # (no 'before_grad' statements)
                        # --- kernel ---
                        function_value = epsilon * (r - a) * (r - a) / a / a / 2
                        # ---  grad  ---
                        g = epsilon * (r - a) / a / a
                        # --------------
                        for dim in range(3):
                            x = (cartesian_row[row, dim] - cartesian_col[col, dim]) / r * g
                            out[row, row, dim] += x   # df_self / dr_self
                            out[row, col_, dim] -= x  # df_self / dr_neighbor


# Template potential-2.pyx
# A two-point potential: depends on the distance between pairs of atoms

def kernel_lj(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, 
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r
    cdef int row_mask_, col_mask_, reverse

    # --- preamble ---
    # (no 'preamble' statements)
    # ----------------

    for row in range(nrows,):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if species_row[col_] == col_mask:
                    r = r_data[ptr]
                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # --- kernel ---
                        out[row] += 4 * (pow(r, -12) - pow(r, -6))


# Template potential-2-g.pyx
# A two-point potential: depends on the distance between pairs of atoms

def kernel_g_lj(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, 
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_, dim
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r, function_value, g, x

    # --- preamble ---
    # (no 'preamble' statements)
    # (no 'preamble_grad' statements)
    # ----------------

    for row in range(nrows,):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if species_row[col_] == col_mask:
                    r = r_data[ptr]

                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # (no 'before_grad' statements)
                        # --- kernel ---
                        function_value = 4 * (pow(r, -12) - pow(r, -6))
                        # ---  grad  ---
                        g = 4 * (- 12 * pow(r, -12) + 6 * pow(r, -6)) / r
                        # --------------
                        for dim in range(3):
                            x = (cartesian_row[row, dim] - cartesian_col[col, dim]) / r * g
                            out[row, row, dim] += x   # df_self / dr_self
                            out[row, col_, dim] -= x  # df_self / dr_neighbor


# Template potential-2.pyx
# A two-point potential: depends on the distance between pairs of atoms
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_lj(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, 
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r
    cdef int row_mask_, col_mask_, reverse

    # --- preamble ---
    # (no 'preamble' statements)
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if species_row[col_] == col_mask:
                    r = r_data[ptr]
                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # --- kernel ---
                        out[row] += 4 * (pow(r, -12) - pow(r, -6))


# Template potential-2-g.pyx
# A two-point potential: depends on the distance between pairs of atoms
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_g_lj(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, 
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_, dim
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r, function_value, g, x

    # --- preamble ---
    # (no 'preamble' statements)
    # (no 'preamble_grad' statements)
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if species_row[col_] == col_mask:
                    r = r_data[ptr]

                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # (no 'before_grad' statements)
                        # --- kernel ---
                        function_value = 4 * (pow(r, -12) - pow(r, -6))
                        # ---  grad  ---
                        g = 4 * (- 12 * pow(r, -12) + 6 * pow(r, -6)) / r
                        # --------------
                        for dim in range(3):
                            x = (cartesian_row[row, dim] - cartesian_col[col, dim]) / r * g
                            out[row, row, dim] += x   # df_self / dr_self
                            out[row, col_, dim] -= x  # df_self / dr_neighbor


# Template potential-2.pyx
# A two-point potential: depends on the distance between pairs of atoms

def kernel_sw_phi2(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double gauge_a, double gauge_b, double p, double q,
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r
    cdef int row_mask_, col_mask_, reverse

    # --- preamble ---
    # (no 'preamble' statements)
    # ----------------

    for row in range(nrows,):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if species_row[col_] == col_mask:
                    r = r_data[ptr]
                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # --- kernel ---
                        out[row] += gauge_a * (gauge_b * r ** (-p) - r ** (-q)) * exp(1. / (r - a))


# Template potential-2-g.pyx
# A two-point potential: depends on the distance between pairs of atoms

def kernel_g_sw_phi2(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double gauge_a, double gauge_b, double p, double q,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_, dim
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r, function_value, g, x

    # --- preamble ---
    # (no 'preamble' statements)
    # (no 'preamble_grad' statements)
    # ----------------

    for row in range(nrows,):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if species_row[col_] == col_mask:
                    r = r_data[ptr]

                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # (no 'before_grad' statements)
                        # --- kernel ---
                        function_value = gauge_a * (gauge_b * r ** (-p) - r ** (-q)) * exp(1. / (r - a))
                        # ---  grad  ---
                        g = (- p * gauge_a * gauge_b * r ** (- p - 1) + gauge_a * q * r ** (- q - 1)) * exp(1. / (r - a)) - function_value / (r - a) / (r - a)
                        # --------------
                        for dim in range(3):
                            x = (cartesian_row[row, dim] - cartesian_col[col, dim]) / r * g
                            out[row, row, dim] += x   # df_self / dr_self
                            out[row, col_, dim] -= x  # df_self / dr_neighbor


# Template potential-2.pyx
# A two-point potential: depends on the distance between pairs of atoms
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_sw_phi2(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double gauge_a, double gauge_b, double p, double q,
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r
    cdef int row_mask_, col_mask_, reverse

    # --- preamble ---
    # (no 'preamble' statements)
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if species_row[col_] == col_mask:
                    r = r_data[ptr]
                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # --- kernel ---
                        out[row] += gauge_a * (gauge_b * r ** (-p) - r ** (-q)) * exp(1. / (r - a))


# Template potential-2-g.pyx
# A two-point potential: depends on the distance between pairs of atoms
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_g_sw_phi2(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double gauge_a, double gauge_b, double p, double q,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_, dim
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r, function_value, g, x

    # --- preamble ---
    # (no 'preamble' statements)
    # (no 'preamble_grad' statements)
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if species_row[col_] == col_mask:
                    r = r_data[ptr]

                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # (no 'before_grad' statements)
                        # --- kernel ---
                        function_value = gauge_a * (gauge_b * r ** (-p) - r ** (-q)) * exp(1. / (r - a))
                        # ---  grad  ---
                        g = (- p * gauge_a * gauge_b * r ** (- p - 1) + gauge_a * q * r ** (- q - 1)) * exp(1. / (r - a)) - function_value / (r - a) / (r - a)
                        # --------------
                        for dim in range(3):
                            x = (cartesian_row[row, dim] - cartesian_col[col, dim]) / r * g
                            out[row, row, dim] += x   # df_self / dr_self
                            out[row, col_, dim] -= x  # df_self / dr_neighbor


# Template potential-3.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed

def kernel_sw_phi3(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double l, double gamma, double cos_theta0,
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col1, col2, dim
    cdef int ptr1, ptr2, ptr_fr, ptr_to, _ptr_fr
    cdef int row_mask = species_mask[0]
    cdef int col1_mask = species_mask[1]
    cdef int col2_mask = species_mask[2]

    cdef int r12_symmetry_allowed = 0 and col1_mask == col2_mask

    cdef double r1, r2, r12_cos

    # --- preamble ---
    # (no 'preamble' statements)
    # ----------------

    for row in range(nrows,):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                if species_row[cython.cmod(col1, nrows)] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        # (no 'before1' statements)
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                if species_row[cython.cmod(col2, nrows)] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)
                                        # --- before ---
                                        # (no 'before' statements)
                                        if True:
                                            # --- before ---
                                            # (no 'before_inner' statements)
                                            # --- kernel ---
                                            out[row] += (1 + r12_symmetry_allowed * (ptr1 != ptr2)) * (l * (r12_cos - cos_theta0) * (r12_cos - cos_theta0) * exp(gamma * (1 / (r1 - a) + 1 / (r2 - a))))


# Template potential-3-g.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed

def kernel_g_sw_phi3(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double l, double gamma, double cos_theta0,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col1, col1_, col2, col2_, dim
    cdef int ptr1, ptr2, ptr_fr, ptr_to, _ptr_fr
    cdef int row_mask = species_mask[0]
    cdef int col1_mask = species_mask[1]
    cdef int col2_mask = species_mask[2]

    cdef double r1, r2, r12_cos, function_value, dfunc_dr1, dfunc_dr2, dfunc_dct
    cdef double nx1, nx2, cx1, cx2

    cdef int r12_symmetry_allowed = 0 and col1_mask == col2_mask

    # --- preamble ---
    # (no 'preamble' statements)
    # (no 'preamble_grad' statements)
    # ----------------

    for row in range(nrows,):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                col1_ = cython.cmod(col1, nrows)
                if species_row[col1_] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        # (no 'before1' statements)
                        # (no 'before1_grad' statements)
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                col2_ = cython.cmod(col2, nrows)
                                if species_row[col2_] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)

                                        # --- before ---
                                        # (no 'before' statements)
                                        # (no 'before_grad' statements)
                                        if True:
                                            # --- before ---
                                            # (no 'before_inner' statements)
                                            # (no 'before_inner_grad' statements)
                                            # --- kernel ---
                                            function_value = l * (r12_cos - cos_theta0) * (r12_cos - cos_theta0) * exp(gamma * (1 / (r1 - a) + 1 / (r2 - a)))
                                            # ---  grad  ---
                                            dfunc_dr1 = - function_value * gamma / (r1 - a) / (r1 - a)
                                            dfunc_dr2 = - function_value * gamma / (r2 - a) / (r2 - a)
                                            dfunc_dct = 2 * l * (r12_cos - cos_theta0) * exp(gamma * (1 / (r1 - a) + 1 / (r2 - a)))
                                            if r12_symmetry_allowed and ptr1 != ptr2:
                                                dfunc_dr1 = dfunc_dr1 * 2
                                                dfunc_dr2 = dfunc_dr2 * 2
                                                dfunc_dct = dfunc_dct * 2

                                            # Derivatives

                                            for dim in range(3):
                                                nx1 = (cartesian_row[row, dim] - cartesian_col[col1, dim]) / r1
                                                nx2 = (cartesian_row[row, dim] - cartesian_col[col2, dim]) / r2
                                                # d(cos θ) / dr = 1/r (n_s - n_r cos θ)
                                                cx1 = (nx2 - nx1 * r12_cos) / r1
                                                cx2 = (nx1 - nx2 * r12_cos) / r2

                                                out[row, row, dim] += nx1 * dfunc_dr1 + cx1 * dfunc_dct + nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_self
                                                out[row, col1_, dim] -= nx1 * dfunc_dr1 + cx1 * dfunc_dct  # df_self / dr_n1
                                                out[row, col2_, dim] -= nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_n2


# Template potential-3.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_sw_phi3(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double l, double gamma, double cos_theta0,
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col1, col2, dim
    cdef int ptr1, ptr2, ptr_fr, ptr_to, _ptr_fr
    cdef int row_mask = species_mask[0]
    cdef int col1_mask = species_mask[1]
    cdef int col2_mask = species_mask[2]

    cdef int r12_symmetry_allowed = 0 and col1_mask == col2_mask

    cdef double r1, r2, r12_cos

    # --- preamble ---
    # (no 'preamble' statements)
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                if species_row[cython.cmod(col1, nrows)] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        # (no 'before1' statements)
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                if species_row[cython.cmod(col2, nrows)] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)
                                        # --- before ---
                                        # (no 'before' statements)
                                        if True:
                                            # --- before ---
                                            # (no 'before_inner' statements)
                                            # --- kernel ---
                                            out[row] += (1 + r12_symmetry_allowed * (ptr1 != ptr2)) * (l * (r12_cos - cos_theta0) * (r12_cos - cos_theta0) * exp(gamma * (1 / (r1 - a) + 1 / (r2 - a))))


# Template potential-3-g.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_g_sw_phi3(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double l, double gamma, double cos_theta0,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col1, col1_, col2, col2_, dim
    cdef int ptr1, ptr2, ptr_fr, ptr_to, _ptr_fr
    cdef int row_mask = species_mask[0]
    cdef int col1_mask = species_mask[1]
    cdef int col2_mask = species_mask[2]

    cdef double r1, r2, r12_cos, function_value, dfunc_dr1, dfunc_dr2, dfunc_dct
    cdef double nx1, nx2, cx1, cx2

    cdef int r12_symmetry_allowed = 0 and col1_mask == col2_mask

    # --- preamble ---
    # (no 'preamble' statements)
    # (no 'preamble_grad' statements)
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                col1_ = cython.cmod(col1, nrows)
                if species_row[col1_] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        # (no 'before1' statements)
                        # (no 'before1_grad' statements)
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                col2_ = cython.cmod(col2, nrows)
                                if species_row[col2_] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)

                                        # --- before ---
                                        # (no 'before' statements)
                                        # (no 'before_grad' statements)
                                        if True:
                                            # --- before ---
                                            # (no 'before_inner' statements)
                                            # (no 'before_inner_grad' statements)
                                            # --- kernel ---
                                            function_value = l * (r12_cos - cos_theta0) * (r12_cos - cos_theta0) * exp(gamma * (1 / (r1 - a) + 1 / (r2 - a)))
                                            # ---  grad  ---
                                            dfunc_dr1 = - function_value * gamma / (r1 - a) / (r1 - a)
                                            dfunc_dr2 = - function_value * gamma / (r2 - a) / (r2 - a)
                                            dfunc_dct = 2 * l * (r12_cos - cos_theta0) * exp(gamma * (1 / (r1 - a) + 1 / (r2 - a)))
                                            if r12_symmetry_allowed and ptr1 != ptr2:
                                                dfunc_dr1 = dfunc_dr1 * 2
                                                dfunc_dr2 = dfunc_dr2 * 2
                                                dfunc_dct = dfunc_dct * 2

                                            # Derivatives

                                            for dim in range(3):
                                                nx1 = (cartesian_row[row, dim] - cartesian_col[col1, dim]) / r1
                                                nx2 = (cartesian_row[row, dim] - cartesian_col[col2, dim]) / r2
                                                # d(cos θ) / dr = 1/r (n_s - n_r cos θ)
                                                cx1 = (nx2 - nx1 * r12_cos) / r1
                                                cx2 = (nx1 - nx2 * r12_cos) / r2

                                                out[row, row, dim] += nx1 * dfunc_dr1 + cx1 * dfunc_dct + nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_self
                                                out[row, col1_, dim] -= nx1 * dfunc_dr1 + cx1 * dfunc_dct  # df_self / dr_n1
                                                out[row, col2_, dim] -= nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_n2


# Template potential-2.pyx
# A two-point potential: depends on the distance between pairs of atoms

def kernel_mlsf_g2(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double eta, double r_sphere, double[:, ::1] pre_compute_r, int[::1] pre_compute_r_handles,
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r
    cdef int row_mask_, col_mask_, reverse

    # --- preamble ---
    cdef int pre_compute_r_fn_handle = pre_compute_r_handles[0]
    # ----------------

    for row in range(nrows,):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if species_row[col_] == col_mask:
                    r = r_data[ptr]
                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # --- kernel ---
                        out[row] += exp(- eta * (r - r_sphere) * (r - r_sphere)) * pre_compute_r[ptr, pre_compute_r_fn_handle]


# Template potential-2-g.pyx
# A two-point potential: depends on the distance between pairs of atoms

def kernel_g_mlsf_g2(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double eta, double r_sphere, double[:, ::1] pre_compute_r, int[::1] pre_compute_r_handles,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_, dim
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r, function_value, g, x

    # --- preamble ---
    cdef int pre_compute_r_fn_handle = pre_compute_r_handles[0]
    cdef int pre_compute_r_fp_handle = pre_compute_r_handles[1]
    # ----------------

    for row in range(nrows,):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if species_row[col_] == col_mask:
                    r = r_data[ptr]

                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # (no 'before_grad' statements)
                        # --- kernel ---
                        function_value = exp(- eta * (r - r_sphere) * (r - r_sphere)) * pre_compute_r[ptr, pre_compute_r_fn_handle]
                        # ---  grad  ---
                        g = - 2 * eta * (r - r_sphere) * function_value + exp(- eta * (r - r_sphere) * (r - r_sphere)) * pre_compute_r[ptr, pre_compute_r_fp_handle]
                        # --------------
                        for dim in range(3):
                            x = (cartesian_row[row, dim] - cartesian_col[col, dim]) / r * g
                            out[row, row, dim] += x   # df_self / dr_self
                            out[row, col_, dim] -= x  # df_self / dr_neighbor


# Template potential-2.pyx
# A two-point potential: depends on the distance between pairs of atoms
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_mlsf_g2(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double eta, double r_sphere, double[:, ::1] pre_compute_r, int[::1] pre_compute_r_handles,
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r
    cdef int row_mask_, col_mask_, reverse

    # --- preamble ---
    cdef int pre_compute_r_fn_handle = pre_compute_r_handles[0]
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if species_row[col_] == col_mask:
                    r = r_data[ptr]
                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # --- kernel ---
                        out[row] += exp(- eta * (r - r_sphere) * (r - r_sphere)) * pre_compute_r[ptr, pre_compute_r_fn_handle]


# Template potential-2-g.pyx
# A two-point potential: depends on the distance between pairs of atoms
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_g_mlsf_g2(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double eta, double r_sphere, double[:, ::1] pre_compute_r, int[::1] pre_compute_r_handles,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_, dim
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r, function_value, g, x

    # --- preamble ---
    cdef int pre_compute_r_fn_handle = pre_compute_r_handles[0]
    cdef int pre_compute_r_fp_handle = pre_compute_r_handles[1]
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if species_row[col_] == col_mask:
                    r = r_data[ptr]

                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # (no 'before_grad' statements)
                        # --- kernel ---
                        function_value = exp(- eta * (r - r_sphere) * (r - r_sphere)) * pre_compute_r[ptr, pre_compute_r_fn_handle]
                        # ---  grad  ---
                        g = - 2 * eta * (r - r_sphere) * function_value + exp(- eta * (r - r_sphere) * (r - r_sphere)) * pre_compute_r[ptr, pre_compute_r_fp_handle]
                        # --------------
                        for dim in range(3):
                            x = (cartesian_row[row, dim] - cartesian_col[col, dim]) / r * g
                            out[row, row, dim] += x   # df_self / dr_self
                            out[row, col_, dim] -= x  # df_self / dr_neighbor


# Template potential-3.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed

def kernel_mlsf_g5(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double epsilon, double eta, double l, double zeta, double[:, ::1] pre_compute_r, int[::1] pre_compute_r_handles,
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col1, col2, dim
    cdef int ptr1, ptr2, ptr_fr, ptr_to, _ptr_fr
    cdef int row_mask = species_mask[0]
    cdef int col1_mask = species_mask[1]
    cdef int col2_mask = species_mask[2]

    cdef int r12_symmetry_allowed = 1 and col1_mask == col2_mask

    cdef double r1, r2, r12_cos

    # --- preamble ---
    cdef double _fn_cutoff1, _fn_cutoff2, _fn_exponent, _fn_pw
    cdef double _prefactor = pow(2, 1 - zeta) * epsilon
    cdef int pre_compute_r_cutoff_fn_handle = pre_compute_r_handles[0], pre_compute_r_exp_fn_handle = pre_compute_r_handles[2]
    # ----------------

    for row in range(nrows,):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                if species_row[cython.cmod(col1, nrows)] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        _fn_cutoff1 = pre_compute_r[ptr1, pre_compute_r_cutoff_fn_handle]
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                if species_row[cython.cmod(col2, nrows)] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)
                                        # --- before ---
                                        _fn_cutoff2 = pre_compute_r[ptr2, pre_compute_r_cutoff_fn_handle]
                                        _fn_exponent = _prefactor * pre_compute_r[ptr1, pre_compute_r_exp_fn_handle] * pre_compute_r[ptr2, pre_compute_r_exp_fn_handle]
                                        _fn_pw = pow(1 + l * r12_cos, zeta)
                                        if True:
                                            # --- before ---
                                            # (no 'before_inner' statements)
                                            # --- kernel ---
                                            out[row] += (1 + r12_symmetry_allowed * (ptr1 != ptr2)) * (_fn_pw * _fn_exponent * _fn_cutoff1 * _fn_cutoff2)


# Template potential-3-g.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed

def kernel_g_mlsf_g5(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double epsilon, double eta, double l, double zeta, double[:, ::1] pre_compute_r, int[::1] pre_compute_r_handles,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col1, col1_, col2, col2_, dim
    cdef int ptr1, ptr2, ptr_fr, ptr_to, _ptr_fr
    cdef int row_mask = species_mask[0]
    cdef int col1_mask = species_mask[1]
    cdef int col2_mask = species_mask[2]

    cdef double r1, r2, r12_cos, function_value, dfunc_dr1, dfunc_dr2, dfunc_dct
    cdef double nx1, nx2, cx1, cx2

    cdef int r12_symmetry_allowed = 1 and col1_mask == col2_mask

    # --- preamble ---
    cdef double _fn_cutoff1, _fn_cutoff2, _fn_exponent, _fn_pw
    cdef double _prefactor = pow(2, 1 - zeta) * epsilon
    cdef int pre_compute_r_cutoff_fn_handle = pre_compute_r_handles[0], pre_compute_r_exp_fn_handle = pre_compute_r_handles[2]
    cdef double _fp_cutoff1, _fp_cutoff2
    cdef int pre_compute_r_cutoff_fp_handle = pre_compute_r_handles[1]
    # ----------------

    for row in range(nrows,):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                col1_ = cython.cmod(col1, nrows)
                if species_row[col1_] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        _fn_cutoff1 = pre_compute_r[ptr1, pre_compute_r_cutoff_fn_handle]
                        _fp_cutoff1 = pre_compute_r[ptr1, pre_compute_r_cutoff_fp_handle]
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                col2_ = cython.cmod(col2, nrows)
                                if species_row[col2_] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)

                                        # --- before ---
                                        _fn_cutoff2 = pre_compute_r[ptr2, pre_compute_r_cutoff_fn_handle]
                                        _fn_exponent = _prefactor * pre_compute_r[ptr1, pre_compute_r_exp_fn_handle] * pre_compute_r[ptr2, pre_compute_r_exp_fn_handle]
                                        _fn_pw = pow(1 + l * r12_cos, zeta)
                                        _fp_cutoff2 = pre_compute_r[ptr2, pre_compute_r_cutoff_fp_handle]
                                        if True:
                                            # --- before ---
                                            # (no 'before_inner' statements)
                                            # (no 'before_inner_grad' statements)
                                            # --- kernel ---
                                            function_value = _fn_pw * _fn_exponent * _fn_cutoff1 * _fn_cutoff2
                                            # ---  grad  ---
                                            dfunc_dr1 = - 2 * eta * r1 * function_value + _fn_pw * _fn_exponent * _fn_cutoff2 * _fp_cutoff1
                                            dfunc_dr2 = - 2 * eta * r2 * function_value + _fn_pw * _fn_exponent * _fn_cutoff1 * _fp_cutoff2
                                            dfunc_dct = zeta * l * pow(1 + l * r12_cos, zeta - 1) * _fn_exponent * _fn_cutoff1 * _fn_cutoff2
                                            if r12_symmetry_allowed and ptr1 != ptr2:
                                                dfunc_dr1 = dfunc_dr1 * 2
                                                dfunc_dr2 = dfunc_dr2 * 2
                                                dfunc_dct = dfunc_dct * 2

                                            # Derivatives

                                            for dim in range(3):
                                                nx1 = (cartesian_row[row, dim] - cartesian_col[col1, dim]) / r1
                                                nx2 = (cartesian_row[row, dim] - cartesian_col[col2, dim]) / r2
                                                # d(cos θ) / dr = 1/r (n_s - n_r cos θ)
                                                cx1 = (nx2 - nx1 * r12_cos) / r1
                                                cx2 = (nx1 - nx2 * r12_cos) / r2

                                                out[row, row, dim] += nx1 * dfunc_dr1 + cx1 * dfunc_dct + nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_self
                                                out[row, col1_, dim] -= nx1 * dfunc_dr1 + cx1 * dfunc_dct  # df_self / dr_n1
                                                out[row, col2_, dim] -= nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_n2


# Template potential-3.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_mlsf_g5(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double epsilon, double eta, double l, double zeta, double[:, ::1] pre_compute_r, int[::1] pre_compute_r_handles,
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col1, col2, dim
    cdef int ptr1, ptr2, ptr_fr, ptr_to, _ptr_fr
    cdef int row_mask = species_mask[0]
    cdef int col1_mask = species_mask[1]
    cdef int col2_mask = species_mask[2]

    cdef int r12_symmetry_allowed = 1 and col1_mask == col2_mask

    cdef double r1, r2, r12_cos

    # --- preamble ---
    cdef double _fn_cutoff1, _fn_cutoff2, _fn_exponent, _fn_pw
    cdef double _prefactor = pow(2, 1 - zeta) * epsilon
    cdef int pre_compute_r_cutoff_fn_handle = pre_compute_r_handles[0], pre_compute_r_exp_fn_handle = pre_compute_r_handles[2]
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                if species_row[cython.cmod(col1, nrows)] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        _fn_cutoff1 = pre_compute_r[ptr1, pre_compute_r_cutoff_fn_handle]
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                if species_row[cython.cmod(col2, nrows)] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)
                                        # --- before ---
                                        _fn_cutoff2 = pre_compute_r[ptr2, pre_compute_r_cutoff_fn_handle]
                                        _fn_exponent = _prefactor * pre_compute_r[ptr1, pre_compute_r_exp_fn_handle] * pre_compute_r[ptr2, pre_compute_r_exp_fn_handle]
                                        _fn_pw = pow(1 + l * r12_cos, zeta)
                                        if True:
                                            # --- before ---
                                            # (no 'before_inner' statements)
                                            # --- kernel ---
                                            out[row] += (1 + r12_symmetry_allowed * (ptr1 != ptr2)) * (_fn_pw * _fn_exponent * _fn_cutoff1 * _fn_cutoff2)


# Template potential-3-g.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_g_mlsf_g5(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double epsilon, double eta, double l, double zeta, double[:, ::1] pre_compute_r, int[::1] pre_compute_r_handles,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col1, col1_, col2, col2_, dim
    cdef int ptr1, ptr2, ptr_fr, ptr_to, _ptr_fr
    cdef int row_mask = species_mask[0]
    cdef int col1_mask = species_mask[1]
    cdef int col2_mask = species_mask[2]

    cdef double r1, r2, r12_cos, function_value, dfunc_dr1, dfunc_dr2, dfunc_dct
    cdef double nx1, nx2, cx1, cx2

    cdef int r12_symmetry_allowed = 1 and col1_mask == col2_mask

    # --- preamble ---
    cdef double _fn_cutoff1, _fn_cutoff2, _fn_exponent, _fn_pw
    cdef double _prefactor = pow(2, 1 - zeta) * epsilon
    cdef int pre_compute_r_cutoff_fn_handle = pre_compute_r_handles[0], pre_compute_r_exp_fn_handle = pre_compute_r_handles[2]
    cdef double _fp_cutoff1, _fp_cutoff2
    cdef int pre_compute_r_cutoff_fp_handle = pre_compute_r_handles[1]
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                col1_ = cython.cmod(col1, nrows)
                if species_row[col1_] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        _fn_cutoff1 = pre_compute_r[ptr1, pre_compute_r_cutoff_fn_handle]
                        _fp_cutoff1 = pre_compute_r[ptr1, pre_compute_r_cutoff_fp_handle]
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                col2_ = cython.cmod(col2, nrows)
                                if species_row[col2_] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)

                                        # --- before ---
                                        _fn_cutoff2 = pre_compute_r[ptr2, pre_compute_r_cutoff_fn_handle]
                                        _fn_exponent = _prefactor * pre_compute_r[ptr1, pre_compute_r_exp_fn_handle] * pre_compute_r[ptr2, pre_compute_r_exp_fn_handle]
                                        _fn_pw = pow(1 + l * r12_cos, zeta)
                                        _fp_cutoff2 = pre_compute_r[ptr2, pre_compute_r_cutoff_fp_handle]
                                        if True:
                                            # --- before ---
                                            # (no 'before_inner' statements)
                                            # (no 'before_inner_grad' statements)
                                            # --- kernel ---
                                            function_value = _fn_pw * _fn_exponent * _fn_cutoff1 * _fn_cutoff2
                                            # ---  grad  ---
                                            dfunc_dr1 = - 2 * eta * r1 * function_value + _fn_pw * _fn_exponent * _fn_cutoff2 * _fp_cutoff1
                                            dfunc_dr2 = - 2 * eta * r2 * function_value + _fn_pw * _fn_exponent * _fn_cutoff1 * _fp_cutoff2
                                            dfunc_dct = zeta * l * pow(1 + l * r12_cos, zeta - 1) * _fn_exponent * _fn_cutoff1 * _fn_cutoff2
                                            if r12_symmetry_allowed and ptr1 != ptr2:
                                                dfunc_dr1 = dfunc_dr1 * 2
                                                dfunc_dr2 = dfunc_dr2 * 2
                                                dfunc_dct = dfunc_dct * 2

                                            # Derivatives

                                            for dim in range(3):
                                                nx1 = (cartesian_row[row, dim] - cartesian_col[col1, dim]) / r1
                                                nx2 = (cartesian_row[row, dim] - cartesian_col[col2, dim]) / r2
                                                # d(cos θ) / dr = 1/r (n_s - n_r cos θ)
                                                cx1 = (nx2 - nx1 * r12_cos) / r1
                                                cx2 = (nx1 - nx2 * r12_cos) / r2

                                                out[row, row, dim] += nx1 * dfunc_dr1 + cx1 * dfunc_dct + nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_self
                                                out[row, col1_, dim] -= nx1 * dfunc_dr1 + cx1 * dfunc_dct  # df_self / dr_n1
                                                out[row, col2_, dim] -= nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_n2


# Template potential-3.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed

def kernel_mlsf_g4(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double epsilon, double eta, double l, double zeta, double[:, ::1] pre_compute_r, int[::1] pre_compute_r_handles,
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col1, col2, dim
    cdef int ptr1, ptr2, ptr_fr, ptr_to, _ptr_fr
    cdef int row_mask = species_mask[0]
    cdef int col1_mask = species_mask[1]
    cdef int col2_mask = species_mask[2]

    cdef int r12_symmetry_allowed = 1 and col1_mask == col2_mask

    cdef double r1, r2, r12_cos

    # --- preamble ---
    cdef double _fn_cutoff1, _fn_cutoff2, _fn_cutoff3, _fn_exponent, _fn_pw
    cdef double _prefactor = pow(2, 1 - zeta) * epsilon
    cdef int pre_compute_r_cutoff_fn_handle = pre_compute_r_handles[0], pre_compute_r_exp_fn_handle = pre_compute_r_handles[2]
    cdef double _r3, _r3_factor, g5_fun
    # ----------------

    for row in range(nrows,):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                if species_row[cython.cmod(col1, nrows)] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        _fn_cutoff1 = pre_compute_r[ptr1, pre_compute_r_cutoff_fn_handle]
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                if species_row[cython.cmod(col2, nrows)] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)
                                        # --- before ---
                                        _r3 = sqrt(r1 * r1 + r2 * r2 - 2 * r1 * r2 * r12_cos)
                                        if _r3 < a:
                                            # --- before ---
                                            _fn_cutoff2 = pre_compute_r[ptr2, pre_compute_r_cutoff_fn_handle]
                                            _fn_exponent = _prefactor * pre_compute_r[ptr1, pre_compute_r_exp_fn_handle] * pre_compute_r[ptr2, pre_compute_r_exp_fn_handle]
                                            _fn_pw = pow(1 + l * r12_cos, zeta)
                                            g5_fun = _fn_pw * _fn_exponent * _fn_cutoff1 * _fn_cutoff2
                                            _r3_factor = exp(-eta * _r3 * _r3) * (.5 + cos(pi * _r3 / a) / 2)
                                            # --- kernel ---
                                            out[row] += (1 + r12_symmetry_allowed * (ptr1 != ptr2)) * (g5_fun * _r3_factor)


# Template potential-3-g.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed

def kernel_g_mlsf_g4(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double epsilon, double eta, double l, double zeta, double[:, ::1] pre_compute_r, int[::1] pre_compute_r_handles,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col1, col1_, col2, col2_, dim
    cdef int ptr1, ptr2, ptr_fr, ptr_to, _ptr_fr
    cdef int row_mask = species_mask[0]
    cdef int col1_mask = species_mask[1]
    cdef int col2_mask = species_mask[2]

    cdef double r1, r2, r12_cos, function_value, dfunc_dr1, dfunc_dr2, dfunc_dct
    cdef double nx1, nx2, cx1, cx2

    cdef int r12_symmetry_allowed = 1 and col1_mask == col2_mask

    # --- preamble ---
    cdef double _fn_cutoff1, _fn_cutoff2, _fn_cutoff3, _fn_exponent, _fn_pw
    cdef double _prefactor = pow(2, 1 - zeta) * epsilon
    cdef int pre_compute_r_cutoff_fn_handle = pre_compute_r_handles[0], pre_compute_r_exp_fn_handle = pre_compute_r_handles[2]
    cdef double _r3, _r3_factor, g5_fun
    cdef double _fp_cutoff1, _fp_cutoff2
    cdef int pre_compute_r_cutoff_fp_handle = pre_compute_r_handles[1]
    cdef double _r3_factor_p, _r3_grad_r1, _r3_grad_r2, _r3_grad_cosine, g5_grad_r1, g5_grad_r2, g5_grad_cosine
    # ----------------

    for row in range(nrows,):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                col1_ = cython.cmod(col1, nrows)
                if species_row[col1_] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        _fn_cutoff1 = pre_compute_r[ptr1, pre_compute_r_cutoff_fn_handle]
                        _fp_cutoff1 = pre_compute_r[ptr1, pre_compute_r_cutoff_fp_handle]
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                col2_ = cython.cmod(col2, nrows)
                                if species_row[col2_] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)

                                        # --- before ---
                                        _r3 = sqrt(r1 * r1 + r2 * r2 - 2 * r1 * r2 * r12_cos)
                                        # (no 'before_grad' statements)
                                        if _r3 < a:
                                            # --- before ---
                                            _fn_cutoff2 = pre_compute_r[ptr2, pre_compute_r_cutoff_fn_handle]
                                            _fn_exponent = _prefactor * pre_compute_r[ptr1, pre_compute_r_exp_fn_handle] * pre_compute_r[ptr2, pre_compute_r_exp_fn_handle]
                                            _fn_pw = pow(1 + l * r12_cos, zeta)
                                            g5_fun = _fn_pw * _fn_exponent * _fn_cutoff1 * _fn_cutoff2
                                            _r3_factor = exp(-eta * _r3 * _r3) * (.5 + cos(pi * _r3 / a) / 2)
                                            _fp_cutoff2 = pre_compute_r[ptr2, pre_compute_r_cutoff_fp_handle]
                                            g5_grad_r1 = - 2 * eta * r1 * g5_fun + _fn_pw * _fn_exponent * _fn_cutoff2 * _fp_cutoff1
                                            g5_grad_r2 = - 2 * eta * r2 * g5_fun + _fn_pw * _fn_exponent * _fn_cutoff1 * _fp_cutoff2
                                            g5_grad_cosine = zeta * l * pow(1 + l * r12_cos, zeta - 1) * _fn_exponent * _fn_cutoff1 * _fn_cutoff2
                                            _r3_factor_p = - 2 * eta * _r3 * _r3_factor - exp(- eta * _r3 * _r3) * sin(pi * _r3 / a) * pi / a / 2
                                            _r3_grad_r1 = (r1 - r2 * r12_cos) / _r3
                                            _r3_grad_r2 = (r2 - r1 * r12_cos) / _r3
                                            _r3_grad_cosine = - r1 * r2 / _r3
                                            # --- kernel ---
                                            function_value = g5_fun * _r3_factor
                                            # ---  grad  ---
                                            dfunc_dr1 = g5_grad_r1 * _r3_factor + g5_fun * _r3_factor_p * _r3_grad_r1
                                            dfunc_dr2 = g5_grad_r2 * _r3_factor + g5_fun * _r3_factor_p * _r3_grad_r2
                                            dfunc_dct = g5_grad_cosine * _r3_factor + g5_fun * _r3_factor_p * _r3_grad_cosine
                                            if r12_symmetry_allowed and ptr1 != ptr2:
                                                dfunc_dr1 = dfunc_dr1 * 2
                                                dfunc_dr2 = dfunc_dr2 * 2
                                                dfunc_dct = dfunc_dct * 2

                                            # Derivatives

                                            for dim in range(3):
                                                nx1 = (cartesian_row[row, dim] - cartesian_col[col1, dim]) / r1
                                                nx2 = (cartesian_row[row, dim] - cartesian_col[col2, dim]) / r2
                                                # d(cos θ) / dr = 1/r (n_s - n_r cos θ)
                                                cx1 = (nx2 - nx1 * r12_cos) / r1
                                                cx2 = (nx1 - nx2 * r12_cos) / r2

                                                out[row, row, dim] += nx1 * dfunc_dr1 + cx1 * dfunc_dct + nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_self
                                                out[row, col1_, dim] -= nx1 * dfunc_dr1 + cx1 * dfunc_dct  # df_self / dr_n1
                                                out[row, col2_, dim] -= nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_n2


# Template potential-3.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_mlsf_g4(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double epsilon, double eta, double l, double zeta, double[:, ::1] pre_compute_r, int[::1] pre_compute_r_handles,
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col1, col2, dim
    cdef int ptr1, ptr2, ptr_fr, ptr_to, _ptr_fr
    cdef int row_mask = species_mask[0]
    cdef int col1_mask = species_mask[1]
    cdef int col2_mask = species_mask[2]

    cdef int r12_symmetry_allowed = 1 and col1_mask == col2_mask

    cdef double r1, r2, r12_cos

    # --- preamble ---
    cdef double _fn_cutoff1, _fn_cutoff2, _fn_cutoff3, _fn_exponent, _fn_pw
    cdef double _prefactor = pow(2, 1 - zeta) * epsilon
    cdef int pre_compute_r_cutoff_fn_handle = pre_compute_r_handles[0], pre_compute_r_exp_fn_handle = pre_compute_r_handles[2]
    cdef double _r3, _r3_factor, g5_fun
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                if species_row[cython.cmod(col1, nrows)] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        _fn_cutoff1 = pre_compute_r[ptr1, pre_compute_r_cutoff_fn_handle]
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                if species_row[cython.cmod(col2, nrows)] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)
                                        # --- before ---
                                        _r3 = sqrt(r1 * r1 + r2 * r2 - 2 * r1 * r2 * r12_cos)
                                        if _r3 < a:
                                            # --- before ---
                                            _fn_cutoff2 = pre_compute_r[ptr2, pre_compute_r_cutoff_fn_handle]
                                            _fn_exponent = _prefactor * pre_compute_r[ptr1, pre_compute_r_exp_fn_handle] * pre_compute_r[ptr2, pre_compute_r_exp_fn_handle]
                                            _fn_pw = pow(1 + l * r12_cos, zeta)
                                            g5_fun = _fn_pw * _fn_exponent * _fn_cutoff1 * _fn_cutoff2
                                            _r3_factor = exp(-eta * _r3 * _r3) * (.5 + cos(pi * _r3 / a) / 2)
                                            # --- kernel ---
                                            out[row] += (1 + r12_symmetry_allowed * (ptr1 != ptr2)) * (g5_fun * _r3_factor)


# Template potential-3-g.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_g_mlsf_g4(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double epsilon, double eta, double l, double zeta, double[:, ::1] pre_compute_r, int[::1] pre_compute_r_handles,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col1, col1_, col2, col2_, dim
    cdef int ptr1, ptr2, ptr_fr, ptr_to, _ptr_fr
    cdef int row_mask = species_mask[0]
    cdef int col1_mask = species_mask[1]
    cdef int col2_mask = species_mask[2]

    cdef double r1, r2, r12_cos, function_value, dfunc_dr1, dfunc_dr2, dfunc_dct
    cdef double nx1, nx2, cx1, cx2

    cdef int r12_symmetry_allowed = 1 and col1_mask == col2_mask

    # --- preamble ---
    cdef double _fn_cutoff1, _fn_cutoff2, _fn_cutoff3, _fn_exponent, _fn_pw
    cdef double _prefactor = pow(2, 1 - zeta) * epsilon
    cdef int pre_compute_r_cutoff_fn_handle = pre_compute_r_handles[0], pre_compute_r_exp_fn_handle = pre_compute_r_handles[2]
    cdef double _r3, _r3_factor, g5_fun
    cdef double _fp_cutoff1, _fp_cutoff2
    cdef int pre_compute_r_cutoff_fp_handle = pre_compute_r_handles[1]
    cdef double _r3_factor_p, _r3_grad_r1, _r3_grad_r2, _r3_grad_cosine, g5_grad_r1, g5_grad_r2, g5_grad_cosine
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                col1_ = cython.cmod(col1, nrows)
                if species_row[col1_] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        _fn_cutoff1 = pre_compute_r[ptr1, pre_compute_r_cutoff_fn_handle]
                        _fp_cutoff1 = pre_compute_r[ptr1, pre_compute_r_cutoff_fp_handle]
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                col2_ = cython.cmod(col2, nrows)
                                if species_row[col2_] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)

                                        # --- before ---
                                        _r3 = sqrt(r1 * r1 + r2 * r2 - 2 * r1 * r2 * r12_cos)
                                        # (no 'before_grad' statements)
                                        if _r3 < a:
                                            # --- before ---
                                            _fn_cutoff2 = pre_compute_r[ptr2, pre_compute_r_cutoff_fn_handle]
                                            _fn_exponent = _prefactor * pre_compute_r[ptr1, pre_compute_r_exp_fn_handle] * pre_compute_r[ptr2, pre_compute_r_exp_fn_handle]
                                            _fn_pw = pow(1 + l * r12_cos, zeta)
                                            g5_fun = _fn_pw * _fn_exponent * _fn_cutoff1 * _fn_cutoff2
                                            _r3_factor = exp(-eta * _r3 * _r3) * (.5 + cos(pi * _r3 / a) / 2)
                                            _fp_cutoff2 = pre_compute_r[ptr2, pre_compute_r_cutoff_fp_handle]
                                            g5_grad_r1 = - 2 * eta * r1 * g5_fun + _fn_pw * _fn_exponent * _fn_cutoff2 * _fp_cutoff1
                                            g5_grad_r2 = - 2 * eta * r2 * g5_fun + _fn_pw * _fn_exponent * _fn_cutoff1 * _fp_cutoff2
                                            g5_grad_cosine = zeta * l * pow(1 + l * r12_cos, zeta - 1) * _fn_exponent * _fn_cutoff1 * _fn_cutoff2
                                            _r3_factor_p = - 2 * eta * _r3 * _r3_factor - exp(- eta * _r3 * _r3) * sin(pi * _r3 / a) * pi / a / 2
                                            _r3_grad_r1 = (r1 - r2 * r12_cos) / _r3
                                            _r3_grad_r2 = (r2 - r1 * r12_cos) / _r3
                                            _r3_grad_cosine = - r1 * r2 / _r3
                                            # --- kernel ---
                                            function_value = g5_fun * _r3_factor
                                            # ---  grad  ---
                                            dfunc_dr1 = g5_grad_r1 * _r3_factor + g5_fun * _r3_factor_p * _r3_grad_r1
                                            dfunc_dr2 = g5_grad_r2 * _r3_factor + g5_fun * _r3_factor_p * _r3_grad_r2
                                            dfunc_dct = g5_grad_cosine * _r3_factor + g5_fun * _r3_factor_p * _r3_grad_cosine
                                            if r12_symmetry_allowed and ptr1 != ptr2:
                                                dfunc_dr1 = dfunc_dr1 * 2
                                                dfunc_dr2 = dfunc_dr2 * 2
                                                dfunc_dct = dfunc_dct * 2

                                            # Derivatives

                                            for dim in range(3):
                                                nx1 = (cartesian_row[row, dim] - cartesian_col[col1, dim]) / r1
                                                nx2 = (cartesian_row[row, dim] - cartesian_col[col2, dim]) / r2
                                                # d(cos θ) / dr = 1/r (n_s - n_r cos θ)
                                                cx1 = (nx2 - nx1 * r12_cos) / r1
                                                cx2 = (nx1 - nx2 * r12_cos) / r2

                                                out[row, row, dim] += nx1 * dfunc_dr1 + cx1 * dfunc_dct + nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_self
                                                out[row, col1_, dim] -= nx1 * dfunc_dr1 + cx1 * dfunc_dct  # df_self / dr_n1
                                                out[row, col2_, dim] -= nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_n2


# Template potential-2.pyx
# A two-point potential: depends on the distance between pairs of atoms

def kernel_sigmoid(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double r0, double dr,
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r
    cdef int row_mask_, col_mask_, reverse

    # --- preamble ---
    # (no 'preamble' statements)
    # ----------------

    for row in range(nrows,):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if species_row[col_] == col_mask:
                    r = r_data[ptr]
                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # --- kernel ---
                        out[row] += 1. / (1 + exp((r - r0) / dr)) * (.5 + cos(pi * r / a) / 2)


# Template potential-2-g.pyx
# A two-point potential: depends on the distance between pairs of atoms

def kernel_g_sigmoid(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double r0, double dr,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_, dim
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r, function_value, g, x

    # --- preamble ---
    # (no 'preamble' statements)
    # (no 'preamble_grad' statements)
    # ----------------

    for row in range(nrows,):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if species_row[col_] == col_mask:
                    r = r_data[ptr]

                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # (no 'before_grad' statements)
                        # --- kernel ---
                        function_value = 1. / (1 + exp((r - r0) / dr)) * (.5 + cos(pi * r / a) / 2)
                        # ---  grad  ---
                        g = - 1. / (1 + exp((r - r0) / dr)) * exp((r - r0) / dr) / dr * function_value - 1. / (1 + exp((r - r0) / dr)) * .5 * sin(pi * r / a) * pi / a
                        # --------------
                        for dim in range(3):
                            x = (cartesian_row[row, dim] - cartesian_col[col, dim]) / r * g
                            out[row, row, dim] += x   # df_self / dr_self
                            out[row, col_, dim] -= x  # df_self / dr_neighbor


# Template potential-2.pyx
# A two-point potential: depends on the distance between pairs of atoms
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_sigmoid(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double r0, double dr,
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r
    cdef int row_mask_, col_mask_, reverse

    # --- preamble ---
    # (no 'preamble' statements)
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if species_row[col_] == col_mask:
                    r = r_data[ptr]
                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # --- kernel ---
                        out[row] += 1. / (1 + exp((r - r0) / dr)) * (.5 + cos(pi * r / a) / 2)


# Template potential-2-g.pyx
# A two-point potential: depends on the distance between pairs of atoms
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_g_sigmoid(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double r0, double dr,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_, dim
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r, function_value, g, x

    # --- preamble ---
    # (no 'preamble' statements)
    # (no 'preamble_grad' statements)
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if species_row[col_] == col_mask:
                    r = r_data[ptr]

                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # (no 'before_grad' statements)
                        # --- kernel ---
                        function_value = 1. / (1 + exp((r - r0) / dr)) * (.5 + cos(pi * r / a) / 2)
                        # ---  grad  ---
                        g = - 1. / (1 + exp((r - r0) / dr)) * exp((r - r0) / dr) / dr * function_value - 1. / (1 + exp((r - r0) / dr)) * .5 * sin(pi * r / a) * pi / a
                        # --------------
                        for dim in range(3):
                            x = (cartesian_row[row, dim] - cartesian_col[col, dim]) / r * g
                            out[row, row, dim] += x   # df_self / dr_self
                            out[row, col_, dim] -= x  # df_self / dr_neighbor
