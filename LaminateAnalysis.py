import pickle
import numpy as np
import LaminaAnalysis
import DefMaterial

def LaminateStiffness():
    totalLamina = pickle.load(open('Data/LaminaCount.dat', 'rb'))

    A = np.array([[0] * 3] * 3)
    B = np.array([[0] * 3] * 3)
    D = np.array([[0] * 3] * 3)
    Q = []
    thickness = [0]
    for k in range(totalLamina):
        filename = f'Data/Lamina{k + 1}.dat'
        lamina = pickle.load(open(filename, 'rb'))

        neu21 = (lamina.neu12 * lamina.E2) / lamina.E1
        plyAngle = lamina.sig1T_ult
        thickness.append(lamina.sig1C_ult)
        laminaProp = [lamina.E1, lamina.E2, lamina.neu12, neu21, lamina.G, plyAngle]

        Q.append(LaminaAnalysis.stiff_mat(laminaProp))

    z = np.array(thickness)
    z = np.cumsum(z)
    z = z - z[totalLamina] / 2

    Q = np.array(Q)
    for k in range(totalLamina):
        A = np.add(A, Q[k, :, :] * (z[k + 1] - z[k]))
        B = np.add(B, (Q[k, :, :] * (pow(z[k + 1], 2) - pow(z[k], 2)))/2)
        D = np.add(D, (Q[k, :, :] * (pow(z[k + 1], 3) - pow(z[k], 3)))/3)

    for i in range(3):
        file = DefMaterial.DefMaterial(A[i])
        pickle.dump(file, open(f'Data/Stiff{i+1}.dat', 'wb'))

        file = DefMaterial.DefMaterial(B[i])
        pickle.dump(file, open(f'Data/Stiff{i+4}.dat', 'wb'))

        file = DefMaterial.DefMaterial(D[i])
        pickle.dump(file, open(f'Data/Stiff{i+7}.dat', 'wb'))

def ReadStiff():
    A = []
    B = []
    D = []
    for i in range(3):
        temp = pickle.load(open(f'Data/Stiff{i+1}.dat', 'rb'))
        tempMat = [temp.E1, temp.E2, temp.neu12]
        A.append(tempMat)

        temp = pickle.load(open(f'Data/Stiff{i+4}.dat', 'rb'))
        tempMat = [temp.E1, temp.E2, temp.neu12]
        B.append(tempMat)

        temp = pickle.load(open(f'Data/Stiff{i+7}.dat', 'rb'))
        tempMat = [temp.E1, temp.E2, temp.neu12]
        D.append(tempMat)

    stiff = np.array([A[0][0], A[0][1], A[0][2], B[0][0], B[0][1], B[0][2]])
    for i in range(1,3):
        stiff = np.vstack([stiff, [A[i][0], A[i][1], A[i][2], B[i][0], B[i][1], B[i][2]]])
    for i in range(3):
        stiff = np.vstack([stiff, [B[i][0], B[i][1], B[i][2], D[i][0], D[i][1], D[i][2]]])

    return stiff

def LaminateStrain():
    stiff = ReadStiff()
    stress = pickle.load(open('Data/LaminateStresses.dat', 'rb'))
    stress = np.array([stress.E1, stress.E2, stress.neu12, stress.G, stress.sig1T_ult, stress.sig1C_ult])

    strain = (np.matmul(np.linalg.inv(stiff), np.transpose(stress))) * pow(10, 3)

    strain = DefMaterial.DefMaterial(strain)

    file_strain = 'Data/LaminateStrains.dat'
    pickle.dump(strain, open(file_strain, 'wb'))

def LaminateStress():
    stiff = ReadStiff()
    strain = pickle.load(open('Data/LaminateStrains.dat', 'rb'))
    strain = np.array([strain.E1, strain.E2, strain.neu12, strain.G, strain.sig1T_ult, strain.sig1C_ult])

    stress = (np.matmul(stiff, np.transpose(strain)))*pow(10, -3)

    stress = DefMaterial.DefMaterial(stress)

    file_stress = 'Data/LaminateStresses.dat'
    pickle.dump(stress, open(file_stress, 'wb'))
