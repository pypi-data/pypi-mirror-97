import codecs

import requests
from bs4 import BeautifulSoup

from tronpytool.compile.basetest import WrapContract


class Collector:
    """
    collection of new fees

    """
    matchnumbmarker = "1"
    tab_content = []
    DEMO_AMOUNT = 5000.00

    def __init__(self, marknumb: str, filename: str, network: str, master_wallet_address: str):
        self.list = []
        self.matchnumbmarker = marknumb
        self.file = filename
        self.network = network
        self.home_add = master_wallet_address

    def ConveyFund(self):
        f = codecs.open(self.file, 'r')
        soup = BeautifulSoup(f, "lxml")
        tables = soup.find_all("table")
        index = 0
        for table in tables:
            self.tab_content = [[td.text for td in row.find_all("td")] for row in table.find_all("tr")]

            for li in self.tab_content:
                if index > 0:
                    add = li[0]
                    pri = li[1]
                    operated = li[2]
                    if operated == self.matchnumbmarker:
                        self.assemblyAssets(add, pri, index)

                index = index + 1

    def assemblyAssets(self, address: str, priv: str, k: int):
        work_space = WrapContract(self.network)
        tronc = work_space.getNewTronClient(address, priv)

        try:
            tronc.trx.send_trx(self.home_add, self.DEMO_AMOUNT)
            print("processed address {} at {}".format(address, k))

        except ValueError as e:
            print("insufficient balance", e, k)

        except TypeError as e:
            print("insufficient balance", e, k)

        except requests.exceptions.Timeout as eg:
            # Maybe set up for a retry, or continue in a retry loop
            print("☯︎ request time out", eg)

        except requests.exceptions.ConnectionError as ef:
            # Maybe set up for a retry, or continue in a retry loop
            print("☯︎ request time out", ef)

        except requests.exceptions.TooManyRedirects as ep:
            # Tell the user their URL was bad and try a different one
            print("☯︎ too many requests now", ep)

        except requests.exceptions.HTTPError as eh:
            print("☯︎ http error is now", eh)
