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
# Date          : September 23 2020 15:16 UTC-8
# Company       : Spiralworks Technologies Inc.
#
from .configurations import Configurations


class ConfigHelper(Configurations):
    """
    Kitica Configuration Helper.
    """
    def __init__(self):
        super().__init__()
        print('Kitica API Configuration Helper.\n')

    def __del__(self):
        print('\nbye!...')
