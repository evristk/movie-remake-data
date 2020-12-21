import pandas as pd
import regex as re

# For regex matching we use positive lookbehind/lookahead

# This regex expression matches iteration measurement by JMH output:
# JMH example: " Iteration 1   : 304.390 ms/op"
pattern_iter_val = re.compile("(?<=Iteration\s+\d:\s)\d+\.\d+(?=\s+ms)")

# This regex matches the parameter values as written by JMH output.
# JMH example: "(param1 = 99, param2 = full, param3 = true)"
pattern_param_val = "(?<=(\(|(,\s))[\w\d]+\s=\s)[\w\d\[\]\.\,\s]+[\w\d]+(?=\)|,)"

txt_file = "jmh_result.txt"
csv_file = "jmh_result.csv"

with open(txt_file, "r") as f:
    params = []
    rows = []
    for line in f:
        if "# Parameters:" in line:
            params = []
            for match in re.finditer(pattern_param_val, line):
                param = match.group()
                params.append(param)

        # This line is an iteration measurement
        if pattern_iter_val.search(line):
            # extract measurement number
            measurement = pattern_iter_val.search(line).group()
            iteration = [measurement]
            # collect current number and parameters
            iteration.extend(params)
            # rows to add in dataframe
            rows.append(iteration)

df = pd.DataFrame(data=rows)

# first column contains a measurement, make sure data type is number
df[0] = df[0].apply(pd.to_numeric)

# set names for columns. First columns is measurement, rest are parameter columns
columns = ['measurement']
columns.extend([f'param{x}' for x in range(1, df.shape[1])])
df.columns = columns

# create to CSV file
df.to_csv(csv_file, index=True)
