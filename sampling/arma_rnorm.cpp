#include <RcppArmadillo.h>
// [[Rcpp::depends(RcppArmadillo)]]
using namespace Rcpp;
using namespace arma;

// [[Rcpp::export]]
vec arma_rnorm(int n, double mean, double sd) {
  vec out(n); // Allocate a vector of dimension n
  for (int i = 0; i < n; i++) {
    out[i] = R::rnorm(mean, sd); // Sample from a Gaussian distribution
  }
  return out; 
}


// [[Rcpp::export]]
mat arma_dist(const mat& X){
  int n = X.n_rows;
  mat D(n, n, fill::zeros); // Allocate a matrix of dimension n x n
  for (int i = 0; i < n; i++) {
    for(int k = 0; k < i; k++){
      D(i, k) = sqrt(sum(pow(X.row(i) - X.row(k), 2)));
      D(k, i) = D(i, k);
    }
  }
  return D; 
}