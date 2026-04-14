import matplotlib.pyplot as plt
import numpy as np
from IPython.display import Image
from qutip import (Qobj, about, basis, coherent, coherent_dm, create, destroy,
                   expect, fock, fock_dm, mesolve, qeye, sigmax, sigmay,
                   sigmaz, tensor, thermal_dm, anim_matrix_histogram,
                   anim_fock_distribution)
# set a parameter to see animations in line
from matplotlib import rc
rc('animation', html='jshtml')

N = 5 # truncated Hilbert space dimension for both cavities (optical and microwave)

hbar = 1 

Delta_a = 1.0 # frequency detuning for the optical cavity
Delta_b = 2.0 # frequency detuning for the microwave cavity
G = 2*np.pi*1.0 # coupling strength between the optical and microwave cavities (GHz)


a = tensor(destroy(N), qeye(N)) # annihilation operator for the optical cavity (a)
b = tensor(qeye(N), destroy(N)) # annihilation operator for the microwave cavity (b)
print("a:", a)
print("b:", b)

na = a.dag()*a # number of photon in optical cavity
nb = b.dag()*b # number of photon in microwave cavity
print("na:", na)
print("nb:", nb)

cross_interaction = a.dag()*b  +  a*b.dag() # Interactions between microawave and optical cavity
print("cross_interaction:", cross_interaction)

H = hbar*(Delta_a*na  +  Delta_b*nb  +  G*cross_interaction) #Hamiltonian of the system


# Dissipation Parameters (GHz)
kappa_a = 2 * np.pi * 0.5  # Optical cavity leakage (to fiber)
kappa_b = 2 * np.pi * 0.1  # Microwave cavity intrinsic loss (heat)

# Collapse Operators
c_ops = [np.sqrt(kappa_a)*a,  # Optical decay
         np.sqrt(kappa_b)*b]  # Microwave decay


print("H:", H)

# Initial State: |na=0, nb=1> with the tensor(optical_state, microwave_state)
psi0 = tensor(basis(N, 0), basis(N, 1))
print("psi0:", psi0)

#The time vector for the simulation (0 to 30 ns, 300 steps)
tlist = np.linspace(0, 30, 300)


kappa_a_array = np.linspace(0.1, 10.0, 50)  #  Test 50 different values of kappa_a from 0.1 to 10 GHz
efficiencies = []

for ka in kappa_a_array:
    kappa_a = 2 * np.pi * ka
    H = G * cross_interaction
    c_ops = [np.sqrt(kappa_a) * a, np.sqrt(kappa_b) * b]
    
    # Run solver
    result = mesolve(H, psi0, tlist, c_ops=c_ops, e_ops=[na])
    opt_pop = result.expect[0]
    
    # Calculate Total Efficiency: Integral of (kappa_a * na) dt
    # np.trapz performs numerical integration using the trapezoidal rule
    dt = tlist[1] - tlist[0]
    efficiency = np.trapezoid(kappa_a * opt_pop, dx=dt)
    efficiencies.append(efficiency)

print("Efficiencies:", efficiencies)
print("max efficiency:", np.max(efficiencies))
print("Optimal Leakage Rate (GHz):", kappa_a_array[np.argmax(efficiencies)])

# Plot the Sweep Result
plt.plot(kappa_a_array, efficiencies, linewidth=2, color='red')
plt.axvline(x=kappa_a_array[np.argmax(efficiencies)], linestyle='--', color='gray', label='Approx Optimal (2*G)')
plt.xlabel("Optical Leakage Rate ($\kappa_a$ / 2$\pi$ GHz)")
plt.ylabel("Total Transduction Efficiency")
plt.title("Efficiency vs. Leakage (Finding the Sweet Spot)")
plt.legend()
plt.grid(True)
plt.show()

