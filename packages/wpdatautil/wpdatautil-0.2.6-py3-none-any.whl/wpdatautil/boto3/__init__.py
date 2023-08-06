"""boto3 utilities."""
import logging
import time
import timeit

import boto3

log = logging.getLogger(__name__)


def glue_crawl(crawler: str, *, timeout_minutes: int = 60, retry_seconds: int = 5) -> None:
    """Crawl the specified AWS Glue crawler, waiting until completion."""
    # Ref: https://stackoverflow.com/a/66072347/
    timeout_seconds = timeout_minutes * 60
    client = boto3.client("glue")
    start_time = timeit.default_timer()
    abort_time = start_time + timeout_seconds

    def check_for_timeout() -> None:
        if timeit.default_timer() > abort_time:
            raise TimeoutError(f"Failed to crawl {crawler}. The allocated time of {timeout_minutes:,} minutes has elapsed.")

    def wait_until_ready() -> None:
        state_previous = None
        while True:
            response_get = client.get_crawler(Name=crawler)
            state = response_get["Crawler"]["State"]
            if state != state_previous:
                log.info(f"Crawler {crawler} is {state.lower()}.")
                state_previous = state
            if state == "READY":  # Other known states: RUNNING, STOPPING
                return
            check_for_timeout()
            time.sleep(retry_seconds)

    wait_until_ready()
    response_start = client.start_crawler(Name=crawler)
    assert response_start["ResponseMetadata"]["HTTPStatusCode"] == 200
    log.info(f"Crawling {crawler}.")
    wait_until_ready()
    log.info(f"Crawled {crawler}.")
