from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans


import time


# class GMM_model():

#     # def __init__( ):






# def gmm_defined_analytic(pyqum_path,samplename,df_local_csv=''):
#     pyqum = Load_pyqum(pyqum_path)
#     # loaded dataframe
#     df = pyqum.dataframe
#     # loaded jobid
#     jobid = pyqum.jobid
#     # Loaded R-JSON
#     rjson = pyqum.rjson()
#     key = list(df.select_dtypes('number').columns)
#     gmm_condition = ['ROF','ROL','XYF']
#     gmm_parameter = ['XYL','TOMO', 'TOMOR']
#     removable = ['RECORD-SUM','I','Q','Amp','UPhase']
#     [key.remove(i) for i in removable if i in key]
#     # [print('{:^15} : {:^6} to {:^6} * {:^5}'.format(i,df[i].min(),df[i].max(),df[i].nunique())) for i in key]
#     row = np.prod(df[key].nunique())
#     result = ['0','1','SNR','T(mk)']
#     gmm_condition_count = ['']*len(gmm_condition)
#     scroll = 0
#     tmp = gmm_condition.copy()
#     for index ,value in enumerate(tmp):
#         if value not in df:
#             if value not in rjson:
#                 gmm_condition.remove(value)
#                 scroll += 1
#                 gmm_condition_count.pop()
#             else:
#                 gmm_condition_count[index-scroll]  = 1
#         else:
#             gmm_condition_count[index-scroll] = df[value].nunique()
#     gmm_parameter_count = ['']*len(gmm_parameter)
#     scroll = 0
#     tmp = gmm_parameter.copy()
#     for index ,value in enumerate(tmp):
#         if value not in df:
#             if value not in rjson:
#                 gmm_parameter.remove(value)
#                 scroll += 1
#                 gmm_parameter_count.pop()
#             else:
#                 gmm_parameter_count[index-scroll]  = 1
#         else:
#             gmm_parameter_count[index-scroll] = df[value].nunique()
#     df_local_csv = DataFrame({key: [] for key in ['JOBID']+gmm_condition+gmm_parameter+result})
#     ground_index, excited_index = 0,-1
#     XYL_ground, XYL_excited = df['XYL'].unique()[ground_index],df['XYL'].unique()[excited_index]

#     time_start = time.time()
#     for i in range(prod(gmm_condition_count)):
#         print('\n')
#         gmm_status = unpack(i,gmm_condition_count)
#         train = df
#         status = ['']*len(gmm_condition)
#         for pos,label in enumerate(gmm_status):
#             if gmm_condition[pos] not in df:
#                 try:
#                     status[pos] = rjson[gmm_condition[pos]]
#                 except:
#                     print("There is no {} in R-JSON.".format(gmm_condition[pos]))
#                 if label == 'ROL':
#                     ROL=str(rjson[gmm_condition[pos]])
#             else:
#                 compare = df[gmm_condition[pos]].unique()[label]
#                 status[pos] = compare
#                 train = train[train[gmm_condition[pos]]==compare]
#                 if label == 'ROL':
#                     ROL=str(compare)
#         test = train
#         # ------- train -------
#         # if 'TOMO' in train:
#         #     train = train[train['TOMO']==0]
#         excited = train[train["XYL"]==XYL_excited]
#         ground = train[train["XYL"]==XYL_ground]
#         gmm, mark_gmm,data1,label1,data2,label2,SNR = gmm_analytic(train,excited,ground)
#         # S,N,SNR,SNR_dB = cal_SNR(gmm,change_label)
#         meas_condition = dict(zip(gmm_condition,status))
#         print(meas_condition)
#         title =''
#         for key,value in meas_condition.items():
#             title +='{:^3}_{:.4f} , '.format(key,float(value))
#         print_para = data1,label1,data2,label2,gmm.means_,gmm.covariances_,samplename,jobid \
#                                 ,mark_gmm,[XYL_ground,XYL_excited],title,float(meas_condition['XYF'])

#         gmm_plot_class(print_para)

#         # ------- test -------
#         for j in range(np.prod(gmm_parameter_count)):
#             data = test
#             predict_status = unpack(j,gmm_parameter_count)
#             status_index = ['']*len(gmm_parameter)
#             for pos,label in enumerate(predict_status): 
#                 try:
#                     compare = df[gmm_parameter[pos]].unique()[label]
#                     status_index[pos] = compare
#                     data = data[data[gmm_parameter[pos]]==compare]
#                 except ValueError:
#                         print("There is no {} in R-JSON.".format(label))
#             print("\t"+str(dict(zip(gmm_parameter,status_index))))
#             p0,p1 = gmm_predict(data,gmm,mark_gmm)
#             if dict(zip(gmm_parameter,status_index))['XYL'] == XYL_ground:
#                 T = cal_Tmk(p1,float(meas_condition['XYF']))
#             else:
#                 T = ''
#             df_local_csv.loc[len(df_local_csv)] =[jobid]+status+status_index+[p0,p1,SNR,T]
#     return df_local_csv,jobid
