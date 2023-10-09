import pickle
import numpy as np
import DefMaterial
from tkinter import messagebox


# Engineering constants determination for composite
def lamina_const(method, Vf, file_fiber, file_matrix):
    f = pickle.load(open(file_fiber, 'rb'))
    m = pickle.load(open(file_matrix, 'rb'))
    Vf = Vf
    Vm = 1 - Vf
    d_by_s = pow((4*Vf)/3.1416, 0.5)

    eps_f_ult = f.sig1T_ult / (f.E1*1000)
    eps_m_ult = m.sig1T_ult / (m.E1*1000)

    # Longitudinal Modulus by Rule of Mixture
    E1 = f.E1 * Vf + m.E1 * Vm

    # Major Poisson's Ratio by Rule of Mixture
    neu12 = f.neu12*Vf + m.neu12*Vm

    if method == 1:     #Rule of Mixture
        # Transverse Modulus by Rule of Mixture
        E2 = (f.E2*m.E2)/(Vf*m.E2 + Vm*f.E2)

        # Shear Modulus by Rule of Mixture
        G = (f.G*m.G)/(Vf*m.G + Vm*f.G)
    elif method == 2:
        # Transverse Modulus by Halpin-Tsai Equation
        zita = 2    # Generic Value of zita for E2
        eta = ((f.E2/m.E2)-1)/((f.E2/m.E2)+zita)
        E2 = ((1+zita*eta*Vf)/(1-eta*Vf))*m.E2

        # Shear Modulus by Halpin-Tsai Equation
        zita = 1  # Generic Value of zita for G
        eta = ((f.G / m.G) - 1) / ((f.G / m.G) + zita)
        G = ((1 + zita * eta * Vf) / (1 - eta * Vf)) * m.G
    else:
        return

    # Longitudinal Tensile Strength Calculation
    Vf_cr = (m.sig1T_ult - (m.E1*eps_f_ult*1000))/(f.sig1T_ult - (m.E1*eps_f_ult*1000))

    if Vf < Vf_cr:
        run_Or_not = messagebox.askquestion(title='Material Error',
                                            message='Fiber volume falls below critical point.\n'
                                                               'Do you still want to continue?')
        if run_Or_not == 'no':
            return

    sig1T_ult = f.sig1T_ult*Vf + eps_f_ult*m.E1*Vm*1000

    # Longitudinal Compressive Strength Calculation
    eps2T_ult_1 = eps_m_ult*(1 - pow(Vf, 1/3))
    eps2T_ult_2 = eps_m_ult*(d_by_s*((m.E1/f.E1)-1)+1)

    if eps2T_ult_1 < eps2T_ult_2:
        eps2T_ult = eps2T_ult_1
    else:
        eps2T_ult = eps2T_ult_2

    sig1C_ult_1 = (E1*eps2T_ult*1000)/neu12
    SC1 = 2*(Vf + Vm*(m.E1/f.E1))*pow((Vf*m.E1*f.E1*pow(10, 6))/(3*Vm), 0.5)
    SC2 = (m.G*1000)/Vm
    sig1C_ult_2 = 2*(f.tow12_ult*Vf + m.tow12_ult*Vm)

    sig1C_ult = min(sig1C_ult_1, SC1, SC2, sig1C_ult_2)

    # Transverse Tensile Strength Calculation
    sig2T_ult = E2*eps2T_ult*1000

    # Transverse Compressive Strength Calculation
    eps2C_ult = (d_by_s*(m.E2/f.E2) + (1-d_by_s))*(m.sig2C_ult/(m.E2*1000))
    sig2C_ult = E2*eps2C_ult*1000

    # Shear Strength Calculation
    gamma12_ult = (d_by_s*(m.G/f.G) + (1-d_by_s))*(m.tow12_ult/(m.G*1000))
    tow12_ult = G*gamma12_ult*1000

    lamina = np.array([E1, E2, neu12, G, sig1T_ult, sig1C_ult, sig2T_ult, sig2C_ult, tow12_ult])
    lamina = DefMaterial.DefMaterial(lamina)

    file_lamina = 'Data/Lamina.dat'
    pickle.dump(lamina, open(file_lamina, 'wb'))

    return file_lamina
