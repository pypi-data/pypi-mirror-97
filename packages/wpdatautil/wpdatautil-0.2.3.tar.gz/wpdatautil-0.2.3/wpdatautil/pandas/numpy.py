"""pandas numpy utilities."""
import logging
from typing import Optional

import numpy as np
import pandas as pd

from wpdatautil.humanfriendly import format_size

log = logging.getLogger(__name__)


def fill_memory(*, len_per_allocation: int = (1024 ** 3) // 8, max_allocations: Optional[int] = None) -> None:
    """Allocate available memory into a dataframe of int64 columns.

    This function is for diagnostic purposes.

    :param len_per_allocation: Length of each int64 column in dataframe.
    :param max_allocations: Optional number of max allocations.
    """
    num_allocation_bytes = len_per_allocation * (64 // 8)
    log.info(
        f"Allocating cumulative instances of {num_allocation_bytes:,} bytes ({format_size(num_allocation_bytes)}), "
        f"with each allocation using {len_per_allocation:,} int64 numbers."
    )

    # Allocate memory
    df = pd.DataFrame()
    num_allocation = 1
    while True:
        df[f"c{num_allocation}"] = np.arange(start=num_allocation, stop=num_allocation + len_per_allocation, dtype="int64")
        num_total_bytes_allocated = num_allocation * num_allocation_bytes
        log.info(f"Used a total of {num_total_bytes_allocated:,} bytes ({format_size(num_total_bytes_allocated)}) via {num_allocation:,} allocations.")
        if max_allocations and (max_allocations == num_allocation):
            break
        num_allocation += 1
