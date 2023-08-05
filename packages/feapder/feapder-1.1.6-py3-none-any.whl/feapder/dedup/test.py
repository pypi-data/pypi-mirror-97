# -*- coding: utf-8 -*-
'''
Created on 2019/9/17 4:31 PM
---------
@summary:
---------
@author: Boris
@email: boris@bzkj.tech
'''

from feapder.dedup import bitarray
import time
from feapder.dedup import Dedup

ba = bitarray.RedisBitArray('dedup:bloomfilter:bloomfilter0')

total = 0
for i in range(20):

    s= time.time()
    count = ba.count()
    print(type(count))
    e = time.time() - s

    print(count)
    print(e)

    total += e

print(total, total/20)

dedup = Dedup(filter_type=Dedup.BloomFilter)
datas=[1,2,3]
a = dedup.filter_exist_data(datas=datas)
print(datas)
print(a)

datas=[1,2,3, 4]
dedup.filter_exist_data(datas=datas)
print(datas)