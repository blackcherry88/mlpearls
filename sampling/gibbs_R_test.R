gibbs_R <- function(x, mu_mu, sigma2_mu, a_sigma, b_sigma, R, burn_in) {
  
  # Initialization
  n <- length(x)
  xbar <- mean(x)
  out <- matrix(0, R, 2)
  
  # Initial values for mu and sigma
  sigma2 <- var(x)
  mu <- xbar
  
  for (r in 1:(burn_in + R)) {
    
    # Sample mu
    sigma2_n <- 1 / (1 / sigma2_mu + n / sigma2)
    mu_n <- sigma2_n * (mu_mu / sigma2_mu + n / sigma2 * xbar)
    mu <- rnorm(1, mu_n, sqrt(sigma2_n))
    
    # Sample sigma2
    a_n <- a_sigma + 0.5 * n
    b_n <- b_sigma + 0.5 * sum((x - mu)^2)
    sigma2 <- 1 / rgamma(1, a_n, b_n)
    
    # Store the values after the burn-in period
    if (r > burn_in) {
      out[r - burn_in, ] <- c(mu, sigma2)
    }
  }
  out
}