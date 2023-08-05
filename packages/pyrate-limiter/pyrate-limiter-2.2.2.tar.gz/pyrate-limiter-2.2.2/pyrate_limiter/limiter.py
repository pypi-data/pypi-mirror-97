""" Basic Rate-Limiter
"""
import asyncio
from functools import wraps
from inspect import iscoroutinefunction
from logging import getLogger
from typing import List, Dict, Union
from time import sleep, time
from .exceptions import InvalidParams, BucketFullException
from .request_rate import RequestRate
from .bucket import AbstractBucket, MemoryQueueBucket

logger = getLogger(__name__)


class Limiter:
    """Basic rate-limiter class that makes use of built-in python Queue"""

    bucket_group: Dict[str, AbstractBucket] = {}

    def __init__(
        self,
        *rates: List[RequestRate],
        bucket_class: AbstractBucket = MemoryQueueBucket,
        bucket_kwargs=None,
    ):
        """Init a limiter with rates and specific bucket type
        - Bucket type can be any class that extends AbstractBucket
        - 3 kinds of Bucket are provided, being MemoryQueueBucket, MemoryListBucket and RedisBucket
        - Opts is extra keyword-arguements for Bucket class constructor
        """
        self._validate_rate_list(rates)
        self._rates = rates
        self._bkclass = bucket_class
        self._bucket_args = bucket_kwargs or {}

    def _validate_rate_list(self, rates):  # pylint: disable=no-self-use
        if not rates:
            raise InvalidParams("Rate(s) must be provided")

        for idx, rate in enumerate(rates[1:]):
            prev_rate = rates[idx]
            invalid = (
                rate.limit <= prev_rate.limit or rate.interval <= prev_rate.interval
            )
            if invalid:
                msg = f"{prev_rate} cannot come before {rate}"
                raise InvalidParams(msg)

    def _init_buckets(self, identities) -> None:
        """Setup Queue for each Identity if needed
        Queue's maxsize equals the max limit of request-rates
        """
        for id in identities:
            if not self.bucket_group.get(id):
                maxsize = self._rates[-1].limit
                # print(self._bucket_args)
                self.bucket_group[id] = self._bkclass(
                    maxsize=maxsize,
                    identity=id,
                    **self._bucket_args,
                )

    def try_acquire(self, *identities) -> None:
        """Acquiring an item or reject it if rate-limit has been exceeded"""
        self._init_buckets(identities)
        now = int(time())

        for idx, rate in enumerate(self._rates):
            for id in identities:
                bucket = self.bucket_group[id]
                volume = bucket.size()
                
                if volume < rate.limit:
                    continue

                # Determine rate's time-window starting point
                start_time = now - rate.interval
                item_count, remaining_time = bucket.inspect_expired_items(start_time)

                if item_count >= rate.limit:
                    raise BucketFullException(id, rate, remaining_time)

                if idx == len(self._rates) - 1:
                    # We remove item based on the request-rate with the max-limit
                    bucket.get(volume - item_count)

        for id in identities:
            self.bucket_group[id].put(now)

    def ratelimit(
        self,
        *identities,
        delay: bool = False,
        max_delay: Union[int, float] = None,
    ):
        """A decorator that applies rate-limiting, with async support.
        Depending on arguments, calls that exceed the rate limit will either raise an exception, or
        sleep until space is available in the bucket.

        Args:
            identities: Bucket identities
            delay: Delay until the next request instead of raising an exception
            max_delay: The maximum allowed delay time (in seconds); anything over this will raise
                an exception
        """

        def ratelimit_decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    self.try_acquire(*identities)
                except BucketFullException as err:
                    delay_time = self._delay_or_reraise(err, delay, max_delay)
                    sleep(delay_time)

                return func(*args, **kwargs)

            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                try:
                    self.try_acquire(*identities)
                except BucketFullException as err:
                    delay_time = self._delay_or_reraise(err, delay, max_delay)
                    await asyncio.sleep(delay_time)

                return await func(*args, **kwargs)

            # Return either an async or normal wrapper, depending on the type of the wrapped function
            return async_wrapper if iscoroutinefunction(func) else wrapper

        return ratelimit_decorator

    @staticmethod
    def _delay_or_reraise(
        err: BucketFullException,
        delay: bool,
        max_delay: Union[int, float],
    ) -> int:
        """Determine if we should delay after exceeding a rate limit. If so, return the delay time,
        otherwise re-raise the exception.
        """
        delay_time = err.meta_info["remaining_time"]
        logger.info(
            f"Rate limit reached; {delay_time} seconds remaining before next request"
        )
        exceeded_max_delay = max_delay and (delay_time > max_delay)
        if delay and not exceeded_max_delay:
            return delay_time
        raise err

    def get_current_volume(self, identity) -> int:
        """Get current bucket volume for a specific identity"""
        bucket = self.bucket_group[identity]
        return bucket.size()

    # def get_filled_slots(self, rate, identity) -> List[int]:
    #     """ Get logged items in bucket for a specific identity
    #     """
    #     found_rate = next(
    #         (r for r in self._rates
    #          if r.limit == rate.limit and r.interval == rate.interval), None)

    #     if not found_rate:
    #         raise ValueError(f'Such rate {rate} is not found')

    #     if not self.bucket_group.get(identity):
    #         raise ValueError(f'Such identity {identity} is not found')

    #     bucket = self.bucket_group[identity]
    #     time_frame_start_point = int(time()) - rate.interval
    #     return [
    #         log_item for log_item in bucket.all_items()
    #         if log_item >= time_frame_start_point
    #     ]
