from dataclasses import dataclass

@dataclass
class Result:
    sma: int
    current_price: float
    yesterday_close: float
    current_sma: float
    yesterday_sma: float
    #
    current_diff: float
    yesterday_diff: float
    current_distance: float
    yesterday_distance: float