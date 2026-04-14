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

#The Master Equation Solver
result = mesolve(H, psi0, tlist, c_ops=c_ops, e_ops=[na, nb])

# Extract the tracked populations
opt_pop = result.expect[0]
mw_pop  = result.expect[1]

# Plot the results
plt.plot(tlist, mw_pop, label="Microwave Photons (b)")
plt.plot(tlist, opt_pop, label="Optical Photons (a)")
plt.xlabel("Time (ns)")
plt.ylabel("Photon Population")
plt.title("Lossless Microwave-to-Optical Transduction")
plt.legend()
plt.show()
