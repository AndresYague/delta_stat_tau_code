import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.lines as lines
import numpy as np


def read_input(inpt_file):
    '''Parse the input file'''

    inpt_dict = {}

    # Save input into inpt_dict
    with open(inpt_file, "r") as fread:
        for line in fread:
            lnlst = line.split()
            if len(lnlst) > 0 and "#" not in lnlst[0]:
                key = lnlst[0]
                if "label" not in key and "ref" not in key:
                    val = float(lnlst[1])

                    # If integer, transform
                    if "n_" in key:
                        val = int(val)
                # Deal with labels
                else:
                    lab = []
                    for st in lnlst[1:]:
                        if "#" in st:
                            break

                        lab.append(st)

                    val = " ".join(lab)

                inpt_dict[key] = val

    return inpt_dict

#main function
def get_sept(deltas, pr, kk, tau, ESS, t_gal, ref = "stable"):
    pp = 47.7 # Probability at 2 sigma

    septime = []
    plus_2_sig = []
    minus_2_sig = []

    # Go for each delta in the array deltas, previously calculated
    for delta in deltas:
        if ref == "stable":
            mm = pr * delta / t_gal * kk
        elif ref == "u235":
            mm = pr * kk * (1 - np.exp(-delta / 1009))

        septs = -np.log(ESS/mm) * tau

        septime.append(np.mean(septs))

        # Get all the possible 2_sigmas
        f = lambda x: np.percentile(x, 50 + pp)
        plus_2_sig.append(f(septs))

        f = lambda x: np.percentile(x, 50 - pp)
        minus_2_sig.append(f(septs))

    septime = np.array(septime)
    plus_2_sig = np.array(plus_2_sig)
    minus_2_sig = np.array(minus_2_sig)

    return septime, plus_2_sig, minus_2_sig

# Read input
inpt_dict = read_input("input.in")

# Number of draws
n_draws = inpt_dict["n_draws"]

# Age of galaxy in Myr
t_gal = inpt_dict["t_gal"]

n_isotopes = inpt_dict["n_isotopes"]

tau_monte_carlo=inpt_dict["tau_monte"]

ESS_isot = []; tau_isot = []
for ni in range(n_isotopes):

    # ESS values per isotope
    string = "_ESS_{}".format(ni + 1)
    avg_ESS_isot = inpt_dict["avg" + string]
    sig_ESS_isot = inpt_dict["std" + string]
    ESS_isot.append(np.random.normal(avg_ESS_isot, sig_ESS_isot,
                                     size = n_draws))
    # Tau values per isotope
    if tau_monte_carlo == 1:
        string = "_tau_{}".format(ni + 1)
        avg_tau_isot = inpt_dict["avg" + string]
        sig_tau_isot = inpt_dict["std" + string]
        tau_isot.append(np.random.normal(avg_tau_isot, sig_tau_isot,
                                        size = n_draws))
    elif tau_monte_carlo == 0:
        string = "_tau_{}".format(ni + 1)
        avg_tau_isot = inpt_dict["avg" + string]
        tau_isot.append(avg_tau_isot)

# Parameters for deltas array
delt0 = inpt_dict["delt0"]
deltlast = inpt_dict["deltlast"]
step = inpt_dict["step"]

# Define the deltas array
deltas = np.arange(delt0, deltlast + 1, step)

# Plot input
xlim = [deltas[0], deltas[-1]]
ylim = [15, 71]; step = 10
yticks = np.arange(ylim[0], ylim[1], step)
yticks = [x for x in yticks]

#plotting...............................................................................................................
n_plots = inpt_dict["n_plots"]
matplotlib.rcParams.update({'font.size': inpt_dict["font_size"]})
f, axarr = plt.subplots(n_plots, 1, figsize = (8, 7.7), sharex = True, sharey = False) # [row][col]
f.subplots_adjust(hspace = 0.)
f.subplots_adjust(wspace = 0.)

for pl in range(n_plots):
    # Get the upper, middle, and lower K
    kk = []
    for nk in range(3):
        kk.append(inpt_dict["kk_{}_{}".format(pl + 1, nk + 1)])
    kk = np.array(kk)
    
    # Calculate
    for ni in range(n_isotopes):
        pr_is = inpt_dict["pr_{}_{}".format(pl + 1, ni + 1)]
        reference = inpt_dict["ref_{}".format(ni + 1)]
        
        # T_iso values
        upper = get_sept(deltas, pr_is, kk[0], tau_isot[ni], ESS_isot[ni], t_gal)
        middle = get_sept(deltas, pr_is, kk[1], tau_isot[ni], ESS_isot[ni], t_gal)
        lower = get_sept(deltas, pr_is, kk[2], tau_isot[ni], ESS_isot[ni], t_gal)

        # Plot
        label = inpt_dict["label_{}".format(ni + 1)]
        axarr[pl].fill_between(deltas, upper[1], lower[2], alpha = 0.5)
        axarr[pl].plot(deltas, middle[0], linestyle = '--',label = "Using " + label)
        axarr[pl].set_xlim(xlim)
        axarr[pl].set_ylim(ylim)
        axarr[pl].set_yticks(yticks)

        # Floating text
        if pl == 0:
            axarr[pl].legend(frameon = False, loc = 2)
        axarr[pl].annotate(inpt_dict["label_ann_{}".format(pl + 1)],
                        xy = (0.98, 0.90), xycoords = "axes fraction",
                        ha = 'right', va = 'center', color = 'k')

        # Ticks
        axarr[pl].minorticks_on()
        axarr[pl].yaxis.set_ticks_position("both")
        axarr[pl].xaxis.set_ticks_position("both")

# Labels
axarr[n_plots - 1].set_xlabel(inpt_dict["xlabel"], fontsize = inpt_dict["font_size"])
axarr[n_plots - 2].set_ylabel(inpt_dict["ylabel"], fontsize = inpt_dict["font_size"])
plt.savefig("current_fig.pdf")

print('Done')
