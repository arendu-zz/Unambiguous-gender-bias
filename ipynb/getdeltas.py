import torch
import jsonlines as jsl
#import matplotlib.pyplot as plt
import csv
import pandas as pd
import numpy as np
#import seaborn as sns

import os
# import seaborn as sns
from nltk.corpus import stopwords
import random
import copy
import scipy
import glob

path='/private/home/adinawilliams/Projects/UnAmbiguousGender/Unambiguous-gender-bias/generated/xl/'

print(os.path.isdir(path))

fulldf=pd.DataFrame()
for m in ['m2m_100_1.2B','m2m_100_418M','mbart50_m2m','opus-mt']:
            genericfiles=glob.glob(path +'/'  + m + '/target.*.tok.analysis.context_npo_A')
            print(m)
            ful_res=pd.DataFrame()
            headliner=pd.DataFrame()
            for f in genericfiles:
                resultsfile=pd.read_csv(f, delim_whitespace=True, header=None, names=list(range(12)))
                headlineresult=resultsfile[[1,2,3,4,5]][0:1]
                headlineresult.insert(0, 'Language', f[-29:-27])
                result=pd.concat([resultsfile[[1,2,3,4,5]][9:11], resultsfile[[1,2,3,4,5]][19:21]])
                result.insert(0, 'Language', f[-29:-27])
                ful_res=pd.concat([ful_res, result])
                headliner=pd.concat([headliner, headlineresult])
            ful_res = ful_res[ful_res[5] != 1.0] # remove examples where translation didn't work
            headliner = headliner[['Language', 1,2,3]]
            headliner[headliner[3] != 1.00]
            ful_res.columns=['Language', 'Clue', 'Occupation', '%Correct', '%Wrong', '%N/A']
                # print(headliner)
            headliner.columns=['Language','%Correct', '%Wrong', '%N/A']

            listolang=[]
            listofdelt=[]
            listomdelt=[]
            for l in ful_res['Language'].unique():
                    # print(l)
                cluef = ful_res.loc[(ful_res['Language']==l) & (ful_res['Clue']=='CLUE_F')]
                cluem = ful_res.loc[(ful_res['Language']==l) & (ful_res['Clue']=='CLUE_M')]
                fdelt=cluef.loc[cluef['Occupation']=='OCC_F']['%Correct'].astype(float).values[0]-cluef.loc[cluef['Occupation']=='OCC_M']['%Correct'].astype(float).values[0] 
                mdelt=cluem.loc[cluem['Occupation']=='OCC_M']['%Correct'].astype(float).values[0]-cluem.loc[cluem['Occupation']=='OCC_F']['%Correct'].astype(float).values[0]
                listolang.append(l)
                listofdelt.append(fdelt)
                listomdelt.append(mdelt)

            deltadf=pd.DataFrame({'Language': listolang,'delta M': listomdelt, 'deltaF':listofdelt}, index=None).set_index('Language')
            fulldf=pd.concat([fulldf, deltadf], axis=1)
            print(['m2m_100_1.2B','m2m_100_418M','mbart50_m2m','opus-mt'])
            print('test')
            print(fulldf)
            print(fulldf.sort_index().to_latex(index=True))


