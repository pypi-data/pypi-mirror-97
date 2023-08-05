#ifndef STAN_MATH_PRIM_FUN_QR_THIN_R_HPP
#define STAN_MATH_PRIM_FUN_QR_THIN_R_HPP

#include <stan/math/prim/err.hpp>
#include <stan/math/prim/fun/Eigen.hpp>
#include <algorithm>

namespace stan {
namespace math {

/**
 * Returns the upper triangular factor of the thin QR decomposition
 *
 * @tparam EigMat type of the matrix
 * @param m Matrix.
 * @return Upper triangular matrix with minimal rows
 */
template <typename EigMat, require_eigen_t<EigMat>* = nullptr>
Eigen::Matrix<value_type_t<EigMat>, Eigen::Dynamic, Eigen::Dynamic> qr_thin_R(
    const EigMat& m) {
  using matrix_t
      = Eigen::Matrix<value_type_t<EigMat>, Eigen::Dynamic, Eigen::Dynamic>;
  check_nonzero_size("qr_thin_R", "m", m);
  Eigen::HouseholderQR<matrix_t> qr(m.rows(), m.cols());
  qr.compute(m);
  const int min_size = std::min(m.rows(), m.cols());
  matrix_t R = qr.matrixQR().topLeftCorner(min_size, m.cols());
  for (int i = 0; i < min_size; i++) {
    for (int j = 0; j < i; j++) {
      R.coeffRef(i, j) = 0.0;
    }
    if (R(i, i) < 0) {
      R.row(i) *= -1.0;
    }
  }
  return R;
}

}  // namespace math
}  // namespace stan

#endif
