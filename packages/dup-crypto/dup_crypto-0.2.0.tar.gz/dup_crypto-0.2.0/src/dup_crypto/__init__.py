from dup_crypto.libdup_crypto import *

__all__ = ["__title__", "__summary__", "__uri__", "__version__", "__author__", "__email__", "__license__", "__copyright__"]

__author__ = "elois <c@elo.tf>, Pascal Engélibert <tuxmain@zettascript.org>"
__copyright__ = "Copyright 2019-2021 {0}".format(__author__)
__license__ = "AGPL 3.0"
__summary__ = "Duniter Protocol cryptography"
__title__ = "DUP crypto"
__uri__ = "https://git.duniter.org/tuxmain/dup-crypto-py"
__version__ = "0.2.0"

keys.ed25519.Pubkey.__eq__ = keys.ed25519.Pubkey.__eq__
seeds.Seed32.__eq__ = seeds.Seed32.__eq__
