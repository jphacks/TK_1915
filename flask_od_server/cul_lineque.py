import random
from collections import deque


q = deque()
tenMinuteComer=0
for i in range(100):
   print(i)
   #最近1分間の来客数（とりあえず1~3のランダム）
   newcomer=random.randrange(1,4)
   #過去10分間の来客を足し上げる
   tenMinuteComer+=newcomer
   #過去10分間の来客を記録
   q.append(newcomer)
   if i > 9:
       tenMinuteComer-=q.popleft()#10分前のものを引く
   print(q)
   print("number of people who comes in past 10 mins"+str(tenMinuteComer))
   #1分当たりの来客数
   averageComer=tenMinuteComer/10
   #列の現在の客数（とりあえず5~7のランダム）
   linePerson=random.randrange(5,8)
   #待ち時間
   waitMinute=linePerson/averageComer
   print("que time"+str(waitMinute))