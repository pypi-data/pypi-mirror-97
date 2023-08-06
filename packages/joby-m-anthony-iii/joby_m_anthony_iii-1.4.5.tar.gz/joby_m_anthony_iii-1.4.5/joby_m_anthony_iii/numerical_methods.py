#################################
## Preamble
# import necessary modules/tools

import math
import numpy as np
import random
from scipy.integrate import quad
import sympy as sp
import sys
from types import FunctionType
#   #   #   #   #   #   #   #   #

#################################
## Universal Variables/Methods
# common error messages
must_be_expression = 'I am sorry. The input function must be an expression.'
must_be_collection = 'I am sorry. The input function must be a collection.'
opposite_signs = 'Initial guesses must yield opposite signs.'
solution_found = 'Solution found!'
solution_not_found = 'Solution could not be found with initial guess or tolerance.'
func_func = 'Input expression used.'
# string outputs of polynomials
sym_x = sp.Symbol('x')

# common functions
def varname(obj, callingLocals=locals()):
    """
    quick function to print name of input and value. 
    If not for the default-Valued callingLocals, the function would always
    get the name as "obj", which is not what I want.    
    """
    for k, v in list(callingLocals.items()):
         if v is obj:
            name = k
            return name
# preceded by varname()
def diagonality(A):
    """Determines if matrix is strictly, diagonally dominant.

    Parameters
    ----------
    A : array
        Input matrix to be tested.

    Warns
    -----
    good_matrix : string
        Will print to console if strictly, diagonally dominant.
    
    bad_matrix : string
        Matrix, `A` not being strictly, diagonally dominant could lead to poor solution of 'Ac = g'.
    """
    sym_A = 'A' # varname(A)
    good_matrix = "WARNING! Matrix, " + sym_A + " is strictly, diagonally dominant."
    bad_matrix = "WARNING! Matrix, " + sym_A + " is not strictly, diagonally dominant. Solution may be inaccurate."
    A = np.array(A)
    i, diags, long = 0, np.zeros_like(A), np.zeros_like(A)
    while i < len(A):
        j = 0
        while j < len(A):
            aij = A[i][j]
            if i == j: long[i][j] = aij
            else: diags[i][j] = aij
            j += 1
        i += 1
    if np.sum(long) >= np.sum(diags): print(good_matrix)
    else: print(bad_matrix)

def eigen_values(A):
    """Finds the eigen values of matrix.

    Parameters
    ----------
    A : array
        Matrix of interest.
    
    Returns
    -------
    lambdas : array
        Eigen vector containing roots.

    Raises
    ------
    bad_matrix : string
        Matrix of interest must be square.
    """
    sym_A = 'A' # varname(A)
    bad_matrix = 'WARNING! Matrix, ' + sym_A + ' must be square!'
    if len(A) != len(A[0]): sys.exit(bad_matrix)
    A = np.array(A)
    sym_r = sp.Symbol('r')
    i, identityA = 0, np.zeros_like(A)
    while i < len(A):
        j = 0
        while j < len(A[0]):
            if i == j: identityA[i][j] = 1
            j += 1
        i += 1
    lambda_identity = identityA*sym_r
    determinant = sp.det(sp.Matrix(A - lambda_identity))
    roots = sp.solve(determinant)
    lambdas = []
    for r in roots:
        r = complex(r)
        if np.imag(r) == 0: r = np.real(r)
        lambdas.append(r)
    return lambdas
# preceded by eigen_values
def spectral_radius(A):
    """Finds the spectral radius of matrix.

    Parameters
    ----------
    A : array
        Matrix of interest.
    
    Returns
    -------
    rho : float
        Spectral radius.
    
    Raises
    ------
    bad_matrix : string
        Matrix of interest must be square.
    
    See Also
    --------
    eigen_values() : method to find eigen vector of `A`.
    """
    sym_A = 'A' # varname(A)
    bad_matrix = 'Matrix, ' + sym_A + ' must be square!'
    if len(A) != len(A[0]): sys.exit(bad_matrix)
    rho = np.max(np.abs(eigen_values(A)))
    return rho
# preceded by spectral_radius
def l_2_norm(x, x0=[]):
    """Square root of sum of differences squared along i'th row.

    Parameters
    ----------
    x : array
        Newly approximated guess.
    
    x0 : array
        Previously approximated guess.

    Returns
    -------
    l2_norm : float
        Scalar value.

    Examples
    --------
    [x0] = (1, 1, 1)^(t)

    [x] = (1.2001, 0.99991, 0.92538)^(t)

    ||x0 - x|| = sqrt[ (1 - 1.2001)^2 \
        + (1 - 0.99991)^2 + (1 - 0.92538)^2 ]

    ||x0 - x|| = 0.21356
    """
    x, x0 = np.array(x), np.array(x0)
    if x0.shape[0] == 0:
        # initialize loop
        i, norm_i = 0, np.zeros_like(x)
        if np.sum(x.shape) == x.shape[0]:
            for i in range(len(x)):
                # evaluate and store norm, ||.||
                norm_i[i] += x[i]**2
            l2_norm = math.sqrt(np.sum(norm_i))
        elif np.sum(x.shape) > x.shape[0]:
            x0 = np.reshape(x, (x.shape[0], x.shape[1]))
            xt = np.reshape(x, (x.shape[1], x.shape[0]))
            l2_norm = math.sqrt(spectral_radius(x0*xt))
    elif len(x) == len(x0):
        if np.sum(x0.shape) > x0.shape[0]:
            x0 = np.reshape(x0, (x0.shape[0], x0.shape[1]))
            xt = np.reshape(x, (x0.shape[1], x0.shape[0]))
        else: 
            x0 = np.reshape(x0, (len(x0), 1))
            xt = np.reshape(x, (1, len(x0)))
            # xt = np.reshape(x, (1, x.shape[0]))
        l2_norm = math.sqrt(spectral_radius(x0*xt))
    else: sys.exit("ERROR! 'x', and 'x0' must be the same size!")
    return l2_norm

def l_infinity_norm(x, x0=[]):
    """Maximum difference between absolute sum of i'th rows.

    Parameters
    ----------
    x : array or vector
        Newly approximated guess.
    
    x0 : array or vector
        Previously approximated guess.

    Returns
    -------
    `np.amax(norm_i)` : float
        Scalar value.

    Notes
    -----
    Best thought as "actual" distance between vectors.

    Also calculates infinity norm of matrix(ces).

    Examples
    --------
    [x0] = (1, 1, 1)^(t)

    [x] = (1.2001, 0.99991, 0.92538)^(t)

    ||x0 - x|| = max{|1 - 1.2001|, |1 - 0.99991|, |1 - 0.92538|}

    ||x0 - x|| = 0.2001
    """
    x, x0 = np.array(x), np.array(x0)
    # initialize loop
    i, norm_i = 0, np.zeros_like(x)
    if x0.shape[0] == 0:
        if np.sum(x.shape) == x.shape[0]:
            for i in range(x.shape[0]):
                # evaluate and store norm, ||.||
                norm_i[i] = abs(x[i])
        elif np.sum(x.shape) > x.shape[0]:
            norm_ij = np.zeros_like(x)
            for i in range(x.shape[0]):
                for j in range(x.shape[1]):
                    # evaluate and store norm, ||.||
                    norm_ij[i][j] = abs(x[i][j])
                norm_i[i] = np.sum(norm_ij[i][:])
    elif len(x) == len(x0):
        if np.sum(x0.shape) == x0.shape[0]:
            for i in range(x0.shape[0]):
                norm_i[i] = abs(x[i] - x0[i])
        elif np.sum(x0.shape) > x0.shape[0]:
            if np.sum(x.shape) == np.sum(x0.shape):
                for i in range(x0.shape[0]):
                    for j in range(x0.shape[1]):
                        norm_ij = np.zeros_like(x)
                        # evaluate and store norm, ||.||
                        norm_ij[i][j] = abs(x[i][j] - x0[i][j])
                    norm_i[i] = np.sum(norm_ij[i][:])
            elif np.sum(x.shape) == np.sum(x0.shape):
                for i in range(x0.shape[0]):
                    # evaluate and store norm, ||.||
                    norm_i[i] = abs(x[i] - x0[i])
    else: sys.exit("ERROR! 'x', and 'x0' must be the same size!")
    # return the l_infinity norm
    return np.amax(norm_i)
# preceded by l_2_norm and l_infinity_norm
def condition_number(A, norm_type):
    """Find the condition number of a given matrix and norm type.

    Parameters
    ----------
    A : array
        Input matrix for analysis.
    
    norm_type : string
        Selects norm comparison.
    
    Returns
    -------
    k : float
        Condition number of matrix, A.

    Warnings
    --------
    Will output evaluation of condition number and show in console.

    See Also
    --------
    l_2_norm() : Yields the l_2 norm.
    
    l_infinity_norm() : Yields the l_infinity norm.
    """
    sym_A = 'A' # varname(A)
    A = np.array(A)
    i, A_inv = 0, np.zeros_like(A)
    while i < len(A):
        j = 0
        while j < len(A):
            aij = A[i][j]
            if aij != 0: A_inv[i][j] = 1/aij
            j += 1
        i += 1
    if norm_type == 'l_2_norm': 
        norm, abnorm = l_2_norm(A), l_2_norm(A_inv)
    if norm_type == 'l_infinity_norm':
        norm, abnorm = l_infinity_norm(A), l_infinity_norm(A_inv)
    k = norm*abnorm
    print('Condition Number K(' + sym_A + ') = ', k)
    return k

def make_array(X, f):
    """Maps domain to range.

    Parameters
    ----------
    X : array
        Collection if input data.

    f : expression
        Equation which maps the domain to range.
    
    Returns
    -------
    g : array
        Mapped range from equation.
    
    Warns
    -----
    func_func : string
        Input expression was in fact used.
    """
    print(func_func)
    X = np.array(X)
    i, g = 0, np.zeros_like(X)
    while i < len(X):
        j = 0
        if np.sum(X.shape) > np.sum(X.shape[0]):
            while j < len(X[0]):
                g[i][j] = (f(X[i][j]))
                j += 1
        else: g[i] = f(X[i])
        i += 1
    return g

def symmetry(A):
    """Determines boolean truth value if symmetric or not.

    Parameters
    ----------
    A : array
        Matrix of interest.
    
    Returns
    -------
    value : int
        Boolean truth value.
    
    Raises
    ------
    bad_matrix : string
        Matrix of interest must be square.

    Warns
    -----
    symmetric : string
        Console print that `A` is symmetric.

    asymmetric : string
        Console print that `A` is not symmetric.
    """
    sym_A = 'A' # varname(A)
    bad_matrix = 'ERROR! Matrix, ' + sym_A + ' must be square!'
    symmetric = 'Matrix, ' + sym_A + ' is symmetric.'
    asymmetric = 'Matrix, ' + sym_A + ' is not symmetric.'
    if len(A) != len(A[0]): sys.exit(bad_matrix)
    A = np.array(A)
    i, At, value = 0, np.transpose(A), 0
    for ai in A:
        j = 0
        for aj in ai:
            if aj == At[i][j]: value = 1
            else: value = 0; print(asymmetric); break
            j += 1
        i += 1
    if value == 1: print(symmetric)
    return value

def tridiagonality(A):
    """Find the condition number of a given matrix and norm type.

    Parameters
    ----------
    A : array
        Input matrix for analysis.
    
    norm_type : string
        Selects norm comparison.
    
    Returns
    -------
    value : int
        Boolean state of truth.

    Warns
    -----
    bad_matrix : string
        Matrix is not tridiagonal.
    
    good_matrix : string
        Matrix is tridiagonal.
    """
    sym_A = 'A' # varname(A)
    bad_matrix = 'Matrix, ' + sym_A + ' is not tridiagonal.'
    good_matrix = 'Matrix, ' + sym_A + ' is tridiagonal.'
    A = np.array(A)
    long, above, below = np.zeros_like(A), np.zeros_like(A), np.zeros_like(A)
    i = 0
    while i < len(A):
        j = 0
        while j < len(A):
            aij = A[i][j]
            if i == j: long[i][j] = aij
            if i == j + 1: above[i][j] = aij
            if i == j - 1: below[i][j] = aij
            j += 1
        i += 1 
    non_A = A - (long + above + below)
    for ai in non_A:
        for aj in ai:
            if aj == 0: value = 1
            else: value = 0; print(bad_matrix); break
    if value == 1: print(good_matrix)
    return value
#   #   #   #   #   #   #   #   #


#################################
## Specific Functions
# various techniques

# --------------------
# iterative techniques
def max_iterations(a, b, power, method, k=0, p0=0):
    """Find greatest integer for maximum iterations for tolerance.

    Parameters
    ----------
    f : expression
        Input function.
    
    a : float
        Left-hand bound of interval.
    
    b : float
        Right-hand bound of interval.
    
    tol : float
        Specified tolerance until satisfying method.
    
    method : string
        Selection of iterative method for iterations are needed.
    
    k : float
        Maximum possible slope of input function.
    
    p0 : float
        Initial guess for function solution.
    
    Returns
    -------
    N_max : integer
        Maximum number of iterations required for specified tolerance.

    Raises
    ------
    bad_method : string
        Prescribed method is not an available option.
    
    Warnings
    --------
    number_of_iter : Informs user of maximum number of iterations.

    Notes
    -----
    Will round away from zero to higher integers.

    Examples
    --------
    If `method == 'bisection'` & a=1, b=2, and tol=-3, then:
    `N_max` >= -log(`tol`/(`b` - `a`))/log(2)

    `N_max` >= -log((10**(-3)/(2 - 1))/log(2)

    `N_max` >= 9.96

    `N_max` = 10

    Else, if a=1, b=2, tol=-3, p0=1.5, nd k=0.9, then:
    `N_max` >= log(`tol`/max('p0' - `a`, `b` - `p0`))/log(k)
    
    `N_max` >= log(10**(-3)/max(1.5 - 1, 2 - 1.5))/log(0.9)
    
    `N_max` >= log(10**(-3)/0.5)/log(0.9)
    
    `N_max` >= 58.98
    
    `N_max` >= 59
    """
    number_of_iter = 'With the inputs, I will terminate the technique after so many iterations, N = '
    bad_method = 'I am sorry. The desired method must be: bisection, fixed point, newton raphson, secant method, or false position.'
    a, b, tol = float(a), float(b), float(10**power)
    if method == 'bisection':
        N_max = math.ceil(-math.log(tol/(b - a))/math.log(2))
    for each in ['fixed point', 'newton raphson', 'secant method', 'false position']:
        if method == each:
            N_max = math.ceil(math.log(tol/max(p0 - a, b - p0))/math.log(k))
            break
        else: continue
    else: sys.exit('ERROR! ', bad_method)
    print(number_of_iter, N_max)
    return N_max

# the following 5 functions are preceded by max_iterations

def bisection(f, a, b, power):
    """Given f(x) in [`a`,`b`] find x within tolerance, `tol`.
    Root-finding method: f(x) = 0.

    Parameters
    ----------
    f : expression
        Input function.
    
    a : float
        Left-hand bound of interval.
    
    b : float
        Right-hand bound of interval.
    
    power : float
        Signed, specified power of tolerance until satisfying method.
    
    Returns
    -------
    P : list
        Aggregate collection of evaluated points, `p`.
    
    ERROR : list
        Propogation of `error` through method.
    
    I : list
        Running collection of iterations through method.

    Raises
    ------
    opposite_signs : string
        If initial guesses did not evaluate to have opposite signs.
    
    must_be_expression : string
        If input `f` was of array, list, tuple, etcetera...
    
    Warns
    -----
    solution_found : string
        Inform user that solution was indeed found.

    solution_not_found : string
        If initial guess or tolerance were badly defined.

    Notes
    -----
    Relying on the Intermediate Value Theorem, this is a bracketed, root-finding method. Generates a sequence {p_n}^{inf}_{n=1} to approximate a zero of f(x), `p` and converges by O(1 / (2**N)).

    Examples
    --------
    If  f(x) = x**3 + 4*x**2 = 10
    
    =>  f(x) = x**3 + 4*x**2 - 10 = 0
    """
    a, b, tol = float(a), float(b), float(10**power)
    # calculate if expression
    if isinstance(f,(FunctionType, sp.Expr)):
        # check if f(a) and f(b) are opposite signs
        if f(a)*f(b) < 0:
            P, ERROR, I = [], [], []    # initialize lists
            N = max_iterations(a, b, power, 'bisection')
            i, error = 0, tol*10        # initialize
            # exit by whichever condition is TRUE first
            while error >= tol and i <= N:
                x = (b - a)/2
                p = a + x               # new value, p
                P.append(p)
                if f(a)*f(p) > 0: a = p # adjust next bounds
                else: b = p
                error = abs(x)          # error of new value, p
                ERROR.append(error); I.append(i)
                i += 1                  # iterate to i + 1
            if i < N: print('Congratulations! ', solution_found)
            else: print('Warning! ', solution_not_found)
        # abort if f(a) is not opposite f(b)
        else: sys.exit('ERROR! ', opposite_signs)
    # abort if not expression
    else: sys.exit('ERROR! ', must_be_expression)
    return P, ERROR, I

def false_position(f, k, a, b, p0, p1, power):
    """Given f(x) and initial guesses, `p0` and `p1` in [`a`,`b`] find x within tolerance, `tol`.
    
    Root-finding problem: f(x) = 0. 
    
    !!! Use lowest k !!!

    Parameters
    ----------
    f : expression
        Input function.
    
    k : float
        Absolute maximum slope of `f`.
    
    a : float
        Left-hand bound of interval.
    
    b : float
        Right-hand bound of interval.
    
    p0 : float
        First initial guess.
    
    p1 : float
        Second initial guess.
    
    power : float
        Signed, specified power of tolerance until satisfying method.
    
    Returns
    -------
    P : list
        Aggregate collection of evaluated points, `p`.
    
    ERROR : list
        Propogation of `error` through method.
    
    I : list
        Running collection of iterations through method.

    Raises
    ------
    opposite_signs : string
        If initial guesses did not evaluate to have opposite signs.
    
    must_be_expression : string
        If input `f` was of array, list, tuple, etcetera...

    Warns
    -----
    solution_found : string
        Inform user that solution was indeed found.

    solution_not_found : string
        If initial guess or tolerance were badly defined.
    
    Notes
    -----
    Check that |g'(x)| <= (leading coefficient of g'(x)) for all x in [`a`,`b`].

    Theorem:
    1) Existence of a fixed-point:
        If g in C[`a`,`b`] and g(x) in C[`a`,`b`] for all x in [`a`,`b`], then function, g has a fixed point in [`a`,`b`].
    
    2) Uniqueness of a fixed point:
        If g'(x) exists on [`a`,`b`] and a positive constant, `k` < 1 exist with {|g'(x)| <= k  |  x in (`a`,`b`)}, then there is exactly one fixed-point, `p` in [`a`,`b`].

    Converges by O(linear) if g'(p) != 0, and O(quadratic) if g'(p) = 0 and g''(p) < M, where M = g''(xi) that is the error function.

    Examples 
    --------
    If  g(x) = x**2 - 2

    Then    p = g(p) = p**2 - 2
    
    =>  p**2 - p - 2 = 0
    """
    k, a, b, p0, p1, tol = float(k), float(a), float(b), float(p0), float(p1), float(10**power)
    # calculate if expression
    if isinstance(f,(FunctionType, sp.Expr)):
        # check if f(a) and f(b) are opposites signs
        if f(p0)*f(p1) < 0:
            P, ERROR, I = [], [], []    # initialize lists
            N = max_iterations(a, b, power, 'false position', k, p0)
            i, error = 0, tol*10        # initialize
            # exit by whichever condition is TRUE first
            while error >= tol and i <= N:
                q0, q1 = f(p0), f(p1)
                # new value, p
                p = p1 - q1*(p1 - p0)/(q1 - q0)
                P.append(p)
                error = abs(p - p0)     # error of new value, p
                ERROR.append(error); I.append(i)
                if f(p)*q1 < 0: p0 = p1 # adjust next bounds
                p1 = p
                i += 1                  # iterate to i + 1
            if i < N: print('Congratulations! ', solution_found)
            else: print('Warning! ', solution_not_found)
        # abort if f(a) is not opposite f(b)
        else: sys.exit('ERROR! ', opposite_signs)
    # abort if not expression
    else: sys.exit('ERROR! ', must_be_expression)
    return P, ERROR, I

def fixed_point(f, k, a, b, p0, power):
    """Given f(x) and initial guess, `p0` in [`a`,`b`] find x within tolerance, `tol`.
    
    Root-finding problem: f(x) = 0. 
    
    !!! Use lowest k !!!

    Parameters
    ----------
    f : expression
        Input function.
    
    k : float
        Absolute maximum slope of `f`.
    
    a : float
        Left-hand bound of interval.
    
    b : float
        Right-hand bound of interval.
    
    p0 : float
        Initial guess.
    
    power : float
        Signed, specified power of tolerance until satisfying method.
    
    Returns
    -------
    P : list
        Aggregate collection of evaluated points, `p`.
    
    ERROR : list
        Propogation of `error` through method.
    
    I : list
        Running collection of iterations through method.

    Raises
    ------
    must_be_expression : string
        If input `f` was of array, list, tuple, etcetera...

    Warns
    -----
    solution_found : string
        Inform user that solution was indeed found.

    solution_not_found : string
        If initial guess or tolerance were badly defined.
    
    Notes
    -----
    Check that |g'(x)| <= (leading coefficient of g'(x)) for all x in [`a`,`b`].

    Theorem:
    1) Existence of a fixed-point:
        If g in C[`a`,`b`] and g(x) in C[`a`,`b`] for all x in [`a`,`b`], then function, g has a fixed point in [`a`,`b`].
    
    2) Uniqueness of a fixed point:
        If g'(x) exists on [`a`,`b`] and a positive constant, `k` < 1 exist with {|g'(x)| <= k  |  x in (`a`,`b`)}, then there is exactly one fixed-point, `p` in [`a`,`b`].

    Converges by O(linear) if g'(p) != 0, and O(quadratic) if g'(p) = 0 and g''(p) < M, where M = g''(xi) that is the error function.

    Examples 
    --------
    If  g(x) = x**2 - 2

    Then    p = g(p) = p**2 - 2
    
    =>  p**2 - p - 2 = 0
    """
    k, a, b, p0, tol = float(k), float(a), float(b), float(p0), float(10**power)
    # calculate if expression
    if isinstance(f,(FunctionType, sp.Expr)):
        P, ERROR, I = [], [], []    # initialize lists
        N = max_iterations(a, b, power, 'fixed point', k, p0)
        i, error = 0, tol*10        # initialize
        # exit by whichever condition is TRUE first
        while error >= tol and i <= N:
            p = f(p0)               # new value, p
            P.append(p)
            error = abs(p - p0)     # error of new value, p
            ERROR.append(error); I.append(i)
            p0 = p                  # set future previous value
            i += 1                  # iterate to i + 1
        if i < N: print('Congratulations! ', solution_found)
        else: print('Warning! ', solution_not_found)
    # abort if not expression
    else: sys.exit('ERROR! ', must_be_expression)
    return P, ERROR, I

class newton_raphson:

    def single_variable(f, k, a, b, p0, power, x=sp.Symbol('x')):
        """Given f(x) and initial guess, `p0` in [`a`,`b`], find x within tolerance, `tol`.
        
        Root-finding problem: f(x) = 0. 
        
        !!! Use lowest k !!!

        Parameters
        ----------
        f : expression
            Input function.
        
        k : float
            Absolute maximum slope of `f`.
        
        a : float
            Left-hand bound of interval.
        
        b : float
            Right-hand bound of interval.
        
        p0 : float
            Initial guess.
        
        power : float
            Signed, specified power of tolerance until satisfying method.
        
        x : symbol
            Respected variable in derivative. Assumed to be `'x'` if not stated.
        
        Returns
        -------
        P : list
            Aggregate collection of evaluated points, `p`.
        
        ERROR : list
            Propogation of `error` through method.
        
        I : list
            Running collection of iterations through method.

        Raises
        ------
        must_be_expression : string
            If input `f` was of array, list, tuple, etcetera...

        Warns
        -----
        solution_found : string
            Inform user that solution was indeed found.
        
        solution_not_found : string
            If initial guess or tolerance were badly defined.

        Notes
        -----
        f'(x) != 0.
        
        Not root-bracketed.

        Initial guess must be close to real solution; else, will converge to different root or oscillate (if symmetric).

        Check that |g'(x)| <= (leading coefficient of g'(x)) for all x in [`a`,`b`].

        Technique based on first Taylor polynomial expansion of `f` about `p0` and evaluated at x = p. |p - p0| is assumed small; therefore, 2nd order Taylor term, the error, is small.

        Newton-Raphson has quickest convergence rate.

        This method can be viewed as fixed-point iteration.

        Theorem:
        1) Existence of a fixed-point:
            If g in C[`a`,`b`] and g(x) in C[`a`,`b`] for all x in [`a`,`b`], then function, g has a fixed point in [`a`,`b`].
        
        2) Uniqueness of a fixed point:
            If g'(x) exists on [`a`,`b`] and a positive constant, `k` < 1 exist with {|g'(x)| <= k  |  x in (`a`,`b`)}, then there is exactly one fixed-point, `p` in [`a`,`b`].

        Converges by O(linear) if g'(p) != 0, and O(quadratic) if g'(p) = 0 and g''(p) < M, where M = g''(xi) that is the error function.

        Examples 
        --------
        If  g(x) = x**2 - 2

        Then    p = g(p) = p**2 - 2
        
        =>  p**2 - p - 2 = 0
        """
        k, a, b, p0, tol = float(k), float(a), float(b), float(p0), float(10**power)
        # calculate if expression
        if isinstance(f,(FunctionType, sp.Expr)):
            # determine form of derivative
            df = sp.lambdify(x, sp.diff(f(x)))
            P, ERROR, I = [], [], []    # initialize lists
            N = max_iterations(a, b, power, 'newton raphson', k, p0)
            i, error = 0, tol*10        # initialize
            # exit by whichever condition is TRUE first
            while error >= tol and i <= N:
                fp0 = f(p0)
                dfp0 = df(p0)
                p = p0 - (fp0/dfp0)     # new value, p
                P.append(p)
                error = abs(p - p0)     # error of new value, p
                ERROR.append(error); I.append(i)
                p0 = p                  # set future previous value
                i += 1                  # iterate to i + 1
            if i < N: print('Congratulations! ', solution_found)
            else: print('Warning! ', solution_not_found)
        # abort if not expression
        else: sys.exit('ERROR! ', must_be_expression)
        return P, ERROR, I
    
    def multi_variate(f, symbols, x0, powers, N, normType=0):
        def jacobian(g, sym_x, x):
            n = len(x)
            jacMatrix = np.zeros((n, n))
            for i in range(0, n):
                for j in range(0, n):
                    J_ij = sp.diff(g[i](*sym_x), sym_x[j])
                    temp = sp.lambdify(sym_x, J_ij)(*x)
                    if isinstance(temp, type(np.array([1]))): temp = temp[0]
                    jacMatrix[i][j] = temp
            return jacMatrix
        f, x0 = np.array(f), np.array(x0)
        for each in symbols:
            if isinstance(each, type(sp.Symbol('x'))): continue
            else: sys.exit('')
        if not isinstance(N, int): sys.exit('')
        n = len(x0)
        if normType == 0:
            tol = []
            for p in powers: tol.append(10**p)
        else: tol = 10**powers
        f, x0 = np.reshape(f, (1, n))[0], np.reshape(x0, (n, 1))
        for k in range(1, N):
            J = jacobian(f, symbols, x0)
            xk, g = np.zeros_like(x0), np.zeros_like(x0)
            for i in range(0, n): 
                g[i] = sp.lambdify(symbols, f[i](*symbols))(*x0)
            y0 = np.linalg.solve(J, -g)
            xk = x0 + y0
            if normType == 0:
                boolean = []
                for i in range(0, n-1):
                    if abs(xk[i] - x0[i])[0] <= tol[i]: boolean.append(1)
                    else: boolean.append(0)
                x0 = xk
                if sum(boolean) < n: continue
                else: break
            elif normType == 'infinity':
                norm = l_infinity_norm(xk, x0)
                if norm <= tol: return xk
                else: x0 = xk
            else: sys.exit('')
        return x0

def secant_method(f, k, a, b, p0, p1, power):
    """Given f(x) and initial guesses, `p0` and `p1` in [`a`,`b`], find x within tolerance, `tol`.
    Root-finding problem: f(x) = 0. 
    
    !!! Use lowest k !!!

    Parameters
    ----------
    f : expression
        Input function.
    
    k : float
        Absolute maximum slope of `f`.
    
    a : float
        Left-hand bound of interval.
    
    b : float
        Right-hand bound of interval.
    
    p0 : float
        First initial guess.
    
    p1 : float
        Second initial guess.
    
    power : float
        Signed, specified power of tolerance until satisfying method.
    
    Returns
    -------
    P : list
        Aggregate collection of evaluated points, `p`.
    
    ERROR : list
        Propogation of `error` through method.
    
    I : list
        Running collection of iterations through method.

    Raises
    ------
    opposite_signs : string
        If initial guesses did not evaluate to have opposite signs.
    
    must_be_expression : string
        If input `f` was of array, list, tuple, etcetera...

    Warns
    -----
    solution_found : string
        Inform user that solution was indeed found.

    solution_not_found : string
        If initial guess or tolerance were badly defined.

    Notes
    -----
    Not root-bracketed.

    Bypasses need to calculate derivative (as in Newton-Raphson).

    Check that |g'(x)| <= (leading coefficient of g'(x)) for all x in [`a`,`b`].

    Theorem:
    1) Existence of a fixed-point:
        If g in C[`a`,`b`] and g(x) in C[`a`,`b`] for all x in [`a`,`b`], then function, g has a fixed point in [`a`,`b`].
    
    2) Uniqueness of a fixed point:
        If g'(x) exists on [`a`,`b`] and a positive constant, `k` < 1 exist with {|g'(x)| <= k  |  x in (`a`,`b`)}, then there is exactly one fixed-point, `p` in [`a`,`b`].

    Converges by O(linear) if g'(p) != 0, and O(quadratic) if g'(p) = 0 and g''(p) < M, where M = g''(xi) that is the error function.

    Examples 
    --------
    If  g(x) = x**2 - 2

    Then    p = g(p) = p**2 - 2
    
    =>  p**2 - p - 2 = 0
    """
    k, a, b, p0, p1, tol = float(k), float(a), float(b), float(p0), float(p1), float(10**power)
    # calculate if expression
    if isinstance(f,(FunctionType, sp.Expr)):
        # check if f(a) and f(b) are opposite signs
        if f(p0)*f(p1) < 0:
            P, ERROR, I = [], [], []    # initialize lists
            N = max_iterations(a, b, power, 'secant method', k, p0)
            i, error = 0, tol*10        # initialize
            # exit by whichever condition is TRUE first
            while error >= tol and i <= N:
                q0, q1 = f(p0), f(p1)
                # new value, p
                p = p1 - q1*(p1 - p0)/(q1 - q0)
                P.append(p)
                error = abs(p - p0)     # error of new value
                ERROR.append(error); I.append(i)
                p0, p1 = p1, p          # set future previous values
                i += 1                  # iterate to i + 1
            if i < N: print('Congratulations! ', solution_found)
            else: print('Warning! ', solution_not_found)
        # abort if f(a) is not opposite f(b)
        else: sys.exit('ERROR! ', opposite_signs)
    # abort if not expression
    else: sys.exit('ERROR! ', must_be_expression)
    return P, ERROR, I

# systems of equations

def jacobi(A, x0, b, N, power, norm_type):
    """Given [`A`]*[`x`] = [`b`], use `norm_type` to find [x].

    Parameters
    ----------
    A : matrix
        Characteristic matrix.
    
    x0 : vector
        Dimensions of system of equations.
    
    b : vector
        Input vector.
    
    N : int
        Maximum number of iterations.
    
    power : float
        Signed, specified power of tolerance until satisfying method.
    
    norm_type : string
        Prescription of desired norm.
    
    Returns
    -------
    X_matrix : array
        Finally evaluated solution.
    
    NORM : list
        Aggregate of yielded norms.
    
    K : list
        Running collection of iterations through method.

    Raises
    ------
    bad_matrix : string
        If [`A`] is not square.
    
    bad_x0 : string
        If {`x0`} is neither n x 1 nor 1 x n array.
    
    bad_b : string
        If {`b`} is neither n x 1 nor 1 x n array.
    
    bad_N : string
        If iterations constraints is not an integer.
    
    bad_type : string
        If desired norm method was neither `'l_infinity'` nor `'l_2'`.

    Warns
    -----
    non_triad : string
        Matrix, `A` not being tridiagonal violates theorem.

    incalculable : string
        Matrix, `A` not being positive definite violates theorem.

    solution_found : string
        Inform user that solution was indeed found.

    solution_not_found : string
        If initial guess or tolerance were badly defined.
    
    See Also
    --------
    diagonality() : Informs user if matrix, `A` is strictly, diagonally dominant. Solution will proceed even if not, but with a caveat that final solution may be inaccurate.

    l_infinity_norm() : Will find the l_infinity norm between `x0` and `xi`.

    l_2_norm() : Will find the l_2 norm between `x0` and `xi`.

    Notes
    -----
    jacobi():
    [x]_(k) = ( D^(-1)*(L + U) ) * [x]_(k - 1) + ( D^(-1) ) * [b]
    """
    sym_A, sym_x0, sym_b = 'A', 'x0', 'b' # varname(A), varname(x0), varname(b)
    bad_matrix = 'Characteristic matrix, ' + sym_A + ' must be square!'
    bad_x0 = 'Systems vector, ' + sym_x0 + ' must be n x 1 or 1 x n array!'
    bad_b = 'Input vector, ' + sym_b + ' must be n x 1 or 1 x n array!'
    bad_N = "Maximum iterations, N must be an integer greater than zero."
    bad_type = "Desired norm type was not understood. Please choose 'l_infinity' or 'l_2'."
    A = np.array(A)
    if len(A) != len(A[0]): sys.exit('ERROR! ', bad_matrix)
    if np.sum(x0.shape) > np.sum(x0.shape[0]): sys.exit('ERROR! ', bad_x0)
    if np.sum(b.shape) > np.sum(b.shape[0]): sys.exit('ERROR! ', bad_b)
    if N <= 0 or not isinstance(N, int): sys.exit('ERROR! ', bad_N)
    if norm_type != 'l_infinity' and norm_type != 'l_2': sys.exit('ERROR! ', bad_type)
    diagonality(A)
    tol = float(10**power)
    n = len(x0)
    k, x0, b, norm = 0, np.reshape(x0,(n,1)), np.reshape(b,(n,1)), tol*10
    xi = np.zeros_like(x0)
    X, NORM, K = [], [], [] 
    X.append(x0); K.append(k)
    if norm > tol and k >= N:
        i = 0
        while i < n:
            j, y = 0, 0.
            while j < n:
                if j != i:
                    y += A[i][j]*x0[j]
                    j += 1
            xi[i] = (-y + b[i])/A[i][i]
            i += 1
        if norm_type == 'l_infinity': norm = l_infinity_norm(xi, x0)
        if norm_type == 'l_2': norm = l_2_norm(xi, x0)
        X.append(xi); NORM.append(norm); K.append(k)
        x0 = xi
        k += 1
    if k < N: print('Congratulations! ', solution_found)
    else: print('Warning! ' + solution_not_found)
    m, n = len(X[0]), len(X)
    X_matrix, j = np.zeros((m,n)), 0
    while j < n:
        i = 0
        while i < m:
            X_matrix[i][j] = float(X[j][i])
            i += 1
        j += 1
    return X_matrix, NORM, K

def gauss_seidel(A, x0, b, N, power, norm_type):
    """Given [`A`]*[`x`] = [`b`], use `norm_type` to find [x].

    Parameters
    ----------
    A : matrix
        Characteristic matrix.
    
    x0 : vector
        Dimensions of system of equations.
    
    b : vector
        Input vector.
    
    N : int
        Maximum number of iterations.
    
    power : float
        Signed, specified power of tolerance until satisfying method.
    
    norm_type : string
        Prescription of desired norm.
    
    Returns
    -------
    X_matrix : array
        Finally evaluated solution.
    
    NORM : list
        Aggregate of yielded norms.
    
    K : list
        Running collection of iterations through method.

    Raises
    ------
    bad_matrix : string
        If [`A`] is not square.
    
    bad_x0 : string
        If {`x0`} is neither n x 1 nor 1 x n array.
    
    bad_b : string
        If {`b`} is neither n x 1 nor 1 x n array.
    
    bad_N : string
        If iterations constraints is not an integer.
    
    bad_type : string
        If desired norm method was neither `'l_infinity'` nor `'l_2'`.

    Warns
    -----
    non_triad : string
        Matrix, `A` not being tridiagonal violates theorem.

    incalculable : string
        Matrix, `A` not being positive definite violates theorem.

    solution_found : string
        Inform user that solution was indeed found.

    solution_not_found : string
        If initial guess or tolerance were badly defined.

    See Also
    --------
    diagonality() : Informs user if matrix, `A` is strictly, diagonally dominant. Solution will proceed even if not, but with a caveat that final solution may be inaccurate.

    l_infinity_norm() : Will find the l_infinity norm between `x0` and `xi`.

    l_2_norm() : Will find the l_2 norm between `x0` and `xi`.

    Notes
    -----
    gauss_seidel():
        [x]_(k) = ( (D - L)^(-1) * U ) * [x]_(k - 1) + ( (D - L)^(-1) )*[b]
    """
    sym_A, sym_x0, sym_b = 'A', 'x0', 'b' # varname(A), varname(x0), varname(b)
    bad_matrix = 'Characteristic matrix, ' + sym_A + ' must be square!'
    bad_x0 = 'Systems vector, ' + sym_x0 + ' must be n x 1 or 1 x n array!'
    bad_b = 'Input vector, ' + sym_b + ' must be n x 1 or 1 x n array!'
    bad_N = "Maximum iterations, N must be an integer greater than zero."
    bad_type = "Desired norm type was not understood. Please choose 'l_infinity' or 'l_2'."
    A = np.array(A)
    if len(A) != len(A[0]): sys.exit('ERROR! ', bad_matrix)
    if np.sum(x0.shape) > np.sum(x0.shape[0]): sys.exit('ERROR! ', bad_x0)
    if np.sum(b.shape) > np.sum(b.shape[0]): sys.exit('ERROR! ', bad_b)
    if N <= 0 or not isinstance(N, int): sys.exit('ERROR! ', bad_N)
    if norm_type != 'l_infinity' and norm_type != 'l_2': sys.exit('ERROR! ', bad_type)
    diagonality(A)
    tol = float(10**power)
    n = len(x0)
    k, x0, b, norm = 0, np.reshape(x0,(n,1)), np.reshape(b,(n,1)), tol*10
    xi = np.zeros_like(x0)
    X, NORM, K = [], [], [] 
    X.append(x0); K.append(k)
    if norm > tol and k >= N:
        i = 0
        while i < n:
            j, y1, y2 = 0, 0., 0.
            while j < i-1:
                y1 += A[i][j]*xi[j]
                j += 1
            j = i + 1
            while j < n:
                y2 += A[i][j]*x0[j]
                j += 1
            xi[i] = (-y1 - y2 + b[i])/A[i][i]
            i += 1
        if norm_type == 'l_infinity': norm = l_infinity_norm(xi, x0)
        if norm_type == 'l_2': norm = l_2_norm(xi, x0)
        X.append(xi); NORM.append(norm); K.append(k)
        x0 = xi
        k += 1
    if k < N: print('Congratulations! ', solution_found)
    else: print('Warning! ' + solution_not_found)
    m, n = len(X[0]), len(X)
    X_matrix, j = np.zeros((m,n)), 0
    while j < n:
        i = 0
        while i < m:
            X_matrix[i][j] = float(X[j][i])
            i += 1
        j += 1
    return X_matrix, NORM, K

def find_omega(A, x0, w=0):
    """Given the characteristic matrix and solution vector, determine if prescribed `w` is the optimum choice.

    Parameters
    ----------
    A : array
        Characteristic matrix of system of equations.
    
    x0 : vector
        Dimensions of systems of equations.
    
    w : float
        Relaxation parameter.
    
    Returns
    -------
    omega : float
        If found, is the optimum choice of `w`.
    
    Warns
    -----
    will_converege : string
        If 0<w<2, then method will converge regardless of choice for `x0`.
    
    non_triad : string
        Will inform user that matrix, `A` is not tridiagonal, but will proceed with calculation all the same.

    incalculable : string
        If matrix, `A` is poorly defined and not found to be positive definite, then user is informed but calculation proceeds.

    See Also
    --------
    tridiagonality() : Determines if matrix, `A` is tridiagonal or not.

    spectral_radius() : Uses the spectral radius of Gauss-Seidel's T-matrix to calculate omega.

    Notes
    -----
    Unless specified, `w` will be zero and chosen, if possible.
    """
    sym_A = 'A' # varname(A)
    will_converge = "According to Ostrowski-Reich's Theorem, the successive relaxation technique will converge."
    non_triad = 'Matrix, ' + sym_A + ' is not tridiagonal.'
    incalculable = 'I could not determine if matrix, ' + sym_A + ' was positive definite.'
    A, omega = np.array(A), float(w)
    xn = sp.Matrix(np.reshape(np.zeros_like(x0), (len(x0), 1)))
    xt = sp.Matrix(np.reshape(np.zeros_like(x0), (1, len(x0))))
    i = 0
    for x in np.array(x0): xn[i], xt[i] = x, x; i += 1
    y = xt*sp.Matrix(A)*xn
    if y[0] > 0: state = 1
    else: state = 0
    if symmetry(A) == 1 and state == 1: theorem_6_22 = 1
    i = 1
    while i <= len(A):
        Ai = sp.Matrix(A[:i,:i])
        if sp.det(Ai) > 0: theorem_6_25 = 1
        else : theorem_6_25 = 0; break
        i += 1
    if theorem_6_22 == 1 or theorem_6_25 == 1:
        if 0 < w and w < 2: print(will_converge)
        if tridiagonality(A) == 1:
            D, L, U = np.zeros_like(A), np.zeros_like(A), np.zeros_like(A)
            i, n = 0, len(A)
            while i < n:
                j = 0
                while j < n:
                    aij = A[i][j]
                    if i == j: D[i][j] = aij
                    if i > j: L[i][j] = aij
                    if i < j: U[i][j] = aij
                    j += 1
                i += 1
            DL = D - L
            i, inv_DL = 0, np.zeros_like(DL)
            while i < len(inv_DL):
                j = 0
                while j < len(inv_DL[0]):
                    dl = DL[i][j]
                    if dl != 0: inv_DL[i][j] = 1/(dl)
                    j += 1
                i += 1
            Tg = inv_DL*U
            omega = 2 / (1 + math.sqrt(1 - spectral_radius(Tg)))
        else: print('Warning! ', non_triad)
    else: print('Warning! ', incalculable)
    return omega
# preceded by find_omega
def successive_relaxation(A, x0, b, N, power, norm_type, w=0):
    """Given [`A`]*[`x`] = [`b`], use `norm_type` to find [x].

    Parameters
    ----------
    A : matrix
        Characteristic matrix.
    
    x0 : vector
        Dimensions of system of equations.
    
    b : vector
        Input vector.
    
    N : int
        Maximum number of iterations.
    
    power : float
        Signed, specified power of tolerance until satisfying method.
    
    norm_type : string
        Prescription of desired norm.
    
    w : float
        Relaxation parameter.
    
    Returns
    -------
    X_matrix : array
        Finally evaluated solution.
    
    NORM : list
        Aggregate of yielded norms.
    
    K : list
        Running collection of iterations through method.

    Raises
    ------
    bad_matrix : string
        If [`A`] is not square.
    
    bad_x0 : string
        If {`x0`} is neither n x 1 nor 1 x n array.
    
    bad_b : string
        If {`b`} is neither n x 1 nor 1 x n array.
    
    bad_N : string
        If iterations constraints is not an integer.
    
    bad_omega : string
        If omega was not given or less than zero or if a positive omega could not be found.
    
    bad_type : string
        If desired norm method was neither `'l_infinity'` nor `'l_2'`.

    Warns
    -----
    non_triad : string
        Matrix, `A` not being tridiagonal violates theorem.

    incalculable : string
        Matrix, `A` not being positive definite violates theorem.

    calculate_omega : string
        If `'successive_relaxation'` does not specify `w`, then an attempt will be made to find an optimal one.

    optimal_omega : string
        An ideal omega was found.

    solution_found : string
        Inform user that solution was indeed found.

    solution_not_found : string
        If initial guess or tolerance were badly defined.
    
    See Also
    --------
    diagonality() : Informs user if matrix, `A` is strictly, diagonally dominant. Solution will proceed even if not, but with a caveat that final solution may be inaccurate.
    
    find_omega() : Will analyze system of equation to find an optimal omega, if possible, and inform user.

    gauss_seidel() : Technique is Gauss-Seidel's modified by omega.

    l_infinity_norm() : Will find the l_infinity norm between `x0` and `xi`.

    l_2_norm() : Will find the l_2 norm between `x0` and `xi`.

    Notes
    -----
    gauss_seidel():
        [x]_(k) = ( (D - L)^(-1) * U ) * [x]_(k - 1) + ( (D - L)^(-1) )*[b]
    
    successive_relaxation():
        [x]_(k) = ( (D - wL)^(-1) * ((1 - w)*D + w*U) ) * [x]_(k - 1) + w*( (D - w*L)^(-1) )*[b]
    
    `w` will be analyzed independent of assigned value. Which will be used if not specified in assignment.
    """
    sym_A, sym_x0, sym_b = 'A', 'x0', 'b' # varname(A), varname(x0), varname(b)
    bad_matrix = 'Characteristic matrix, ' + sym_A + ' must be square!'
    bad_x0 = 'Systems vector, ' + sym_x0 + ' must be n x 1 or 1 x n array!'
    bad_b = 'Input vector, ' + sym_b + ' must be n x 1 or 1 x n array!'
    bad_N = "Maximum iterations, N must be an integer greater than zero."
    bad_type = "Desired norm type was not understood. Please choose 'l_infinity' or 'l_2'."
    calculate_omega = 'w was not given; therefore, I will attempt to choose one.'
    optimal_omega = 'w = ' + str(w) + ' given. Which is not optimum: '
    bad_omega = 'Either a positive omega was not given, or I could not choose one.'
    A = np.array(A)
    if len(A) != len(A[0]): sys.exit('ERROR! ', bad_matrix)
    if np.sum(x0.shape) > np.sum(x0.shape[0]): sys.exit('ERROR! ', bad_x0)
    if np.sum(b.shape) > np.sum(b.shape[0]): sys.exit('ERROR! ', bad_b)
    if N <= 0 or not isinstance(N, int): sys.exit('ERROR! ', bad_N)
    if norm_type != 'l_infinity' and norm_type != 'l_2': sys.exit('ERROR! ', bad_type)
    diagonality(A)
    if w == 0: 
        w = find_omega(A, x0)
        if w <= 0: sys.exit(bad_omega)
        print('Warning!', calculate_omega, str(w), sep=' ', end='.\n')
    elif w > 0:
        omega = find_omega(A, x0, w)
        print('Warning!', optimal_omega, str(omega), sep=' ', end='.\n')
    else: sys.exit(bad_omega)
    tol = float(10**power)
    n = len(x0)
    k, x0, b, norm = 0, np.reshape(x0,(n,1)), np.reshape(b,(n,1)), tol*10
    xi = np.zeros_like(x0)
    X, NORM, K = [], [], [] 
    X.append(x0); K.append(k)
    if norm > tol and k >= N:
        i = 0
        xgs = gauss_seidel(x0)
        while i < n:
            xi[i] = (1 - w)*x0[i] + w*xgs[i]
            i += 1
        if norm_type == 'l_infinity': norm = l_infinity_norm(xi, x0)
        if norm_type == 'l_2': norm = l_2_norm(xi, x0)
        X.append(xi); NORM.append(norm); K.append(k)
        x0 = xi
        k += 1
    if k < N: print('Congratulations! ', solution_found)
    else: print('Warning! ' + solution_not_found)
    m, n = len(X[0]), len(X)
    X_matrix, j = np.zeros((m,n)), 0
    while j < n:
        i = 0
        while i < m:
            X_matrix[i][j] = float(X[j][i])
            i += 1
        j += 1
    return X_matrix, NORM, K
# --------------------

# --------------------
# interpolations
class cubic_spline:
    
    def clamped(X, f, x=sp.Symbol('x'), fp=0):
        """Given a domain and range, construct a spline polynomial within interval by some condition.

        Parameters
        ----------
        X : array
            Input domain.
        
        f : array or expression
            Desired/Found range of interest.
        
        x : symbol
            Respected variable in derivative of equation. Assumed to be `'x'` if not stated.
        
        fp : array or expression
            Derivative at each point in `f`.
        
        Returns
        -------
        Y : array
            Finally evaluated solutions.
        
        splines_j : list
            Aggregate of splines on each interval.
        
        spline : string
            Totally constructed spline polynomial.

        Raises
        ------
        bad_X : string
            If {`X`} is neither n x 1 nor 1 x n array.
        
        bad_f : string
            If `f` is not an expression or function and is not an n x 1 or 1 x n array.
        
        bad_data : string
            If {`X`} and {`f`} are of unequal length.
        
        bad_fp : string
            If `fp` is not an expression or function and is not an n x 1 or 1 x n array.
        
        missing_fp : string
            Output message that derivative data or expression is missing.

        See Also
        --------
        make_array() : Translates input expression to array from given `X`.

        endpoint() : Relies on another technique to find derivatives at endpoints if not explicitly provided by data, `fp` nor an expression.

        midpoint() : Finds the derivatives at points within the bounds of the endpoints.

        diagonality() : Determines whether input matrix is strictly, diagonally dominant.

        Notes
        -----
        `fp` will be calculated if not specified.

        Method uses many, low-ordered polynomials to fit larger data sets. This minimizes computational load, which conversely greatly increases for larger data sets that yield high-ordered polynomials.

        General form: 
        Sj(x) = aj + bj(x - xj) + cj(x - xj)^2 + dj(x - xj)^3

        Clamped splines fit the constructed polynomial to the given data and its der
        ivatives at either endpoint.

        If selected `condition` is `'natural'`, then `fp = 0`, because derivative is assumed to be straight line outside of data set.

        Definitions of cubic spline conditions:
        a) S(x) is a cubic polynomial, Sj(x) on sub-interval [x_(j), x_(j + 1)] for each j = 0, 1, ..., n - 1;

        b) Sj(x_(j)) = f(x_(j)) and Sj(x_(j + 1)) = f(x_(j + 1)) for each j = 0, 1, ..., n - 1;

        c) S_(j + 1)(x_(j + 1)) = Sj(x_(j + 1)) for each j = 0, 1, ..., n - 2;

        d) S_(j + 1)'(x_(j + 1)) = Sj'(x_(j + 1)) for each j = 0, 1, ..., n - 2;

        e) One of the following conditions is satisfied:
            1) S''(x0) = S''(xn) = 0                ->  `'natural'`
            
            2) S'(x0) = f'(x0) and S'(xn) = f'(xn)  ->  `'clamped'`
        """
        def algorithm():
            Y, YP = np.array(g), np.array(gp)
            # STEP 1:   build list, h_i
            i, H = 0, np.zeros(n)
            while i < n:
                H[i] = X[i+1] - X[i]
                i += 1
            # STEP 2:   define alpha list endpoints
            A, AP, ALPHA = Y, YP, np.zeros(m)
            ALPHA[0] = 3*(A[1] - A[0])/H[0] - 3*AP[0]
            ALPHA[n] = 3*AP[n] - 3*(A[n] - A[n-1])/H[n-1]
            # STEP 3:   build list, alpha_i
            i = 1
            while i <= n-1:
                ALPHA[i] = 3/H[i]*(A[i+1] - A[i]) - 3/H[i-1]*(A[i] - A[i-1])
                i += 1
            # Algorithm 6.7 to solve tridiagonal
            # STEP 4:   define l, mu, and z first points
            L, MU, Z, C = np.zeros(m), np.zeros(m), np.zeros(m), np.zeros(m)
            L[0], MU[0] = 2*H[0], 0.5
            Z[0] = ALPHA[0]/L[0]
            # STEP 5:   build lists l, mu, and z
            i = 1
            while i <= n-1:
                L[i] = 2*(X[i+1] - X[i-1]) - H[i-1]*MU[i-1]
                MU[i] = H[i]/L[i]
                Z[i] = (ALPHA[i] - H[i-1]*Z[i-1])/L[i]
                i += 1
            # STEP 6:   define l, z, and c endpoints
            L[n] = H[n-1]*(2-MU[i-1])
            Z[n] = (ALPHA[n] - H[n-1]*Z[n-1])/L[n]
            C[n] = Z[n]
            # STEP 7:   build lists c, b, and d
            i, j, B, D = 1, 0, np.zeros(n), np.zeros(n)
            while i <= n:
                j = n-i
                C[j] = Z[j] - MU[j]*C[j+1]
                B[j] = (A[j+1] - A[j])/H[j] - H[j]*(C[j+1] + 2*C[j])/3
                D[j] = (C[j+1] - C[j])/(3*H[j])
                i += 1
            return Y, A, B, C, D
        sym_X, sym_f, sym_fp = 'X', 'f', 'fp' # varname(X), varname(f), varname(fp)
        bad_X = 'Input domain, ' + sym_X + ' was neither an n x 1 nor a 1 x n array.'
        bad_f = 'Input range, ' + sym_f + ' was neither function nor expression and not an n x 1 or 1 x n array.'
        bad_data = 'Arrays ' + sym_X + ' and ' + sym_f + ' must be of equal length.'
        bad_fp = 'Derivative range was neither function nor expression and not an n x 1 or 1 x n array.'
        bad_fp_data = 'Arrays ' + sym_X + ', ' + sym_f + ', and ' + sym_fp + ' must be of equal length.'
        missing_fp = 'Missing derivative data or expression.'
        if np.sum(X.shape) > np.sum(X.shape[0]): sys.exit(bad_X)
        if not isinstance(f, (FunctionType, sp.Expr)):
            if np.sum(f.shape) > np.sum(f.shape[0]): sys.exit(bad_f)
            elif len(X) != len(f): sys.exit(bad_data)
            else: g = f
        elif isinstance(f, (FunctionType, sp.Expr)): g = make_array(X, f)
        if np.sum(fp.shape) != 0:
            if not isinstance(fp, (FunctionType, sp.Expr)):
                if np.sum(fp.shape) > np.sum(fp.shape[0]): sys.exit(bad_fp)
                elif len(X) != len(fp): sys.exit(bad_fp_data)
                else: gp = fp
            elif isinstance(fp, (FunctionType, sp.Expr)): gp = make_array(X, fp)
        elif fp == 0:
            if isinstance(f,(FunctionType, sp.Expr)):
                fp = sp.lambdify(x, sp.diff(f(x)))
                gp = make_array(X, fp)
            elif not isinstance(f,(FunctionType, sp.Expr)):
                gp = []
                if len(X) > 2:
                    gp.append(endpoint(X, f, X[1]-X[0], 'three', 'left'))
                    i, n = 1, len(f) - 1
                    while i < n: 
                        gp.append(midpoint(X, f, X[i]-X[i-1], 'three', i))
                        i += 1
                    gp.append(endpoint(X, f, X[-2]-X[-1], 'three', 'right'))
                elif len(X) > 5:
                    gp.append(endpoint(X, f, X[1]-X[0], 'five', 'left'))
                    i, n = 1, len(X) - 1
                    while i < n: 
                        gp.append(midpoint(X, f, X[i]-X[i-1], 'five', i))
                        i += 1
                    gp.append(endpoint(X, f, X[-2]-X[-1], 'five', 'right'))
            else: sys.exit(missing_fp)
        m = len(X)
        n = m - 1
        Y, A, B, C, D = algorithm()
        j, splines_j = 0, []
        while j <= n-1:
            xj, aj, bj, cj, dj = X[j], A[j], B[j], C[j], D[j]
            sj = aj + bj*(sym_x - xj) + cj*(sym_x - xj)**2 + dj*(sym_x - xj)**3
            splines_j.append(sj)
            j += 1
        spline = sp.simplify(sum(splines_j))
        return Y, splines_j, spline

    def natural(X, f):
        """Given a domain and range, construct a spline polynomial within interval by some condition.

        Parameters
        ----------
        X : array
            Input domain.
        
        f : array or expression
            Desired/Found range of interest.
        
        Returns
        -------
        Y : array
            Finally evaluated solutions.
        
        splines_j : list
            Aggregate of splines on each interval.
        
        spline : string
            Totally constructed spline polynomial.

        Raises
        ------
        bad_X : string
            If {`X`} is neither n x 1 nor 1 x n array.
        
        bad_f : string
            If `f` is not an expression or function and is not an n x 1 or 1 x n array.
        
        bad_data : string
            If {`X`} and {`f`} are of unequal length.

        See Also
        --------
        make_array() : Translates input expression to array from given `X`.

        diagonality() : Determines whether input matrix is strictly, diagonally dominant.

        Notes
        -----
        Method uses many, low-ordered polynomials to fit larger data sets. This minimizes computational load, which conversely greatly increases for larger data sets that yield high-ordered polynomials.

        General form: 
        Sj(x) = aj + bj(x - xj) + cj(x - xj)^2 + dj(x - xj)^3

        Clamped splines fit the constructed polynomial to the given data and its der
        ivatives at either endpoint.

        If selected `condition` is `'natural'`, then `fp = 0`, because derivative is assumed to be straight line outside of data set.

        Definitions of cubic spline conditions:
        a) S(x) is a cubic polynomial, Sj(x) on sub-interval [x_(j), x_(j + 1)] for each j = 0, 1, ..., n - 1;

        b) Sj(x_(j)) = f(x_(j)) and Sj(x_(j + 1)) = f(x_(j + 1)) for each j = 0, 1, ..., n - 1;

        c) S_(j + 1)(x_(j + 1)) = Sj(x_(j + 1)) for each j = 0, 1, ..., n - 2;

        d) S_(j + 1)'(x_(j + 1)) = Sj'(x_(j + 1)) for each j = 0, 1, ..., n - 2;

        e) One of the following conditions is satisfied:
            1) S''(x0) = S''(xn) = 0                ->  `'natural'`
            
            2) S'(x0) = f'(x0) and S'(xn) = f'(xn)  ->  `'clamped'`
        """
        def algorithm():
            Y = g
            # STEP 1:   build list, h_i
            H, i = np.zeros(n), 0
            while i < n:
                H[i] = X[i+1] - X[i]
                i += 1
            # STEP 2:   build list, alpha_i
            A, ALPHA = Y, np.zeros(m)
            i = 1
            while i <= n-1:
                ALPHA[i] = 3/H[i]*(A[i+1] - A[i]) - 3/H[i-1]*(A[i] - A[i-1])
                i += 1
            # Algorithm 6.7 to solve tridiagonal
            # STEP 3:   define l, mu, and z first points
            L, MU, Z, C = np.zeros(m), np.zeros(m), np.zeros(m), np.zeros(m)
            L[0], MU[0], Z[0] = 1, 0, 0
            # STEP 4:   build lists l, mu, and z
            i = 1
            while i <= n-1:
                L[i] = 2*(X[i+1] - X[i-1]) - H[i-1]*MU[i-1]
                MU[i] = H[i]/L[i]
                Z[i] = (ALPHA[i] - H[i-1]*Z[i-1])/L[i]
                i += 1
            # STEP 5:   define l, z, and c endpoints
            L[n], Z[n], C[n] = 1, 0, 0
            # STEP 6:   build lists c, b, and d
            i, j, B, D = 1, 0, np.zeros(n), np.zeros(n)
            while i <= n:
                j = n-i
                C[j] = Z[j] - MU[j]*C[j+1]
                B[j] = (A[j+1] - A[j])/H[j] - H[j]*(C[j+1] + 2*C[j])/3
                D[j] = (C[j+1] - C[j])/(3*H[j])
                i += 1
            return Y, A, B, C, D
        sym_X, sym_f = 'X', 'f' # varname(X), varname(f)
        bad_X = 'Input domain, ' + sym_X + ' was neither an n x 1 nor a 1 x n array.'
        bad_f = 'Input range, ' + sym_f + ' was neither function nor expression and not an n x 1 or 1 x n array.'
        bad_data = 'Arrays ' + sym_X + ' and ' + sym_f + ' must be of equal length.'
        X = np.array(X)
        if np.sum(X.shape) > np.sum(X.shape[0]): sys.exit(bad_X)
        if not isinstance(f, (FunctionType, sp.Expr)):
            f = np.array(f)
            if np.sum(f.shape) > np.sum(f.shape[0]): sys.exit(bad_f)
            elif len(X) != len(f): sys.exit(bad_data)
            else: g = f
        elif isinstance(f, (FunctionType, sp.Expr)): g = make_array(X, f)
        m = len(X)
        n = m - 1
        Y, A, B, C, D = algorithm()
        j, splines_j = 0, []
        while j <= n-1:
            xj, aj, bj, cj, dj = X[j], A[j], B[j], C[j], D[j]
            sj = aj + bj*(sym_x - xj) + cj*(sym_x - xj)**2 + dj*(sym_x - xj)**3
            splines_j.append(sj)
            j += 1
        spline = sp.simplify(sum(splines_j))
        return Y, splines_j, spline

def hermite(X, FX, x=sp.Symbol('x'), FP=0):
    """Given a domain and range, construct a Hermetic polynomial.

    Parameters
    ----------
    X : array
        Input domain.
    
    FX : array
        Desired/Found range of interest.
    
    x : symbol
        Respected variable in derivative of equation. Assumed to be `'x'` if not stated.
    
    FP : array or expression
        Derivative at each point in `FX`.
    
    Returns
    -------
    polynomial : expression
        Lambdified Hermetic polynomial.

    Raises
    ------
    bad_X : string
        If {`X`} is neither n x 1 nor 1 x n array.
    
    bad_FX : string
        If {`FX`} is neither n x 1 nor 1 x n array.
    
    bad_data : string
        If {`X`} and {`FX`} are of unequal length.
    
    bad_FP : string
        If `FP` is not an expression or function and is not an n x 1 or 1 x n array.

    bad_FP_data : string
        If {`X`}, {`FX`}, or {`FP`} are of unequal lengths.
    
    missing_FP : string
        If `FP = 0` and `FX` is not an expression, then missing derivative data or expression.
    
    Warns
    -----
    made_poly : string
        Displays the string form of the equation.

    See Also
    --------
    make_array() : Prints string that expression was used to make array.
    
    Notes
    -----
    `FP` calculated if not specified.

    Slow computation time for larger data sets.

    Oscullating curve incorporates Taylor and Lagrangian polynomials to kiss the data and match each data point's derivatives. Which fits the curve to the shape of the data and its trend.
    """
    sym_X, sym_FX, sym_FP = 'X', 'FX', 'FP' # varname(X), varname(FX), varname(FP)
    bad_X = 'Input domain, ' + sym_X + ' was neither an n x 1 nor a 1 x n array.'
    bad_FX = 'Input range, ' + sym_FX + ' was neither an n x 1 nor a 1 x n array.'
    bad_data = 'Arrays ' + sym_X + ' and ' + sym_FX + ' must be of equal length.'
    bad_FP = 'Derivative range was neither function nor expression and not an n x 1 or 1 x n array.'
    bad_FP_data = 'Arrays ' + sym_X + ', ' + sym_FX + ', and ' + sym_FP + ' must be of equal length.'
    missing_FP = 'Missing derivative data or expression.'
    made_poly = 'I have found your requested polynomial! P = '
    if np.sum(X.shape) > np.sum(X.shape[0]): sys.exit(bad_X)
    if not isinstance(FX, (FunctionType, sp.Expr)):
        if np.sum(FX.shape) > np.sum(FX.shape[0]): sys.exit(bad_FX)
        elif len(X) != len(FX): sys.exit(bad_data)
    elif isinstance(FX,(FunctionType, sp.Expr)): g = make_array(X, FX)
    if FP != 0:
        if not isinstance(FP, (FunctionType, sp.Expr)):
            if np.sum(FP.shape) > np.sum(FP.shape[0]): sys.exit(bad_FP)
            if len(X) != len(FP): sys.exit(bad_FP_data)
        elif isinstance(FP,(FunctionType, sp.Expr)): FP = make_array(X, FP)
    elif FP == 0:
        if isinstance(FX,(FunctionType, sp.Expr)):
            fp = sp.lambdify(x, sp.diff(FX(x)))
            gp = make_array(X, fp)
        else: print(missing_FP)
    n = len(X)
    i, Q, Z = 0, np.zeros((2*n+1,2*n+1)), np.zeros((2*n+1,1))
    while i < n:
        Z[2*i], Z[2*i + 1] = X[i], X[i]
        Q[2*i][0], Q[2*i + 1][0] = g[i], g[i]
        Q[2*i + 1][1] = gp[i]
        if i != 0: Q[2*i][1] = (Q[2*i][0] - Q[2*i - 1][0]) \
            / (Z[2*i] - Z[2*i - 1])
        i += 1
    i = 2
    while i < 2*n + 1:
        j = 2
        while j <= i:
            Q[i][j] = (Q[i][j - 1] - Q[i - 1][j - 1]) \
            / (Z[i] - Z[i - j])
            j += 1
        i += 1
    i, y, terms = 0, 1, []
    while i < n:
        j, xi = 2*i, (x - X[i])
        qjj, qj1 = Q[j][j], Q[j + 1][j + 1]
        terms.append(qjj*y)
        y = y*xi
        terms.append(qj1*y)
        y = y*xi
        i += 1
    polynomial = sp.lambdify(x, sp.simplify(sum(terms)))
    print(made_poly + str(polynomial(x)))
    return polynomial

def lagrange(X, Y, x=sp.Symbol('x')):
    """Given a domain and range, construct a Lagrangian polynomial.

    Parameters
    ----------
    X : array
        Input domain.
    
    Y : array or expression
        Desired/Found range of interest.
    
    x : symbol
        Respected variable in derivative of equation. Assumed to be `'x'` if not stated.
    
    Returns
    -------
    yn : list
        Aggregate of Lagrangian terms.
    
    sp.lambdify(x, polynomial) : expression
        Lambdified Lagrangian polynomial.
    
    bound : list
        Propogation of error through construction.
    
    sum(bound)
        Total error.

    Raises
    ------
    bad_X : string
        If {`X`} is neither n x 1 nor 1 x n array.
    
    bad_Y : string
        If {`Y`} is neither n x 1 nor 1 x n array.
    
    bad_data : string
        If {`X`} and {`Y`} are of unequal length.
    
    Warns
    -----
    made_poly : string
        Displays the string form of the equation.

    See Also
    --------
    make_array() : Prints string that expression was used to make array.

    Notes
    --------
    Polynomial will quickly begin to oscillate for larger data sets.

    Finds a polynomial of degree n-1.

    Polynomial is of the following form:
    P(x) = f(x0)L_(n,0)(x) + ... + f(xn)L_(n,n)(x), where

    L_(n,k) = prod_(i=0, i!=k)^(n) (x - xi)/(xk - xi)

    Examples
    --------
    A Lagrange polynomial between (2,4) and (5,1) would be found as follows:
    L_(0)(x) = (x - 5)/(2 - 5) = -(x - 5)/3

    L_(1)(x) = (x - 2)/(5 - 2) = (x - 2)/3

    =>  P(x)    = (4)*(-(x - 5)/3) + (1)*((x - 2)/3)
                = -x + 6
    """
    def term(xk, yk, x):
        num, den, L_k = [], [], []
        for xl in X:
            if xl != xk:
                num.append(x-xl)
                den.append(xk-xl)
        L_k = (np.divide(np.prod(num), np.prod(den)))
        return L_k * yk
    def error(n, xi, x):
        i, roots, g, xi_error = 0, [], [], []
        while i <= n:
            root = X[i]
            roots.append(x - root)
            g = np.prod(roots)
            k = 0
            while k <= n:
                xi = sp.simplify(sp.diff(xi))
                k += 1
            dxi = np.abs(xi.evalf(subs={x: root})/(math.factorial(k)))
            xi_error.append(np.abs(dxi))
            xi_err = np.max(xi_error)
            g_prime = sp.diff(g)
            r = solve(g_prime)
            if i == 0:
                r = g_prime
                gx = g.evalf(subs={x: r})
            elif i == 1:
                gx = g.evalf(subs={x: r[0]})
            else:
                R = []
                for s in r:
                    if not isinstance(s, complex):
                        R.append(g.evalf(subs={x: s}))
                gx = np.amax(np.abs(R))
            i += 1
        return np.abs(xi_err*gx)
    sym_X, sym_Y = 'X', 'Y' # varname(X), varname(Y)
    bad_X = 'Input domain, ' + sym_X + ' was neither an n x 1 nor a 1 x n array.'
    bad_Y = 'Input range, ' + sym_Y + ' was neither an n x 1 nor a 1 x n array.'
    bad_data = 'Arrays ' + sym_X + ' and ' + sym_Y + ' must be of equal length.'
    made_poly = 'I have found your requested polynomial! P = '
    if np.sum(X.shape) > np.sum(X.shape[0]): sys.exit(bad_X)
    if not isinstance(Y,(FunctionType, sp.Expr)):
        if np.sum(Y.shape) > np.sum(Y.shape[0]): sys.exit(bad_Y)
        elif len(X) != len(Y): sys.exit(bad_data)
    elif isinstance(Y,(FunctionType, sp.Expr)): Y = make_array(X, Y)
    k, yn, bound = 0, [], []
    for xk in X:
        yn.append(term(xk, Y[k], x))
        bound.append(error(k, sp.simplify(sum(yn)), x))
        k += 1
    polynomial = sp.simplify(sum(yn))
    print(made_poly, str(polynomial))
    return yn, sp.lambdify(x, polynomial), bound, sum(bound)

def linear_least_squares(X_i, Y_i, n):
    """Given a domain and range, construct some polynomial.

    Parameters
    ----------
    X_i : array
        Input domain.
    
    Y_i : array or expression
        Desired/Found range of interest.
    
    n : int
        Degree of polynomial.
    
    Returns
    -------
    P : expression
        Lambdified linear least square polynomial.
    
    E : float
        Total error.

    Raises
    ------
    bad_X : string
        If {`X_i`} is neither n x 1 nor 1 x n array.
    
    bad_Y : string
        If {`Y_i`} is neither n x 1 nor 1 x n array.
    
    bad_data : string
        If {`X_i`} and {`Y_i`} are of unequal length.
    
    bad_n : string
        If prescribed `n` is not an integer or is zero.
    
    Warns
    -----
    made_poly : string
        Displays the string form of the equation.
    """
    def poly(X):
        terms, k = [], 0
        for x in X:
            terms.append(x*(sym_x**k))
            k += 1
        p = sp.simplify(sum(terms))
        err, i = 0, 0
        for x_i in X_i:
            px = p.subs(sym_x, x_i)
            err += (Y_i[i] - px)**2
            i += 1
        return p, err
    sym_X_i, sym_Y_i = 'X_i', 'Y_i' # varname(X_i), varname(Y_i)
    bad_X = 'Input domain, ' + sym_X_i + ' was neither an n x 1 nor a 1 x n array.'
    bad_Y = 'Input range, ' + sym_Y_i + ' was neither an n x 1 nor a 1 x n array.'
    bad_data = 'Arrays ' + sym_X_i + ' and ' + sym_Y_i + ' must be of equal length.'
    bad_n = 'Degree of polynomial must be integer and non-zero.'
    made_poly = 'I have found your requested polynomial! P = '
    if np.sum(X_i.shape) > np.sum(X_i.shape[0]): sys.exit(bad_X)
    if np.sum(Y_i.shape) > np.sum(Y_i.shape[0]): sys.exit(bad_Y)
    if len(X_i) != len(Y_i): sys.exit(bad_data)
    if not isinstance(n,(int)) or n == 0: sys.exit(bad_n)
    m = len(X_i)
    A, x = np.zeros((n+1, n+1)), np.zeros((n+1,1))
    i, b = 0, np.zeros_like(x)
    while i <= n:
        j = 0
        while j <= n:
            a_ij, k = 0, 0
            while k < m:
                a_ij += (X_i[k])**(i + j)
                k += 1
            A[i][j] = a_ij
            j += 1
        b_i, k = 0, 0
        while k < m:
            b_i += Y_i[k]*(X_i[k]**(i))
            k += 1
        b[i] = b_i
        i += 1
    x = np.transpose(np.linalg.solve(A, b))
    k, X, terms = 0, x[0], []
    for x in X:
        terms.append(x*(sym_x**k))
        k += 1
    polynomial = sp.simplify(sum(terms))
    print(made_poly, str(polynomial))
    P = sp.lambdify(sym_x, polynomial)
    i, E = 0, 0
    for x_i in X_i:
        E += (Y_i[i] - P(x_i))**2
        i += 1
    return P, E

def linear_interpolation(x0, y0, x1, y1, x):
    return y0 + (x - x0)*(y1 - y0)/(x1 - x0)

def newton_difference(X, FX, x0, direction=0):
    """Given a domain and range, construct some polynomial by Newton's Divided Difference.

    Parameters
    ----------
    X : array
        Input domain.
    
    FX : array or expression
        Desired/Found range of interest.

    x0 : float
        Point about which polynomial is evaluated.
    
    direction : string
        `'forward'` or `'backward'` construction. Will be chosen automatically if not specified.
    
    Returns
    -------
    p : expression
        Lambdified constructed polynomial.
    
    p(x0) : float
        Evaluation of `p` at `x`.

    Raises
    ------
    bad_X : string
        If {`X_i`} is neither n x 1 nor 1 x n array.
    
    bad_FX : string
        If {`FX`} is neither n x 1 nor 1 x n array.
    
    bad_data : string
        If {`X`} and {`FX`} are of unequal length.
    
    bad_direction : string
        If `direction` is neither `'forward'` nor `'backward'`.
    
    Warns
    -----
    made_poly : string
        Displays the string form of the equation.

    See Also
    --------
    make_array() : Prints string that expression was used to make array.

    Notes
    -----
    Direction will be chosen if not specified.

    Polynomials best made with even spacing in `X`; although, this is not completely necessary.
    """
    def fterm(i, j):
        fij = (fxn[i][j] - fxn[i-1][j])/(fxn[i][0] - fxn[i-j][0])
        return fij
    sym_X, sym_FX = 'X', 'FX' # varname(X), varname(FX)
    bad_X = 'Input domain, ' + sym_X + ' was neither an n x 1 nor a 1 x n array.'
    bad_FX = 'Input range, ' + sym_FX + ' was neither an n x 1 nor a 1 x n array.'
    bad_data = 'Arrays ' + sym_X + ' and ' + sym_FX + ' must be of equal length.'
    bad_direction = "Supplied direction was not understood. Please specify 'forward' or 'backward', or let me choose."
    made_poly = 'I have found your requested polynomial! P = '
    X, x0 = np.array(X), float(x0)
    if not isinstance(FX,(FunctionType, sp.Expr)):
        FX = np.array(FX)
        if np.sum(X.shape) > np.sum(X.shape[0]): sys.exit(bad_X)
        if np.sum(FX.shape) > np.sum(FX.shape[0]): sys.exit(bad_FX)
        if len(X) != len(FX): sys.exit(bad_data)
    if isinstance(FX,(FunctionType, sp.Expr)): FX = make_array(X, FX)
    if direction == 0:
        if x0 <= np.median(X): direction = 'forward'
        else: direction = 'backward'
    elif direction != 'forward' and direction != 'backward': sys.exit(bad_direction)
    m = len(X)
    n = m + 1
    fxn, coeff, term, poly = np.zeros((m,n)), [], [], []
    m, n = m - 1, n - 1     # change m and n from length to index
    j, fxn[:,0], fxn[:,1] = 1, X, FX
    while j < m:
        i = 1
        while i < m:
            fk = fterm(i, j)
            fxn[i][j+1] = fk
            if direction == 'forward' and i == j:
                coeff.append(fk)
            if direction == 'backward' and i == m - 1:
                coeff.append(fk)
            i += 1
        j += 1
    for c in coeff:
        k = coeff.index(c)
        term.append(sym_x - X[k])
        poly.append(c*np.prod(term))
    if direction == 'forward': polynomial = sp.simplify(sum(poly) + FX[0])
    if direction == 'backward': polynomial = sp.simplify(sum(poly) + FX[m])
    print(made_poly, str(polynomial))
    p = sp.lambdify(sym_x, polynomial)
    return p, p(x0)

def sine_cosine_algorithm(
    maxIteration = 1000,
    dim = 20,
    searchAgents = 30,
    func = 8,
    lowerBound = -5,
    upperBound = 10,
    dist = 3,
    runs = 10
    ):
    """'"An implementation in Python of the Since Cosine Algorithm (SCA), for solving optimization problems, with different randomization methods.

    GitHub: https://github.com/luizaes/sca-algorithm
    Source: http://dx.doi.org/10.1016/j.knosys.2015.12.022
    """
    # Funcao de mapeamento
    def remap(number, fromMin, fromMax, toMin, toMax):

        fromAbs = number - fromMin
        fromMaxAbs = fromMax - fromMin

        normal = fromAbs / fromMaxAbs

        toMaxAbs = toMax - toMin
        toAbs = toMaxAbs * normal

        to = toAbs + toMin

        return to

    # Funcao para calculo da diversidade
    def diversityCalc(population, dim):
        ciVec = []
        for x in range(0,dim):
            ci = 0
            for y in range(0,len(population)):
                ci += population[y][x] / float(len(population))
            ciVec.append(ci)

        Isd = 0
        t1 = 0
        t2 = 0
        for x in range(0,dim):
            t1 = 0
            for y in range(0,len(population)):
                t2 = population[y][x] - ciVec[x]
                t1 += t2 * t2
            Isd += math.sqrt(t1/(len(population)-1))
        Isd /= float(dim)
        return Isd

    # Mapas caoticos
    def logisticMap(randomNum):
        randomNum = 4.0 * randomNum * (1 - randomNum)
        return randomNum

    # Funcoes objetivo
    def funcObjective(individual, type):
        fitness = 0
        top1 = 0
        top = 0

        if type == 1:
            # Esfera -5.12 .. 5.12
            for x in range(0,len(individual)):
                fitness = fitness + individual[x] ** 2
        elif type == 2:
            # Rosenbrock -30 .. 30
            for x in range(0,len(individual)-1):
                fitness = fitness + (100.0 * (individual[x+1]-individual[x]**2) ** 2) + (individual[x]-1.0) ** 2
        elif type == 3:
            # Rastrigin -5.12 .. 5.12
            for x in range(0,len(individual)):
                fitness = fitness + individual[x] ** 2 - 10 * math.cos(2*math.pi*individual[x]) + 10
        elif type == 4:
            # Schaffer -100 .. 100
            for x in range(0,len(individual)):
                top = top + (individual[x]**2)
            top = top ** 0.25
            for x in range(0,len(individual)):
                top1 = top1 + (individual[x] ** 2)
            top1 = top1 ** 0.1
            top1 = (math.sin(50*top1)**2) +1.0
            fitness = top * top1
        elif type == 5:
            # Ackley -32 .. 32
            aux = aux1 = 0.0
            for x in range(0, len(individual)):
                aux = aux + (individual[x]*individual[x])

            for x in range(0, len(individual)):
                aux1 = aux1 + math.cos(2.0*math.pi*individual[x])

            fitness = -20.0*(math.exp(-0.2*math.sqrt(1.0/len(individual)*aux)))-math.exp(1.0/len(individual)*aux1)+20.0+math.exp(1)
        elif type == 6:
            # Griewank -600 .. 600
            top1 = 0
            top2 = 1
            for x in range(0, len(individual)):
                top1 = top1 + individual[x] ** 2
                top2 = top2 * math.cos((((individual[x])/math.sqrt((x+1)))*math.pi)/180)
            fitness = (1/4000.0) * top1 - top2 + 1
        elif type == 7:
            # Schwefel -500 .. 500
            aux = 0.0
            for x in range(0, len(individual)):
                aux = aux + individual[x] * math.sin(math.sqrt(math.fabs(individual[x]))) 
            fitness = (-1*aux/len(individual))
        elif type == 8:
            # Zakharov -5 .. 10
            aux = aux1 = 0
            for x in range(0, len(individual)):
                aux = aux + individual[x] ** 2
                aux1 = aux1 + 0.5 * x * individual[x]
            
            fitness = aux + aux1 ** 2 + aux1 ** 4
        return fitness

    # Parametros
    average = 0
    averageNormalized = 0
    finalSolutions = []
    bestSolutionFinal = []
    worstSolutionFinal = []
    meanSolutionFinal = []
    diversityFinal = []
    lastBest = 0
    std = 0

    for z in range(0,runs):
        bestSolution = []
        bestFitness = []
        best = 0
        contador = 1
        population = []
        initialPoint = random.uniform(0.0,1.0)
        worst = 0
        mean = 0
        diversity = 0
        desvio = 1

        # Geracao da Populacao Inicial
        for x in range(0,searchAgents):
            individual = []
            for y in range(0,dim):
                # Uniforme
                if dist == 1:
                    individual.append(random.uniform(lowerBound, upperBound))	
                # Logistico
                elif dist == 2:
                    initialPoint = logisticMap(initialPoint)
                    individual.append(remap(initialPoint, 0, 1, lowerBound, upperBound))
                # Gaussiana
                elif dist == 3:
                    num = np.random.normal((lowerBound+upperBound)/2, upperBound-((lowerBound+upperBound)/2))
                    if num < lowerBound:
                        num = lowerBound
                    if num > upperBound:
                        num = upperBound
                    individual.append(num)
            population.append(individual)

        #print(population)

        mean = 0
        # Avaliacao da Populacao Inicial
        for x in range(0,searchAgents):
            fitness = funcObjective(population[x], func)
            mean = mean + fitness
            if x == 0:
                bestSolution = population[x]
                best = fitness
                worst = fitness
            elif fitness < best:
                best = fitness
                bestSolution = population[x]
            elif worst < fitness:
                worst = fitness

        mean = mean / searchAgents

        diversity = diversityCalc(population, dim)

        if z == 0:
            bestSolutionFinal.append(best)
            worstSolutionFinal.append(worst)
            meanSolutionFinal.append(mean)
            diversityFinal.append(diversity)
        else:
            bestSolutionFinal[0] = bestSolutionFinal[0] + best 
            worstSolutionFinal[0] = worstSolutionFinal[0] + worst 
            meanSolutionFinal[0] = meanSolutionFinal[0] + mean
            diversityFinal[0] = diversityFinal[0] + diversity

        # Algoritmo Principal
        while contador < maxIteration:
            a = 2
            mean = 0
            r1 = a-contador*((a)/maxIteration)

            # Para cada agente de busca e para cada dimensao, faz o update
            for x in range(0,searchAgents):
                    for y in range(0,dim):
                        # Uniforme
                        if dist == 1:
                            r2 = 2*math.pi*random.uniform(0.0,1.0)
                            r3 = 2*random.uniform(0.0,1.0)	
                            r4 = random.uniform(0.0,1.0)	
                        # Logistico
                        elif dist == 2:
                            initialPoint = logisticMap(initialPoint)
                            r2 = 2*math.pi*initialPoint
                            initialPoint = logisticMap(initialPoint)
                            r3 = 2*initialPoint
                            initialPoint = logisticMap(initialPoint)
                            r4 = initialPoint
                        # Gaussiana
                        elif dist == 3:
                            r2 = np.random.normal(0.5, 0.5)
                            if r2 < 0:
                                r2 = 0.0
                            if r2 > 1:
                                r2 = 1.0
                            r2 = 2*math.pi*r2
                            r3 = np.random.normal(0.5, 0.5)
                            if r3 < 0:
                                r3 = 0.0
                            if r3 > 1:
                                r3 = 1.0
                            r3 = 2*r3
                            r4 = np.random.normal(0.5, 0.5)
                            if r4 < 0:
                                r4 = 0.0
                            if r4 > 1:
                                r4 = 1.0

                    
                        if r4 < 0.5:
                            population[x][y] = population[x][y]+(r1*math.sin(r2)*abs(r3*bestSolution[y]-population[x][y]))
                            if population[x][y] > upperBound or population[x][y] < lowerBound:
                                # Uniforme
                                if dist == 1:
                                    population[x][y] = random.uniform(lowerBound, upperBound)
                                # Logistico
                                elif dist == 2:
                                    initialPoint = logisticMap(initialPoint)
                                    population[x][y] = remap(initialPoint, 0, 1, lowerBound, upperBound)
                                # Gaussiana
                                elif dist == 3:
                                    num = np.random.normal((lowerBound+upperBound)/2, upperBound-((lowerBound+upperBound)/2))
                                    if num < lowerBound:
                                        num = lowerBound
                                    if num > upperBound:
                                        num = upperBound
                                    population[x][y] = num
                        else:
                            population[x][y] = population[x][y]+(r1*math.cos(r2)*abs(r3*bestSolution[y]-population[x][y]))
                            if population[x][y] > upperBound or population[x][y] < lowerBound:
                                # Uniforme
                                if dist == 1:
                                    population[x][y] = random.uniform(lowerBound, upperBound)
                                # Logistico
                                elif dist == 2:
                                    initialPoint = logisticMap(initialPoint)
                                    population[x][y] = remap(initialPoint, 0, 1, lowerBound, upperBound)
                                # Gaussiana
                                elif dist == 3:
                                    num = np.random.normal((lowerBound+upperBound)/2, upperBound-((lowerBound+upperBound)/2))
                                    if num < lowerBound:
                                        num = lowerBound
                                    if num > upperBound:
                                        num = upperBound
                                    population[x][y] = num
            
            mean = 0
            # Avalia novamente as solucoes
            for x in range(0,searchAgents):
                fitness = funcObjective(population[x], func)
                mean = mean + fitness
                if x == 0:
                    worst = fitness
                if fitness < best:
                    best = fitness
                    bestSolution = population[x]
                elif worst < fitness:
                    worst = fitness

            mean = mean / searchAgents

            diversity = diversityCalc(population, dim)

            if z == 0:
                bestSolutionFinal.append(best)
                worstSolutionFinal.append(worst)
                meanSolutionFinal.append(mean)
                diversityFinal.append(diversity)
            else:
                bestSolutionFinal[contador] = bestSolutionFinal[contador] + best
                worstSolutionFinal[contador] = worstSolutionFinal[contador] + worst
                meanSolutionFinal[contador] = meanSolutionFinal[contador] + mean
                diversityFinal[contador] = diversityFinal[contador] + diversity

            contador = contador + 1
            bestFitness.append(best)

        print("Melhor fitness da execucao:")
        print(best)
        finalSolutions.append(best)
        average = average + best

    average = average/runs

    for x in range(0,len(finalSolutions)):
        std = std + (finalSolutions[x] - average) ** 2

    for x in range(0,len(bestSolutionFinal)):
        bestSolutionFinal[x] = bestSolutionFinal[x] / runs
        worstSolutionFinal[x] = worstSolutionFinal[x] / runs
        meanSolutionFinal[x] = meanSolutionFinal[x] / runs
        diversityFinal[x] = diversityFinal[x] / runs

    print("-------------------- Informacoes das execucoes ------------------------")
    print("Average: " + str(average))
    std = math.sqrt(std/len(finalSolutions))
    print("Std: " + str(std))

    #plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
    # axes.set_xlim([0, maxIteration])
    # axes.set_ylim([0,100])

    plt.plot([i for i in reversed(range(999))],[float(bestSolutionFinal[i]) for i in reversed(range(999))])
    plt.plot([i for i in reversed(range(999))],[float(worstSolutionFinal[i]) for i in reversed(range(999))])
    plt.plot([i for i in reversed(range(999))],[float(meanSolutionFinal[i]) for i in reversed(range(999))])
    plt.ylabel('Fitness')
    plt.xlabel('Iterations')
    plt.title('Convergence Graph')
    plt.show()

    plt.plot([i for i in reversed(range(999))],[(round(diversityFinal[i], 2)) for i in reversed(range(999))])
    plt.ylabel('Diversity')
    plt.xlabel('Iterations')
    plt.title('Diversity Graph')
    plt.show()
# --------------------

# --------------------
# numerical differentiation
# and integration
class simpson:

    def open(f, X, h=0, a=0, b=0):
        """Find the integral of a function within some interval, using Simpson's Rule.

        Parameters
        ----------
        f : expression
            Polynomial equation that defines graphical curve.
        
        X : list
            Domain over which `f` is evaluated.
        
        h : float
            Step-size through interval.
        
        a : float
            Left-hand bound of interval.
        
        b : float
            Right-hand bound of interval.
        
        Returns
        -------
        XJ : list
            Values of domain at which `f` was analyzed.
        
        YJ : list
            Evaluations of `f` from domain.
        
        F : float
            Total area under curve, `f`.

        Raises
        ------
        bad_X : string
            If {`X_i`} is neither n x 1 nor 1 x n array.
        
        bad_f : string
            If {`f`} is not an expression.

        Warns
        -----
        func_func : string
            Evaluate input expression for Newton difference approximation.
        
        Notes
        -----
        `X = 0` if not a list nor n x 1 or 1 x n array.

        Unless specified and if `X` is defined, `a` and `b` will be the minimum and maximum, respectively, of `X`.

        Theorem:
        Let f be in C4[a,b], n be even, h = (b-a)/n, and xj = a + jh for j = 0, 1, ..., n. There exists a mu in (a,b) for which the quadrature for n sub-intervals can be written with its error term as:
        int_(a)^(b)f(x)dx = h[f(a) + 2*[sum_(j=1)^(n/2 - 1){f(x_(2j))}] + 4*[sum_(j=1)^(n/2){f(x_(2j-1))}] + f(b)]/3 - (b-a)*(h^4)f''''(mu)/180.

        Where: (b-a)*(h^4)f''''(mu)/180 -> O(h^4)
        """
        X = np.array(X)
        sym_X, sym_f = 'X', 'f' # varname(X), varname(f)
        bad_X = 'Input domain, ' + sym_X + ' was neither an n x 1 nor a 1 x n array.'
        bad_f = 'Input range, ' + sym_f + ' must be expression, not list or tuple.'
        func_func = 'Input expression used.'
        if np.sum(X.shape) > np.sum(X.shape[0]): sys.exit(bad_X)
        if not isinstance(f,(FunctionType, sp.Expr)):
            if np.sum(f.shape) > np.sum(f.shape[0]): sys.exit(bad_X)
            else: sys.exit(bad_f)
        if isinstance(f,(FunctionType, sp.Expr)): print(func_func)
        if h == 0: h = X[1]-X[0]
        if a == 0: a = min(X)
        if b == 0: b = max(X)
        h, a, b = float(h), float(a), float(b)
        n = math.ceil((b-a)/h)
        XJ1, XJ2, XJ, = [], [], []
        YJ1, YJ2, YJ, = [], [], []
        XJ.append(a); YJ.append(f(a))
        j, z1 = 1, 0
        while j <= (n/2)-1:
            xj = a + 2*j*h
            yj = f(xj)
            XJ1.append(xj); YJ1.append(yj)
            z1 += yj
            j += 1
        k, z2 = 1, 0
        while k <= n/2:
            xj = a + (2*k - 1)*h
            yj = f(xj)
            XJ2.append(xj); YJ2.append(yj)
            z2 += yj
            k += 1
        l = 0
        while l < np.array(XJ1).shape[0]:
            XJ.append(XJ2[l]); YJ.append(YJ2[l])
            XJ.append(XJ1[l]); YJ.append(YJ1[l])
            l += 1
        XJ.append(XJ2[l]); YJ.append(YJ2[l])
        XJ.append(b); YJ.append(f(b))
        F = h/3*(f(a) + 2*z1 + 4*z2 + f(b))
        return XJ, YJ, F
    
    def closed(f, X, h=0, a=0, b=0):
        """Find the integral of a function within some interval, using Simpson's Rule.

        Parameters
        ----------
        f : expression
            Polynomial equation that defines graphical curve.
        
        X : list
            Domain over which `f` is evaluated.
        
        h : float
            Step-size through interval.
        
        a : float
            Left-hand bound of interval.
        
        b : float
            Right-hand bound of interval.
        
        Returns
        -------
        XJ : list
            Values of domain at which `f` was analyzed.
        
        YJ : list
            Evaluations of `f` from domain.
        
        F : float
            Total area under curve, `f`.

        Raises
        ------
        bad_X : string
            If {`X_i`} is neither n x 1 nor 1 x n array.
        
        bad_f : string
            If {`f`} is not an expression.

        Warns
        -----
        func_func : string
            Evaluate input expression for Newton difference approximation.
        
        Notes
        -----
        `X = 0` if not a list nor n x 1 or 1 x n array.

        Unless specified and if `X` is defined, `a` and `b` will be the minimum and maximum, respectively, of `X`.

        Theorem:
        Let f be in C4[a,b], n be even, h = (b-a)/n, and xj = a + jh for j = 0, 1, ..., n. There exists a mu in (a,b) for which the quadrature for n sub-intervals can be written with its error term as:
        int_(a)^(b)f(x)dx = h[f(a) + 2*[sum_(j=1)^(n/2 - 1){f(x_(2j))}] + 4*[sum_(j=1)^(n/2){f(x_(2j-1))}] + f(b)]/3 - (b-a)*(h^4)f''''(mu)/180.

        Where: (b-a)*(h^4)f''''(mu)/180 -> O(h^4)
        """
        X = np.array(X)
        sym_X, sym_f = 'X', 'f' # varname(X), varname(f)
        bad_X = 'Input domain, ' + sym_X + ' was neither an n x 1 nor a 1 x n array.'
        other_bad_X = 'Input domain, ' + sym_X + ' must be only 4 elements!'
        bad_f = 'Input range, ' + sym_f + ' must be expression, not list or tuple.'
        func_func = 'Input expression used.'
        if np.sum(X.shape) > np.sum(X.shape[0]): sys.exit(bad_X)
        if np.sum(X.shape[0]) != 4: sys.exit('ERROR! ' + other_bad_X)
        if not isinstance(f,(FunctionType, sp.Expr)):
            f = np.array(f)
            if np.sum(f.shape) == np.sum(f.shape[0]) and np.sum(f.shape) == 4: Y = np.array(f)
            elif np.sum(f.shape) > np.sum(f.shape[0]): sys.exit(bad_X)
            else: sys.exit(bad_f)
        if h == 0: h = X[1]-X[0]
        if a == 0: a = min(X)
        if b == 0: b = max(X)
        if isinstance(f,(FunctionType, sp.Expr)): 
            print(func_func)
            Y = make_array(X, f)
            if a < np.min(X): Y[0] = f(a)
            if b > np.max(X): Y[3] = f(b)
        h, a, b = float(h), float(a), float(b)
        F = 3*h/8*(Y[0] + 3*(Y[1] + Y[2]) + Y[3])
        return X, Y, F

class trapezoidal:

    def open(f, X, h=0, a=0, b=0):
        """Find the integral of a function within some interval, using Trapezoidal Rule.

        Parameters
        ----------
        f : expression
            Polynomial equation that defines graphical curve.
        
        X : list
            Domain over which `f` is evaluated.

        h : float
            Step-size through interval.
        
        a : float
            Left-hand bound of interval.
        
        b : float
            Right-hand bound of interval.
        
        Returns
        -------
        XJ : list
            Values of domain at which `f` was analyzed.
        
        YJ : list
            Evaluations of `f` from domain.
        
        F : float
            Total area under curve, `f`.

        Raises
        ------
        bad_X : string
            If {`X_i`} is neither n x 1 nor 1 x n array.
        
        bad_f : string
            If {`f`} is not an expression.

        Warns
        -----
        func_func : string
            Evaluate input expression for Newton difference approximation.
        
        Notes
        -----
        `X = 0` if not a list nor n x 1 or 1 x n array.

        Unless specified and if `X` is defined, `a` and `b` will be the minimum and maximum, respectively, of `X`.

        Theorem:
        Let f be in C2[a,b], h = (b-a)/n, and xj = a + jh for j = 0, 1, ..., n. There exists a mu in (a,b) for which the quadrature for n sub-intervals can be written with its error term as:
        int_(a)^(b)f(x)dx = h[f(a) + 2*[sum_(j=1)^(n - 1){f(xj)}] + f(b)]/2 - (b-a)*(h^2)f''(mu)/12.

        Where: (b-a)*(h^2)f''(mu)/12 -> O(h^2)
        """
        X = np.array(X)
        sym_X, sym_f = 'X', 'f' # varname(X), varname(f)
        bad_X = 'Input domain, ' + sym_X + ' was neither an n x 1 nor a 1 x n array.'
        bad_f = 'Input range, ' + sym_f + ' must be expression, not list or tuple.'
        func_func = 'Input expression used.'
        if np.sum(X.shape) > np.sum(X.shape[0]): sys.exit(bad_X)
        if not isinstance(f,(FunctionType, sp.Expr)):
            if np.sum(X.shape) > np.sum(X.shape[0]): sys.exit(bad_X)
            else: sys.exit(bad_f)
        if isinstance(f,(FunctionType, sp.Expr)): print(func_func)
        if h == 0: h = X[1]-X[0]
        if a == 0: a = min(X)
        if b == 0: b = max(X)
        h, a, b = float(h), float(a), float(b)
        XJ, YJ = [], []
        XJ.append(a); YJ.append(f(a))
        j, n, z = 1, math.ceil((b-a)/h), 0
        while j <= n-1:
            x_j = a + j*h
            XJ.append(x_j)
            y_j = f(x_j)
            YJ.append(y_j)
            z += y_j
            j += 1
        XJ.append(b); YJ.append(f(b))
        F = h/2*(f(a) + 2*z + f(b))
        return XJ, YJ, F
    
    def closed(f, X, h=0, a=0, b=0):
        """Find the integral of a function within some interval, using Trapezoidal Rule.

        Parameters
        ----------
        f : expression
            Polynomial equation that defines graphical curve.
        
        X : list
            Domain over which `f` is evaluated.

        h : float
            Step-size through interval.
        
        a : float
            Left-hand bound of interval.
        
        b : float
            Right-hand bound of interval.
        
        Returns
        -------
        XJ : list
            Values of domain at which `f` was analyzed.
        
        YJ : list
            Evaluations of `f` from domain.
        
        F : float
            Total area under curve, `f`.

        Raises
        ------
        bad_X : string
            If {`X_i`} is neither n x 1 nor 1 x n array.
        
        bad_f : string
            If {`f`} is not an expression.

        Warns
        -----
        func_func : string
            Evaluate input expression for Newton difference approximation.
        
        Notes
        -----
        `X = 0` if not a list nor n x 1 or 1 x n array.

        Unless specified and if `X` is defined, `a` and `b` will be the minimum and maximum, respectively, of `X`.

        Theorem:
        Let f be in C2[a,b], h = (b-a)/n, and xj = a + jh for j = 0, 1, ..., n. There exists a mu in (a,b) for which the quadrature for n sub-intervals can be written with its error term as:
        int_(a)^(b)f(x)dx = h[f(a) + 2*[sum_(j=1)^(n - 1){f(xj)}] + f(b)]/2 - (b-a)*(h^2)f''(mu)/12.

        Where: (b-a)*(h^2)f''(mu)/12 -> O(h^2)
        """
        X = np.array(X)
        sym_X, sym_f = 'X', 'f' # varname(X), varname(f)
        bad_X = 'Input domain, ' + sym_X + ' was neither an n x 1 nor a 1 x n array.'
        other_bad_X = 'Input domain, ' + sym_X + ' must be only 2 elements!'
        bad_f = 'Input range, ' + sym_f + ' must be expression, not list or tuple.'
        func_func = 'Input expression used.'
        if np.sum(X.shape) > np.sum(X.shape[0]): sys.exit(bad_X)
        if np.sum(X.shape[0]) != 2: sys.exit('ERROR! ' + other_bad_X)
        if not isinstance(f,(FunctionType, sp.Expr)):
            f = np.array(f)
            if np.sum(f.shape) == np.sum(f.shape[0]) and np.sum(f.shape) == 2: Y = np.array(f)
            elif np.sum(X.shape) > np.sum(X.shape[0]): sys.exit(bad_X)
            else: sys.exit(bad_f)
        if h == 0: h = X[1]-X[0]
        if a == 0: a = min(X)
        if b == 0: b = max(X)
        if isinstance(f,(FunctionType, sp.Expr)): 
            print(func_func)
            Y = make_array(X, f)
            if a < np.min(X): Y[0] = f(a)
            if b > np.max(X): Y[1] = f(b)
        h, a, b = float(h), float(a), float(b)
        F = h/2*(Y[0] + Y[1])
        return X, Y, F

def endpoint(X, Y, h, point_type, which_end):
    """Find the derivative at an endpoint of data set.

    Parameters
    ----------
    X : list
        Domain of collected data.
    
    Y : array or expression
        Range of collected data.
    
    h : float
        Step-size through interval.
    
    point_type : string
        Determines if 3 or 5 pt. method is used.
    
    which_end : string
        Dictates whether evaluated point is left or right most data point.
    
    Returns
    -------
    dY : float
        Evaluated derivative at point.

    Raises
    ------
    bad_X : string
        If {`X`} is neither n x 1 nor 1 x n array.
    
    bad_Y : string
        If {`Y`} is not an expression.
    
    bad_data : string
        If `X` and `Y` are of unequal length.

    See Also
    --------
    make_array() : Prints string that expression was used to make array.

    Notes
    -----
    5 point is more accurate than 3 point; however, round-off error increases.
    """
    sym_X, sym_Y = 'X', 'Y' # varname(X), varname(Y)
    bad_X = 'Input domain, ' + sym_X + ' was neither an n x 1 nor a 1 x n array.'
    bad_Y = 'Input range, ' + sym_Y + ' was neither an n x 1 nor a 1 x n array.'
    bad_data = 'Arrays ' + sym_X + ' and ' + sym_Y + ' must be of equal length.'
    if not isinstance(Y,(FunctionType, sp.Expr)):
        if np.sum(X.shape) > np.sum(X.shape[0]): sys.exit(bad_X)
        if np.sum(Y.shape) > np.sum(Y.shape[0]): sys.exit(bad_Y)
        if len(X) != len(Y): sys.exit(bad_data)
    if isinstance(Y,(FunctionType, sp.Expr)): Y = make_array(X, Y)
    h, dY = float(h), 0
    if which_end == 'left':
        i = 0
        if point_type == 'three':
            dY = (-3*Y[i] + 4*Y[i+1] - Y[i+2])/(2*h)
        if point_type == 'five':
            dY = (-25*Y[i] + 48*Y[i+1] \
                - 36*Y[i+2] + 16*Y[i+3] \
                    - 3*Y[i+4])/(12*h)
    if which_end == 'right':
        i = -1
        if point_type == 'three':
            dY = (-3*Y[i] + 4*Y[i-1] - Y[i-2])/(2*h)
        if point_type == 'five':
            dY = (-25*Y[i] + 48*Y[i-1] \
                - 36*Y[i-2] + 16*Y[i-3] \
                    - 3*Y[i-4])/(12*h)
    return dY

def gaussian_legendre(function, a, b):
    return quad(function, a, b)

def integrate(function, a, b):
    return quad(function, a, b)

def midpoint(X, Y, h, point_type, i):
    """Find derivative information at some point within data set.

    Parameters
    ----------
    X : list
        Domain of collected data.
    
    Y : array or expression
        Range of collected data.
    
    h : float
        Step-size through interval.
    
    point_type : string
        Determines if 3 or 5 pt. method is used.

    i : int
        Index at which point is to be evaluated.
    
    Returns
    -------
    dY : float
        Evaluated derivative at point.

    Raises
    ------
    bad_X : string
        If {`X`} is neither n x 1 nor 1 x n array.
    
    bad_Y : string
        If {`Y`} is not an expression.
    
    bad_data : string
        If `X` and `Y` are of unequal length.
    
    bad_i : string
        `i` must be an integer and non-zero for indexing.
    
    bad_type : string
        If `point_type` was not an acceptable option.

    See Also
    --------
    make_array() : Prints string that expression was used to make array.

    Notes
    -----
    5 point is more accurate than 3 point; however, round-off error increases.
    """
    sym_x, sym_Y = 'X', 'Y' # varname(X), varname(Y)
    bad_X = 'Input domain, ' + sym_X + ' was neither an n x 1 nor a 1 x n array.'
    bad_Y = 'Input range, ' + sym_Y + ' was neither an n x 1 nor a 1 x n array.'
    bad_data = 'Arrays ' + sym_X + ' and ' + sym_Y + ' must be of equal length.'
    bad_i = 'Index must be an integer.'
    bad_type = "I am sorry. The selected type was not understood. Please select: 'three', 'five', or '2nd_derivative'."
    if not isinstance(Y,(FunctionType, sp.Expr)):
        if np.sum(X.shape) > np.sum(X.shape[0]): sys.exit(bad_X)
        if np.sum(Y.shape) > np.sum(Y.shape[0]): sys.exit(bad_Y)
        if len(X) != len(Y): sys.exit(bad_data)
    if isinstance(Y,(FunctionType, sp.Expr)): Y = make_array(X, Y)
    if not isinstance(i,int): sys.exit(bad_i)
    h, dY = float(h), 0
    if point_type == 'three':
        dY = (Y[i+1] - Y[i-1])/(2*h)
    if point_type == 'five':
        dY = (Y[i-2] - 8*Y[i-1] \
            + 8*Y[i+1] - Y[i+2])/(12*h)
    if point_type == '2nd_derivative':
        dY = (Y[i-1] - 2*Y[i] + Y[i+1])/(h**2)
    else: sys.exit(bad_type)
    return dY

def richard_extrapolation(function, x0, h, order, direction=0):
    """Results in higher-accuracy of derivative at point in function with lower-order formulas to minimize round-off error and increase O(h) of truncation error.

    Parameters
    ----------
    function : expression
        Polynomial over which derivative must be calculated.
    
    x0 : float
        Point about which extrapolation centers
    
    h : float
        Step-size through interval.

    order : int
        Order for rate of convergence.
    
    direction : string
        `'forward'` or `'backward'` construction.
    
    Returns
    -------
    p : expression
        Lambdified constructed polynomial.
    
    p(x0) : float
        Evaluation of `p` at `x`.

    Raises
    ------
    bad_function : string
        If `function` is not an expression.
    
    bad_order : string
        `order` must be an integer and non-zero.
    
    bad_direction : string
        If `direction` is neither `'forward'` nor `'backward'`.
    
    Warns
    -----
    func_func : string
        Evaluate input expression for Newton difference approximation.
    
    See Also
    --------
    newton_difference() : Newton Difference method to build extrapolation for function's derivative and order of error.
    """
    sym_function = 'function' # varname(function)
    bad_function = 'Function, ' + sym_function + ' must be expression.'
    bad_order = 'Expected integer.'
    bad_direction = "Supplied direction was not understood. Please specify 'forward' or 'backward'."
    made_poly = 'I have found your requested polynomial! P = '
    if not isinstance(function,(FunctionType, sp.Expr)): 
        sys.exit(bad_function)
    if isinstance(function,(FunctionType, sp.Expr)):  print(func_func)
    if not isinstance(order,int): sys.exit(bad_order)
    if direction != 0 and direction != 'forward' and direction != 'backward': sys.exit(bad_direction)
    def f(h):
        x = x0 + h
        return x, function(x)
    x0, h = float(x0), float(h)
    i, X, FX = 0, [], []
    while i < order:
        dx = h / (2**order) * (2**i)
        x_i, fx_i = f(dx)
        X.append(x_i); FX.append(fx_i)
        i += 1
    m = len(X)
    n = m + 1
    return newton_difference(X, FX, x0, direction)
# --------------------

# --------------------
# differential equations
class ode:
    """Solve ordinary differential equations.

    Attributes
    ----------
    runge_katta : function
        Gives Taylor method-like high-order, local truncation error, but without calculation of higher-order derivatives.
    """
    def runge_kutta(f, t0, w0, tn, N):
        """Approximate solution of initial value problem.

        Parameters
        ----------
        f : expression
            Equation to which derivative will be made.
        
        t0 : float
            Point at which initial condition is evaluated.
        
        w0 : float
            Initial condition for function.
        
        tn : float
            Final point in domain for which function is to be evaluated.

        N : integer
            Maximum number of iterations for approximation.
        
        Returns
        -------
        T : list
            Points of t0 < t < tn which were analyzed at each step.
        
        W : list
            Evaluations of t at each step.
        
        I : list
            Collection of steps evaluated.
        
        Raises
        ------
        bad_f : string
            The input for `f` was not an expression.
        
        bad_N : string
            Desired number of iterations was not an integer.
        
        Warnings
        --------
        Outputs to console the solution steps.
        """
        sym_f = 'f' # varname(f)
        bad_f = 'Input, ' + sym_f + ' was not an expression.'
        bad_N = 'Desired number of iterations must be integer and non-zero.'
        if not isinstance(f,(FunctionType, sp.Expr)): sys.exit('ERROR! ' + bad_f)
        if not isinstance(N,(int)) or N == 0: sys.exit('ERROR!\n' + bad_N)
        h, t, w, T, W, I = (tn - t0) / N, t0, float(w0), [], [], []
        T.append(t); W.append(w)
        print('\n-----------SOLUTION-----------')
        print('------------------------------')    
        print('i\tt0\tw0\twn')
        print('------------------------------')
        for i in range(N):
            w0 = w
            K1 = h*f(t, w)
            K2 = h*f(t + h/2, w + K1/2)
            K3 = h*f(t + h/2, w + K2/2)
            K4 = h*f(t + h, w + K3)
            w += (K1 + 2*K2 + 2*K3 + K4) / 6
            t += h
            T.append(t); W.append(w); I.append(i)
            if isinstance(t, (FunctionType, sp.Expr)): print('%s\t%s\t%s\t%s'% (i,t,w0,w) )
            else: print('%.0f\t%.4f\t%.4f\t%.4f'% (i,t,w0,w) )
        print('------------------------------')
        I.append(N)
        return T, W, I
# --------------------
#   #   #   #   #   #   #   #   #


#################################
## Test
# test compile of module.
class test:                     # test class
    def test():                 # test function
        """Was the module loaded correctly?

        Raises
        ------
        success : string
            Prints a message of successful function call.
        """
        success = 'Test complete.'
        sys.exit(success)
#   #   #   #   #   #   #   #   #


#################################
## End of Code
# test.test()     # 'Test complete.'
#   #   #   #   #   #   #   #   #