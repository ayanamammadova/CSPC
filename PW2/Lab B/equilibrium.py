"""
PW2 Lab B Part 4 -- chemical equilibrium via the equilibrium constant K.

Reaction  H2 + I2 <=> 2 HI, starting from 1 mol H2 and 1 mol I2.
As the reaction proceeds by an extent x:  H2 = 1-x,  I2 = 1-x,  HI = 2x.
At equilibrium the composition satisfies the equilibrium constant
        K = [HI]^2 / ([H2][I2]) = (2x)^2 / ((1-x)(1-x)).
Given K, find the extent x. Solve it TWO ways and compare.
Run:  python equilibrium.py
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton, minimize

K = 15.6
a = b = 1.0

# TODO 1: write k_imbalance(x) = (2x)^2/((a-x)(b-x)) - K.
#         It equals zero exactly at equilibrium.

def k_imbalance(x):
    return (2*x)**2 / ((a-x)*(b-x)) - K

# TODO 2 (method 1): use scipy.optimize.newton to find the root of k_imbalance
#         (start x0=0.5). This is root-finding.

x_newton = newton(k_imbalance, 0.5)

# TODO 3 (method 2): use scipy.optimize.minimize to minimise k_imbalance(x)**2
#         (method "SLSQP", bounds [(0, 0.999)], x0=[0.5]). Print both answers
#         and confirm they agree.

x = minimize(lambda x: k_imbalance(x[0])**2, x0=[0.5], method="SLSQP", bounds=[(0, 0.999)]
)

x_slsqp = x.x[0]
print("SLSQP x:", x_slsqp)
print("Newton x:", x_newton)
if x_slsqp // 0.01 == x_newton // 0.01:
    print("SLSQP and Newton agree")
else:
    print("SLSQP and Newton do not agree")

# TODO 4: report the equilibrium amounts (H2, I2, HI), and plot how the three
#         amounts change with the extent x, marking the equilibrium. Save
#         equilibrium.png.

n_H2 = a-x_slsqp
n_I2 = b-x_slsqp
n_HI =2*x_slsqp

print("H2:", n_H2)
print("I2:", n_I2)
print("HI:", n_HI)

x_values = np.linspace(0, 0.99, 200)

H2 = a-x_values
I2 = b-x_values
HI = 2*x_values

plt.plot(x_values, H2, label="H2")
plt.plot(x_values, I2, label="I2")
plt.plot(x_values, HI, label="HI")

plt.axvline(x_slsqp, linestyle="--", label="equilibrium")

plt.xlabel("extent x")
plt.ylabel("amount (mol)")
plt.title("H2 + I2 -> 2HI")
plt.legend()
plt.grid()
plt.savefig("equilibrium.png")
plt.show()