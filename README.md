# CSPC - Computer Science for Physics and Chemistry
My coursework repository. Each practical is under PW<n>/Lab <A>/.
## Setup
Create the environment for a given lab:
    conda env create -f PW<n>/Lab\ <A>/environment.yml
    conda activate cspc
---
## PW1 - Lab A: Reproducible Foundations
Computer Science for Physics and Chemistry PW1 – Lab A
**What I built:**
- I created a repository using Git, set up and activated a Conda environment with the required packages, added a .gitignore file to prevent unnecessary files from being tracked, and implemented testing and a speed check for the decay simulation
**Speed comparison (loop vs NumPy):**
- loop : 2.828086 s
- numpy : 0.000281 s
- speed-up: 10075.80 x faster
**Tests:** all passing? yes
**Conclusion:**
- I learned to work with tools like Conda, Git, and GitHub that will be useful for future projects. I also learned the usefulness of .gitignore and pytest and improved my knowledge of using the command line during this PW. From the speed test results, it is clear that using NumPy significantly reduces the run time. The time is slightly different each time because the computer's CPU, background processes, and memory conditions can vary and all 3 tests passed successfully, showing that the functions behave as expected

## PW1 - Lab B: Data, Plotting, and Automation
Computer Science for Physics and Chemistry PW1 – Lab B
**Data showed:**
- The graph decreases rapidly at first and then gradually slows down. The observed count starts at 5000 and reaches approximately 0 by the end of the observation period (19 seconds)
- **Comparison:**
- The observed data just follows the analitical data but with some negligible fluctuations. Analitical figure is calculated using formula (analitical = N0 * np.exp(-LAMBDA * t))
- **What Snakemake do:**
- Snakemake automates the creation of figure.png by running plot.py when the input data is newer than the generated figure or the figure is not created yet

## PW2 - Lab A: Motion from Tracking Data
Computer Science for Physics and Chemistry PW2 – Lab A
**Data showed:**
Mean acceleration: -8.57968750000008
Acceleration standard deviation: 28.71612572170628
Largest position difference: 0.7845625000002201
- **Discussion:**
- Acceleration is much noisier because calculating it requires differentiating the position data twice, which increases small measurement errors and fluctuations

## PW2 - Lab B: Optimization in Chemistry
Computer Science for Physics and Chemistry PW2 – Lab B
**Data showed:**
For Part 2

- Gradient descent x = 2.9999999996088893
- Newton           x = 3.0
- SLSQP            x = 3.0

When x0 = 0
- Gradient descent  x = -1.3008395659232233
- Newton            x = 0.16993844331159128
d2g(x) = -5.653451105817997
d2g(x) < 0 so it is maximum
- SLSQP             x = -1.3008569445066596

When x0 = 2
- Gradient descent  x = -1.300839565941577
- Newton            x = 1.1309011226299859
g(x) = 3.929769818223846
d2g(x) = 9.347248189989148
d2g(x) > 0 so it is minimum
- SLSQP             x = -1.3006394477423422

For f(x), all three methods agreed and found x approximatly 3
For g(x), the methods did not always agree. From x0=0, Newton found a maximum, while gradient descent and SLSQP found the minimum. From x0=2, Newton found a minimum. Thus, the starting point affects Newton’s result, while the other methods found the minimum near x=−1.30

For Part 3

k = 0.26176137053117843

For Part 4

- SLSQP x: 0.6638474279789005
- Newton x: 0.6638476669609822
- SLSQP and Newton x are the same
- H2: 0.3361525720210995
- I2: 0.3361525720210995
- HI: 1.327694855957801

For Part 5

equivalence point: 50.0 mL