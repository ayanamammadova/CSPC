"""
PW2 Lab B Part 2 -- three routes to a minimum.

Compare gradient descent, Newton, and SLSQP on two functions:
  2A: f(x) = (x-3)**2 + 1          (easy, one minimum at x=3)
  2B: g(x) = x**4 - 3*x**2 + x + 5 (harder, several stationary points)
Run:  python warmup.py
"""
import numpy as np
from scipy.optimize import newton, minimize

# ---------- 2A: easy convex function ----------
def f(x):   return (x-3)**2 + 1
def df(x):  return 2*(x-3)
def d2f(x): return 2.0

# TODO 2A: minimise f three ways from x0=0 and print each result:
#   (1) gradient descent by hand (loop x = x - lr*df(x) until the step is tiny)
#   (2) scipy.optimize.newton(df, x0, fprime=d2f)
#   (3) scipy.optimize.minimize(f, x0, method="SLSQP")

# gradient descent
x0 = 0
x = x0
lr = 0.1
for i in range(1, 1000):
    grad = df(x)
    a = x
    x = x - lr * grad
    if abs(x - a) < 1e-10:
        break
print("\nGradient descent")
print(f"x = {x}")

# Newton
x_newton = newton(df, x0, fprime = d2f)

print("\nNewton")
print(f"x = {x_newton}")

# SLSQP
x_slsqp = minimize(f, x0, method = "SLSQP")

print("\nSLSQP")
print(f"x = {x_slsqp.x[0]}")




# ---------- 2B: harder landscape ----------
def g(x):   return x**4 - 3*x**2 + x + 5
def dg(x):  return 4*x**3 - 6*x + 1
def d2g(x): return 12*x**2 - 6

# TODO 2B: run the same three methods on g, from x0=0 AND from x0=2.
#   For Newton (which solves dg(x)=0), also check the sign of d2g at the answer:
#   d2g > 0 means a minimum, d2g < 0 means a maximum.
#   In your README note: do the methods agree? did Newton find a minimum or
#   another stationary point? how did the starting point change the result?

# when x0 = 0
print("\n\nWhen x0 = 0\n")
# gradient descent
x0 = 0
x = x0
lr = 0.1
for i in range(1, 1000):
    grad = dg(x)
    a = x
    x = x - lr * grad
    if abs(x - a) < 1e-10:
        break
print("\nGradient descent")
print(f"x = {x}")

# Newton
x_newton = newton(dg, x0, fprime = d2g)

print("\nNewton")
print(f"x = {x_newton}")
print(f"d2g(x) = {d2g(x_newton)}")
if d2g(x_newton) > 0:
  print(f"d2g(x) > 0 so it is minimum")
elif d2g(x_newton) < 0:
  print(f"d2g(x) < 0 so it is maximum")

# SLSQP
x_slsqp = minimize(g, x0, method = "SLSQP")

print("\nSLSQP")
print(f"x = {x_slsqp.x[0]}")


# When x0 = 2

print("\n\nWhen x0 = 2\n")

# gradient descent
x0 = 2
x = x0
lr = 0.1
for i in range(1, 1000):
    grad = dg(x)
    a = x
    x = x - lr * grad
    if a == x:
        break
print("\nGradient descent")
print(f"x = {x}")

# Newton
x_newton = newton(dg, x0, fprime = d2g)

print("\nNewton")
print(f"x = {x_newton}")
print(f"g(x) = {g(x_newton)}")
print(f"d2g(x) = {d2g(x_newton)}")
if d2g(x_newton) > 0:
  print(f"d2g(x) > 0 so it is minimum")
elif d2g(x_newton) < 0:
  print(f"d2g(x) < 0 so it is maximum")

# SLSQP
x_slsqp = minimize(g, x0, method = "SLSQP")

print(f"\nSLSQP")
print(f"x = {x_slsqp.x[0]}")

