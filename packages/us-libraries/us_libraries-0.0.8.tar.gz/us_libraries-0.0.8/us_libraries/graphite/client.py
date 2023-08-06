from typing import Dict, Optional

import graphyte


class Client:

    def __init__(self, url: str = 'graphite', interval: int = 60, prefix: Optional[str] = None):
        self.graphite = graphyte.init(url, prefix=prefix, interval=interval)

    def send(self, stats: str, value: int, tags: Optional[Dict] = {}) -> None:
        self.graphite.send(stats, value=value, tags=tags)
