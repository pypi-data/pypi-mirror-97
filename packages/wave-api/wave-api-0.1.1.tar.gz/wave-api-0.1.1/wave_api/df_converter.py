import pandas as pd


class DfConverter():
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_metric_dict(self) -> dict:
        # Convert first column as array
        first_col = self.df.iloc[:, 0]
        index_col = first_col.values.tolist()

        # Remove whitespace from all col names (str)
        index_col = [str(col_name) for col_name in index_col]
        index_col = [col_name.strip() for col_name in index_col]

        # Dictionary of column names and indices of dataframe
        counter = list(range(0, len(index_col)))
        metrics = {
            col_name: count
            for col_name, count in zip(index_col, counter)
        }
        return metrics

    def get_date_dict(self) -> dict:
        # Get first row as array
        first_row = self.df.iloc[0, :]
        date_col = first_row.values.tolist()

        counter = list(range(0, len(date_col)))
        dates = {date: count for date, count in zip(date_col, counter)}
        return dates
