#!/usr/bin/env python3
import os,sys

import pandas as pd
import numpy as np

def __WR (data, t, cl='Close'):
    highh = data["High"].rolling(t).max()
    lowl  = data["Low"].rolling(t).min()
    close = data[cl]

    data['WR_{}'.format(t)] = -100 * ((highh - close) / (highh - lowl))
    return data


