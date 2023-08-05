#ifndef STAN_MATH_OPENCL_REV_LOG10_HPP
#define STAN_MATH_OPENCL_REV_LOG10_HPP
#ifdef STAN_OPENCL

#include <stan/math/opencl/kernel_generator.hpp>
#include <stan/math/rev/core.hpp>
#include <stan/math/rev/fun/value_of.hpp>

namespace stan {
namespace math {

/**
 * Returns the elementwise `log10()` of a var_value<matrix_cl<double>>.
 *
 * @param A argument
 * @return Elementwise `log10()` of the input.
 */
template <typename T,
          require_all_kernel_expressions_and_none_scalar_t<T>* = nullptr>
inline var_value<matrix_cl<double>> log10(const var_value<T>& A) {
  return make_callback_var(
      log10(A.val()), [A](vari_value<matrix_cl<double>>& res) mutable {
        A.adj() = A.adj() + elt_divide(res.adj(), A.val() * LOG_TEN);
      });
}

}  // namespace math
}  // namespace stan

#endif
#endif
