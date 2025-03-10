from dataclasses import dataclass


@dataclass
class Result:
    sma_days: int
    sma_current_value: float
    current_price: float
    yesterday_close: float
    current_sma: float
    yesterday_sma: float
    #
    current_diff: float
    yesterday_diff: float
    current_distance: float
    yesterday_distance: float

    # crossings
    signal_now: str = "hold"
    intraday_to_below: bool = False
    intraday_to_above: bool = False
    nightly_cross_to_below: bool = False
    nightly_cross_to_above: bool = False
