import codecs

from bs4 import BeautifulSoup

"""
allow google sheet html to be read offline for the member fund in operations
reading the google sheet
"""


class MemberNetworkTestCase:

    def __init__(self, read_html_file: str, test_amount: int, target_stop_at: str = "", vegas_credit_callback=None):
        self.lock_id = -1
        self.target_start_address = target_stop_at
        self.line_depo_amount = test_amount
        self.file = read_html_file
        self.fun_vegas_credit_callback = vegas_credit_callback
        self.functionAtLocation = target_stop_at is not ""

    def in_line_use(self, address: str, pri: str, up: str, down: str, index: int) -> bool:
        if up is "" or down is "":
            return True

        if self.functionAtLocation:
            if self.target_start_address is address:
                self.lock_id = index

            if index >= self.lock_id:
                if not self.fun_vegas_credit_callback(address, pri, self.line_depo_amount, down, up):
                    return False

            return False

        if not self.fun_vegas_credit_callback(address, pri, self.line_depo_amount, down, up):
            return False

    def readNetworkLines(self, callbackx=None) -> None:
        f = codecs.open(self.file, 'r')
        soup = BeautifulSoup(f, "lxml")
        tables = soup.find_all("table")
        index = 0
        for table in tables:
            tab_content = [[td.text for td in row.find_all("td")] for row in table.find_all("tr")]
            for li in tab_content:
                if index > 0:
                    add = li[0]
                    pri = li[1]
                    upline = li[2]
                    myline = li[3]

                    if callbackx is not None:
                        if callbackx(add, pri, upline, myline, index) is True:
                            break

                index = index + 1

    def Exec(self) -> None:
        self.readNetworkLines(self.in_line_use)
