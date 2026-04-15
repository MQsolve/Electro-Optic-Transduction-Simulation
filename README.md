# Quantum transduction

This repository contains a QuTiP (Quantum Toolbox in Python) simulation modeling the electro-optic transduction of a single photon from a superconducting microwave cavity to a telecom-wavelength optical cavity.

## Physics overview:
The system utilizes the Lindblad Master Equation to model the open quantum dynamics. 
It explores the critical balance between the coherent coupling rate ($G$) and the cavity dissipation rates ($\kappa_a$, $\kappa_b$).

## Key findings:
By sweeping the optical extraction rate ($\kappa_a$), the simulation identifies the optimal impedance-matching regime.

It explicitly demonstrates the efficiency drop-off in the overdamped regime due to the Quantum Zeno effect, proving that maximizing optical leakage paradoxically suppresses state transfer.

The maximum achievable efficiency is inherently bounded by the system's multiphoton cooperativity ($C = 4G^2 / \kappa_a \kappa_b$).
## Mathematical framework

This simulation moves beyond closed-system Schrödinger dynamics to model the realistic, noisy environment required for functional quantum hardware. 

### Open system dynamics (the Lindblad Master Equation)
The core time-evolution of the coupled cavities is simulated using the Lindblad master equation, accounting for the continuous leakage of the optical cavity and the intrinsic heat loss of the microwave cavity:

$$\frac{d\rho}{dt} = -i[H, \rho] + \sum_n \left( C_n \rho C_n^\dagger - \frac{1}{2}\{C_n^\dagger C_n, \rho\} \right)$$

Where the collapse operators are defined as $C_{opt} = \sqrt{\kappa_a}\hat{a}$ (telecom fiber leakage) and $C_{mw} = \sqrt{\kappa_b}\hat{b}$ (cryogenic substrate loss).

### Transduction efficiency optimization
The metric for success is the total extracted photon probability. The simulation calculates the Area Under the Curve (AUC) of the optical population over time to find the maximum theoretical state transfer:

$$\eta = \int_0^\infty \kappa_a \langle \hat{n}_a(t) \rangle dt$$

By sweeping $\kappa_a$ via numerical integration (Trapezoidal rule), the tool locates the exact impedance-matching window before the system enters the overdamped Quantum Zeno regime. 
Also we wants to minimize microwave cavity leakage so we set $\kappa_b$ it to $0.1 GHz$ with $G$ the coupling rate set to $1.0$ for practical unit conversion inside the QuTip simulation.

##  Conclusion
So this tool helps finding optimal $\kappa_a$ for fixed $\kappa_b$ and $G$, the next steps are to also find the best fit for those two parameters given the available constraints.
