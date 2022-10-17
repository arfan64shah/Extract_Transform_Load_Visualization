#dashboad prt 8
#subset of the dashfired safety project
import pandas as pd
import datetime as dt
from datetime import timedelta
import matplotlib.pyplot as plt



df=pd.read_excel('dashboard.xlsx')
#1
totac=df.groupby('Date')['Outcome'].count()
print(totac)
totsuc=df[df['Outcome']=='Success'].groupby('Date')['Outcome'].count()
print(totsuc)
totnsuc=df[df['Outcome']=='Failure'].groupby('Date')['Outcome'].count()
print(totnsuc)
fig = plt.figure()

axes = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # left, bottom, width, height (range 0 to 1)

"""axes.plot(df['Date'].unique(), totac, 'r',label='Total')"""#who gurantees that order of index unique
#is the same as the groupby??????
"""axes.plot(df['Date'].unique(), totsuc, 'b')""" #if there is a date withput suc this will fail
#you need to use the dates from the actual totac  how usie the index
axes.plot(totac.index, totac, 'r',label='Total')
axes.plot(totsuc.index, totsuc, 'b',label='Success')
axes.plot(totnsuc.index, totnsuc, 'g',label='Failure')
"""axes.plot(totsuc.index, totsuc/totac, 'b')"""#this will fail because of difference of size
#you need to divide equal sozed vectors
dfsd=totac[totsuc.index]
axes.plot(totsuc.index, totsuc*100/dfsd, 'orange',label='ratio%')



axes.set_xlabel('Dates')
axes.set_ylabel('numbers')
axes.set_title('Action repport')
axes.legend(loc=2)
plt.show()

#what f we do it as scatter plot??
fig = plt.figure()

axes = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # left, bottom, width, height (range 0 to 1)

axes.plot(totac.index, totac,'r',ls='None',marker='o' ,label='Total')

axes.plot(totsuc.index, totsuc, 'b',ls='None',marker='+',label='Success')
axes.plot(totnsuc.index, totnsuc, 'g',ls='None',marker='s',label='Failure')

dfsd=totac[totsuc.index]
axes.plot(totsuc.index, totsuc*100/dfsd,'orange',ls='None', marker='1',label='ratio%')



axes.set_xlabel('Dates')
axes.set_ylabel('numbers')
axes.set_title('Action repport')
axes.legend(loc=2)
plt.show()
#b-----------------------------





totac=df.groupby('State')['Outcome'].count().reset_index()
print(totac)
totsuc=df[df['Outcome']=='Success'].groupby('State')['Outcome'].count().reset_index()
print(totsuc)
totnsuc=df[df['Outcome']=='Failure'].groupby('State')['Outcome'].count().reset_index()
print(totnsuc)
fig = plt.figure()

axes = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # left, bottom, width, height (range 0 to 1)

"""axes.plot(df['Date'].unique(), totac, 'r',label='Total')"""#who gurantees that order of index unique
#is the same as the groupby??????
"""axes.plot(df['Date'].unique(), totsuc, 'b')""" #if there is a date withput suc this will fail
#you need to use the dates from the actual totac  how usie the index
axes.bar(totac.State, totac.Outcome,label='Total')
axes.bar(totsuc.State, totsuc.Outcome,label='Success')
axes.bar(totnsuc.State, totnsuc.Outcome,label='Failure')
#OR use this from pandas!

dfm = pd.merge(totac, totsuc, on='State')
dfm=pd.merge(dfm, totnsuc, on='State')
dfm.plot.bar(x='State', logy=True)


axes.set_xlabel('Dates')
axes.set_ylabel('numbers')
axes.set_title('Action repport')
axes.legend(loc=2)
plt.show()

#C-----------------
a='Failure','Success'
print('here',df[df['Outcome']=='Success'].count())
input()
sizes=[df[df['Outcome']=='Success'].shape[0],df[df['Outcome']=='Failure'].shape[0]]
explode = (0, 0.1)  #get that slice out
fig1,ax1=plt.subplots()
ax1.pie(sizes,explode = explode,labels=a,autopct='%1.1f%%',shadow=True,startangle=90)
ax1.axis('equal')
plt.title('succes vs failure')
plt.show()


#D-------------------
dfm = pd.merge(totac, totsuc, on='State').fillna(0)
print(dfm)
input()
dfm['ratio']=dfm['Outcome_y']/dfm['Outcome_x']
print(dfm)
input()
best=dfm['ratio'].max()
print('best ratio is ',best)
best=dfm.loc[dfm['ratio'].idxmax()]
print('best state is',best)

#E----------------------
totac=df.groupby('State')['Outcome'].count()

totsuc=df[df['Outcome']=='Success'].groupby('State')['Outcome'].count()

fig, ax = plt.subplots(figsize=(12,6))
size = 0.3


ax.pie(totac.values.flatten(), radius=1,
       labels=totac.index,
       autopct='%1.1f%%',
       wedgeprops=dict(width=size, edgecolor='w'))

"""ax.pie(totsuc.values.flatten(), radius=1-size, 
       labels = totsuc.index,
       wedgeprops=dict(width=size, edgecolor='w'))"""

ax.set(aspect="equal", title='Pie plot with `ax.pie`')
plt.show()









