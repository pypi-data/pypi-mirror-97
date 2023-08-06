# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 09:31:45 2019

@author: DrEdC
"""

import pandas as pd
import numpy as np
import scipy.stats as st

def VR_test(data,periods=2,return_p=False,with_drift=True,assume_hete=True):
    """
    This method take a array-like data as input and perform variance ratio test according to Lo and MacKinlay's algorithem.The null hypothesis for the test is that the price data follow a random walk process.
    The test detects deviation from normal distribution incContinuously compounded asset returns by comparing estimated variances from different holding periods.
    This method allows array-like inputs for the choise of long-period variance and it returns the Z statistics or the p-values corresponding to each input.
    assume_hete is a robust option for stock prices exhibiting changing volatility over time
    with_drift option is insignificant for large sample
    """
    if isinstance(data,(pd.Series,np.ndarray,list)):
        P = pd.Series(data).astype(float).dropna() #the price series is assumed to be in ascending order
    else:
        raise ValueError ("only support data type of pd.Series, np.array, or list")
    if np.isscalar(periods):
        periods = [periods]
    N = len(P) #len of the price series
    n = N-1
    lr = (np.log(P) - np.log(P).shift(1)).dropna().values #one-period log return series 
    mu = (np.log(P.iat[-1]) - np.log(P.iat[0]))/n
    musq = (lr - mu)**2
    dmusq = musq.sum()
    va = dmusq/(n-1) #est for the one-period variance term
    
    result = [] #result place holder
    for ss in periods: #loop for all the selected return periods
        sub_slr = np.log(P)-np.log(P).shift(ss) #first ss terms are na
        if with_drift: #for small period returns such as daily returns the drift should be small and thus the difference is insignificant for large size n 
            dom = ss*(n-ss+1)*(1-ss/n)
        else:
            dom = ss*(n-ss+1)  
        vb = (((sub_slr - ss*mu)**2).sum())/dom #est for k-period return variance
        jb = vb/va
        if assume_hete:
            ta = pd.Series([(2*(ss-i))/ss for i in range(1,ss)])**2
            tb = pd.Series([(musq[j:]*np.roll(musq,j)[j:]).sum()/dmusq**2 for j in range(1,ss)])
            #return musq
            #print (musq[1+1:],np.roll(musq,1)[1+1:])
            dek = (ta*tb).sum()
        else:
            dek = 2*(2*ss-1)*(ss-1)/(3*ss*n)
        z = (jb-1)/np.sqrt(dek)
        result.append(z)
    if len(periods) == 1:
        if return_p:
            return 2*(1-st.norm.cdf(abs(result[0])))
        else:
            return result[0]
    else:
        if return_p:
            return_s = pd.Series(2*(1-st.norm.cdf(np.abs(result))),index=periods,name="p-values")
        else:
            return_s = pd.Series(result,index=periods,name="Z-stat")
        return_s.index.name = "periods"
        return return_s

def check_float(string):
    try:
        float(string)
        return True
    except:
        return False
    
def str2list(str_input,number=False,separator_list=[",",";"]):
    if str_input is None or str_input=="":
        return []
    if str_input[-1] not in separator_list:
        str_input += separator_list[0]
    return_list=[]
    temp_str=""
    for ch in str_input:
        if ch in separator_list:
            if temp_str.strip().isnumeric():
                return_list.append(int(temp_str.strip()))
            elif check_float(temp_str.strip()):
                return_list.append(float(temp_str.strip()))
            else:
                return_list.append(temp_str.strip())
            temp_str =""
        else:
            temp_str+=ch
    return return_list