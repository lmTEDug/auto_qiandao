#!/usr/bin/python
# -*- coding: UTF-8 -*-

from base64 import b64decode
from pathlib import Path

import helper


class Signer:
    proxies = {
        "http": "http://127.0.0.1:10809",
        "https": "http://127.0.0.1:10809"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
    }
    log_path = "logs/dailysignin.txt"

    @classmethod
    def log(cls, site, msg):
        with Path(cls.log_path).open("a", encoding="utf8") as f:
            print("{} : {} : {}".format(helper.getbeijingtime(), site, msg), file=f)

    @classmethod
    def jike0_com(cls, useproxies=False):
        # prepare
        s = helper.XSession(cls.log_path)
        s.headers = cls.headers
        if useproxies:
            s.proxies = cls.proxies

        # login
        username = 851962636@qq.com
        password = plmoknlm12333
#         username = b64decode(b"").decode("utf8") # 填用户名
#         password = b64decode(b"").decode("utf8") # 填密码
        res = s.post(
            "https://jike0.com/auth/login",
            data={"email": username, "passwd": password, "code": ""}
        )
        if res.status_code != 200 or res.json().get("ret") != 1:
            return (False, "Failed to login.")

        # sign in
        res = s.post("https://jike0.com/user/checkin")
        if res.status_code != 200 or res.json().get("ret") != 1:
            return (False, "Failed to sign in.")

        # logout
        res = s.get("https://jike0.com/user/logout")
        if res.status_code != 200:
            return (True, "Failed to logout.")

        return (True, "Success!")

    @classmethod
    def run(cls):
        """Run all sign in tasks"""
        _, msg = cls.jike0_com()
        cls.log("jike0.com", msg)


if __name__ == "__main__":
    Signer.run()
