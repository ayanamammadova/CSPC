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

## PW3 - Data, Distributions, Testing, and Causation
Computer Science for Physics and Chemistry PW3

**Data showed:**

- Part 1 

shape:  (303, 14)
first rows: 
   age  sex  cp  trestbps  chol  fbs  ...  exang  oldpeak  slope  ca  thal  target
0   63    1   0       145   233    1  ...      0      2.3      2   0     2       0
1   67    1   3       160   286    0  ...      1      1.5      1   3     1       1
2   67    1   3       120   229    0  ...      1      2.6      1   2     3       1
3   37    1   2       130   250    0  ...      0      3.5      2   0     1       0
4   41    0   1       130   204    0  ...      0      1.4      0   0     1       0

[5 rows x 14 columns]
              age        chol    trestbps     thalach
count  303.000000  303.000000  303.000000  303.000000
mean    54.438944  246.693069  131.689769  149.607261
std      9.038662   51.776918   17.599748   22.875003
min     29.000000  126.000000   94.000000   71.000000
25%     48.000000  211.000000  120.000000  133.500000
50%     56.000000  241.000000  130.000000  153.000000
75%     61.000000  275.000000  140.000000  166.000000
max     77.000000  564.000000  200.000000  202.000000


- Part 2

- Age:                    slightly left-skewed
- Cholesterol:            right-skewed, with a few high values
- Resting blood pressure: almost symmetrical, but with some high values
- Maximum heart rate:     sligtly left-skewed, with high values around 160

- Part 3
Q-Q plots and Shapiro-Wilk tests were used to assess whether the four variables followed a normal distribution

age:
W       = 0.9865
p-value = 0.006069

not normally distributed


chol:
W       = 0.9473
p-value = 0.000000

not normally distributed


trestbps:
W       = 0.9665
p-value = 0.000002

not normally distributed


thalach:
W       = 0.9765
p-value = 0.000070

not normally distributed

All p-values were below 0.05. So, the null hypothesis of normality was rejected for all four variables

- Part 4

Maximum heart rate was compared between healthy individuals (target = 0) and individuals with heart disease (target = 1)

healthy p value:  0.0005433097956480682
disease p value:  0.35231701701128004

Mann-Whiteney U test
test statistic:  16989.5
p-value:         1.8610146112914352e-13

groups differ significantly

healthy:
n     = 164
mean  = 158.3780487804878
SE    = 1.4991962654873978

heart disease:
n     = 139
mean  = 139.25899280575538
SE    = 1.9163330086200157

Since the p-value was below 0.05, a statistically significant difference between the groups was found. The healthy group had a higher mean maximum heart rate than the group with heart disease

- Part 5

pearson correlation:  -0.393805805986821
p-value:              1.1092756352878018e-12

The results showed a negative correlation. 
Older individuals tend to have lower maximum heart rates in this dataset. But correlation does not prove causation

- Part 6

(1000, 5)
   benzene  cadmium  pollution_index  age  malignancy
0     7.90    51.21             77.4   54        85.6
1    28.45    34.42             43.9   71        69.8
2    22.41    60.24             85.9   31        86.8
3    29.00    47.68             69.7   54        78.0
4    18.66     6.17              9.4   55        33.2
Index(['benzene', 'cadmium', 'pollution_index', 'age', 'malignancy'], dtype='str')
           benzene      cadmium  pollution_index          age   malignancy
count  1000.000000  1000.000000      1000.000000  1000.000000  1000.000000
mean     24.797770    34.577010        49.718700    54.679000    60.936100
std      14.921387    20.889587        29.158904    11.785791    24.127447
min       0.000000     0.000000         0.100000    25.000000     0.400000
25%      12.332500    15.975000        24.050000    47.000000    41.975000
50%      24.810000    35.615000        49.500000    55.000000    60.900000
75%      36.580000    52.660000        75.925000    62.000000    81.200000
max      56.830000    75.370000        99.900000    90.000000   100.000000



benzene
number of observations:  1000
correlation:             0.38469912819385765
p-value:                 1.2755900271404846e-36

cadmium
number of observations:  1000
correlation:             0.8799707225667612
p-value:                 0.0

Cadmium had a stronger relationship with malignancy (r = 0.88), while benzene had a weaker correlation (r = 0.385). Firstly, it can seem that cadmium is the main cause. But, other factors, such as pollution level and age, may affect these results


- Part 7

benzene (pollution range 40–60)
number of patients:  199
correlation:         0.7016477487017813
p-value:             8.078189339208182e-31

cadmium (pollution range 40–60)
number of patients:  199
correlation:         0.3156977435684184
p-value:             5.569424879737283e-06

In this group, benzene had a stronger relationship with malignancy (r = 0.702) than cadmium (r = 0.316). Both relationships were statistically significant. This shows that the results change when we look at a smaller group, but it does not prove that either chemical causes malignancy

Conclusion: Initially, cadmium seemed more strongly linked to malignancy. However, in the smaller group, benzene had the stronger relationship. This shows that other factors may affect the results, and correlation alone cannot prove which chemical causes malignancy

- Bonus Part

target proportions:
target
0    0.541254
1    0.458746
Name: proportion, dtype: float64

entropy: 0.9950837594929733 bits

The entropy is 0.995 bits which is close to 1, meaning the dataset has almost equal numbers of healthy people and people with heart disease