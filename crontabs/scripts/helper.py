#!/usr/bin/python
# -*- coding: UTF-8 -*-

from datetime import datetime, timedelta, timezone
from pathlib import Path
from time import sleep

import requests


def getbeijingtime():
    return datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")


class XSession(requests.Session):
    def __init__(self, log_path) -> None:
        super().__init__()
        self.log_path = log_path

    def request(self, method, url, *args, **kwargs):
        try:
            sleep(0.1)
            return super().request(method, url, *args, **kwargs)
        except Exception as e:
            with Path(self.log_path).open("a") as f:
                print("{} : {}".format(getbeijingtime(), str(e)), file=f)
            return requests.Response()
