#include <RcppArmadillo.h>
// [[Rcpp::depends(RcppArmadillo)]]
using namespace Rcpp;
using namespace arma;


// [[Rcpp::export]]
vec lm_coef3(const mat& X, const vec& y) {
  vec coef = solve(X, y);
  return coef;
}
