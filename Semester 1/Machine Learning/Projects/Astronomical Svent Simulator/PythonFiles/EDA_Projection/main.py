from sklearn.metrics import mean_squared_error
from Preprocessing import handle_missing_values, load_data, perform_clustering, remove_some_columns
from Simulations_cpy import actual_orbit_simulates
# from clustering import perform_clustering
from utils import calculate_important_parameters, large_omega
# from sklearn.linear_model import LinearRegression
import pandas as pd
# import ast

file_path = 'csv/data_csv.csv'


# Load data
# data = load_data(file_path)
data = pd.read_csv(file_path)
print(data.shape)
keep_columns=['pl_name','ra','dec','pl_orbincl','pl_bmasse','pl_orbsmax','pl_orbeccen','pl_orblper','pl_orbper']
data=data[keep_columns]
print(data.shape)
data=data.dropna();planet_names=data['pl_name'];data=data.drop(['pl_name'],axis='columns')
data=data.dropna().astype(float)
data['pl_name']=planet_names.str.replace(" ","_")
data = large_omega(data)
print(data.shape)
data, clustering_data, kmeans, scaler = perform_clustering(data, n_clusters=7)
print(data.columns.tolist())
actual_orbit_simulates(data)
# # Plot clusters
# plot_clusters(data, kmeans, scaler)
# for vx, vy, vz in actual_orbit_simulates(data, 6):
#     print(len(vx), len(vy), len(vz))
# dts, mass_planet = calculate_important_parameters(data)
# print(mass_planet)
# dts.to_csv('csv/data_csv.csv', index=False)


# # Apply Multilinear Regression
# df=pd.read_excel('updated_training_data.xlsx')
# print(f"df.columns:{df.columns}")
# planet_names=df['pl_name'].to_list()

# unique_queue = set{}

# for i,name in df['pl_name']:
#     current_clusture=[]
#     planet_object=df['planetary'][i]
#     # nested_planet_names=planet_names
#     if planet_object in planet_names:
#         current_clusture.append(planet_object)
#         current_clusture.append(df['planetary'][i])
#         while 
#         planet_names.remove(planet_object);planet_names.remove(df['planetary'][i])
#         nested_planet_names=df['planetary'][i]

#         galaxy_objects=df['planetray'][i]


# for i, row in df.iterrows():
#     print(row['planetary'])
#     df['planetary'][i]=[str(df['planetary'][i]).strip("\"").strip("[").strip("]").split(",")]
#     print(f"df['planetary'][{i}]:{df['planetary'][i]}")
'''
galaxy_clustures=[]
for planet in df['pl_name']:
    current_clusture=set()
    pending_list=set()
    if planet in planet_names:
        pending_list.add(planet)
        while len(pending_list)>0:
            current_clusture.add(planet)
            print(f"df['pl_name']:{df['pl_name']}")
            print(f"df[df['pl_name']==planet].index:{df[df['pl_name']==planet].index}")
            # print(f"df.iloc[df[df['pl_name']==planet].index,'planetary']:{df.iloc[df[df['pl_name']==planet].index,'planetary']}")
            print(f"df['planetary'][{df[df['pl_name']==planet].index[0]}]:{df['planetary'][df[df['pl_name']==planet].index[0]]}")
            # current_clusture.add(df.iloc[df[df['pl_name']==planet].index,'planetary']);
            if type(df['planetary'][df[df['pl_name']==planet].index[0]]) == str:
                # current_clusture.add(df['planetary'][df[df['pl_name']==planet].index[0]]);
                current_clusture.add(ast.literal_eval(df['planetary'][df[df['pl_name']==planet].index]));
                pending_list.add(ast.literal_eval(df['planetary'][df[df['pl_name']==planet].index]));
                # pending_list.add(df['planetary'][df[df['pl_name']==planet].index[0]]);
            current_clusture.add(df['planetary'][df[df['pl_name']==planet].index[0]]);
            # current_clusture.add(ast.literal_eval(df['planetary'][df[df['pl_name']==planet].index[0]]));
            # pending_list.add(ast.literal_eval(df['planetary'][df[df['pl_name']==planet].index[0]]));
            pending_list.add(df['planetary'][df[df['pl_name']==planet].index[0]]);
            # pending_list.add(df['planetary'][df[df['pl_name']==planet].index[0]]);
            # pending_list.add(df.iloc[df[df['pl_name']==planet].index,'planetary']);
            # pending_list.add(df['planetary'][df['pl_name']==planet].index[0]);
            pending_list.remove(planet)
            planet=pending_list.pop()
    planet_names=[temp for temp in planet_names if temp not in current_clusture]
    # planet_names -= list(current_clusture)
    # planet_names.remove(list(current_clusture))
    galaxy_clustures.append(list(current_clusture))
    print(f"--------")
for i in range(len(galaxy_clustures)):
    print(f"galaxy_clustures[{i}]:{galaxy_clustures[i]}")
# print(f"----\ngalaxy_clustures:{galaxy_clustures}")
print(f"----\nlen(galaxy_clustures):{len(galaxy_clustures)}")
'''
'''
galaxy_clustures=[]
print(f"planet_names:{planet_names}")
for planet in df['pl_name']:
    # print(f"planet:{planet}")
    current_clusture=[]
    pending_list=[];useless_list=[]
    if planet in planet_names:
        pending_list+=[planet]
        # print(f"pending_list:{pending_list}")
        while len(pending_list)>0 and (planet in planet_names):
            current_clusture+=[planet]
            # print(f"type(df['planetary'][df[df['pl_name']==planet].index]):{type(df['planetary'][df[df['pl_name']==planet].index])}")
            # useless_list=[name for name in ast.literal_eval(df['planetary'][df[df['pl_name']==planet].index])]
            useless_list=[ast.literal_eval(name) for _,name in df['planetary'][df[df['pl_name']==planet].index].items()][0]
            # print(f"useless_list:{useless_list}")
            current_clusture+=useless_list;pending_list+=useless_list
            current_clusture=list(set(current_clusture));pending_list=list(set(pending_list))
            # current_clusture+=list(df['planetary'][df[df['pl_name']==planet].index]);
            # [current_clusture.append(name) for name in df['planetary'][df[df['pl_name']==planet].index]]
            print(f"current_clusture:{current_clusture}")
            try:
                pending_list.remove(planet)
            except ValueError:
                pass
            if len(pending_list)>0:planet=pending_list.pop()
            planet_names=[planet_name for planet_name in planet_names if planet_name not in current_clusture]
            if len(planet_names)==0:
                break
    galaxy_clustures.append(list(current_clusture));max_len=max([len(clusture) for clusture in galaxy_clustures])
    df_temp=pd.DataFrame({"clusture_"+str(i):galaxy_clustures[i]+[None]*(max_len-len(galaxy_clustures[i])) for i in range(len(galaxy_clustures)) if len(galaxy_clustures[i])>0})
    df_temp.to_csv("galaxy_clustures.csv",index=False)
    del df_temp
    
for i in range(len(galaxy_clustures)):
    print(f"galaxy_clustures[{i}]:{galaxy_clustures[i]}")

'''

'''
galaxy_clustures=[]
for planet in df['pl_name']:
    current_clusture=[]
    pending_list=[]
    if planet in planet_names:
        pending_list+=planet
        while len(pending_list)>0:
            current_clusture+=planet
            print(f"df['pl_name']:{df['pl_name']}")
            print(f"df[df['pl_name']==planet].index:{df[df['pl_name']==planet].index}")
            # print(f"df.iloc[df[df['pl_name']==planet].index,'planetary']:{df.iloc[df[df['pl_name']==planet].index,'planetary']}")
            print(f"df['planetary'][{df[df['pl_name']==planet].index}]:{df['planetary'][df[df['pl_name']==planet].index]}")
            # # current_clusture.add(df.iloc[df[df['pl_name']==planet].index,'planetary']);
            # if type(df['planetary'][df[df['pl_name']==planet].index]) == str:
            #     # current_clusture.add(df['planetary'][df[df['pl_name']==planet].index[0]]);
            #     # current_clusture+=ast.literal_eval(df['planetary'][df[df['pl_name']==planet].index]);
            #     current_clusture+=df['planetary'][df[df['pl_name']==planet].index[0]];
            #     pending_list+=df['planetary'][df[df['pl_name']==planet].index[0]];
            #     # pending_list+=ast.literal_eval(df['planetary'][df[df['pl_name']==planet].index]);
            #     # pending_list.add(df['planetary'][df[df['pl_name']==planet].index[0]]);
            current_clusture+=df['planetary'][df[df['pl_name']==planet].index];
            # current_clusture.add(ast.literal_eval(df['planetary'][df[df['pl_name']==planet].index[0]]));
            # pending_list.add(ast.literal_eval(df['planetary'][df[df['pl_name']==planet].index[0]]));
            pending_list+=df['planetary'][df[df['pl_name']==planet].index[0]];
            # pending_list.add(df['planetary'][df[df['pl_name']==planet].index[0]]);
            # pending_list.add(df.iloc[df[df['pl_name']==planet].index,'planetary']);
            # pending_list.add(df['planetary'][df['pl_name']==planet].index[0]);
            try:
                pending_list.remove(planet)
            except ValueError:
                pass
            planet=pending_list.pop()
    planet_names=[temp for temp in planet_names if temp not in current_clusture]
    # planet_names -= list(current_clusture)
    # planet_names.remove(list(current_clusture))
    galaxy_clustures.append(list(current_clusture))
    print(f"--------")
for i in range(len(galaxy_clustures)):
    print(f"galaxy_clustures[{i}]:{galaxy_clustures[i]}")
# print(f"----\ngalaxy_clustures:{galaxy_clustures}")
print(f"----\nlen(galaxy_clustures):{len(galaxy_clustures)}")
'''
'''
x=df[['x','y','z','vx','vy','vz','pl_bmasse']]
# print(f"x.columns:{x.columns}")
y=df[['ra','dec','pl_orbincl','pl_orbsmax','pl_orbeccen','pl_orblper','pl_orbper']]
split_ratio=0.8
x_train,x_test=x.iloc[:int(split_ratio*len(x)),:],x.iloc[int(split_ratio*len(x)):len(x),:]
y_train,y_test=y.iloc[:int(split_ratio*len(y)),:],y.iloc[int(split_ratio*len(y)):len(y),:]
model=LinearRegression()
model.fit(x_train,y_train)
y_pred=model.predict(x_test)
# print(y_pred)
mse = mean_squared_error(y_test,y_pred)
print(mse)

'''