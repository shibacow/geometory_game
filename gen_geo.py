#!/usr/bin/env python
# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import math
import random
import json
import numpy as np
import pandas as pd

def gen_building():
    xs=[]
    ys=[]
    for i,x in enumerate(range(500)):
        d=x%360
        c=np.radians(d)
        y=math.sin(c)
        y=y*100
        y=y+random.normalvariate(0,120)
        y=abs(y)
        ys.append(y)
        xs.append(x*30)
        ys.append(y)
        xs.append((x*30)+30)

        #sg="x={} y={}".format(x,y)
        #print(msg)
    #df2=pd.DataFrame({'Y':ys},index=xs)
    #plt.plot(df2)
    #plt.show()

    return (xs,ys)
def gen_json(xs,ys):
    t=[dict(x=x,y=y) for (x,y) in zip(xs,ys)]
    outf=open('out4.json','wb')
    s=json.dumps(t)
    outf.write(s.encode('utf-8'))
    #print(s)
    outf.close()






def main():
    #(xs,ys)=gen_building()
    #gen_json(xs,ys)
if __name__=='__main__':main()
