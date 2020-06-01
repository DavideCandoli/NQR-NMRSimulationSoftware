import numpy as np
import pandas as pd
import math

import matplotlib.pylab as plt

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


def Zeeman_Spectrum():
    spin = Nuclear_Spin(1, 1.)
    h_zeeman = H_Zeeman(spin, math.pi/2, math.pi/2, 1.)
    energy_spectrum = h_zeeman.eigenvalues()
    print("Energy spectrum of the pure Zeeman Hamiltonian = %r" % energy_spectrum)
    
        
def Quadrupole_Spectrum_Axially_Symmetric():
    spin = Nuclear_Spin(1, 0.)
    h_quadrupole = H_Quadrupole(spin, 1., 0, math.pi/2, math.pi/2, math.pi/2)
    energy_spectrum = h_quadrupole.eigenvalues()
    print("Energy spectrum of the pure Quadrupole Hamiltonian = %r" % energy_spectrum)
    
        
def Quadrupole_Spectrum_Axially_Asymmetric():
    spin = Nuclear_Spin(1, 0.)
    h_quadrupole = H_Quadrupole(spin, 1., 1, math.pi/2, math.pi/2, math.pi/2)
    energy_spectrum = h_quadrupole.eigenvalues()
    print("Energy spectrum of the pure Quadrupole Hamiltonian = %r" % energy_spectrum)
    
    
def Quadrupole_Perturbation_Satellite_Frequency_Shift():
    spin = Nuclear_Spin(3/2, 1.)
    
    h_zeeman = H_Zeeman(spin, 0., 0., 5.)
    
    field_crystal_angles = np.linspace(0, math.pi, num=15)
    
    frequency_shift = {}
    
    x = field_crystal_angles
    y = []
    
    for theta_q in field_crystal_angles:
        
        h_quadrupole = H_Quadrupole(spin, 0.1, 0., 0., theta_q, 0.)
        
        h_unperturbed = Observable(h_zeeman.matrix + h_quadrupole.matrix)
        
        energy_spectrum = h_unperturbed.eigenvalues()
        
        energy_spectrum = np.sort(energy_spectrum)
        
        satellite_frequency = energy_spectrum[3] - energy_spectrum[2]
        
        central_frequency = energy_spectrum[2] - energy_spectrum[1]
        
        frequency_shift[theta_q] = satellite_frequency - central_frequency
        
        y.append(frequency_shift[theta_q])

    plt.plot(x, y)
    
    plt.xlabel("\N{GREEK SMALL LETTER THETA} (rad)")    
    plt.ylabel("\N{GREEK SMALL LETTER NU}3/2 - \N{GREEK SMALL LETTER NU}1/2 (MHz)")
    
    plt.show()
    
    return frequency_shift
    