/* A less simple result type
(C) 2017-2019 Niall Douglas <http://www.nedproductions.biz/> (6 commits)
File Created: June 2017


Boost Software License - Version 1.0 - August 17th, 2003

Permission is hereby granted, free of charge, to any person or organization
obtaining a copy of the software and accompanying documentation covered by
this license (the "Software") to use, reproduce, display, distribute,
execute, and transmit the Software, and to prepare derivative works of the
Software, and to permit third-parties to whom the Software is furnished to
do so, all subject to the following:

The copyright notices in the Software and this entire statement, including
the above license grant, this restriction and the following disclaimer,
must be included in all copies of the Software, in whole or in part, and
all derivative works of the Software, unless such copies or derivative
works are solely in the form of machine-executable object code generated by
a source language processor.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT
SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE
FOR ANY DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
*/

#ifndef BOOST_OUTCOME_STD_OUTCOME_HPP
#define BOOST_OUTCOME_STD_OUTCOME_HPP

#include "basic_outcome.hpp"
#include "std_result.hpp"

#ifndef STD_BASIC_OUTCOME_FAILURE_EXCEPTION_FROM_ERROR
#define STD_BASIC_OUTCOME_FAILURE_EXCEPTION_FROM_ERROR
namespace std  // NOLINT
{
  inline exception_ptr basic_outcome_failure_exception_from_error(const error_code &ec) { return make_exception_ptr(system_error(ec)); }
}  // namespace std
#endif

BOOST_OUTCOME_V2_NAMESPACE_EXPORT_BEGIN

/*! AWAITING HUGO JSON CONVERSION TOOL 
SIGNATURE NOT RECOGNISED
*/
template <class R, class S = std::error_code, class P = std::exception_ptr, class NoValuePolicy = policy::default_policy<R, S, P>>  //
using std_outcome = basic_outcome<R, S, P, NoValuePolicy>;

BOOST_OUTCOME_V2_NAMESPACE_END

#include "policy/outcome_error_code_throw_as_system_error.hpp"
#include "policy/outcome_exception_ptr_rethrow.hpp"

#endif
