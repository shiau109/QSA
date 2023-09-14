from resonator_tools.circuit import notch_port
# from .electronic_delay import *
import scipy.io
import pandas as pd
from scipy.optimize import curve_fit 
import numpy as np
import matplotlib.pyplot as plt


def cavityQ_fit( freq:np.ndarray, s21:np.ndarray, power:np.ndarray=None ):

    # Fit part
    fitParas = []
    fitCurves = []
    with_power = False
    dep_num = s21.shape[0]
    print(f"Dimen {freq.shape} {s21.shape}")
    if type(power) != type(None):
        with_power = True
        print("get power input")
        if type(power) != float:
            np.full(dep_num, power)
    
    if s21.ndim == 1:
        s21 = np.array([s21])

    for xi in range(dep_num):
        freq_fit = freq
        iq_fit = s21[xi]
        myResonator = notch_port()        

        # try:
            # print("auto fitting")
            #delay, params =myResonator.get_delay(freq_fit,iq_fit)
            # myResonator.autofit(electric_delay=mydelay)

        delay, amp_norm, alpha, fr, Ql, A2, frcal =\
                myResonator.do_calibration(freq_fit,iq_fit, fixed_delay=None)
        myResonator.z_data = myResonator.do_normalization(freq_fit,iq_fit,delay,amp_norm,alpha,A2,frcal)

        myResonator.fitresults = myResonator.circlefit(freq_fit,myResonator.z_data,fr,Ql)
        myResonator.z_data_sim = myResonator._S21_notch(
            freq_fit,fr=myResonator.fitresults["fr"],
            Ql=myResonator.fitresults["Ql"],
            Qc=myResonator.fitresults["absQc"],
            phi=myResonator.fitresults["phi0"],
            a=amp_norm,alpha=alpha,delay=delay)
        fit_results = myResonator.fitresults
        fit_results["A"] = amp_norm
        fit_results["alpha"] = alpha
        fit_results["delay"] = delay
        if with_power:
            fit_results["photons"] = myResonator.get_photons_in_resonator(power[xi])
        fitCurves.append(myResonator.z_data_sim)
            
        # except:
        #     print(f"{xi}th Fit failed")
        
        fitParas.append(fit_results)
    df_fitParas = pd.DataFrame(fitParas)

    
    chi = df_fitParas["chi_square"].to_numpy()
    # Refined fitting

    # min_chi_idx = chi.argmin()
    # print(df_fitParas["alpha"].to_numpy())
    # print(np.unwrap( df_fitParas["alpha"].to_numpy(), period=np.pi))
    # weights = 1/chi**2
    # fixed_delay = np.average(df_fitParas["delay"].to_numpy(), weights=weights)
    # fixed_amp = np.average(df_fitParas["A"].to_numpy(), weights=weights)
    # fixed_alpha = np.average(np.unwrap( df_fitParas["alpha"].to_numpy(), period=np.pi), weights=weights)
    
    # fixed_delay = df_fitParas["delay"].to_numpy()[min_chi_idx]  
    # fixed_amp = df_fitParas["A"].to_numpy()[min_chi_idx]  
    # fixed_alpha = df_fitParas["alpha"].to_numpy()[min_chi_idx] 
      
    
    return df_fitParas, fitCurves

def find_row( file_name, colname, value ):

    df = pd.read_csv( file_name )
    searchedArr = df[[colname]].values
    idx = (np.abs(searchedArr - value)).argmin()
    #print( searchedArr[idx] )
    return df.iloc[[idx]]

def tan_loss(x,a,c,nc):
    return (c+a/(1+(x/nc))**0.5)

def fit_tanloss( n, loss, loss_err ):
    upper_bound = [1,1,1e4]
    lower_bound = [0,0,0]
    
    min_loss = np.amin(loss)
    max_loss = np.amax(loss)

    p0=[max_loss-min_loss,min_loss,0.1]
    try:
        popt, pcov = curve_fit(tan_loss, n, loss,sigma=loss_err**2, p0=p0, bounds=(lower_bound,upper_bound))
        p_sigma = np.sqrt(np.diag(pcov))
    except:
        popt = [0,0,0]
        p_sigma = [0,0,0]
    results_dict = {
        "A_TLS": [popt[0]],
        "const": [popt[1]],
        "nc": [popt[2]],
        "A_TLS_err": [p_sigma[0]],
        "const_err": [p_sigma[1]],
        "nc_err": [p_sigma[2]],
    }
    results = pd.DataFrame(results_dict)

    return results
    #paras[cav]={"fr (GHz)":float(int(cav[1:])/10000),"TLS":popt[0],"Const.":popt[1],"Nc":popt[2]}
