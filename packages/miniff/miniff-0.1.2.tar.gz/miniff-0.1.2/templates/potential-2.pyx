# Template potential-2.pyx
# A two-point potential: depends on the distance between pairs of atoms
$decorators
def $name(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, $parameters
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
    $preamble
    # ----------------

    for row in $range(nrows,$range_args):
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
                        $before
                        # --- kernel ---
                        out[row] += $kernel
