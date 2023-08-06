#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/4 10:58
# @Author  : kiway
# @Software: PyCharm
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np

class InfProcess(BaseEstimator, TransformerMixin):

    def __init__(self, decimal, fillValue):
        self.decimal = decimal
        self.fillValue = fillValue


    def fit(self, X, y=None):

        return self

    def transform(self, X: pd.DataFrame):
        """fill all inf in X"""

        df = X.where(X != np.inf, 9999)
        df = df.applymap(lambda x: round(x, 4))

        return df