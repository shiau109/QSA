from sqlite3 import connect
from pandas import read_sql, DataFrame


class read_sql_lab:
    def __init__(self,db_path,data_path):

        self.data_path = data_path
        conn = connect(db_path) #建立資料庫
        
        #透過SQL語法讀取資料庫中的資料
        # pd.read_sql(sql, con, index_col=None, coerce_float=True, params=None, parse_dates=None, columns=None, chunksize=None)
        self.job = read_sql("SELECT * FROM job", conn, dtype=str )
        self.user = read_sql("SELECT * FROM user", conn, dtype=str)[['id','username']]
        self.sample = read_sql("SELECT * FROM sample", conn, dtype=str)[['id','samplename','author_id','registered']]
        self.sample = self.sample.sort_values(by = 'registered', ascending=False) 
        self.queue = read_sql("SELECT * FROM queue", conn, dtype=str)
        self.list_samplename()
        
    def list_samplename(self):
        self.tmp_samplelist = self.sample
        return list(self.tmp_samplelist['samplename'].unique())
    
#     def update_list_samplename(self, keyword:str=None):
#         if keyword == '' or keyword == None:
#             return self.list_samplename()
        
#         self.tmp_samplelist = self.tmp_samplelist[self.tmp_samplelist['samplename'].str.contains(keyword, na=False)]
#         return list(self.tmp_samplelist.sort_values(by = 'registered', ascending=False)['samplename'].unique())

    def select_sample(self,samplename):
#         print("Selected the sample : "+samplename)
        select_filter = self.tmp_samplelist['samplename']==samplename
        select_sample = self.tmp_samplelist[select_filter]
        if len(select_sample.index) > 0:
            select_sample_id = select_sample['id'].iloc[0]
        else:
            select_sample_id = None
        return select_sample_id
    
    # def list_time(self, samplename=''):
    #     try:
    #         sample_id = self.select_sample(samplename)
    #         return list(self.job[self.job['sample_id']==sample_id]['dateday'].unique())
    #     except:
    #         return list(self.job['dateday'].unique())

    def get_job( self, jobid: str ):
        f_check, job_filter = self.__filter_check(self.job, "id", jobid)
        if f_check:
            return self.job.loc[job_filter]
        else:
            return None
#     def update_list_time(self,keyword:str):
#         tmp = self.job[self.job['dateday'].str.contains(keyword.split(r'(')[0], na=False)]
#         return list(tmp.sort_values(by = 'id', ascending=True)['dateday'].unique())
    def filter_job( self, column_name:str, term:str )->DataFrame:
        # sample_id = self.select_sample(term)
        
        sample_id = self.sample[self.sample["samplename"] == term]['id'].iloc[0]
        b_filter = self.job[column_name]==sample_id
        if b_filter.sum() > 0:
            filtered = self.job[ b_filter ]
        else:
            print("No result")
            filtered = None
        return filtered
    
    def __filter_check(self, df, column_name, term):
        b_filter = df[column_name]==term
        match_num = b_filter.sum()
        if match_num == 1:
            return True, b_filter
        elif match_num == 0:
            print(f"Can't find {term} in {column_name}")
            return False, b_filter
        else:
            print(f"{column_name} filter has problem")
            return False, b_filter
        
    def jobid_search_pyqum(self, jobid:str):
        # sample_id = self.job[self.job['id']==id]['sample_id'].iloc[0]
        


        

        f_check, job_filter = self.__filter_check(self.job, "id", jobid)

        if f_check:
            sample_id = self.job[job_filter]['sample_id'].iloc[0]
            f_check, sample_filter = self.__filter_check(self.sample, "id", sample_id)

        if f_check:
            name_id = self.sample[sample_filter]['author_id'].iloc[0]
            f_check, name_filter = self.__filter_check(self.user, "id", name_id)

        if f_check:
            queue_name = self.job[job_filter]['queue'].iloc[0]
            f_check, queue_filter = self.__filter_check(self.queue, "system", queue_name)

        if f_check:
            name = self.user[name_filter]['username'].iloc[0]
            sample_name = self.sample[sample_filter]['samplename'].iloc[0]
            mission = self.queue[queue_filter]['mission'].iloc[0]
            dateday = self.job[job_filter]['dateday'].iloc[0]
            task = self.job[job_filter]['task'].iloc[0]
            wmoment  = self.job[job_filter]['wmoment'].iloc[0]
        
            pyqum_path = f"%s\%s\%s\%s\%s\%s.pyqum(%d)"%(self.data_path,name,sample_name,mission,dateday,task,int(wmoment))
        else: 
            pyqum_path = None
            task = None
        print("Pyqum Path : ",pyqum_path)
        return pyqum_path