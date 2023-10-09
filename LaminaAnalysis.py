import math
import pickle
import numpy as np
import DefMaterial


def calcStrains(fileStress, fileLamina, plyAngle=0):
    stressFile = pickle.load(open(fileStress, 'rb'))
    sigma1 = stressFile.E1
    sigma2 = stressFile.E2
    tow12 = stressFile.neu12
    stress = np.array([sigma1, sigma2, tow12])

    lamina = pickle.load(open(fileLamina, 'rb'))
    laminaProp = [lamina.E1, lamina.E2, lamina.neu12, lamina.neu21, lamina.G, plyAngle]

    Qbar = stiff_mat(laminaProp)

    strain = (np.matmul(np.linalg.inv(Qbar), np.transpose(stress)))*pow(10, 3)

    strain = DefMaterial.DefMaterial(strain)

    file_strains = 'Data/Strains.dat'
    pickle.dump(strain, open(file_strains, 'wb'))


def calcStresses(fileStrain, fileLamina, plyAngle=0):
    strainFile = pickle.load(open(fileStrain, 'rb'))
    eps1 = strainFile.E1
    eps2 = strainFile.E2
    gamma = strainFile.neu12
    strain = np.array([eps1, eps2, gamma])

    lamina = pickle.load(open(fileLamina, 'rb'))
    laminaProp = [lamina.E1, lamina.E2, lamina.neu12, lamina.neu21, lamina.G, plyAngle]

    Qbar = stiff_mat(laminaProp)

    stress = (np.matmul(Qbar, np.transpose(strain)))*pow(10, -3)

    stress = DefMaterial.DefMaterial(stress)

    file_stress = 'Data/Stresses.dat'
    pickle.dump(stress, open(file_stress, 'wb'))


def stiff_mat(laminaProp):
    E1 = laminaProp[0]
    E2 = laminaProp[1]
    neu12 = laminaProp[2]
    neu21 = laminaProp[3]
    G = laminaProp[4]
    plyAngle = laminaProp[5]

    Q11 = E1/(1 - neu12*neu21)
    Q12 = (neu12*E2)/(1 - neu12*neu21)
    Q21 = Q12
    Q22 = E2/(1 - neu12*neu21)
    Q66 = G

    Q = np.array([[Q11, Q12, 0],
                  [Q21, Q22, 0],
                  [0, 0, Q66]])

    T = transformation(plyAngle)

    R = np.array([[1, 0, 0],
                  [0, 1, 0],
                  [0, 0, 2]])

    Q_invT = np.matmul(np.linalg.inv(T), Q)
    RQ_invT = np.matmul(Q_invT, R)
    TRQ_invT = np.matmul(RQ_invT, T)
    Qbar = np.matmul(TRQ_invT, np.linalg.inv(R))

    return Qbar


def transformation(plyAngle = 0.0):
    c = math.cos(math.radians(plyAngle))
    s = math.sin(math.radians(plyAngle))

    T = np.array([[c * c, s * s, 2 * c * s],
                  [s * s, c * c, (-2) * c * s],
                  [(-1) * c * s, c * s, c * c - s * s]])

    return T


def failureCheck(fileStress, fileLamina, plyAngle=0.0):
    c = pickle.load(open(fileLamina, 'rb'))
    stress = pickle.load(open(fileStress, 'rb'))

    sig1T = c.sig1T_ult
    sig1C = c.sig1C_ult
    sig2T = c.sig2T_ult
    sig2C = c.sig2C_ult
    tow12ult = c.tow12_ult

    if sig1C>0:
        sig1C = sig1C*(-1)
    if sig2C>0:
        sig2C = sig2C*(-1)

    ult = [[sig1C, sig1T],
           [sig2C, sig2T],
           [tow12ult*(-1), tow12ult]]

    stress = [stress.E1, stress.E2, stress.neu12]

    T = transformation(plyAngle)

    stress = np.matmul(T, stress)

    failure = []

    for i in range(len(stress)):
        if ult[i][0] < stress[i] < ult[i][1]:
            failure.append(False)
        else:
            failure.append(True)

    return failure
