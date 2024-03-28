import pandas as pd
import pickle

def read_pickle_file(file):
  pickle_data = pd.read_pickle(file)
  
return pickle_data


pickle_data = pickle.load("/Volumes/Seagate Backup Plus Drive/plan_2014/comp/WTP RB/stochastic_full_rb.pickle")
tmp = pickle_data.iloc[0]
tmp = pd.DataFrame(data = tmp)

.iloc[]
