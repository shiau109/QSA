import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as sco


from fastapi import APIRouter, Depends, HTTPException, FastAPI, Response, BackgroundTasks

from fastapi import File, UploadFile
import pandas as pd
import io

router = APIRouter(
    prefix="/analysis/T1",
    # tags=["myapp"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post('/T1_relexation/uploadfile', tags=["analysis"])
def upload_file( file: UploadFile, background_tasks: BackgroundTasks ):
    """
    Only can give one qubit analysis yet.
    """
    df_data = pd.read_csv(file.file)
    relaxation_time = df_data['<b>T1</b>'].to_numpy()
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
    ydata = project_line(I0, Q0, I1, Q1, iq_data.transpose())
    print(ydata.shape)
    img_buf = create_img( relaxation_time, ydata)# , qubit_freq )

    background_tasks.add_task(img_buf.close)
    headers = {'Content-Disposition': 'inline; filename="out.png"'}
    return Response(img_buf.getvalue(), headers=headers, media_type='image/png')


def create_img( xdata, ydata):

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
    popt, pcov = sco.curve_fit(expdecay, xdata, ydata)
    ax_iq_all.plot(xdata,expdecay(xdata,*popt), "-")
    # Output image
    img_buf = io.BytesIO()
    fig.savefig(img_buf, format='png')
    plt.close(fig)
    return img_buf


def expdecay(x,a, b,c):
    #p: amp, tau, offset
    return a*np.exp(-x/b)+c

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
def project_line(I0, Q0, I1, Q1, t_I_Q):
    pro = []
    a = np.array([I1-I0,Q1-Q0])
    for i in range(101):
        b = np.array([[float(t_I_Q[i,0])-I0],[float(t_I_Q[i,1])-Q0]])
        c = np.dot(a,b)/((I1-I0)**2+(Q1-Q0)**2)**0.5
        pro.append(c[0])
    pro = np.array(pro)
    return pro
def data_project():
    return

if __name__ == "__main__":
    a = readfile("1DSingle_Qubit.csv")
    I1 = float(a[0,1])
    Q1 = float(a[0,2])
    I0 = float(a[100,1])
    Q0 = float(a[100,2])
    xdata = project_line(I0, Q0, I1, Q1, a)[:,0]/10**6
    ydata = project_line(I0, Q0, I1, Q1, a)[:,1]
    # print(xdata)
    plt.plot(xdata,ydata)


    popt, pcov = sco.curve_fit(expdecay, xdata, ydata)
    print(popt)
    plt.plot(xdata,expdecay(xdata,*popt))
    plt.show()
