from dataclasses import dataclass

@dataclass
class Result:
    current_price: float
    yesterday_close: float
    current_sma: float
    yesterday_sma: float