# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 22:56:09 2021

@author: Suheda
"""

#1. kutuphaneler
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import numpy as np
# -*- coding: utf-8 -*-
import unicodecsv as csv
import csv

file_path=input("Enter file path:")
veriler = pd.read_csv(file_path)    
#veriler = pd.read_csv('Tumveri-son.csv')
m=input("Enter input columns from 1 to ")
m=int(m)
n=input("Enter output columns from  ")
n=int(n)
k=input("to ") 
k=int(k)
#data frame dilimleme (slice)
x = veriler.iloc[:,1:m]
y = veriler.iloc[:,n:k]

#NumPY dizi (array) dönüşümü
X = x.values
Y = y.values

y_preds=[]
degree=input("Enter the degree of the polynomial ")
degree=int(degree)
poly_reg = PolynomialFeatures(degree = degree)
for i in range(len(X)):
    data = pd.read_csv(file_path)   
    x_test,y_test=data.iloc[i,1:m],data.iloc[i,n:k]
    data=data.drop(i)
    x_train,y_train=data.iloc[:,1:m],data.iloc[:,n:k]
    x_poly = poly_reg.fit_transform(x_train)
    lin_reg = LinearRegression(fit_intercept=False)
    lin_reg.fit(x_poly,y_train.values.ravel())   
    coef = lin_reg.coef_
    names=poly_reg.get_feature_names()    
    sample = x_test.values.reshape(1,-1)
    sample = poly_reg.fit_transform(sample)
    ress = lin_reg.predict(sample) 
    y_preds.append(ress)

    

samples=[]
for count, samp in enumerate(sample):
    res = (coef*samp).sum()
    samples.append(samp)


i = 1
list1=[]
for (name,c) in zip(names,np.nditer(coef)):
    name +=" "+ "("+str(c)+")"
    new_name = name.replace("x0","B"+str(i)).replace("x1","C"+str(i)).replace("x2","D"+str(i)).replace("x3","E"+str(i)).replace("x4","F"+str(i)).replace(" ","*")
    new_name+="+"   
    list1.append(new_name)

list2=[]
list2.append(list1[-1][: -1])
list3 = list1[:-1]
list4 =list3+list2

denklem="'="+str(list4)
 

denklem=denklem.replace("'","").replace(",","").replace(".",",").replace("[","(").replace("]",")").replace(" ","")
print(denklem)

saving_path=input("Enter the model with the file name and extension you want to save:")
#example_path= C:/Users/Şuheda/Desktop/model.csv
import csv
with open(saving_path,'w',newline='',encoding='utf-8-sig') as f:
    w = csv.writer(f, delimiter=',')
    # Write Unicode strings.
   
    w.writerow([denklem])
    


