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
    for i,x in enumerate(range(500)):
        d=x%360
        c=np.radians(d)
        y=math.sin(c)
        y=y*100
        y=y+random.normalvariate(0,10)
        #y=y*random.randint(0,120)
        y=abs(y)
        if i>0:
            prex=xs[i-1]
            prey=ys[i-1]
            print("i={} prex={} prey={}".format(i,prex,prey))
            xs.append(30)
            ys.append(y-prey)
        else:
            xs.append(30)
            ys.append(y)

        #msg="x={} y={}".format(x,y)
        #print(msg)
    #@df2=pd.DataFrame({'Y':ys},index=xs)
    #plt.plot(df2)
    #plt.show()
    return (xs,ys)
def gen_json(xs,ys):
    t=[dict(x=x,y=y) for (x,y) in zip(xs,ys)]
    outf=open('out2.json','wb')
    s=json.dumps(t)
    outf.write(s.encode('utf-8'))
    #print(s)
    outf.close()
def main():
    (xs,ys)=gen()
    gen_json(xs,ys)
if __name__=='__main__':main()
