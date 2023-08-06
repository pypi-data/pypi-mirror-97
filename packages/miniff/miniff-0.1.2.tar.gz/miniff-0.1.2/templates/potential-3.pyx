# Template potential-3.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed
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
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col1, col2, dim
    cdef int ptr1, ptr2, ptr_fr, ptr_to, _ptr_fr
    cdef int row_mask = species_mask[0]
    cdef int col1_mask = species_mask[1]
    cdef int col2_mask = species_mask[2]

    cdef int r12_symmetry_allowed = $r12_symmetry_allowed and col1_mask == col2_mask

    cdef double r1, r2, r12_cos

    # --- preamble ---
    $preamble
    # ----------------

    for row in $range(nrows,$range_args):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                if species_row[cython.cmod(col1, nrows)] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        $before1
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or $degenerate:
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
                                        $before
                                        if $final_filter:
                                            # --- before ---
                                            $before_inner
                                            # --- kernel ---
                                            out[row] += (1 + r12_symmetry_allowed * (ptr1 != ptr2)) * ($kernel)
