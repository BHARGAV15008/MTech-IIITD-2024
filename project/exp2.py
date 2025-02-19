import numpy as np
from sklearn.linear_model import LinearRegression 
from sklearn.metrics import mean_squared_error
import os
import pandas as pd
import matplotlib.pyplot as plt

def main_v1():
	dir_name="planet_evolution/"
	files=os.listdir(dir_name)
	print(f"files:{files}")
	use_files=files[0:10]
	df=pd.DataFrame();df_columns=[]
	for f_name in use_files:
		temp_df=pd.read_csv(dir_name+f_name,sep=",")
		df=pd.concat([df,temp_df],axis=1,ignore_index=True)
		df_columns+=temp_df.columns.to_list()
	df.columns=df_columns
	#print(f"df.shape:{df.shape}")
	#print(f"df.columns:{df.columns}")
	model=LinearRegression()
	use_samples=df.shape[0]-int(df.shape[0]/10)
	model.fit(df.iloc[0:use_samples-1,:],df.iloc[1:use_samples,:])
	total_error=0;err_list=[]
	for sample in range(use_samples,df.shape[0]-1,1):
		y=model.predict(df.iloc[sample:sample+1,:])
		#err=df.iloc[sample+1:sample+1,:]-y
		err=mean_squared_error(y,df.iloc[sample+1:sample+2,:])
		total_error+=err;err_list.append(total_error)
	print(model.coef_)
	err_list=[err_list[i]/(i+1) for i in range(len(err_list))]
	plt.plot(err_list)
	plt.savefig("results/planet_evolution_err.pdf")

if __name__=="__main__":
	main_v1()
