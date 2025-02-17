import numpy as np
import pandas as pd
from Simulations_v2 import actual_orbit_simulates
from utils import large_omega
from os import sys
import re
import matplotlib.pyplot as plt

'''
This file creates the evolution form the obtained NASA dataframe
It's a one time use file.
Do note that you have to change the numbe rof planets in Simulation_v2.
'''


def main_v1():
	df=pd.read_csv("astrCsv.csv",sep=",",low_memory=False)
	#df=pd.read_csv("temp.csv",sep=",")
	'''
	nan_index=[]
	for i,name in enumerate(df["pl_bmasse"]):
		#print(f"name:{name},i:{i}")
		if str(name)=="nan":
			nan_index.append(i)
	df=df.drop(nan_index,axis='rows')
	'''
	keep_columns=['pl_name','ra','dec','pl_orbincl','pl_bmasse','pl_orbsmax','pl_orbeccen','pl_orblper','pl_orbper']
	df=df[keep_columns]
	df=df.dropna();planet_names=df['pl_name'];df=df.drop(['pl_name'],axis='columns')
	df=df.dropna().astype(float)
	df['pl_name']=planet_names.str.replace(" ","_")
	# create angular velocity
	print(f"df.columns:{df.columns},type(df):{type(df)}")
	df=large_omega(data=df,reference_ra=0,reference_dec=0);
	print(f"df.columns:{df.columns},df.shape:{df.shape}")
	df.to_csv("temp_data.csv")
	# get the data frame fro initial and final parameters
	#(x_list,y_list,z_list)=actual_orbit_simulates(data=df,cluster_idx=0)	# clusture_idex is not being used
	(pos_df)=actual_orbit_simulates(data=df,cluster_idx=0)	# clusture_idex is not being used
	print(f"pos_df.shape:{pos_df.shape},pos_df.columns:{pos_df.columns}")
	plot_galaxy(pos_df=pos_df)
	'''
	#print(f"x_list:{x_list},type(x_list):{type(x_list)}")
	print(f"x_list[0][0]:{x_list[0][0:]}")
	print(f"y_list[0][0]:{y_list[0][0:]}")
	print(f"z_list[0][0]:{z_list[0][0:]}")
	print(f"type(x_list):{type(x_list[0])}")
	print(f"len(x_list):{len(x_list)},len(y_list):{len(y_list)},len(z_list):{len(z_list)}")
	print(f"x_list.shape:{x_list.shape},y_list.shape:{y_list.shape},z_list.shape:{z_list.shape}")
	'''

def main_v2():
	df=pd.read_csv("../Astronomical Svent Simulator/astrCsv.csv",sep=",",low_memory=False)
	#df=pd.read_csv("temp.csv",sep=",")
	keep_columns=['pl_name','ra','dec','pl_orbincl','pl_bmasse','pl_orbsmax','pl_orbeccen','pl_orblper','pl_orbper']
	df=df[keep_columns]
	df=df.dropna();planet_names=df['pl_name'];df=df.drop(['pl_name'],axis='columns')
	df=df.dropna().astype(float)
	df['pl_name']=planet_names.str.replace(" ","_")
	# create angular velocity
	#print(f"df.columns:{df.columns},type(df):{type(df)}")
	df=large_omega(data=df,reference_ra=0,reference_dec=0);
	#print(f"df.columns:{df.columns},df.shape:{df.shape}")
	# get the data frame fro initial and final parameters
	(pos_df)=actual_orbit_simulates(data=df,cluster_idx=0)	# clusture_idex is not being used
	#print(f"pos_df.shape:{pos_df.shape},pos_df.columns:{pos_df.columns}")

def plot_galaxy(pos_df=pd.DataFrame):
	in_cols=list(pos_df.columns)
	print(f"in_cols:{in_cols}")
	print(f"in_cols[0]:{in_cols[0]}")
	col0=str(in_cols[0].split("_")[0])
	planet_names=list({str(in_cols[i].split("_")[0]) for i in range(len(pos_df.columns))})
	print(f"col0:{col0}")
	fig=plt.figure()
	ax=fig.add_subplot(projection='3d')
	no_planets=int(len(pos_df.columns)/3)
	for i,row in pos_df.iterrows():
		for j in range(len(planet_names)):
			ax.scatter(row[(3*j)+0],row[(3*j)+1],row[(3*j)+2],marker='o')
	#for x,y,z in zip(pos_df[col0+"_x"],pos_df[col0+"_y"],pos_df[col0+"_z"]):
	#	ax.scatter(x,y,z,marker='o')
	#ax.scatter(pos_df[col0+"_x"],pos_df[col0+"_y"],pos_df[col0+"_z"],marker='o')
	#plt.savefig("single_planet.pdf")
	plt.savefig("multi_planet.pdf")

if __name__=="__main__":
	main_v2()
