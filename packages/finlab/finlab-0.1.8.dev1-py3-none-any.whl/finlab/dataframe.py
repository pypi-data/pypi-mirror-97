import os
import copy
import datetime
import numpy as np
import pandas as pd

import sys

class FinlabDataFrame(pd.DataFrame):

    @property
    def _constructor(self):
        return FinlabDataFrame

    @staticmethod
    def reshape(df1, df2):

        if isinstance(df2, pd.Series):
            df2 = pd.DataFrame({c:df2 for c in df1.columns})

        if isinstance(df2, FinlabDataFrame) or isinstance(df2, pd.DataFrame):
            index = df1.index | df2.index
            columns = df1.columns & df2.columns
            return df1.reindex(index=index,columns=columns, method='ffill'), \
            df2.reindex(index=index,columns=columns, method='ffill')
        else:
            return df1, df2

    def __lt__(self, other):
        df1, df2 = self.reshape(self, other)
        return pd.DataFrame.__lt__(df1, df2)

    def __gt__(self, other):
        df1, df2 = self.reshape(self, other)
        return pd.DataFrame.__gt__(df1, df2)

    def __le__(self, other):
        df1, df2 = self.reshape(self, other)
        return pd.DataFrame.__le__(df1, df2)

    def __ge__(self, other):
        df1, df2 = self.reshape(self, other)
        return pd.DataFrame.__ge__(df1, df2)

    def __eq__(self, other):
        df1, df2 = self.reshape(self, other)
        return pd.DataFrame.__eq__(df1, df2)

    def __ne__(self, other):
        df1, df2 = self.reshape(self, other)
        return pd.DataFrame.__ne__(df1, df2)

    def __sub__(self, other):
        df1, df2 = self.reshape(self, other)
        return pd.DataFrame.__sub__(df1, df2)

    def __add__(self, other):
        df1, df2 = self.reshape(self, other)
        return pd.DataFrame.__add__(df1, df2)

    def __mul__(self, other):
        df1, df2 = self.reshape(self, other)
        return pd.DataFrame.__mul__(df1, df2)

    def __truediv__(self, other):
        df1, df2 = self.reshape(self, other)
        return pd.DataFrame.__truediv__(df1, df2)

    def __rshift__(self, other):
        return self.shift(-other)

    def __lshift__(self, other):
        return self.shift(other)

    def __and__(self, other):
        df1, df2 = self.reshape(self, other)
        return pd.DataFrame.__and__(df1, df2)

    def __or__(self, other):
        df1, df2 = self.reshape(self, other)
        return pd.DataFrame.__or__(df1, df2)

    def average(self, n):
        return self.rolling(n, min_periods=int(n/2)).mean()

    def is_largest(self, n):
        return (self.fillna(self.min().min()).transpose().apply(lambda s:s.nlargest(n)).transpose().notna())

    def is_smallest(self, n):
        return (self.fillna(self.max().max()).transpose().apply(lambda s:s.nsmallest(n)).transpose().notna())

    def rise(self, n=1):
        return self > self.shift(n)

    def fall(self, n=1):
        return self < self.shift(n)

    def sustain(self, n):
        return self.rolling(n).sum() > 0

    def quantile(self, c):
        s = self.quantile(c, axis=1)
        return s

