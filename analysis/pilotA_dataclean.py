import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import sys
import os
import glob
# this is based off of Tyler's analysis code in his first replication of this paper

def extract_data():
    # gets all filenames for subject data
    path = os.path.abspath("pilotA")
    sys.path.append(path)
    print(sys.path)
    # abs_path = "./data/pilotA/"
    subjectfiles = ["pilotA-rescue-251_1.csv", "pilotA-rescue-251_3.csv"]
    # for file in glob.glob("*pilotA-rescue-251_*.csv"):
    #     subjectfiles.append(file)
    #     print(file)
    
    # initialize data frame
    subject_trial_data = pd.DataFrame()
    
    # iterate over each subject (file)
    for filename in subjectfiles:
        # fullname = sys.path + filename
        df_curr = pd.read_csv (filename)
        print(df_curr)
        subject_trial_data = pd.concat([subject_trial_data,df_curr])
    
    return subject_trial_data # will return a pandas dataframe with all of the subjects data concatenated, where each row is a subject's trial
  
# extract and format data from database
data = extract_data()

# data['positive_key'] = np.nan
# data['negative_key'] = np.nan
# data['association'] = np.nan

# mapping = {'p':80, 'q':81, 'space':32}

# for i_subject in data.subject.unique(): 
#     for i_valence in ['positive', 'negative']: 
        
#         conditions = (data.subject==i_subject) * (data.valence==i_valence) * (data.condition=='instrumental')
#         # get the key value and map it to the numerical value
#         i_key = mapping[np.unique(data[conditions]['correct_response'])[0]]
        
#         # update subject valence-key mapping 
#         data['%s_key'%i_valence][data.subject==i_subject] = int(i_key)
        
# # save for later analysis
# data.to_csv('./data/pilotA/subject_data_pilotA_processed.csv')