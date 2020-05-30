import numpy as np
import math

from Operators import Operator, Density_Matrix, \
                      Observable, Random_Operator, \
                      Random_Observable, Random_Density_Matrix, \
                      Commutator, \
                      Magnus_Expansion_1st_Term, \
                      Magnus_Expansion_2nd_Term, \
                      Canonical_Density_Matrix

from Nuclear_Spin import Nuclear_Spin

from Hamiltonians import H_Zeeman, H_Quadrupole, \
                         H_Single_Mode_Pulse, \
                         H_Multiple_Mode_Pulse, \
                         H_Pulse_IP, \
                         V0, V1, V2

# Function that runs the simulation
def Simulate(s, gyro_ratio, \
             theta_z, phi_z, H_0, \
             eQ, eq, eta, alpha_q, beta_q, gamma_q, \
             temperature, \
             mode, \
             pulse_duration):
    
    # Nuclear spin under study
    spin = Nuclear_Spin(s, gyro_ratio)
    
    # Computes the unperturbed Hamiltonian of the system, namely the sum of the Zeeman and Quadrupole
    # contribution
    h_unperturbed = H_Zeeman(spin, theta_z, phi_z, H_0) + \
                    H_Quadrupole(spin, eQ, eq, eta, alpha_q, beta_q, gamma_q)
    
    # Density matrix of the system at time t=0, when the ensemble of spins is considered at equilibrium
    dm_initial = Canonical_Density_Matrix(h_unperturbed, temperature)
    
    # Sampling of the time-dependent term of the Hamiltonian representing the coupling with the
    # electromagnetic pulse (already cast in the interaction picture)
    times, time_step = np.linspace(0, pulse_duration, num=int(pulse_duration*100), retstep=True)
    h_pulse_ip = []
    for t in times:
        h_pulse_ip.append(H_Pulse_IP(spin, mode, t, h_unperturbed))
        
    # Evaluation of the 1st and 2nd terms of the Magnus expansion for the pulse Hamiltonian in the
    # interaction picture
    magnus_1st = Magnus_Expansion_1st_Term(h_pulse_ip, time_step)
    magnus_2nd = Magnus_Expansion_2nd_Term(h_pulse_ip, time_step)
    
    # Density matrix of the system after evolution under the action of the pulse
    dm_evolved_ip = dm_initial.sim_trans(-(magnus_1st+magnus_2nd), exp=True)
    
    # Evolved density matrix cast back in the interaction picture
    dm_evolved = dm_evolved_ip.interaction_picture(h_unperturbed, pulse_duration, invert=True)
    
    return Density_Matrix(dm_evolved.matrix)