import pandas as pd
import os

EXCELSHEET_FILENAME = "D:/IS/stracktraces/StackTraceClassification/Apache/Top-1/"
exception_count = {}
for filename in os.listdir(EXCELSHEET_FILENAME):
    if filename.endswith(".csv"):
        df = pd.read_csv(EXCELSHEET_FILENAME + filename)
        bug_df = pd.DataFrame(df[df['Label'].isin(['Misleading'])].groupby(['BugID', 'Exception']))
        for exception in bug_df[0]:
            if not exception_count.get(exception[1]):
                exception_count[exception[1]] = 1
            else:
                exception_count[exception[1]] = exception_count.get(exception[1]) + 1

print(dict(sorted(exception_count.items(), key=lambda item: item[1])))
