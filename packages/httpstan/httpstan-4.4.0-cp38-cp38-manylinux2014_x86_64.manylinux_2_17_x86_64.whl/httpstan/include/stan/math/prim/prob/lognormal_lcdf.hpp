#ifndef STAN_MATH_PRIM_PROB_LOGNORMAL_LCDF_HPP
#define STAN_MATH_PRIM_PROB_LOGNORMAL_LCDF_HPP

#include <stan/math/prim/meta.hpp>
#include <stan/math/prim/err.hpp>
#include <stan/math/prim/fun/as_column_vector_or_scalar.hpp>
#include <stan/math/prim/fun/as_array_or_scalar.hpp>
#include <stan/math/prim/fun/constants.hpp>
#include <stan/math/prim/fun/erfc.hpp>
#include <stan/math/prim/fun/exp.hpp>
#include <stan/math/prim/fun/log.hpp>
#include <stan/math/prim/fun/max_size.hpp>
#include <stan/math/prim/fun/promote_scalar.hpp>
#include <stan/math/prim/fun/size.hpp>
#include <stan/math/prim/fun/size_zero.hpp>
#include <stan/math/prim/fun/to_ref.hpp>
#include <stan/math/prim/fun/value_of.hpp>
#include <stan/math/prim/functor/operands_and_partials.hpp>
#include <cmath>

namespace stan {
namespace math {

template <typename T_y, typename T_loc, typename T_scale>
return_type_t<T_y, T_loc, T_scale> lognormal_lcdf(const T_y& y, const T_loc& mu,
                                                  const T_scale& sigma) {
  using T_partials_return = partials_return_t<T_y, T_loc, T_scale>;
  using T_y_ref = ref_type_if_t<!is_constant<T_y>::value, T_y>;
  using T_mu_ref = ref_type_if_t<!is_constant<T_loc>::value, T_loc>;
  using T_sigma_ref = ref_type_if_t<!is_constant<T_scale>::value, T_scale>;
  static const char* function = "lognormal_lcdf";

  T_y_ref y_ref = y;
  T_mu_ref mu_ref = mu;
  T_sigma_ref sigma_ref = sigma;

  const auto& y_col = as_column_vector_or_scalar(y_ref);
  const auto& mu_col = as_column_vector_or_scalar(mu_ref);
  const auto& sigma_col = as_column_vector_or_scalar(sigma_ref);

  const auto& y_arr = as_array_or_scalar(y_col);
  const auto& mu_arr = as_array_or_scalar(mu_col);
  const auto& sigma_arr = as_array_or_scalar(sigma_col);

  ref_type_t<decltype(value_of(y_arr))> y_val = value_of(y_arr);
  ref_type_t<decltype(value_of(mu_arr))> mu_val = value_of(mu_arr);
  ref_type_t<decltype(value_of(sigma_arr))> sigma_val = value_of(sigma_arr);

  check_not_nan(function, "Random variable", y_val);
  check_nonnegative(function, "Random variable", y_val);
  check_finite(function, "Location parameter", mu_val);
  check_positive_finite(function, "Scale parameter", sigma_val);

  if (size_zero(y, mu, sigma)) {
    return 0;
  }

  operands_and_partials<T_y_ref, T_mu_ref, T_sigma_ref> ops_partials(
      y_ref, mu_ref, sigma_ref);

  if (sum(promote_scalar<int>(y_val == 0))) {
    return ops_partials.build(NEGATIVE_INFTY);
  }

  const auto& log_y = log(y_val);
  const auto& scaled_diff
      = to_ref_if<!is_constant_all<T_y, T_loc, T_scale>::value>(
          (log_y - mu_val) / (sigma_val * SQRT_TWO));
  const auto& erfc_calc
      = to_ref_if<!is_constant_all<T_y, T_loc, T_scale>::value>(
          erfc(-scaled_diff));
  size_t N = max_size(y, mu, sigma);
  T_partials_return cdf_log = N * LOG_HALF + sum(log(erfc_calc));

  if (!is_constant_all<T_y, T_loc, T_scale>::value) {
    const auto& exp_m_sq_diff = exp(-scaled_diff * scaled_diff);
    const auto& rep_deriv = to_ref_if<!is_constant_all<T_y>::value
                                          + !is_constant_all<T_scale>::value
                                          + !is_constant_all<T_loc>::value
                                      >= 2>(
        -SQRT_TWO_OVER_SQRT_PI * exp_m_sq_diff / (sigma_val * erfc_calc));
    if (!is_constant_all<T_y>::value) {
      ops_partials.edge1_.partials_ = -rep_deriv / y_val;
    }
    if (!is_constant_all<T_loc>::value) {
      ops_partials.edge2_.partials_ = rep_deriv;
    }
    if (!is_constant_all<T_scale>::value) {
      ops_partials.edge3_.partials_ = rep_deriv * scaled_diff * SQRT_TWO;
    }
  }
  return ops_partials.build(cdf_log);
}

}  // namespace math
}  // namespace stan
#endif
