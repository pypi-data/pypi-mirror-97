from heapapi import HeapAPIClient
import logging

PRODUCTION_HEAP_KEY = '540300130'
STAGING_HEAP_KEY = '3353132567'

PRODUCTION = "PRODUCTION"
LOCAL = "LOCAL"
DOMAINS = {
    PRODUCTION: "api.rasgoml.com",
    LOCAL: "localhost"
}


class BaseLogger(object):
    def track(self, event, identity=None, properities=None):
        raise NotImplementedError("Child class must implement")


class LocalLogger(BaseLogger):
    def __init__(self, user_profile: dict):
        self.logger = logging
        self.track(user_profile)

    def track(self, event, identity=None, properties=None):
        self.logger.info(f"Event logged: {event}, from identity: {identity}, add'l properties; {properties}")


class HeapLogger(BaseLogger):
    def __init__(self, user_profile: dict, hostname: str):
        if hostname == DOMAINS.get(PRODUCTION):
            self._heap_key = PRODUCTION_HEAP_KEY
        else:
            # Default to dev/staging account.
            self._heap_key = STAGING_HEAP_KEY

        self.logger = HeapAPIClient(self._heap_key)

        from pyrasgo.version import __version__
        self.event_properties = {"host": hostname,
                                 "version": __version__,
                                 "username": user_profile.get('username', None),
                                 "orgId": user_profile.get('orgId', None)
                                 }

    def track(self, event, identity=None, properties=None):
        try:
            logging.info("Tracking...")
            self.logger.track(identity=identity or "Unknown",
                              event=event,
                              properties={**self.event_properties,
                                          **properties} if properties else self.event_properties)
        except Exception:
            logging.info("No heap connection.")
