#[alpha,falpha,Dq,Rsqr_alpha,Rsqr_falpha,Rsqr_Dq,muScale,Md,Ma,Mf]

import numpy as np
from scipy import stats

def chj(Timeseries,qValues,scales):
    """Run LEiDA Routine for BOLD signal.
    Args:

        Timeseries (ndarray): Signal vector. This function assumes that your time series 
        is all positive values (sigm transform it if needed).
        qValues (ndarray): Vector containing $q$ values. None of the $q$ can be between 0 and 1
        scales (ndarrray): Vector containing scales (dyadic).
    Returns:

        tuple:
            alpha: Holder exponent $\alpha$ vector of estimated spectrum,
            falpha: Hausdorff dimension $f(\alpha)$ vector of estimated spectrum,
            qValues: Vector containing $q$ values.
            Dq: Vector containing generalised dimensions $D_q$.
            Rsqr_alpha: $R^2$ values for each of the values in Holder exponent $\alpha$ vector.
            Rsqr_falpha: $R^2$ values for each of the values in Hausdorff dimension $f(\alpha)$ vector.
            Rsqr_Dq: $R^2$ values for each of the values in generalised dimensions $D_q$.


    References
    ----------
    .. [1] 
    Chhabra, A. and Jensen, R. V. (1989) ‘Direct determination 
    of the $f(\alpha)$ singularity spectrum’, Physical Review 
    Letters, 62(12), pp. 1327–1330. doi: 10.1103/PhysRevLett.62.1327.

    .. [2] 
    França, L. G. S. et al. (2018) ‘Fractal and Multifractal Properties 
    of Electrographic Recordings of Human Brain Activity: Toward Its Use 
    as a Signal Feature for Machine Learning in Clinical Applications’, 
    Frontiers in Physiology, 9(December), pp. 1–18. 
    doi: 10.3389/fphys.2018.01767.
    
    """

    ## initialise
    nq = qValues.shape[0]
    ns = scales.shape[0]
    Ma = np.zeros([nq,ns])
    Mf = np.zeros([nq,ns])
    Md = np.zeros([nq,ns])
        
    muScale = -np.log10(np.power(2,scales))
    #muScale=[muScale 0]
        
    alpha = np.zeros([nq,1])
    falpha = np.zeros([nq,1])
    Dq = np.zeros([nq,1])
        
    Rsqr_alpha = np.zeros([nq,1])
    Rsqr_falpha = np.zeros([nq,1])
    Rsqr_Dq = np.zeros([nq,1])

    ## calculating Ma_ij Mf_ij Md_ij
    for i in range(nq):
        
        q = qValues[i]

        for j in range(ns):
                
            # determine how many windows we will have at this scale
            window = 2**scales[j]
                
            # break the time series into windows & sum
            TimeseriesReshaped = np.reshape(Timeseries, (-1, window), order="F")
            TimeseriesSummed = np.sum(Timeseries)
                
            # calculate p
            ps = np.sum(TimeseriesReshaped, axis = 0)
            p = np.divide(ps,TimeseriesSummed)
                
                
            Nor = sum(np.power(p,q))
                
                
            # calculation of Md
            Md[i,j] = np.log10(Nor); # not accounting for q between 0 and 1
            
            if q<=1 and q>0:
                Md[i,j] = np.divide(sum(np.multiply(p,np.log10(p))),Nor)
                
                
            # Ma & Mf
            mu = np.divide((np.power(p,q)),Nor)
            Ma[i,j] = np.sum(np.multiply(mu,np.log10(p)))
            Mf[i,j] = np.sum(np.multiply(mu,np.log10(mu)))
            
            #looping through scales
            
            
        ## regression part
        slope, intercept, r_value, p_value, std_err = stats.linregress(muScale,Ma[i,:])
        b_Ma = slope
        R2_Ma = r_value
        slope, intercept, r_value, p_value, std_err = stats.linregress(muScale,Mf[i,:])
        b_Mf = slope
        R2_Mf = r_value
        slope, intercept, r_value, p_value, std_err = stats.linregress(muScale,Md[i,:])
        b_Md = slope
        R2_Md = r_value
            
        alpha[i] = b_Ma
        falpha[i] = b_Mf
        Dq[i] = np.divide(b_Md,(q - 1))
            
        if q<=1 and q>0: 
            Dq[i] = b_Md
            
            
        Rsqr_alpha[i] = R2_Ma
        Rsqr_falpha[i] = R2_Mf
        Rsqr_Dq[i] = R2_Md

    return alpha,falpha,Dq,Rsqr_alpha,Rsqr_falpha,Rsqr_Dq,muScale,Md,Ma,Mf
            
    #looping through qValues
