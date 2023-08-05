#ifndef STAN_MATH_PRIM_CORE_OPERATOR_DIVISION_HPP
#define STAN_MATH_PRIM_CORE_OPERATOR_DIVISION_HPP

#include <stan/math/prim/meta/return_type.hpp>
#include <complex>

namespace stan {
namespace math {

namespace internal {
/**
 * Return the quotient of the specified arguments.  At least one of the
 * arguments must be a complex number.
 *
 * @tparam U type of first argumentx
 * @tparam V type of second argument
 * @param[in] lhs first argument
 * @param[in] rhs second argument
 * @return quotient of the arguments
 */
template <typename U, typename V>
inline complex_return_t<U, V> complex_divide(const U& lhs, const V& rhs) {
  complex_return_t<U, V> y(lhs);
  y /= rhs;
  return y;
}
}  // namespace internal

/**
 * Return the quotient of the arguments.
 *
 * @tparam U value type of first argument
 * @tparam V value type of second argument
 * @param x first argument
 * @param y second argument
 * @return quotient of the arguments
 */
template <typename U, typename V>
inline complex_return_t<U, V> operator/(const std::complex<U>& x,
                                        const std::complex<V>& y) {
  return internal::complex_divide(x, y);
}

/**
 * Return the quotient of the arguments.
 *
 * @tparam U value type of first argument
 * @tparam V type of second argument
 * @param x first argument
 * @param y second argument
 * @return quotient of the arguments
 */
template <typename U, typename V>
inline complex_return_t<U, V> operator/(const std::complex<U>& x, const V& y) {
  return internal::complex_divide(x, y);
}

/**
 * Return the quotient of the arguments.
 *
 * @tparam U type of first argument
 * @tparam V value type of second argument
 * @param x first argument
 * @param y second argument
 * @return quotient of the arguments
 */
template <typename U, typename V>
inline complex_return_t<U, V> operator/(const U& x, const std::complex<V>& y) {
  return internal::complex_divide(x, y);
}

}  // namespace math
}  // namespace stan

#endif
