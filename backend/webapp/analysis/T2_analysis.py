import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as sco


from fastapi import APIRouter, Depends, HTTPException, FastAPI, Response, BackgroundTasks

from fastapi import File, UploadFile
import pandas as pd
import io

router = APIRouter(
    prefix="/analysis/T2",
    # tags=["myapp"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post('/T2_relexation/uploadfile', tags=["analysis"])
def upload_file( file: UploadFile, background_tasks: BackgroundTasks ):
    """
    Only can give one qubit analysis yet.
    """
    df_data = pd.read_csv(file.file)
    relaxation_time = df_data['<b>T2</b>'].to_numpy()
    relaxation_time /= 1e3
    iq_data = np.array([df_data['I'].to_numpy(),df_data['Q'].to_numpy()])
    
    print(relaxation_time.shape)
    # data = readfile(file.file)

    I1 = float(iq_data[0][0])
    Q1 = float(iq_data[1][0])
    I0 = float(iq_data[0][-1])
    Q0 = float(iq_data[1][-1])
    print(iq_data.transpose().shape)
    # xdata = project_line(I0, Q0, I1, Q1, iq_data.transpose())[:,0]/10**6
    ydata = project_line(I0, Q0, I1, Q1, iq_data.transpose(), relaxation_time.shape[0])
    print(ydata.shape)
    popt = T2_fitting(relaxation_time, ydata)
    img_buf = create_img( relaxation_time, ydata, popt)# , qubit_freq )

    background_tasks.add_task(img_buf.close)
    headers = {'Content-Disposition': 'inline; filename="out.png"'}
    return Response(img_buf.getvalue(), headers=headers, media_type='image/png')

def create_img( xdata, ydata, popt):

    """
    data type
    3 dim with shape (2*2*N)
    shape[0] is prepare state
    shape[1] is I and Q
    shape[2] is N times single shot
    
    """
    plt.rcParams['figure.figsize'] = [16.0, 8.0]
    plt.rcParams['figure.autolayout'] = True

    fig = plt.figure(constrained_layout=True)
    gs = fig.add_gridspec(1, 1)
    ax_iq_all = plt.subplot(gs[0, 0])
    ax_iq_all.set_title("Training data", fontsize=20  )
    ax_iq_all.tick_params(axis='both', labelsize=15)
    # ax_iq_all.tick_params(axis='y', labelsize=15)
    ax_iq_all.plot( xdata, ydata, "o" )
    ax_iq_all.plot(xdata,cos_expdecay(xdata,*popt), "-")
    # Output image
    img_buf = io.BytesIO()
    fig.savefig(img_buf, format='png')
    plt.close(fig)
    return img_buf

def cos_expdecay(x,a, b, c, d, e):
    #p: amp, tau, offset
    return a*np.cos(b*x+c)*np.exp(-x/d)+e

def readfile(s):
    #T1, I, Q
    t_I_Q = []
    f = open(s,"r")
    for line in f.readlines():
        line = line.strip()
        line = line.split(",")
        t_I_Q.append([line[0],line[1],line[2]])
    t_I_Q.remove(['<b>T1</b>', 'I', 'Q'])
    t_I_Q = np.array(t_I_Q)
    return t_I_Q
def project_line(I0, Q0, I1, Q1, t_I_Q, N):
    pro = []
    a = np.array([I1-I0,Q1-Q0])
    for i in range(N):
        b = np.array([[float(t_I_Q[i,0])-I0],[float(t_I_Q[i,1])-Q0]])
        c = np.dot(a,b)/((I1-I0)**2+(Q1-Q0)**2)**0.5
        pro.append(c[0])
    pro = np.array(pro)
    return pro
def T2_fitting(xdata, ydata):
    popt, pcov = sco.curve_fit(cos_expdecay, xdata, ydata)
    return popt