# coding=utf-8
#!/usr/bin/env python3

from shodan import Shodan, APIError
from libs.helpers import error, success
from ipaddr import IPAddress

class Web:
    def __init__(self, api_key):
        self.api_key = api_key
        self.last_search = {"matches":[], "total": 0}
        self.last_page = 1
    def search(self, query):
        try:
            success("Shodan'daki {}. sayfadan bot aranıyor!".format(self.last_page))
            api = Shodan(self.api_key)
            tmp = api.search(query, page=self.last_page)
            self.last_page = self.last_page + 1
            success("Liste indirildi")
            real_ips = []
            for zombie in tmp["matches"]:
                ip = IPAddress(zombie["ip_str"])
                if (str(ip.version) == "4"):
                    real_ips.append(zombie)

            self.last_search = {
                "matches": self.last_search["matches"] + real_ips,
                "total": self.last_search["total"] + len(real_ips)
            }

            return self.last_search
        except APIError as e:
            error(str(e))
            return False

web = Web(None)
