#!/usr/bin/env python3
############################################################
## Jose F. Sanchez                                        ##
## Copyright (C) 2019-2020 Lauro Sumoy Lab, IGTP, Spain   ##
############################################################
"""
Maths functions used along ``BacterialTyper`` & ``XICRA`` pipeline.
"""
## useful imports
import re

#####################
def percentage(percent, whole):
    if (percent == "0.00%"):
        return 0

    percent_search = re.search(r"(.*)%", percent)
    if percent_search:
        percent_int = float(percent_search.group(1))
    value = (percent_int * whole) / 100.0
    return int(value)