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
