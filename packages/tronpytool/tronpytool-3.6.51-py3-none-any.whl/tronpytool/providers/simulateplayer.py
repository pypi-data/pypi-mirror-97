#!/usr/bin/env python
# coding: utf-8


import codecs
import json
import logging
import os
import random
import string
import time

from tronpytool import Tron
from tronpytool.compile.basetest import WrapContract
from tronpytool.trx import Trx

BAL = "balance"
PRI = "privkey"


class CoreSimulatePlayers:
    """Contract controller for players in game
    features:
    - binding invite code
    - check against existing binded addresses
    - holding private key and public key for internal testing
    - keep track of tron client for each wallet player
    """
    statement = 'End : {}, IO File {}'
    _contract_dict: dict
    _network: str
    FILE_CONTRACT = "backedup"
    ACTION_FOLDER = "deploy_results"
    COLLECTION_CONTRACTS = "players"
    GENESIS_INVITE_CODE = "DPXUS"
    GENESIS_UPLINE_CODE = "OOOOO"

    def __init__(self, network: str, workspace: str):
        self._contract_dict = dict()
        self._tron_clients = dict()
        self._workspace = workspace
        self._network = network
        """try to load up the file from the existing path"""
        try:
            self._contract_dict = json.load(codecs.open(self.playerAddrsFilePath(), 'r', 'utf-8-sig'))
            print("==== 🛄 data is prepared and the player metadata is now ready... ")
            self.preview_all_addresses()
            print("==== 🛄 End ==== ")
        except FileNotFoundError:
            print("==== 🛄 Setup new player list ==== ")
        except TypeError as e:
            print(e)

    def SetupByKeyKeep(self, wallet_addresses: dict) -> "CoreSimulatePlayers":
        if self.is_empty_data():
            for t in wallet_addresses:
                pub = t[0]
                priv = t[1]
                print("--> setup address for {}:".format(t))
                self.AppendInitPlayer(pub, priv)
            self.SaveMetaFile()
        return self

    def WithWrapper(self, contract_wrapper: WrapContract) -> "CoreSimulatePlayers":
        self.contract_wrapper = contract_wrapper
        return self

    def _writeFile(self, content, filename: str) -> None:
        fo = open(filename, "w")
        fo.write(content)
        fo.close()
        print(self.statement.format(time.ctime(), filename))

    def _storeTxDict(self, tx_result_data, filepath) -> None:
        self._writeFile(json.dumps(tx_result_data, ensure_ascii=False), filepath)

    @property
    def backupname(self) -> str:
        """preview the file name"""
        return self.FILE_CONTRACT

    @backupname.setter
    def backupname(self, filename: str) -> None:
        """the file name does not require extension name"""
        self.FILE_CONTRACT = filename

    @property
    def playermeta_data(self) -> str:
        return self.COLLECTION_CONTRACTS

    @playermeta_data.setter
    def playermeta_data(self, path: str) -> None:
        self.COLLECTION_CONTRACTS = path

    def getCachedBalance(self, addr: str) -> int:
        """example: TT67rPNwgmpeimvHUMVzFfKsjL9GZ1wGw8"""
        if addr in self._contract_dict:
            wallet_meta = self._contract_dict[addr]
            print("===> meta {}".format(wallet_meta))
            return int(wallet_meta[BAL])
        return 0

    def isAddressUnbinded(self, addr: str) -> bool:
        if addr in self._contract_dict:
            if "invitecode" in self._contract_dict[addr]:
                if len(self._contract_dict[addr]["invitecode"]) == 0:
                    return True
                else:
                    return False
        return False

    def getAllAddress(self) -> dict:
        return self._contract_dict

    def preview_all_addresses(self) -> None:
        print(self._contract_dict)

    def playerAddrsFilePath(self) -> str:
        return os.path.join(self._workspace, self.ACTION_FOLDER,
                            "{}.json".format(self.COLLECTION_CONTRACTS))

    def GetMetadataByAddr(self, address: str) -> dict:
        return self._contract_dict[address]

    def SaveMetaFile(self) -> "CoreSimulatePlayers":
        self._storeTxDict(self._contract_dict, self.playerAddrsFilePath())
        print("===✅ metafile saved. {}".format(self.playerAddrsFilePath()))
        return self

    def SyncBalances(self) -> "CoreSimulatePlayers":
        if len(self._contract_dict) > 0:
            for address in self._contract_dict:
                amount = self.GetTronModule(address).get_balance(address, False)
                self._contract_dict[address][BAL] = amount
                print("===✅ balance: {} trx --> {}".format(amount, address))
            self.SaveMetaFile()
        return self

    def AppendInitPlayer(self, address_wallet: str, private_key: str) -> "CoreSimulatePlayers":
        self._contract_dict[address_wallet] = dict(
            balance=0,
            upline="",
            invitecode="",
            privkey=private_key,
        )
        return self

    def GetTronModule(self, address: str) -> "Trx":
        return self.GetClientSelfTron(address).trx

    def GetClientSelfTron(self, address: str) -> "Tron":

        if not self.contract_wrapper:
            raise TypeError("contract wrapper is not found.. please use WithWrapper function")

        if address not in self._tron_clients:
            if address in self._contract_dict:
                wallet_keep = self._contract_dict[address]
                privatekey = wallet_keep[PRI]
                self._tron_clients[address] = self.contract_wrapper.getNewTronClient(address, privatekey)
                print("===✅ Tron client initiated for --> {}".format(address))

        return self._tron_clients[address]

    def set_code(self, key: str, address: str, code: str) -> None:
        if len(self._contract_dict) > 0:
            if address in self._contract_dict:
                if key in self._contract_dict[address]:
                    self._contract_dict[address][key] = code
                    print("🦑 -> {} code for {} -> {}".format(key, address, code))

    def has_code(self, key: str, address: str) -> bool:
        if len(self._contract_dict) > 0:
            if address in self._contract_dict:
                if key in self._contract_dict[address]:
                    return len(self._contract_dict[address][key]) > 0
        return False

    def NewMemberSetup(self, address: str, invite: str, upline: str) -> None:
        self.set_code("invitecode", address, invite)
        self.set_code("upline", address, upline)
        self.SaveMetaFile()

    def hasCode(self, address: str) -> bool:
        return self.has_code("invitecode", address) or self.has_code("upline", address)

    def NewInviteCode(self) -> str:
        return ''.join(random.sample(string.ascii_uppercase, 5))

    def is_empty_data(self) -> bool:
        return not len(self._contract_dict) > 0

    def GetMetaAddress(self, address: str) -> (str, str, str):
        if len(self._contract_dict) > 0:
            if address in self._contract_dict:
                uplinecode = self._contract_dict[address]["upline"]
                invitecode = self._contract_dict[address]["invitecode"]
                balance = self._contract_dict[address]["balance"]
                return invitecode, uplinecode, balance
        raise ValueError("address in meta is not found..")

    def PrintNewAccount(self):
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
        logger = logging.getLogger()
        tron = Tron().setNetwork("nile")
        account = tron.create_account()
        logger.debug('Generated account: ')
        logger.debug('- Private Key: ' + account.private_key)
        logger.debug('- Public Key: ' + account.public_key)
        logger.debug('- Address: ')
        logger.debug('-- Base58: ' + account.address.base58)
        logger.debug('-- Hex: ' + account.address.hex)
