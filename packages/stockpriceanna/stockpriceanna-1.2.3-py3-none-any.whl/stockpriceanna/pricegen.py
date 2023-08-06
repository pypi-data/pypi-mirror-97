# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 20:17:06 2019
last_updated July 12 2020
@author: Dr.EdwC
"""
import pandas as pd
import datetime
import numpy as np
from statsmodels.tsa.stattools import adfuller
from stockpriceanna.utils import VR_test,str2list
import inspect
        
class _pricegen ():
    def __init__(self,start_price=100,time_index=None):
        """
        The pricegen class generates a simulated price series made of two components - the real and the noise. 
        The noise component has only an one-period effect on price while the real component has a permanent effect on price, 
        User can further specify a determinsitic trend factor and a decaying effect of random shock on stock prices, which creates artificial autocorrelation in returns. 
        The generated factor and noise components are stored in the self.data dataframe for analysis from an insider's view. 
        start_price set the starting price level
        time_index allows user to specify the Datetime Index of the generated prices if it is not specfied, the program use calendar business days
        """
        self.start_price = float(start_price)
        if time_index is not None:
            if not isinstance(time_index,pd.DatetimeIndex):
                raise ValueError ("pd.DatetimeIndex is required as the time_index input")
        self.time_index=time_index
        self.factor_list = []
        self.noise_list = []
        self.gen_note=0
        
    def _gen_timeindex(self,size,freq="D"):
        """
        an internal method for generating datetime index
        """
        if self.time_index is None:
            return pd.date_range(end=datetime.datetime.today().date(),periods=size,freq=freq)
        else:
            if len(self.time_index)<size:
                raise ValueError ("not enough observation in the time index")
            else:
                return self.time_index[-size:] 
    
    def _gen_datatable(self,size,backward=True):
        """
        an internal for generating the price data table
        """
        self.data = pd.DataFrame(index=self._gen_timeindex(size=size))
    
    def gen_sample(self,batch_size=1,with_time=True,with_rprice=False):
        """
        a data generator method. If only the with_time and with_rprice options are both off, this method returns the next batch of value or list. 
        If with_time optin is ON, this method return a batch of data series
        """
        if batch_size == 1:
            if self.gen_note>=self.data.shape[0]:
                return None
            if not with_time and not with_rprice:
                self.gen_note+=1
                return (self.data["price"].iat[self.gen_note-1])
            else:
                if with_time:
                    if not with_rprice:
                        return_t = self.data.loc[[self.data.index[self.gen_note]],["price"]]
                    else:
                        return_t = self.data.loc[[self.data.index[self.gen_note]],["price","price_r"]]
                    self.gen_note+=1
                    return (return_t)
                else:
                    self.gen_note+=1
                    return [self.data.at[self.data.index[self.gen_note-1],"price"],self.data.at[self.data.index[self.gen_note-1],"price_r"]]
        else:
            if self.gen_note+batch_size>self.data.shape[0]:
                return None
            else:
                if not with_time and not with_rprice:
                    self.gen_note+=batch_size
                    return (self.data["price"].iloc[self.gen_note-batch_size:self.gen_note].to_list())
                else:
                    if with_time:
                        if not with_rprice:
                            return_t = self.data.loc[self.data.index[self.gen_note]:self.data.index[self.gen_note+batch_size-1],["price"]]
                        else:
                            return_t = self.data.loc[self.data.index[self.gen_note]:self.data.index[self.gen_note+batch_size-1],["price","price_r"]]
                        self.gen_note+=batch_size
                        return (return_t)
                    else:
                        self.gen_note+=batch_size
                        return self.data.loc[self.data.index[self.gen_note-batch_size]:self.data.index[self.gen_note-1],["price","price_r"]].values
    
    def __check_name(self,name):
        if name in self.factor_list + self.noise_list:
            raise ValueError ("name %s already used in the factor/noise list" %(name))
    
    def gen_trend(self,rate=0.01,name=None,add_type="factor"):
        """
        This method generate the trend factor component for the prices
        """
        factor_name = "trend_r=%s" %(rate) if name is None else name
        self.__check_name(factor_name)
        self.data[factor_name] = (1+rate)
        if add_type == "factor":
            self.factor_list.append(factor_name)
        elif add_type=="noise":
            self.noise_list.append(factor_name)
        else:
            raise ValueError ("invalid add_type input value")   
            
    def gen_custom(self,func,name,var=None,add_type="factor",period_map=None):
        """
        This generates a new factor or noise using a customized function that may use lag values of a given variable as inputs
        e.g: a func = lambda l1,l2: (l1+l2)/2 if (l1-1)*(l2-2)>0 else 0 specifies a new factor/noise based on the values of lag1 and lag2 values 
        """
        if var is not None:
            if var not in self.factor_list + self.noise_list:
                raise ValueError ("var not found in the factor and noise lists")
        self.__check_name(name)
        arg_list = str2list(str(inspect.signature(func))[1:-1])
        if len(arg_list) !=0:
            if var is None:
                raise ValueError ("must provide the name of the variable from lag values are used for generating a new variable")
            lag_list = [int(x[1:]) for x in arg_list]
            max_lag = max(lag_list)
            for i in range(max_lag,self.data.shape[0]):
                apply_data = self.data[var].iloc[[i-lag for lag in lag_list]]
                apply_data.index = arg_list
                self.data.at[self.data.index[i],name] = func(**apply_data.to_dict())
        else:
            self.data[name] = [func() for i in range(self.data.shape[0])]
        if add_type == "factor":
            self.factor_list.append(name)
        elif add_type=="noise":
            self.noise_list.append(name)
        else:
            raise ValueError ("invalid add_type input value")       
        
    def gen_periodic(self,name,func,period,add_type="factor",var=None):  
        """
        This method generates a periodic factor/noise component on stock prices.
        User specifies a func takes the inputs of a periodic step key and optinally the sample-period value of a variable to determine the value of the component on each step.For            example:       
        d1.gen_periodic(name="2period_factor",func=lambda p: 1.01 if p==0 else 0.99,add_type="noise",period=2)
        
        generates a 2-step periodic noise.
        
        """
        self.__check_name(name)   
        for i in range(self.data.shape[0]):
            if var is None:
                self.data.at[self.data.index[i],name] = func(i%period)
            else:
                if var in self.data.columns:
                    self.data.at[self.data.index[i],name] = func(i%period,self.data.at[self.data.index[i],var])
                else:
                    raise ValueError ("var is not found in the data table")
        if add_type == "factor":
            self.factor_list.append(name)
        elif add_type=="noise":
            self.noise_list.append(name)
        else:
            raise ValueError ("invalid add_type input value")
                
    def gen_teffect(self,name,func,add_type="factor",var=None):
        """
        This method generates a time-effect component on stock prices.
        User specifies a func of time and return the effect value.
        example:
        d1.gen_teffect(name="Jan_effect",func=lambda t: 1.001 if t.month==1 else 1,add_type="factor")
        
        generates a January effect that boosts stock returns by a daily factor.
        
        """        
        self.__check_name(name)
        for i in range(self.data.shape[0]):
            if var is None:
                self.data.at[self.data.index[i],name] = func(self.data.index[i])
            else:
                if var in self.data.columns:
                    self.data.at[self.data.index[i],name] = func(self.data.index[i],self.data.at[self.data.index[i],var])
                else:
                    raise ValueError ("var is not found in the data table")        
        if add_type == "factor":
            self.factor_list.append(name)
        elif add_type=="noise":
            self.noise_list.append(name)
        else:
            raise ValueError ("invalid add_type input value")        
  
    def gen_ln(self,mean=0,std=0.01,name=None,add_type="factor",seed=None):
        """
        This method generates a log-normal return component that may be specifed as factor or noise
        """
        var_name = "ln_u=%s_v=%s" %(mean,std) if name is None else name
        self.__check_name(var_name)
        if seed is not None:
            np.random.seed(seed)
        self.data[var_name] = np.exp(np.random.normal(mean,std,self.data.shape[0]))
        if add_type == "factor":
            self.factor_list.append(var_name)
        elif add_type=="noise":
            self.noise_list.append(var_name)
        else:
            raise ValueError ("invalid add_type input value")      
    
    def gen_ac(self,base,rate=0.5,lag=1,name=None,add_type="factor"):
        """
        This method generate a auto-correlated factor based on a generated base factor (e.g. a random shock). 
        The rate input controls the rate of decay of the base-effect on subsequent returns
        The lag input controls how length of the base-factor impact on subsequent returns
        """
        
        if not isinstance(lag,int) or lag<1:
            raise ValueError ("invalid lag input")
        factor_name = "ac_b=%s_lag=%s" %(base,lag) if name is None else name
        self.__check_name(factor_name)
        if base not in self.data:
            raise ValueError ("base factor is not found")
        for i in range(1,self.data.shape[0]):
            temp_ = 0
            for l in range(1, min(lag+1,i+1)):
                temp_+= (rate**l)*(self.data.at[self.data.index[i-l],base]-1)
            self.data.at[self.data.index[i],factor_name] = (1+temp_)
        if add_type == "factor":
            self.factor_list.append(factor_name)
        elif add_type=="noise":
            self.noise_list.append(factor_name)
        else:
            raise ValueError ("invalid add_type input value")     
            
    def gen_price (self,method="m",factor_spec=None,price_filter=None,external_data=None):
        """
        This method generate the price series according to already specified factor and noise components.
        price = price_r + noise and price_r_t = price_r_t-1*(1+factor_t)
        price_filter allows users to further specify price effect after factor and noise
        external_data provides an interface for bringing in extra data that may be used in the price_filter function
        """
        
        self.data["price"] = self.data["price_r"] = self.start_price
        for i in range(1,self.data.shape[0]):
            temp_p = self.data.at[self.data.index[i-1],"price_r"]
            t = self.data.index[i]
            for f in self.factor_list:
                if  not pd.isnull(self.data.at[t,f]):
                    if factor_spec is not None and f in factor_spec.keys():
                        temp_m = factor_spec[f]
                    else:
                        temp_m = method
                    if temp_m == "m":  #multiplicate
                        temp_p = temp_p * self.data.at[t,f]
                    elif temp_m == "a": #additive
                        temp_p = temp_p + self.data.at[t,f]
                    else:
                        raise ValueError ("unsupported method for factor %s" %(f))
            self.data.at[self.data.index[i],"price_r"] = temp_p
                
            if len(self.noise_list)>0:
                for n in self.noise_list:
                    temp_noise = self.data.at[t,n]
                    if factor_spec is not None and n in factor_spec.keys():
                        temp_m = factor_spec[n]
                    else:
                        temp_m = method
                    if temp_m == "m":
                        if pd.isnull(temp_noise):
                            temp_noise = 1
                        temp_p = temp_p*temp_noise
                    elif temp_m == "a":
                        if pd.isnull(temp_noise):
                            temp_noise = 0
                        temp_p = temp_p + temp_noise
                    else:
                        raise ValueError ("unsupported method for noise %s" %(n))
            #now the filter effect
            self.data.at[t,"price"] = temp_p
            if price_filter is not None:
                self.data.at[t,"price"] = price_filter(price=self.data["price"].iloc[:i+1],external_data=external_data) 
                
    def show_price (self,show_rprice=False):
        """
        A method for returning generated price and price_r
        """
        if "price" not in self.data.columns or "price_r" not in self.data.columns:
            raise ValueError ("need to generate prices first")        
        if show_rprice:
            return self.data[["price","price_r"]]
        else:
            return self.data["price"]
          
    def plot(self,plot_rprice=False):
        if "price" not in self.data.columns or "price_r" not in self.data.columns:
            raise ValueError ("need to generate prices first")
        if plot_rprice:
            return self.data[["price","price_r"]].plot(x="time",y="price",title="simulated price chat")
        else:
            return self.data["price"].plot(x="time",y="price",title="simulated price chat")
            
    def unit_test(self,method="ADF",test_what="price",alpha=0.05):
        """
        this method conducts unit root test on a generated price series,return True if it test find significant evidence of rejecting non-stationary"
        notes: ADF null: a series has a unit root        
        """
        if test_what not in self.data.columns:
            raise ValueError ("test series is not available")
        if method=="ADF":
            result = adfuller(self.data[test_what])
        if result[1] < alpha:
            return True
        else:
            return False

    def RW_test(self,method="VR",test_what="price",alpha=0.05):
        """
        This provies a wapper of various external methods for testing random walk. Return True when evdience suggests random walk and False otherwise
        """
        if test_what not in self.data.columns:
            raise ValueError ("test series is not available")
        else:
            P = self.data[test_what]
            if method == "VR":
                result = VR_test(data=P,periods=range(2,10),return_p=True)
            if (result<alpha).sum()>0:
                return True
            else:
                return False
        
class spgen(_pricegen):
    def __init__ (self,start_price=100,time_index=None,size=1000):
        _pricegen.__init__(self,start_price=start_price,time_index=time_index)
        self._gen_datatable(size=size)
        
"""
test script
d1 = spgen(size=1000)  #specify the size of the simulation
d1.gen_ln(mean=0,std=0.01,seed=1,name="factor") #create a log-normal component as a factor
d1.gen_ln(mean=0,std=0.005,name="noise",add_type="noise",seed=2) #create a log-normal component as a noise
d1.gen_ac(base="factor",rate=0.2,lag=3,name="lag3_ac") #specify how previous shock to stock price decay overtime
d1.gen_trend(rate=0.0005,name="trend") #set a trend 
d1.gen_custom(func =lambda:(1+ 0.02*(np.random.rand()-0.5)),name="unit_noise",add_type="noise") #create another noise variable that follows unitform distribution
d1.gen_custom(func = lambda l1,l2: (l1+l2)/2 if (l1-1)*(l2-1)>0 else 1,var="unit_noise",name="mom_factor",add_type="factor") #create a momentum factor based on the lag values of the uniform noise
d1.gen_price(method="m") #generate the stock prices using multiplicative model
d1.gen_periodic(name="2period_factor",func=lambda p,var: 1.1*var if p==0 else 0.9*var,add_type="noise",period=2,var="noise") #generates a periodic filter that amplifier/reduce the base noise by 10% in cycle. 
d1.gen_teffect(name="Jan_effect",func=lambda t: 1.001 if t.month==1 else 1,add_type="factor") #generates a January effect that boosts stock returns by a daily factor.
d1.show_price(show_rprice=True).tail(10)

#using moving average as a resistence level
def MA5_filter(price,*args,**kargs):
    if price.size>5:
        temp_ma_lag = price.iloc[-6:-1].mean()
        temp_ma = price.iloc[-5:].mean()
        if price.iat[-2]>=temp_ma_lag and price.iat[-1]<temp_ma and price.iat[-1]>temp_ma*0.99:
            return price.iloc[-5:-1].mean()
        else:
            return price.iat[-1]
    else:
        return price.iat[-1]

t1 = spgen(size=100)
t1.gen_ln(mean=0,std=0.02,seed=1,name="factor")
t1.gen_price(price_filter=MA5_filter)
t1.data["price_MA5"] = t1.data["price"].rolling(5).mean()
"""