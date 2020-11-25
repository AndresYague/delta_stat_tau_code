Program to calculate isolation times for different isotopes and conditions.

Written by Benjámin Sóos and Andrés Yagüe López.

This program works with an input file that must be named "input.in" and be in
this same directory.  An example input file can be found in "input.example".
It is enough to rename "input.example" to "input.in" and run the program to
get a test figure, which will be produced with the name "current_fig.pdf".

The input file necessary to reproduce figure S3 of https://ui.adsabs.harvard.edu/abs/2020arXiv200604833C/abstract is:


# Example of input.in
# ==========================================

# Monte Carlo input
n_draws     1e6     # Total number of draws
t_gal       8500    # Galaxy age in Myr
delt0       70      # Starting value of delta in Myr
deltlast    930     # Final value of delta in Myr
step	    2       # Step of the delta calculation in Myr
tau_monte   0       # Should we use Monte Carlo at all? Supported: 1 (on), 0 (off)

# ---------------------------------------

# Isotopes input
n_isotopes   2      # How many isotopes to plot

# Isotope-1 values
avg_ESS_1   1.28e-4 # ESS average
std_ESS_1   1.50e-6 # Standard deviation
avg_tau_1   22.6    # Average of tau in Myr
std_tau_1   0       # Standard deviation of tau in Myr
ref_1       stable  # Reference isotope. Supported: stable, u235
label_1     Using $^{129}$I/$^{127}$I  # Label for plot line

# Isotope-2 values
avg_ESS_2   5.6e-5 	# Hf ESS average
std_ESS_2   1.5e-6  # Hf standard deviation
avg_tau_2   22.5    # Average of tau in Myr
std_tau_2   0      	# Standard deviation of tau in Myr
ref_2       u235    # Reference isotope. Supported: stable, u235
label_2     Using $^{247}$Cm/$^{235}$U  # Label for plot line

# ---------------------------------------

# Plots input
n_plots     3         # How many plots to make
font_size   16.5      # Font size
xlabel      Recurrence time between $r$-process events [Myr]
ylabel      Time since the last $r$-process event [Myr]

# Plot-1 values
kk_1_1        5.7     # Upper value of GCE K. All three values of K can be identical
kk_1_2        2.3     # Middle value of GCE K
kk_1_3	      1.6     # Lower value of GCE K
pr_1_1        X.XX    # Production value for first isotope
pr_1_2        X.XX    # Production value for second isotope
label_ann_1   Dyn. NSNS (B) (DZ10 + ABLA07)  # Annotation in panel

# Plot-2 values
kk_2_1        5.7     # Upper value of GCE K
kk_2_2        2.3     # Middle value of GCE K
kk_2_3	      1.6	  # Lower value of GCE K
pr_2_1        X.XX    # Production value for first isotope
pr_2_2        X.XX    # Production value for second isotope
label_ann_2   MR SN (DZ10 + ABLA07)  # Annotation in panel

# Plot-3 values
kk_3_1        5.7     # Upper value of GCE K
kk_3_2        2.3     # Middle value of GCE K
kk_3_3		  1.6	  # Lower value of GCE K
pr_3_1        X.XX    # Production value for first isotope
pr_3_2        X.XX    # Production value for second isotope
label_ann_3   Disk 1  # Annotation in panel
