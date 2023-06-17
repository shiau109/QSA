
class read_sql_lab:
    def __init__(self,db_path):
        from sqlite3 import connect
        from pandas import read_sql
        
        conn = connect(db_path) #建立資料庫
        
        #透過SQL語法讀取資料庫中的資料
        # pd.read_sql(sql, con, index_col=None, coerce_float=True, params=None, parse_dates=None, columns=None, chunksize=None)
        self.job = read_sql("SELECT * FROM job", conn)
        self.user = read_sql("SELECT * FROM user", conn)[['id','username']]
        self.sample = read_sql("SELECT * FROM sample", conn)[['id','samplename','author_id','registered']]
        self.queue = read_sql("SELECT * FROM queue", conn)
        
    def list_samplename(self):
        self.tmp_samplelist = self.sample.sort_values(by = 'registered', ascending=False) 
        return list(self.tmp_samplelist['samplename'].unique())
    
    def update_list_samplename(self, keyword:str=None):
        if keyword == '' or keyword == None:
            return self.list_samplename()
        self.list_samplename()
        self.tmp_samplelist = self.tmp_samplelist[self.tmp_samplelist['samplename'].str.contains(keyword, na=False)]
        return list(self.tmp_samplelist.sort_values(by = 'registered', ascending=False)['samplename'].unique())

    def select_sample(self,samplename):
#         print("Selected the sample : "+samplename)
        select_sample_id = self.tmp_samplelist[self.tmp_samplelist['samplename']==samplename]['id'].iloc[0]
        return select_sample_id
    
    def list_time(self,samplename=''):
        try:
            sample_id = self.select_sample(samplename)
            return list(self.job[self.job['sample_id']==sample_id]['dateday'].unique())
        except:
            return list(self.job['dateday'].unique())
    
#     def update_list_time(self,keyword:str):
#         tmp = self.job[self.job['dateday'].str.contains(keyword.split(r'(')[0], na=False)]
#         return list(tmp.sort_values(by = 'id', ascending=True)['dateday'].unique())

    def jobid_search_pyqum(self,id:int):
        sample_id = self.job[self.job['id']==id]['sample_id'].iloc[0]
        queue_name = self.job[self.job['id']==id]['queue'].iloc[0]
        dateday = self.job[self.job['id']==id]['dateday'].iloc[0]
        task = self.job[self.job['id']==id]['task'].iloc[0]
        wmoment  = self.job[self.job['id']==id]['wmoment'].iloc[0]
        name_id = self.sample[self.sample['id']==sample_id]['author_id'].iloc[0]
        name = self.user[self.user['id']==name_id]['username'].iloc[0]
        sample_name = self.sample[self.sample['id']==sample_id]['samplename'].iloc[0]
        mission = self.queue[self.queue['system']==queue_name]['mission'].iloc[0]
        pyqum_path = r"C:\Users\ASQUM\HODOR\CONFIG\USRLOG\%s\%s\%s\%s\%s.pyqum(%d)"%(name,sample_name,mission,dateday,task,int(wmoment))
        print("Pyqum Path : ",pyqum_path)
        return pyqum_path,task