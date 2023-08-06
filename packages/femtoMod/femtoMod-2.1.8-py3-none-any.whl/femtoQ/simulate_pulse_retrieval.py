
#%% Import modules
import femtoQ.tools as fq               # Ez functions
import numpy as np                # Fast numerical operations
import matplotlib.pyplot as plt   # Plotting
from scipy.constants import c as C
from scipy.interpolate import interp1d as interp





def TwoDSI():
    
    #%% Set constants and recurrant functions
    C = 2.998e8                       # Speed of light
    pi = np.pi                        # Pi
    sqrt = lambda x: np.sqrt(x)       # Square root
    log = lambda x: np.log(x)         # Natural logarithm
    
    
    #%% Simulation parameters
    T = 10000e-15             # Time domain range. Higher values wield better frequency domain resolution
    dt = 0.05e-15              # Time increments. Lower values wield better time domain resolution
    
    lambda_1 = 0.5e-6         # Shortest wavelength to include in linear propagation calculations
    lambda_2 = 2e-6           # Longuest wavelength to include in linear propagation calculations
    
    #%% Physics parameters
    tau_FWHM = 8e-15         # Initial pulse duration, full width at half maximum
    lambda0 = 1300e-9         # Carrier wavelength of the pulse
    
    
    chirpingMaterials = ['SF11', 'SF68', 'BK7', 'ZnSe'] # Dispersive elements through which your pulse under study is propagating
    chirpingThicknesses = [ 0.00, 0.0 , 0.000 , 0.0000] # Dispersive materials thicknesses
    
    tdsiMaterial = ['SF11', 'SF68', 'BK7', 'ZnSe']  # Dispersive elements in the long pulse branch of 2DSI
    tdsiThicknesses = [ 0.00, 0.00, 2*2.54e-2+2e-3, 5e-3] # Dispersive materials thicknesses
    
    # Manual values of dispersidon, up to 4th order for now
    GDD = 0 * (1e-15)**2
    TOD = 0 * (1e-15)**3
    FOD =  0* (1e-15)**4
    
    #%% Setup parameters
    
    averageUpconvSpectrum = 1
    
    noiseLevel = 0.0 # Gaussian noise on the simulated spectrometer. Signal peaks at 1
    
    xSpectro = np.linspace(187e-9,1037e-9,2048) # Sampling points of the spectrometer, realistic values could be (187e-9,1037e-9,2048)
    
    ancillaType = "perfect" # Define source to use as ancilla (long pulse / monochromatic-like wave) use "real" to simulate dispersive arm, "perfect" for monochromatic waves
    shearFrequency = 3.5e12 # Shear to set when using "perfect" ancilla
    stageShearScanMinMax = [0e-6, 10e-6] # Min/max position of piezo stage. Values closer to 0 lead to lower shear with "real" ancilla. Width should be at least 3x your center wavelength
    stageTraceScanMinMax = [2e-6, 5e-6] # Min/max position of piezo stage. Values closer to 0 lead to lower shear with "real" ancilla. Width should be at least 3x your center wavelength
    traceNumberDataPoints = 200 # Number of data points to acquire during stage displacement from min to max value
    shearNumberDataPoints = 30 # Number of data points to acquire during stage displacement from min to max value
    
    # %% Quick calculations
    #Pulse parameters
    tau = tau_FWHM / sqrt(2*log(2)) # Gaussian pulse half width @ e^-2
    v0 = C/lambda0                  # Pulse's carrier frequency
    w0 = 2*pi*v0                    # Pulse's carrier angular frequency
    bandwidth = 0.44 / tau_FWHM     # Pulse's FWHM bandwidth
    
    # Time vector
    t = np.linspace(-T/2,T/2, round(T/dt) )
    
    # Time-domain electric field vector
    E = np.exp(1j * w0 * t) * np.exp(-  (t)**2 / (tau)**2)
    
    
    # Frequency domain e-field
    v,s = fq.ezfft(t,E, neg = True)
    
    #%% Dispersion of pulse under study
    
    # Add manual dispersion
    w = 2*pi*v
    s_abs = np.abs(s)
    s_phase = np.unwrap(np.angle(s))
    s_phase +=  (1/2 * GDD * (w-w0-2*pi*5e12)**2) + (1/6 * TOD * (w-w0)**3) + (1/24 * FOD * (w-w0)**4)
    s = s_abs * np.exp(1j*s_phase)
    t, E = fq.ezifft(v,s)
    
    # Add material dispersion
    for ii, material in enumerate(chirpingMaterials):
        L = chirpingThicknesses[ii]
        
        window = LinearWindow(material)
        
        n_sellmeier = window.get_n()
        
        
        
        #%% Fast fourier transform
        
        # v is freqnecy vector, s is frequency-domain electric field vector
        v,s = fq.ezfft(t,E, neg = True)
        
        
        #%% Dispersive propagation
        
        # Convert Sellmeier's equations cutoff wavelengths to frequencies
        v1 = C / lambda_2
        v2 = C / lambda_1
        
        # Convert frequencies within the equation's validity domain to wavelengths in um
        vtmp = v[( (v>v1) & (v<v2) )]
        lambdatmp = C / vtmp
        
        # Calculate refractive index for relevant frequencies
        ntmp = n_sellmeier(lambdatmp*1e6)
        
        # Generate refractive index vector n(v). Values outside of validity range are
        # set to zero.
        n = np.ones_like(v)
        n[( (v>v1) & (v<v2) )] = ntmp
        
        # Apply material's spectral phase to frequency domain electric field
        s[v!=0] = s[v!=0] * np.exp(1j * 2 * pi * n[v!=0] * (v[v!=0] / C) * L)
        
        # Finalpulse's spectral phase
        s_phase = np.unwrap(np.angle(s))
        
        #%% Inverse fast fourier transform
        
        # E2 is final time domain electric field vector, t2 is its corresponding time
        # vector. If all works as intended, t2 is equivalent to t at this point
        t2, E2 = fq.ezifft(v,s)
    
        E = E2
        t = t2   
        
    
    # Find final pulse's peak in time
    tpeak = np.mean( t[abs(E)**2 == np.nanmax(abs(E)**2)] )
    
    tExtended = np.concatenate((t-np.abs(np.min(t)) - np.max(t) - dt, t, t+np.abs(np.min(t)) + np.max(t) + dt), axis = 0 )
    
    EExtended = np.pad(E, E.shape, mode = 'wrap')
    
    
    # Shift time vector to get peak at t=0
    E = np.interp(t, tExtended-tpeak, EExtended)
    
    t2 = t
    E2 = E
    
        
    #%% Simulate 2DSI dispersive arm
    for ii, material in enumerate(tdsiMaterial):
        L = tdsiThicknesses[ii]
        
        window = LinearWindow(material)
        
        n_sellmeier = window.get_n()
        
        
        
        #%% Fast fourier transform
        
        # v is freqnecy vector, s is frequency-domain electric field vector
        v,s = fq.ezfft(t2,E2, neg = True)
        
        
        #%% Dispersive propagation
        
        # Convert Sellmeier's equations cutoff wavelengths to frequencies
        v1 = C / lambda_2
        v2 = C / lambda_1
        
        # Convert frequencies within the equation's validity domain to wavelengths in um
        vtmp = v[( (v>v1) & (v<v2) )]
        lambdatmp = C / vtmp
        
        # Calculate refractive index for relevant frequencies
        ntmp = n_sellmeier(lambdatmp*1e6)
        
        # Generate refractive index vector n(v). Values outside of validity range are
        # set to zero.
        n = np.ones_like(v)
        n[( (v>v1) & (v<v2) )] = ntmp
        
        # Apply material's spectral phase to frequency domain electric field
        s[v!=0] = s[v!=0] * np.exp(1j * 2 * pi * n[v!=0] * (v[v!=0] / C) * L)
        
        # Finalpulse's spectral phase
        s_phase = np.unwrap(np.angle(s))
        
        #%% Inverse fast fourier transform
        
        # E2 is final time domain electric field vector, t2 is its corresponding time
        # vector. If all works as intended, t2 is equivalent to t at this point
        t2, E2 = fq.ezifft(v,s)
        
        
    
    
    
    
    
    #%% Final pulse realignment
    
    # Find final pulse's peak in time
    tpeak = np.mean( t2[abs(E2)**2 == np.nanmax(abs(E2)**2)] )
    
    t2Extended = np.concatenate((t2-np.abs(np.min(t2)) - np.max(t2) - dt, t2, t2+np.abs(np.min(t2)) + np.max(t2) + dt), axis = 0 )
    
    E2Extended = np.pad(E2, E2.shape, mode = 'wrap')
    
    
    # Shift time vector
    E2 = np.interp(t2, t2Extended-tpeak, E2Extended)
    #t2 = t2 - tpeak
        
        
    #%% Initial/Final pulse FWHM duration
      
    #%% Instananeous frequency/wavelength calculations
    
    # Temporal phase
    phi_t = np.unwrap(np.angle(E2))
    
    # Instantaneous angular frequency
    w_inst = (phi_t[2:] - phi_t[:-2]) / (t2[2] - t2[0])
    
    
    #%% Plotting
    
    # Time domain initial/final pulse intensity
    figT = plt.figure()
    axT = figT.gca()
    axT.plot(t*1e15,np.abs(E)**2,'b', label = 'Initial')
    axT.plot(t2*1e15,np.abs(E2)**2,'--r', label = 'Final')
    axT.legend(loc = 'best')
    #axT.set_xlim(-3*max([tau1,tau2])*1e15,3*max([tau1,tau2])*1e15)
    axT.set_xlabel('Time [fs]')
    axT.set_ylabel('Intensity [arb. uni.]')
    
    
    # Spectrum (Intensity + Phase)
    figF = plt.figure()
    axFl = figF.gca()
    axFr = axFl.twinx()
    axFl.plot(v/1e12, np.abs(s)**2, 'b')
    axFr.plot(v/1e12, s_phase, 'r')
    axFl.set_xlim((v0-3*bandwidth)/1e12, (v0 + 3*bandwidth)/1e12)
    axFl.set_xlabel('Frequency [THz]')
    axFl.set_ylabel('Intensity [arb. uni.]', color = 'blue')
    axFr.set_ylim(np.min(s_phase[ ( np.abs(v-v0) < 3*bandwidth)  ]),np.max(s_phase[ ( np.abs(v-v0) < 3*bandwidth)  ]) )
    axFr.set_ylabel('Spectral phase [rad]', color = 'red')
    
    
    # Instantaneous frequency. Time intensity included for comparison
    figT = plt.figure()
    axTl = figT.gca()
    axTr = axTl.twinx()
    axTl.plot(t2*1e15,np.abs(E2)**2,'b')
    axTr.plot(t2[1:-1]*1e15, w_inst/(2*pi)/1e12 ,'r')
    #axTl.set_xlim(-2*tau2*1e15,2*tau2*1e15)
    axTr.set_ylim((v0-2*bandwidth)/1e12, (v0+2*bandwidth)/1e12)
    axTl.set_xlabel('Time [fs]')
    axTl.set_ylabel('Intensity [arb. uni.]', color = 'blue')
    axTr.set_ylabel(r'$\nu_{inst}$ [THz]', color = 'red')
    
    
    tau_sfg = 0e-6 / C 
    tau_cw_vec = np.linspace(stageTraceScanMinMax[0],stageTraceScanMinMax[1],traceNumberDataPoints) / C * 2
    tau_omega = 0e-6 / C 
    
    trace = np.zeros((tau_cw_vec.shape[0], xSpectro.shape[0]))
    
    E = E / np.max(np.sqrt(np.abs(E)**2))
    
    if ancillaType == "real":
        Ecw1 = E2 /  np.max(np.sqrt(np.abs(E2)**2)) 
        Ecw2 = E2 /  np.max(np.sqrt(np.abs(E2)**2))
    elif ancillaType == "perfect":
        Ecw1 = np.exp(1j*w0*t2) 
        Ecw2 = np.exp(1j*(w0+2*np.pi*shearFrequency)*t2)
        
        
    # =============================================================================
    # Ecw1 = E2 /  np.max(np.sqrt(np.abs(E2)**2)) #np.exp(1j*w0*t2) #
    # Ecw2 = E2 /  np.max(np.sqrt(np.abs(E2)**2)) #np.exp(1j*(w0+2*np.pi*2.45e12)*t2) #
    # =============================================================================
    
    for  ii, tau_cw in enumerate(tau_cw_vec):
        
        print(str(ii+1)+'/'+str(tau_cw_vec.shape[0]))
    
        E_short = np.interp(t,t+tau_sfg,E)
        
        E_omega = np.interp(t, t2+tau_omega, Ecw1)
        
        E_cw = np.interp(t, t2+tau_cw, Ecw2)
        
        #Etot = E + E2 + E3
        
        Esq = E_short*E_omega + E_short*E_cw
        
        
        nu, Esqnu = fq.ezfft(t,Esq)
        
        lamb = C/nu
        
        II = np.argsort(lamb)
        lamb = lamb[II]
        Esqlamb = Esqnu[II]
        
        trace[ii,:] = np.interp(xSpectro, lamb, np.abs(Esqlamb)**2) + np.random.normal(scale = noiseLevel, size = xSpectro.shape[0])
        
    trace = trace / np.max(trace)
    
    tau_cw_vec = np.linspace(stageShearScanMinMax[0],stageShearScanMinMax[1],shearNumberDataPoints) / C * 2
    
    
    shearSpectra = np.zeros((tau_cw_vec.shape[0], xSpectro.shape[0]))
    
    for  ii, tau_cw in enumerate(tau_cw_vec):
        
        
        E_short = np.interp(t,t+tau_sfg,E)
        
        E_omega = np.interp(t, t2+tau_omega, Ecw1)
        
        E_cw = np.interp(t, t2+tau_cw, Ecw2)
        
        #Etot = E + E2 + E3
        
        Esq = E_short*E_cw
        
        
        nu, Esqnu = fq.ezfft(t,Esq)
        
        lamb = C/nu
        
        II = np.argsort(lamb)
        lamb = lamb[II]
        Esqlamb = Esqnu[II]
        
        shearSpectra[ii,:] = np.interp(xSpectro, lamb, np.abs(Esqlamb)**2)+ np.random.normal(scale = noiseLevel, size = xSpectro.shape[0])
    shearSpectra = shearSpectra/np.max(shearSpectra)
    
    upconvSpectrum =np.interp(xSpectro,lamb, np.abs( fq.ezfft(t, E_short*E_omega )[1][II] )**2)+ np.random.normal(scale = noiseLevel, size = xSpectro.shape[0])
    
    for ii in range(averageUpconvSpectrum-1):
        upconvSpectrum += np.interp(xSpectro,lamb, np.abs( fq.ezfft(t, E_short*E_omega )[1][II] )**2)+ np.random.normal(scale = noiseLevel, size = xSpectro.shape[0])
    
    upconvSpectrum /= averageUpconvSpectrum
    
    
    upconvSpectrum = upconvSpectrum / np.max(upconvSpectrum)
    
    
    zShear = np.linspace(stageShearScanMinMax[0],stageShearScanMinMax[1],shearNumberDataPoints)*1e6
    zTrace = np.linspace(stageTraceScanMinMax[0],stageTraceScanMinMax[1],traceNumberDataPoints)*1e6
    
    
    plt.figure()
    plt.pcolor(xSpectro*1e9,zTrace,trace)
    
    
    
    plt.figure()
    plt.pcolor(xSpectro*1e9,zShear,shearSpectra)
    
    
    
    
    
    plt.figure()
    plt.plot(xSpectro*1e9,upconvSpectrum)
    
    
    
    
    np.savez('sim2dsiData', wavelengths = xSpectro*1e9, shearStagePosition = zShear, twoDSIStagePosition = zTrace,  upconvSpectrum = upconvSpectrum, shearTrace = shearSpectra, twoDSITrace = trace, timeVector = t, inputPulse = np.abs(E)**2/ np.max(np.abs(E)**2))

    return


def FROG():
    
    pulse = fq.Pulse(800e-9,5e-15,T=1000e-15,dt = 0.05e-15)
    pulse = pulse.disperse(dispVec=[-25,-50,500,2000])
    
    v0 = C/800e-9
    
    v, s = fq.ezfft(pulse.t,pulse.E,neg = True)
    
    s *= 0.2*(v-v0)/v0 -0.3*(v-v0)**2/v0**2
    
    pulse.t,pulse.E = fq.ezifft(v,s)
    
    pulse.E = pulse.E / np.max(np.abs(pulse.E))
    
    
    
    delays = np.linspace(-70e-15,70e-15,512)
    spectroX = np.linspace(300e-9,600e-9,512)
    
    noise_level = 0.1
    
    trace = np.zeros((len(delays),len(spectroX)))
    
    for ii,delay in enumerate(delays):
    
        delayedField = interp(pulse.t+delay,pulse.E,'quadratic',bounds_error=False,fill_value=0)
        pulse2 = fq.Pulse(t=pulse.t,E=delayedField(pulse.t))
        
        vtmp, shgV = fq.ezfft(pulse.t,pulse.E*pulse2.E)
    
        shgV = np.abs(shgV)**2
        interpSHG = interp(C/vtmp[-1::-1],shgV[-1::-1],'quadratic',bounds_error=False,fill_value=0)
        
        trace[ii,:] = interpSHG(spectroX)
        
    trace /= np.max(trace)
    trace += np.random.normal(0,noise_level,trace.shape)
    
    
    plt.figure()
    plt.plot(pulse.t*1e15,np.abs(pulse.E)**2 / np.max(np.abs(pulse.E)**2))
    plt.xlabel('Time [fs]')
    plt.ylabel('Normalized power')
    plt.xlim(-100,100)
    
    v, s = fq.ezfft(pulse.t,pulse.E)
    
    plt.figure()
    plt.plot(C/v*1e9,np.abs(s)**2 / np.max(np.abs(s)**2))
    plt.xlabel('Wavelength [nm]')
    plt.xlim(spectroX[0]*2e9,spectroX[-1]*2e9)
    plt.ylabel('Normalized power density')
    
    plt.figure()
    plt.pcolor(spectroX*1e9,delays*1e15,trace)
    plt.xlabel('Wavelength [nm]')
    plt.ylabel('Delay [fs]')
    c = plt.colorbar()
    c.set_label('Normalized power density')
    
    np.savez('simFROGData.npz',time = delays*1e15, wavelengths = spectroX*1e9, trace = trace)
    
    return




class LinearWindow:
    
    def __init__(self, material):
        
        self.material = material
        
        if   material.lower() == 'sf11':
            self.n = lambda x: (1+1.73759695/(1-0.013188707/x**2)+0.313747346/(1-0.0623068142/x**2)+1.89878101/(1-155.23629/x**2))**.5
        elif material.lower() == 'sf68':
            self.n = lambda x: (1+2.3330067/(1-0.0168838419/x**2)+0.452961396/(1-0.0716086325/x**2)+1.25172339/(1-118.707479/x**2))**.5
        elif material.lower() == 'bk7':
            self.n = lambda x: (1+1.03961212/(1-0.00600069867/x**2)+0.231792344/(1-0.0200179144/x**2)+1.01046945/(1-103.560653/x**2))**.5
        elif material.lower() == 'znse':
            self.n = lambda x: (1+3.00+1.90/(1-0.113/x**2))**.5
            
    def get_n(self):
        return self.n