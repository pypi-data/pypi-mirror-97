#!/usr/bin/env python
# --------------------------------------------------------------------
# Copyright (c) iEXBase. All rights reserved.
# Licensed under the MIT License.
# See License.txt in the project root for license information.
# --------------------------------------------------------------------

# Here you can specify links to sites of different types.
# The default is verified links.
# If you do not know what links are used for, it is recommended not to change

from .providers.http import HttpProvider

DEFAULT_NODES = {
    "full_node": "https://api.trongrid.io",
    "solidity_node": "https://api.trongrid.io",
    "event_server": "https://api.trongrid.io"
}

CONF_MAINNET = {
    "full_node": "https://api.trongrid.io",
    "event_server": "https://api.trongrid.io",
    "solidity_node": "https://api.trongrid.io",
}

# The long running, maintained by the tron-us community
CONF_SHASTA = {
    "full_node": "https://api.shasta.trongrid.io",
    "event_server": "https://api.shasta.trongrid.io",
    "solidity_node": "https://api.shasta.trongrid.io",
    "faucet": "https://www.trongrid.io/faucet",
}

# Maintained by the official team
CONF_NILE = {
    "full_node": "https://api.nileex.io",
    "event_server": "https://event.nileex.io",
    "solidity_node": "https://api.nileex.io",
    "faucet": "http://nileex.io/join/getJoinPage",
}

# Maintained by the official team
CONF_TRONEX = {
    "full_node": "https://testhttpapi.tronex.io",
    "event_server": "https://testapi.tronex.io",
    "solidity_node": "https://testapi.tronex.io",
    "faucet": "http://testnet.tronex.io/join/getJoinPage",
}

ALL = {
    "default": CONF_MAINNET,
    "mainnet": CONF_MAINNET,
    "nile": CONF_NILE,
    "shasta": CONF_SHASTA,
    "tronex": CONF_TRONEX
}


def conf_for_name(name: str) -> dict:
    return ALL.get(name, None)


def to_providers_set(d: dict) -> dict:
    return dict(
        full_node=HttpProvider(d["full_node"]),
        solidity_node=HttpProvider(d["solidity_node"]),
        event_server=HttpProvider(d["event_server"])
    )
