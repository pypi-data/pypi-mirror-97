"""list utilities."""
import logging
import secrets
from typing import Optional

from wpdatautil.humanfriendly import format_size

log = logging.getLogger(__name__)


def fill_memory(*, num_unique_bytes_per_allocation: int = 1024, multiplier_per_allocation: int = 1024 ** 2, max_allocations: Optional[int] = None) -> None:
    """Allocate available memory into a list of effectively unique bytes objects.

    This function is for diagnostic purposes.

    :param num_unique_bytes_per_allocation: Each allocation is created by multiplying a random sequence of bytes of this length.
    :param multiplier_per_allocation: Each allocation is created by multiplying the random sequence of bytes by this number.
    :param max_allocations: Optional number of max allocations.
    """
    # Ref: https://stackoverflow.com/a/66109163/
    num_allocation_bytes = num_unique_bytes_per_allocation * multiplier_per_allocation
    log.info(
        f"Allocating cumulative instances of {num_allocation_bytes:,} bytes ({format_size(num_allocation_bytes)}) each. "
        f"Each allocation uses {num_unique_bytes_per_allocation:,} unique bytes ({format_size(num_unique_bytes_per_allocation)}) "
        f"with a multiplier of {multiplier_per_allocation:,} ({format_size(multiplier_per_allocation)})."
    )

    # Allocate memory
    allocated = []
    num_allocation = 1
    while True:
        unique_bytes_for_allocation = secrets.token_bytes(num_unique_bytes_per_allocation)
        allocated.append(unique_bytes_for_allocation * multiplier_per_allocation)
        num_total_bytes_allocated = num_allocation * num_allocation_bytes
        log.info(f"Used a total of {num_total_bytes_allocated:,} bytes ({format_size(num_total_bytes_allocated)}) via {num_allocation:,} allocations.")
        if max_allocations and (max_allocations == num_allocation):
            break
        num_allocation += 1
