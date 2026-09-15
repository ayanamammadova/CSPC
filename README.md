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