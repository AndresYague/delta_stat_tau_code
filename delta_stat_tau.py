import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.lines as lines
import numpy as np
import matplotlib

n_draws = int(1e5)  # Total number of draws
Tgal = 8500  # Myr

# ESS values and uncertainties
ESS_I_avg = 1.28e-4
ESS_Cm_avg = 5.6e-5
ESS_Pu_avg = 0.4
sig_I = 0.03e-4*0.5
sig_Cm = 0.3e-5*0.5

# Generate all ESS values
ESS_I = np.random.normal(ESS_I_avg, sig_I, n_draws)
ESS_Cm = np.random.normal(ESS_Cm_avg, sig_Cm, n_draws)

# We do not put the factor of 2 because is very ugly
#ESS_I = np.random.uniform(ESS_I_avg*1/2, ESS_I_avg*2, size = n_draws)
#ESS_Cm = np.random.uniform(ESS_Cm_avg*1/2, ESS_Cm_avg*2, size = n_draws)

# K values for uranium
#     low   best   high
#u235  1.2   1.4    2.0
#u238  1.5   1.9    4.1

# Define K array (min, best, max):
k_I = np.array((1.6, 2.3, 5.7))
#k_Cm = np.array((1.1, 1.2, 1.8)) # Old values
k_Cm = np.array((1.2, 1.4, 2.0)) # New values

# Parameters for deltas array
delt0 = 70
deltlast = 1400
step = 7

#function for the I129/I127
def normal(deltas, pr, kk, tau, ESS, elem, Tgal):
    pp = 47.7

    septime_best=[]
    plus_2_sig = []
    minus_2_sig = []

    # Go for each delta in the array deltas, previously calculated
    for delta in deltas:
        if elem =='I':
            mm = pr * delta / Tgal * kk
        elif elem =='Cm':
            mm = pr * kk * (1 - np.exp(-delta / 1009))

        septs_min = -np.log(ESS/mm[0]) * tau
        septs_best = -np.log(ESS/mm[1]) * tau
        septs_max = -np.log(ESS/mm[2]) * tau

        septime_best.append(np.mean(septs_best))

        # Get all the possible 2_sigmas
        f = lambda x: np.percentile(x, 50 + pp)
        plus = max(f(septs_min), f(septs_best), f(septs_max))
        plus_2_sig.append(plus)

        f = lambda x: np.percentile(x, 50 - pp)
        minus = min(f(septs_min), f(septs_best), f(septs_max))
        minus_2_sig.append(minus)

    septime_best = np.array(septime_best) * 1e-6  # In Myrs
    plus_2_sig = np.array(plus_2_sig) * 1e-6  # In Myrs
    minus_2_sig = np.array(minus_2_sig) * 1e-6  # In Myrs

    return septime_best, plus_2_sig, minus_2_sig

# Define the deltas array
deltas = np.arange(delt0, deltlast + 1, step)

# Define the taus
avg_I = 15.7; sig_I = 0.4
tau_I = np.random.normal(avg_I, sig_I, size = n_draws) / np.log(2) * 1e6

avg_Cm = 15.6; sig_Cm = 0.5
tau_Cm = np.random.normal(avg_Cm, sig_Cm, size = n_draws) / np.log(2) * 1e6


#First subplot ........................................................................................................
title = "dyn. NSNS (B) + DZ10 + ABLA07"
pr_I = 2.518670e-04 / 2.033514e-04  #production ratio
pr_Cm = 6.048833e-06 / 3.918712e-05

septime_dyn_I = normal(deltas, pr_I, k_I, tau_I, ESS_I, 'I', Tgal)
septime_dyn_Cm = normal(deltas, pr_Cm, k_Cm, tau_Cm, ESS_Cm, 'Cm', Tgal)


#Second subplot.........................................................................................................
title2 = "MR SN + DZ10 + ABLA07"
pr_I = 4.730280e-04 / 1.904814e-04
pr_Cm = 9.513214e-08 / 1.353803e-06

septime_sne_I = normal(deltas, pr_I, k_I, tau_I, ESS_I, 'I', Tgal)
septime_sne_Cm = normal(deltas, pr_Cm, k_Cm, tau_Cm, ESS_Cm, 'Cm', Tgal)


#Third subplot.........................................................................................................
title3 = "Disk def + DZ + ABLA07"
pr_I = 2.924529e-04 / 2.437909e-04
pr_Cm = 6.633196e-07 / 6.420131e-06

septime_wind_I = normal(deltas, pr_I, k_I, tau_I, ESS_I, 'I', Tgal)
septime_wind_Cm = normal(deltas, pr_Cm, k_Cm, tau_Cm, ESS_Cm, 'Cm', Tgal)


#plotting...............................................................................................................
matplotlib.rcParams.update({'font.size': 12.5})
f, axarr = plt.subplots(3, 1, figsize = (8, 7.7), sharex = True, sharey = False) # [row][col]
f.subplots_adjust(hspace = 0.)
f.subplots_adjust(wspace = 0.)

# Dynamical Ejecta
axarr[0].fill_between(deltas, np.array(septime_dyn_I[1]), np.array(septime_dyn_I[2]), alpha = 0.5)
axarr[0].plot(deltas, septime_dyn_I[0], linestyle = '--', label = 'Using $^{129}$I / $^{127}$I')
axarr[0].fill_between(deltas, np.array(septime_dyn_Cm[1]), np.array(septime_dyn_Cm[2]), alpha = 0.5)
axarr[0].plot(deltas, septime_dyn_Cm[0], label = 'Using $^{247}$Cm / $^{235}$U')

# MR-SNe
axarr[1].fill_between(deltas, np.array(septime_sne_I[1]), np.array(septime_sne_I[2]), alpha = 0.5)
axarr[1].plot(deltas, septime_sne_I[0], linestyle = '--')
axarr[1].fill_between(deltas, np.array(septime_sne_Cm[1]), np.array(septime_sne_Cm[2]), alpha = 0.5)
axarr[1].plot(deltas, septime_sne_Cm[0])

# Wind
axarr[2].fill_between(deltas, np.array(septime_wind_I[1]), np.array(septime_wind_I[2]), alpha = 0.5)
axarr[2].plot(deltas, septime_wind_I[0], linestyle = '--')
axarr[2].fill_between(deltas, np.array(septime_wind_Cm[1]), np.array(septime_wind_Cm[2]), alpha = 0.5)
axarr[2].plot(deltas, septime_wind_Cm[0])

axarr[0].set_xlim(70, 930)
axarr[0].set_ylim(90, 260)
axarr[1].set_ylim(90, 260)
axarr[2].set_ylim(90, 260)

axarr[0].set_yticks([100, 125, 150, 175, 200, 225, 250])
axarr[1].set_yticks([100, 125, 150, 175, 200, 225, 250])
axarr[2].set_yticks([100, 125, 150, 175, 200, 225, 250])
# Ticks
for ax in axarr:
    ax.minorticks_on()
    ax.yaxis.set_ticks_position("both")
    ax.xaxis.set_ticks_position("both")

# Legend
axarr[0].legend(frameon = False, loc = 2)
axarr[0].annotate('Dyn. NSNS (B) (DZ10 + ABLA07)', xy = (910, 237.3), ha = 'right', va = 'center', color = 'k')
axarr[1].annotate('MR SN (DZ10 + ABLA07)', xy = (910, 237.3), ha = 'right', va = 'center', color = 'k')
axarr[2].annotate('Disk 1 (DZ10 + ABLA07)', xy = (910, 237.3), ha = 'right', va = 'center', color = 'k')

# Panels annotation
axarr[0].annotate('A', xy = (905, 107), ha = 'right', va = 'center', color = 'k')
axarr[1].annotate('B', xy = (905, 107), ha = 'right', va = 'center', color = 'k')
axarr[2].annotate('C', xy = (905, 107), ha = 'right', va = 'center', color = 'k')

# Labels
axarr[2].set_xlabel('Recurrence time between $r$-process events [Myr]', fontsize = 13)
axarr[1].set_ylabel('Time $\Delta t_\mathrm{LE}$ since the last $r$-process event [Myr]', fontsize = 13)
plt.savefig("delta_stat_tau.pdf", dpi = 250, bbox_inches = 'tight', rasterized = True)


print('Done')
