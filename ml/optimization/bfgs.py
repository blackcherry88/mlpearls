# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/710_optimization.bfgs.ipynb.

# %% auto 0
__all__ = ['line_search', 'bfgs']

# %% ../../nbs/710_optimization.bfgs.ipynb 4
from .grad import naive_grad


def line_search(f, grad_f, x0, p, nabla, c1=1e-4, c2=0.9):
    '''
    BACKTRACK LINE SEARCH WITH WOLFE CONDITIONS
    '''
    a = 1
    fx = f(x0)
    init_grad = grad_f(x0)
    
    x = x0 + a * p 
    nabla_new = grad_f(x)
    while f(x) >= fx + (c1*a*nabla.T@p) or nabla_new.T@p <= c2*nabla.T@p : 
        a *= 0.5
        x = x0 + a * p 
        nabla_new = grad_f(x)
    return a


def bfgs(f,x0,max_it,store=False):
    '''
    DESCRIPTION
    BFGS Quasi-Newton Method, implemented as described in Nocedal:
    Numerical Optimisation.
    INPUTS:
    f:      function to be optimised 
    x0:     intial guess
    max_it: maximum iterations 
    plot:   if the problem is 2 dimensional, returns 
            a trajectory plot of the optimisation scheme.
    OUTPUTS: 
    x:      the optimal solution of the function f 
    '''
    d = len(x0) # dimension of problem
    grad_f = naive_grad(f)
    nabla = grad_f(x0) # initial gradient 
    H = np.eye(d) # initial hessian
    x = x0[:]
    it = 2 
    if store == True: 
        if d == 2: 
            x_store =  np.zeros((1,2)) # storing x values 
            x_store[0,:] = x 
        else: 
            print('Too many dimensions to produce trajectory plot!')
            store = False

    while np.linalg.norm(nabla) > 1e-5: # while gradient is positive
        if it > max_it: 
            print('Maximum iterations reached!')
            break
        it += 1
        p = -H@nabla # search direction (Newton Method)
        a = line_search(f,grad_f, x, p, nabla) # line search 
        s = a * p 
        x_new = x + a * p 
        nabla_new = grad_f(x_new)
        y = nabla_new - nabla 
        y = np.reshape(y,(d,1))
        s = np.reshape(s,(d,1))
        
        r = 1/(y.T@s)
        li = np.eye(d)-r*(s@y.T)
        ri = np.eye(d)-r*(y@s.T)
        hess_inter = li@H@ri
        
        H = hess_inter + r*(s@s.T) # BFGS Update
        nabla = nabla_new[:]
        x = x_new[:]
        if store == True:
            x_store = np.append(x_store,[x],axis=0) # storing x
        
    return x, x_store
