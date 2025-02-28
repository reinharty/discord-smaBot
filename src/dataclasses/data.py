from dataclasses import dataclass
import pandas as pd

@dataclass
class Data:
    daily: pd.DataFrame
    intraday: pd.DataFrame