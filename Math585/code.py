from AlgorithmImports import *
import pandas as pd
import numpy as np
import math 
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint, adfuller

class FuturesAlgorithm(QCAlgorithm):

    def Initialize(self):

        # parameters
        self.trend_reversal = True  # default 
        self.long_order_size = 6
        self.short_order_size = 5
        self.sma_lookback = 12*7


        # self.SetStartDate(2022, 3, 1)
        # self.SetEndDate(2022, 10, 1)

        self.SetStartDate(2020, 12, 1)
        self.SetEndDate(2021, 12, 1)
        self.SetCash(1000000)

        self.future = self.AddFuture(Futures.Energies.CrudeOilWTI, Resolution.Hour)
        self.symbol = self.future.Symbol
        
        self.prices = []  

        self.future.SetFilter(timedelta(0), timedelta(182))

        # self.SetWarmUp(self.sma_lookback)

        seeder = FuncSecuritySeeder(self.GetLastKnownPrices)
        self.SetSecurityInitializer(lambda security: seeder.SeedSecurity(security))

        self.position = 0 
        self.count = 0
        self.open_port_values = []
        self.vars = []


    def OnData(self,slice: Slice) -> None: 

        chain = slice.FutureChains.get(self.symbol) 

        if chain: 

            relevant = sorted(chain, key = lambda x: x.Expiry, reverse = False)
            # df = pd.DataFrame([[x.Expiry, x.AskPrice, x.BidPrice] for x in relevant],
            #                             index=[x.Symbol.Value for x in relevant],
            #                             columns=['expiry', 'ask', 'bid'])

            # self.Log(str(df))

            adjusted_price = self.Securities[self.future.Symbol].Price 
            self.prices.append(adjusted_price) 

            if self.count % 8 == 0:
                port_value = self.Portfolio.TotalPortfolioValue
                self.open_port_values.append(port_value)
                if len(self.open_port_values) > 30:
                    last30_open = pd.Series(self.open_port_values[-30:])
                    last30_ret = last30_open.pct_change().dropna()
                    last30_std = np.std(last30_ret)
                    last30_mean = np.mean(last30_ret)
                    bottom1Normal = -2.3263
                    self.vars.append(last30_std * bottom1Normal + last30_mean)
                    self.Log(min(self.vars))
                    # self.Log(str(last30_std * bottom1Normal + last30_mean) + " Port Value " + str(port_value) + "  average: " + str(last30_mean) + " " + str(slice.Time))

            self.count += 1
            

            if len(self.prices) < self.sma_lookback:
                return 

            elif len(self.prices) == self.sma_lookback: 

                Y = pd.Series(self.prices) 
                X = pd.Series(np.ones(len(self.prices)))
                X = sm.add_constant(X)
                model = sm.OLS(Y,X)
                results = model.fit()
                res = results.resid 
                adf = adfuller(res)[1]
            
                if adf > 0.65: # then this is mean reverting 
                    self.trend_reversal = True 
                    self.Debug(f"Mean Reverting Detected") 
                elif adf < 0.65:
                    self.trend_reversal = False
                    self.Debug(f"Trend Following Detected") 

            sma_price = sum(self.prices[-self.sma_lookback:])/self.sma_lookback
            #self.Debug(f'future price = {adjusted_price}, sma = {sma_price}')

            most_recent = relevant[0]

            if self.trend_reversal:
                if self.position == 0: 
                    if sma_price > adjusted_price: 
                        self.MarketOrder(most_recent.Symbol, self.long_order_size) 
                        self.position = 1

                    elif sma_price < adjusted_price: 
                        self.MarketOrder(most_recent.Symbol, -self.short_order_size)
                        self.position = -1

                elif (self.position == 1 and adjusted_price > sma_price) or (self.position == -1 and adjusted_price < sma_price): 
                    self.Liquidate()
                    self.position = 0

            else:
                if self.position == 0: 
                    if sma_price < adjusted_price: 
                        self.MarketOrder(most_recent.Symbol, self.long_order_size) 
                        self.position = 1

                    elif sma_price > adjusted_price: 
                        self.MarketOrder(most_recent.Symbol, -self.short_order_size)
                        self.position = -1

                elif (self.position == 1 and adjusted_price < sma_price) or (self.position == -1 and adjusted_price > sma_price): 
                    self.Liquidate()
                    self.position = 0

