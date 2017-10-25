import numpy as np
import numpy.random as npr
import pandas as pd
import scipy.stats as scistat
from matplotlib import pyplot as plt


def generate_expression_data(n_analytes=100, n_samples=2, n_replicates=3, p_regulated=0.2, mean_offset=3.0, var=0.2,
                             diff_var=2.0):
    # Here we follow a convension, The first sample is the reference i.e. have all label 1
    labels = npr.binomial(1, p_regulated, (n_analytes, n_samples - 1))
    template = np.hstack((np.zeros((n_analytes, 1)), labels))

    # We expand the template labels into several replicates
    regulated = np.repeat(template, n_replicates, axis=1)

    # If the reading is regulated, offset it with a random offset sampled from the normal distribution
    offset = regulated * npr.normal(0, diff_var, (n_analytes, 1))

    # Model a differentexpression level for the different analytes
    expr_level = np.ones((n_analytes, n_samples * n_replicates)) * npr.normal(mean_offset, mean_offset, (n_analytes, 1))

    # add noice for each measurement
    expression = npr.normal(offset + expr_level, var, (n_analytes, n_replicates * n_samples))
    expression = 2 ** expression

    analyte_names = ["a" + str(i + 1) for i in range(n_analytes)]
    sample_names = ["s" + str(i + 1) + '_' + str(j + 1) for i in range(n_samples) for j in range(n_replicates)]

    # Create a dataframe for expression values
    expr_df = pd.DataFrame(expression, columns=sample_names, index=analyte_names)
    expr_df.loc["Sample", :] = [i + 1 for i in range(n_samples) for j in range(n_replicates)]

    # Create a dataframe with answers if the reading was modeled as differential or not
    label_df = pd.DataFrame(template, columns=[i + 1 for i in range(n_samples)], index=analyte_names)

    return expr_df, label_df


dat = generate_expression_data(n_analytes=10000)
data_labels = dat[1][:]
data = dat[0][:-1]

pval_plur = []

# Generate p-values through t-test
for i in range(0, data.shape[0]):
    pval_plur.append(scistat.ttest_ind(data.iloc[i, :3], data.iloc[i, 3:])[1])

# Number of p-values
m = len(pval_plur)

# Create an array with tuples of index and value from pval_plur
pval_plur = [[x, y] for x, y in sorted(enumerate(pval_plur))]
pval_plur = np.array(pval_plur)

# Sort after p-values, smallest to largest
pval_plur = pval_plur[np.argsort(pval_plur[:, 1])]

# Set our lambda and t
lambd = 0.5
t = 0.05

# Count how many p-values are greater than our lambda
i = 0
for j in range(0, len(pval_plur)):
    if pval_plur[j][1] > lambd:
        i += 1
    else:
        next
lambda_count = i

# Calculate our Pi_0 and Q_P_i(m)
pi_zero = lambda_count / (m * (1 - lambd))
qpim = pi_zero * pval_plur[-1][1]

# qpii = [[1000, qpim]]
qpii = []

# generate q-values iterating over the ordered p-value-indexes from pval_plur
for i in reversed(range(1, len(pval_plur) + 1)):
    if i == len(pval_plur):
        qval = min(((pi_zero * pval_plur[i - 1][1] * m) / i), pi_zero * pval_plur[i - 2][1])
    else:
        qval = min(((pi_zero * pval_plur[i - 1][1] * m) / i), pi_zero * pval_plur[i][1])

    qpii.append([pval_plur[i - 1][0], qval])

qpii = np.array(qpii)

# qvals = np.array(qpii[::-1])
qvals = qpii[np.argsort(qpii[:, 0])]

# put them together before cumsum
df = pd.DataFrame({'q': qvals[:, 1], 'labs': data_labels.iloc[:, 1]})

df = df.sort_values(by='q')

null = np.cumsum(1 - df.iloc[:, 0]) / range(1, len(df.iloc[:, 0]) + 1)
df['null'] = null

del df['labs']
