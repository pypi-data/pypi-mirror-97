import math
import numpy as np
from scipy.integrate import quad
import sympy as sp
from sympy import simplify, solve

def test():
    print('test')

def bisection(f, a, b, tol):
    i, x0, error = 0, 0, tol*10
    P, ERROR, I = [], [], []
    while error >= tol:
        x = (b - a)/2
        p = a + x
        P.append(p)
        if f(a)*f(p) > 0: a = p
        else: b = p
        error = x - x0
        ERROR.append(error); I.append(i)
        x0 = x
        i += 1
    return P, ERROR, I

def clamped_cubic_spline(X, f, a, b):
    def algorithm(f, m):
        n = m - 1
        Y, YP = np.zeros(m), np.zeros(m)
        YP_sym = sp.diff(f, sym_x)
        i = 0
        while i <= n:
            xi = X[i]
            Y[i] = f.evalf(subs={sym_x: xi})
            YP[i] = YP_sym.evalf(subs={sym_x: xi})
            i += 1
        # STEP 1:   build list, h_i
        H, i = np.zeros(n), 0
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
        # STEP 7:   build lists b, c, and d
        B, D, i, j = np.zeros(n), np.zeros(n), 1, 0
        while i <= n:
            j = n-i
            C[j] = Z[j] - MU[j]*C[j+1]
            B[j] = (A[j+1] - A[j])/H[j] - H[j]*(C[j+1] + 2*C[j])/3
            D[j] = (C[j+1] - C[j])/(3*H[j])
            i += 1
        return Y, A, B, C, D
    sym_x, m = sp.Symbol('x'), len(X)
    Y, A, B, C, D = algorithm(f(sym_x), m)
    splines_j, j = [], 0
    while j < n-1:
        xj, aj, bj, cj, dj = X[j], A[j], B[j], C[j], D[j]
        sj = aj + bj*(sym_x - xj) + cj*(sym_x - xj)**2 + dj*(sym_x - xj)**3
        splines_j.append(sj)
        j += 1
    spline = sum(Sj)
    return Y, splines_j, spline

def composite_simpson(f, a, b, h):
    n = math.ceil((b-a)/h)
    XJ1, XJ2, XJ, = [], [], []
    YJ1, YJ2, YJ, = [], [], []
    XJ.append(a); YJ.append(f(a))
    j, y1, z1 = 1, 0, 0
    while j <= (n/2)-1:
        xj = a + 2*j*h
        yj = f(xj)
        XJ1.append(xj); YJ1.append(yj)
        z1 += yj
        j += 1
    k, y2, z2 = 1, 0, 0
    while k <= n/2:
        xj = a + (2*k - 1)*h
        yj = f(xj)
        XJ2.append(xj); YJ2.append(yj)
        z2 += yj
        k += 1
    l = 0
    while l < len(XJ1):
        XJ.append(XJ2[l]); YJ.append(YJ2[l])
        XJ.append(XJ1[l]); YJ.append(YJ1[l])
        l += 1
    XJ.append(XJ2[l]); YJ.append(YJ2[l])
    XJ.append(b); YJ.append(f(b))
    F = h/3*(f(a) + 2*z1 + 4*z2 + f(b))
    return XJ, YJ, F

def composite_trapz(f, a, b, h):
    XJ, YJ = [], []
    XJ.append(a); YJ.append(f(a))
    j, n, y, z = 1, math.ceil((b-a)/h), 0, 0
    while j <= n-1:
        x_j = a + j*h
        XJ.append(x_j)
        y_j = f(x_j)
        YJ.append(y_j)
        z += y_j
        j += 1
    XJ.append(b); YJ.append(f(b))
    return XJ, YJ, h/2*(f(a) + 2*z + f(b))

def gaussian_quadrature(function, a, b):
    return integrate(function, a, b)

def integrate(function, a, b):
    F, error = quad(function, a, b)
    return F, error

def l_infinity_norm(x, x0):
    norm_i, i = np.zeros_like(x0), 0
    while i < n:
        norm_i[i] = np.abs(x[i] - x0[i])
        i += 1
    return np.amax(norm_i)
    
def lagrange_polynomial(X, Y):
    def term(xk, yk):
        num, den, L_k = [], [], []
        for xl in X:
            if xl != xk:
                num.append(sym_x-xl)
                den.append(xk-xl)
        L_k = (np.divide(np.prod(num), np.prod(den)))
        return L_k * yk
    def error(n, xi):
        roots, g, xi_error = [], [], []
        i = 0
        while i <= n:
            root = X[i]
            roots.append(sym_x - root)
            g = np.prod(roots)
            k = 0
            while k <= n:
                xi = sp.diff(xi, sym_x)
                k += 1
            dxi = np.abs(xi.evalf(subs={sym_x: root})/(math.factorial(k)))
            xi_error.append(np.abs(dxi))
            xi_err = np.max(xi_error)
            g_prime = sp.diff(g, sym_x)
            r = solve(g_prime)
            if i == 0:
                x = g_prime
                gx = g.evalf(subs={sym_x: x})
            if i == 1:
                x = r[0]
                gx = g.evalf(subs={sym_x: x})
            else:
                R = []
                for s in r:
                    if not isinstance(s, complex):
                        R.append(g.evalf(subs={sym_x: s}))
                gx = np.amax(np.abs(R))
            i += 1
        return np.abs(xi_err*gx)
    sym_x, yn, bound = sp.Symbol('x'), [], []
    for xk in X:
        k = X.index(xk)
        yn.append(term(xk, Y[k]))
        bound.append(error(k, sum(yn)))
    return yn, sum(yn), bound

def linear_least_squares(X_i, Y_i, n):
    def poly(X):
        terms, k = [], 0
        for x in X:
            terms.append(x*(sym_x**k))
            k += 1
        p = simplify(sum(terms))
        err, i = 0, 0
        for x_i in X_i:
            px = p.subs(sym_x, x_i)
            err += (Y_i[i] - px)**2
            i += 1
        return p, err
    m, sym_x = len(X_i), sp.Symbol('x')
    A, x = np.zeros((n+1, n+1)), np.zeros((n+1,1))
    b, i = np.zeros_like(x), 0
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
    X, terms, k = x[0], [], 0
    for x in X:
        terms.append(x*(sym_x**k))
        k += 1
    polynomial = simplify(sum(terms))
    E, i = 0, 0
    for x_i in X_i:
        E += (Y_i[i] - polynomial.subs(sym_x, x_i))**2
        i += 1
    return polynomial, E

def newton_difference(X, FX, m, n, x, state):
    def fterm(i, j):
        fij = (fxn[i][j] - fxn[i-1][j])/(fxn[i][0] - fxn[i-j][0])
        return fij
    fxn, coeff, term, poly = np.zeros((m,n)), [], [], []
    m, n = m - 1, n - 1
    fxn[:m,0], fxn[:m,1], j = X, FX, 1
    while j <= n:
        i = 1
        while i <= m:
            fk = fterm(i, j)
            fxn[i][j+1] = fk
            if state == 'forward' and i == j:
                coeff.append(fk)
            if state == 'backward' and i == m - 1:
                coeff.append(fk)
            i += 1
        j += 1
    for c in coeff:
        k = coeff.index(c)
        term.append(sym_x - X[k])
        poly.append(c*np.prod(term))
    if state == 'forward': polynomial = simplify(sum(poly) + FX[0])
    if state == 'backward': polynomial = simplify(sum(poly) + FX[m])
    px = polynomial.subs(sym_x, x)
    return polynomial, px

def richard_extrapolation(function, x0, h, order, state):
    def f(h):
        x = x0 + h
        return x, function(x)
    i, X, FX = 0, [], []
    while i < order:
        dx = h / (2**order) * (2**i)
        x_i, fx_i = f(dx)
        X.append(x_i); FX.append(fx_i)
        i += 1
    m = len(X)
    n = m + 1
    return newton_difference(X, FX, m, n, x0, state)

def single_variable_newton_raphson(f, x, p0, tol):
    i, error = 0, tol*10
    P, ERROR, I = [], [], []
    while error >= tol:
        fp0 = f(p0)
        df = sp.lambdify(x, sp.diff(f))
        dfp0 = df(p0)
        p = p0 - (fp0/dfp0)
        P.append(p)
        error = abs(p - p0)
        ERROR.append(error); I.append(i)
        p0 = p
        i += 1
    return P, ERROR, I

def vector_converge(A, x0, b, tol, type, method, w):
    def jacobi(x0):
        while i < n:
            j, y = 0, 0.
            while j < n:
                if j != i:
                    y += A[i][j]*x0[j]
                    j += 1
            xi[i] = (-y + b[i])/A[i][i]
            i += 1
        return xi
    def gauss_seidel(x0):
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
        return xi
    def successive_over_relaxation(x0):
        while i < n:
            gauss_seidel(x0)
            xi[i] = (1 - w)*x0[i] + w*gauss_seidel(x0)
            i += 1
        return xi
    n = len(x0)
    x0, b, norm, k = np.reshape(x0,(n,1)), np.reshape(b,(n,1)), tol*10, 0
    X, NORM, K = [], [], [] 
    X.append(x0); K.append(k)
    while norm > tol:
        xi, i = np.zeros_like(x0), 0
        if method == 'jacobi': xi = jacobi(x0)
        if method == 'gauss_seidel': xi = gauss_seidel(x0)
        if method == 'successive_over_relaxation': xi = successive_over_relaxation(x0)
        if type == 'l_infinity': norm = l_infinity_norm(xi, x0)
        if type == 'l_2': norm = l_2_norm(xi, x0)
        X.append(xi); NORM.append(norm); K.append(k)
        x0 = xi
        k += 1
    m, n = len(X[0]), len(X)
    X_mat, j = np.zeros((m,n)), 0
    while j < n:
        i = 0
        while i < m:
            X_mat[i][j] = float(X[j][i])
            i += 1
        j += 1
    return X_mat, NORM, K