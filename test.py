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
N = 2
H = 1.0*sigmax() + 0.5*sigmay() + 0.25*sigmaz()

I2 = qeye(2)
H_p = tensor(H, I2)

print(H)
print(I2)
print(H_p)

psi1 = tensor(basis(N, 1), basis(N, 0))  # excited first qubit
psi2 = tensor(basis(N, 0), basis(N, 1))  # excited second qubit

print(psi1)
print(psi2)
