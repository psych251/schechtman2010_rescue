import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import sys
import os
# this is based off of Tyler's analysis code in his first replication of this paper

def extract_data_pB():
    # get path to data folder
    path = os.path.abspath("data")
    sys.path.append(path)
    
    subjectfiles = ["/pilotB_testing/pilot-b-251-rescue_17.csv"]
    
    # concatenate all subjects data
    subject_trial_data = pd.DataFrame()
    for filename in subjectfiles:
        fullname = path + filename
        df_curr = pd.read_csv(fullname)
        print(df_curr)
        subject_trial_data = pd.concat([subject_trial_data,df_curr])
    
    # exclude columns that you don't need for the full analysis
    drop_cols = ["recorded_at","source_code_version","ip","user_agent","device","browser","browser_version","platform","platform_version","referer","accept_language","view_history"]
    for col in drop_cols:
        subject_trial_data.drop(col, inplace=True, axis=1)
    print(subject_trial_data)
    
    # clean the data
    # if correct_response is null that means its a random generalization trial?
    null_values = subject_trial_data['correct_response'].isnull()
    subject_trial_data['cr_is_null'] = null_values
    print("here are where the cr responses are null: ")
    print(subject_trial_data['cr_is_null']==True)
    
    null_pos_keys = subject_trial_data['positive_key'].isnull()
    subject_trial_data['no_pos_key'] = null_pos_keys
    
    # I updated this so that it says the positive_key in the original collected data I think
    # subject_trial_data['positive_key'] = np.nan
    # subject_trial_data['negative_key'] = np.nan
    # subject_trial_data['association'] = np.nan
    
    # if positive_key for the subject is p, then its the "first" association
    # mapping = {'p':80, 'q':81, 'space':32}
    associations = {'p':'first','q':'second'} # first means p is positive (80 is positive)
    key_map={} # maps subject to either first or second
    
    # iterate over each subject to get their key map
    subject_trial_data['key_press'].fillna(value='None',method=None,axis=0,inplace=True)
    responses_list = []
    for i_subject in subject_trial_data.run_id.unique():
        conditions = (subject_trial_data.run_id==i_subject) * (subject_trial_data['no_pos_key']==False) #  * (subject_trial_data.stage=='instrumental')
        temp_df = subject_trial_data[conditions] # gets all trials which are in the instrumental stage (during acquisition)
        
        # gets mapping from first trial (it will all be the same)
        # print(temp_df.iloc[0])
        key_map[i_subject] = associations[temp_df.iloc[0]['positive_key']]
        
        responses = {80:'negative',81:'positive',32:'neutral',None:None}
        if key_map[i_subject]=='first': 
            responses = {81:'negative',80:'positive',32:'neutral','None':'no_key',None:None}
        
        # print(subject_trial_data[subject_trial_data.run_id==i_subject])
        for _, row in subject_trial_data[subject_trial_data.run_id==i_subject].iterrows():
            val = row['key_press']
            print(val)
            if val in responses:
                responses_list.append(responses[val])
            else:
                responses_list.append('other_key')
    print(responses_list)
    subject_trial_data["responses"] = responses_list
    print(subject_trial_data["responses"]) # its negative, positive, neutral, no_key, or other_key 
    return subject_trial_data # will return a pandas dataframe with all of the subjects data concatenated, where each row is a subject's trial

cleaned_trial_data = extract_data_pB()
print(cleaned_trial_data)
  