# Template potential-3-g.pyx
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

    cdef int r12_symmetry_allowed = $r12_symmetry_allowed and col1_mask == col2_mask

    # --- preamble ---
    $preamble
    $preamble_grad
    # ----------------

    for row in $range(nrows,$range_args):
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
                        $before1
                        $before1_grad
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or $degenerate:
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
                                        $before
                                        $before_grad
                                        if $final_filter:
                                            # --- before ---
                                            $before_inner
                                            $before_inner_grad
                                            # --- kernel ---
                                            function_value = $kernel
                                            # ---  grad  ---
                                            dfunc_dr1 = $grad_r1
                                            dfunc_dr2 = $grad_r2
                                            dfunc_dct = $grad_cosine
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
