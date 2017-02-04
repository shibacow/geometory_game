#!/usr/bin/env python
# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import math
import random
import json
import numpy as np
import pandas as pd

def gen():
    xs=[]
    ys=[]
    for x in range(500):
        d=x%360
        c=np.radians(d)
        y=math.sin(c)
        y=y*random.randint(0,120)
        y=abs(y)
        #xs.append(x*30)
        #ys.append(y)
        #msg="x={} y={}".format(x,y)
        #print(msg)
    #df2=pd.DataFrame({'Y':ys},index=xs)
    #plt.plot(df2)
    #plt.show()

def main():
    gen()
if __name__=='__main__':main()
