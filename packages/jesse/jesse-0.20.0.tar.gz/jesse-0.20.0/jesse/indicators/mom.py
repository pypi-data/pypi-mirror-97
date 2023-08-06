from typing import Union

import numpy as np
import talib

from jesse.helpers import get_candle_source
from jesse.helpers import get_config


def mom(candles: np.ndarray, period: int = 10, source_type: str = "close", sequential: bool = False) -> Union[
    float, np.ndarray]:
    """
    MOM - Momentum

    :param candles: np.ndarray
    :param period: int - default=10
    :param source_type: str - default: "close"
    :param sequential: bool - default=False

    :return: float | np.ndarray
    """
    warmup_candles_num = get_config('env.data.warmup_candles_num', 240)
    if not sequential and len(candles) > warmup_candles_num:
        candles = candles[-warmup_candles_num:]

    source = get_candle_source(candles, source_type=source_type)
    res = talib.MOM(source, timeperiod=period)

    if sequential:
        return res
    else:
        return None if np.isnan(res[-1]) else res[-1]
