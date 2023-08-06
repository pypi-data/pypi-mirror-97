import os
import json
import fnmatch
import requests
import socket
import time
import functools
import logging
from datetime import datetime, timedelta

from crc32c import crc32c  # pylint: disable=no-name-in-module


environment = os.environ.get("ENVIRONMENT", "dev")
STATSD_HOST = os.environ.get("STATSD_HOST", "localhost")
STATSD_PORT = int(os.environ.get("STATSD_PORT", "8125"))
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

logger = logging.getLogger(__name__)


def push_metrics(flag_name, identifier, active, enabled):
    identifier = identifier.replace(".", "_") or "empty"
    gated = 1 if enabled else 0
    message = f"feature_flags.[flag_name={flag_name},identifier={identifier},environment={environment},active={active}]gated:{gated}|c"
    sock.sendto(message.encode("utf-8"), (STATSD_HOST, STATSD_PORT))


def push_duration(duration_ms):
    message = f"feature_flags.[environment={environment}]duration:{duration_ms}|ms"
    sock.sendto(message.encode("utf-8"), (STATSD_HOST, STATSD_PORT))


def push_exception():
    message = f"feature_flags.[environment={environment}]exception:1|c"
    sock.sendto(message.encode("utf-8"), (STATSD_HOST, STATSD_PORT))


def timed_cache(**timedelta_kwargs):
    def _wrapper(f):
        update_delta = timedelta(**timedelta_kwargs)
        next_update = datetime.utcnow() + update_delta
        # Apply @lru_cache to f with no cache size limit
        f = functools.lru_cache(None)(f)

        @functools.wraps(f)
        def _wrapped(*args, **kwargs):
            nonlocal next_update
            now = datetime.utcnow()
            if now >= next_update:
                f.cache_clear()
                next_update = now + update_delta
            return f(*args, **kwargs)

        return _wrapped

    return _wrapper


class FeatureFlagClient:

    # bucket and folder names
    FF_BUCKET_NAME = os.environ.get("FF_BUCKET_NAME", "stitch-feature-flags")
    FF_PRIVATE = os.environ.get("FF_PRIVATE", "feature-flags-private")
    FF_PUBLIC = os.environ.get("FF_PUBLIC", "feature-flags")

    @timed_cache(seconds=60)
    def get_private_file_content(self):
        response = requests.get(
            f"https://stitch-feature-flags.s3.eu-central-1.amazonaws.com/{self.FF_PRIVATE}/{environment}.json"
        )
        flags_file_content = response.content.decode("utf-8")
        return json.loads(flags_file_content)

    @timed_cache(seconds=60)
    def get_public_file_content(self):
        response = requests.get(
            f"https://stitch-feature-flags.s3.eu-central-1.amazonaws.com/{self.FF_PUBLIC}/{environment}.json"
        )
        flags_file_content = response.content.decode("utf-8")
        return json.loads(flags_file_content)

    def check_is_active(self, flag, identifier):
        if not flag["active"]:
            return False

        is_whitelisted = any(
            fnmatch.fnmatch(identifier, pattern) for pattern in flag["whitelist"]
        )
        is_blacklisted = any(
            fnmatch.fnmatch(identifier, pattern) for pattern in flag["blacklist"]
        )

        return is_whitelisted and not is_blacklisted

    def is_experiment_active(self, flag, identifier):
        if not identifier:
            raise ValueError("identifier is required when using percentages")
        # We generate an arbitrary number between 0-99 based on the identifier
        calculated = crc32c(identifier.encode()) % 100
        # Any number from zero to "percentage" is visible; any number from
        # "percentage" to 99 is not visible
        return calculated < flag["percentage"]

    def is_enabled(self, flag_name, identifier=""):
        # This means the flag is active and the user is whitelisted and not blacklisted
        flag_active = False
        # If the flag doesn't have a percentage, this means the same as flag_active
        # If the flag does have a percentage, this means they are in the experimental
        # bucket (if true) or in the control bucket (if false)
        # This allows us to properly analyse the results of the A/B tests
        flag_enabled = False

        begin = time.time()
        try:
            private_flags_list = self.get_private_file_content()
            public_flags_list = self.get_public_file_content()

            flags_list = private_flags_list + public_flags_list

            for flag in flags_list:
                if flag["name"] == flag_name:
                    flag_active = self.check_is_active(flag, identifier)
                    if not flag_active:
                        flag_enabled = False
                    elif flag.get("percentage"):
                        flag_enabled = self.is_experiment_active(flag, identifier)
                        logger.info(
                            "flag: %s - enabled: %s", flag["name"], flag_enabled
                        )
                    else:
                        flag_enabled = True

                    break
        except Exception:  # pylint: disable=broad-except
            push_exception()
        finally:
            end = time.time()
            # duration in milliseconds
            push_metrics(flag_name, identifier, flag_active, flag_enabled)
            push_duration(int((end - begin) * 1000))
            return flag_enabled  # pylint: disable=lost-exception
