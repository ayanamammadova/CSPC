"""
PW2 Lab A -- Motion from tracking data.

Read noisy free-fall position measurements, then:
  - differentiate once  -> velocity
  - differentiate twice -> acceleration (should be ~ constant -g, but noisy!)
  - integrate the acceleration back up -> recover velocity and position

Complete the TODOs. Run:  python analysis.py
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid

# TODO 1: read freefall.csv into arrays t and y
data = np.loadtxt("freefall.csv", delimiter=",", skiprows=1)

t = data[:, 0]
y = data[:, 1]

# TODO 2: compute velocity and acceleration
v = np.gradient(y, t)
a = np.gradient(v, t)

print("Mean acceleration:", a.mean())
print("Acceleration standard deviation:", a.std())

# TODO 3: integrate a back up to recover velocity and position

v_recover = cumulative_trapezoid(a, t, initial=0) + v[0]
y_recover = cumulative_trapezoid(v_recover, t, initial=0) + y[0]

largest_difference = np.abs(y_recover - y)
print("Largest position difference:", largest_difference.max())

# TODO 4: make a figure with 3 stacked panels

fig, axes = plt.subplots(3, 1, sharex=True, figsize=(8, 10))

# position
axes[0].plot(t, y_recover, color="red")
axes[0].plot(t, y)
axes[0].grid(True)
axes[0].set_title("freefall motion")
axes[0].set_ylabel("position (m)")
axes[0].set_xlabel("time (s)")
# velocity
axes[1].plot(t, v)
axes[1].plot(t, v_recover, color="red")
axes[1].grid(True)
axes[1].set_ylabel("velocity (m/s)")
axes[1].set_xlabel("time (s)")
# acceleration
axes[2].plot(t, a)
axes[2].grid(True)
axes[2].axhline(-9.81, linestyle="--", color="green")
axes[2].set_ylabel("acceleration (m/s²)")
axes[2].set_xlabel("time (s)")

plt.tight_layout()
plt.savefig("motion.png")
plt.show()



# Bonus: A 2D tracked trajectory

data2 = np.loadtxt("trajectory.csv", delimiter=",", skiprows=1)

t2 = data2[:, 0]
x2 = data2[:, 1]
y2 = data2[:, 2]

vx = np.gradient(x2, t2)
vy = np.gradient(y2, t2)
speed = np.sqrt(vx**2 + vy**2)
fig2, axes2 = plt.subplots(2, 1, figsize=(8, 10))

# position
axes2[0].plot(x2, y2)
axes2[0].grid(True)
axes2[0].set_title("Plane 2D trajectory")
axes2[0].set_ylabel("y")
axes2[0].set_xlabel("x")
# velocity
axes2[1].plot(t2, speed)
axes2[1].grid(True)
axes2[1].set_title("speed/time")
axes2[1].set_ylabel("speed")
axes2[1].set_xlabel("time")

plt.tight_layout()
plt.savefig("motion2.png")
plt.show()