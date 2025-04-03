import pandas as pd

def track_flaky_tests(results_csv):
    df = pd.read_csv(results_csv)
    flaky = df[df.duplicated(subset=['test_name', 'status'], keep=False)]
    return flaky
