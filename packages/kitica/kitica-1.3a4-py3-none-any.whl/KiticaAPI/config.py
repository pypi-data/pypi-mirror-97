# -*- coding: utf-8 -*-
#  _     _       _
# | |   (_)  _  (_)
# | |  _ _ _| |_ _  ____ _____
# | |_/ ) (_   _) |/ ___|____ |
# |  _ (| | | |_| ( (___/ ___ |
# |_| \_)_|  \__)_|\____)_____|
#
# kitica DevicePool API
# Created by    : Joshua Kim Rivera
# Date          : February 4 2020 14:55 UTC-8
# Company       : Spiralworks Technologies Inc.
#
import argparse
from KiticaAPI.utils import Constants, ConfigHelper


def config_parser():
    """ Parser Function.

    :return argparse.ArgumentParser Object
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-w",
                        "--whitelistip",
                        help="Whitelist IP.",
                        default=None
                        )
    parser.add_argument("-t",
                        "--teams",
                        help="Device Teams.",
                        default=None
                        )
    parser.add_argument("-db",
                        "--database",
                        help="Database Helper.",
                        default=None
                        )
    parser.add_argument("-del",
                        "--deletekey",
                        help="API Delete Key",
                        default=None
                        )
    return parser


def config():
    """
    Kitica Configuration Helper.

    :config-kitica
    """
    config = ConfigHelper()
    args = config_parser()
    options = args.parse_args()
    for option in options.__dict__:
        if eval('options.' + option) is not None:
            eval('config.' + option + '("' + str(eval('options.' + option)) + '")')
