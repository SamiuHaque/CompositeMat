from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pickle
import DefMaterial
import numpy as np
import LaminaConstants
import LaminaAnalysis
import LaminateAnalysis


class NewWin(Toplevel):
    def __init__(self, master = None, topLabel="New Label", column = 1):
        super().__init__(master=master)
        self.resizable(False, False)
        self.config(bg="#EEE8CD")

        newLabel = Label(self, text=topLabel, bg="#EEE8CD", justify=CENTER,
                          font='Helvetica 12 bold', pady=20)
        newLabel.grid(row = 0, column =column)

    def createEntry(self, allLabel, index=1, column=0, width=30, boxNo = 1):
        propLabel = []
        entryBox = []

        for i in range(len(allLabel)):
            propLabel.append(Label(self, text=allLabel[i], bg="#EEE8CD", font='Helvetica 12', justify=LEFT,
                              width=30, height=2, pady=2))
            propLabel[i].grid(row = index+i, column = 0+column)
            Label(self, bg="#EEE8CD", font='Helvetica 12',
                  width=10, height=2, pady=2).grid(row = index+i, column = 2+column)
            for j in range(boxNo):
                entryBox.append(Entry(self, font='Helvetica 12', justify=CENTER, width=width))
                entryBox[i+j].grid(row = index+i, column = column+j+1)

        return entryBox

    def createDropBox(self, label, options, row, column, width=25):
        Label(self, text=label, bg="#EEE8CD", font='Helvetica 12',
              width=width, height=2, pady=2).grid(row=row, column=column)
        selectOpt = StringVar()
        dropOption = ttk.Combobox(self, font='Helvetica 12', width=width, background="#FFF8DC", textvariable=selectOpt)
        dropOption['values'] = options
        dropOption['state'] = 'readonly'
        dropOption.grid(row=row+1, column=column)

        return selectOpt

    def save(self, parameters, fileName, message=True):
        dataList = []
        for i in parameters:
            if len(i.get()) == 0:
                i.insert(0, '0.0')
            dataList.append(i.get())
        try:
            dataList = np.array(dataList).astype(float)
        except:
            messagebox.showerror(title='Invalid Input', message='Please provide a valid input')
            return
        newMat = DefMaterial.DefMaterial(dataList)
        pickle.dump(newMat, open(fileName, 'wb'))
        if message:
            messagebox.showinfo(title='Save Window', message='Saved successfully')
            self.focus()

    def load(self, parameters, fileName):
        dataValue = pickle.load(open(fileName, 'rb'))
        k = 0
        for att, val in vars(dataValue).items():
            flag = 0
            if parameters[k]['state'] == DISABLED:
                flag = 1
                parameters[k]['state'] = NORMAL
            parameters[k].delete(0, END)
            parameters[k].insert(0, str(round(val, 2)))
            if flag == 1:
                parameters[k]['state'] = DISABLED
            k = k+1
            if k > len(parameters):
                break


def fiber():
    newWin = NewWin(winMain, 'Define Fiber Properties')
    buttonFiber.config(state='disabled')
    def closeWin():
        buttonFiber.config(state='normal')
        newWin.destroy()
    newWin.protocol("WM_DELETE_WINDOW", closeWin)

    allLabel = ['Longitudinal Modulus, E1 (GPa): ',
                'Transverse Modulus, E2 (Gpa): ',
                'Major Poisson\'s Ratio, \u03BD:',
                'Axial Shear Modulus, G (GPa): ',
                'Long. Tensile Strength (MPa): ',
                'Long. Compressive Strength (MPa): ',
                'Trans. Tensile Strength (MPa): ',
                'Trans. Compressive Strength (MPa): ',
                'Shear Strength (MPa): ']

    parameters = newWin.createEntry(allLabel)

    filename = 'Data/Fiber.dat'

    def save():
        newWin.save(parameters, fileName=filename)

    def load():
        newWin.load(parameters, fileName=filename)


    Label(newWin, bg="#EEE8CD", width=30, height=2, pady=2).grid(row=10, column=1)

    saveButton = Button(newWin, text="Save", bg="#FFF8DC", font='Helvetica 9', width=10,
                        height=2, command=save)
    saveButton.grid(row=11, column = 0)
    loadButton = Button(newWin, text="Load", bg="#FFF8DC", font='Helvetica 9', width=10,
                        height=2, command=load)
    loadButton.grid(row=11, column = 1)
    Label(newWin, bg="#EEE8CD", font='Helvetica 12',
          width=10, height=2, pady=2).grid(row=12, column=1)


def matrix():
    newWin = NewWin(winMain, 'Define Matrix Properties')
    buttonMatrix.config(state='disabled')
    def closeWin():
        buttonMatrix.config(state='normal')
        newWin.destroy()
    newWin.protocol("WM_DELETE_WINDOW", closeWin)

    allLabel = ['Longitudinal Modulus, E1 (GPa): ',
                'Transverse Modulus, E2 (Gpa): ',
                'Major Poisson\'s Ratio, \u03BD:',
                'Axial Shear Modulus, G (GPa): ',
                'Long. Tensile Strength (MPa): ',
                'Long. Compressive Strength (MPa): ',
                'Trans. Tensile Strength (MPa): ',
                'Trans. Compressive Strength (MPa): ',
                'Shear Strength (MPa): ']

    parameters = newWin.createEntry(allLabel)

    filename = 'Data/Matrix.dat'

    def save():
        newWin.save(parameters, fileName=filename)

    def load():
        newWin.load(parameters, fileName=filename)


    Label(newWin, bg="#EEE8CD", width=30, height=2, pady=2).grid(row=10, column=1)

    saveButton = Button(newWin, text="Save", bg="#FFF8DC", font='Helvetica 9', width=10,
                        height=2, command=save)
    saveButton.grid(row=11, column = 0)
    loadButton = Button(newWin, text="Load", bg="#FFF8DC", font='Helvetica 9', width=10,
                        height=2, command=load)
    loadButton.grid(row=11, column = 1)
    Label(newWin, bg="#EEE8CD", font='Helvetica 12',
          width=10, height=2, pady=2).grid(row=12, column=1)


def lamina():
    newWin = NewWin(winMain, 'Define/Calculate Lamina Properties')
    buttonLamina.config(state='disabled')
    def closeWin():
        buttonLamina.config(state='normal')
        newWin.destroy()
    newWin.protocol("WM_DELETE_WINDOW", closeWin)

    allLabel = ['Longitudinal Modulus, E1 (GPa): ',
                'Transverse Modulus, E2 (Gpa): ',
                'Major Poisson\'s Ratio, \u03BD:',
                'Axial Shear Modulus, G (GPa): ',
                'Long. Tensile Strength (MPa): ',
                'Long. Compressive Strength (MPa): ',
                'Trans. Tensile Strength (MPa): ',
                'Trans. Compressive Strength (MPa): ',
                'Shear Strength (MPa): ']

    parameters = newWin.createEntry(allLabel)

    # Disable Entry Box
    for i in parameters:
        i.config(state='disabled')

    filename = 'Data/Lamina.dat'

    label = 'Method of Calculation: '
    options = ['Define Manually', 'Strength of Material Approach', 'Semi-Empirical Method']

    def save(message=True):
        newWin.save(parameters, fileName=filename, message=message)

    def load():
        newWin.load(parameters, fileName=filename)

    def calcMethod(*args):
        if method.get() == options[0]:
            process = 0
            for i in parameters:
                i.config(state='normal')
        elif method.get() == options[1]:
            process = 1
            for i in parameters:
                i.config(state='disabled')
        elif method.get() == options[2]:
            process = 2
            for i in parameters:
                i.config(state='disabled')

        return process

    def calculate():
        file_fiber = 'Data/Fiber.dat'
        file_matrix = 'Data/Matrix.dat'
        process = calcMethod()
        try:
            Vf = float(entryVf.get())
            if Vf > 1:
                messagebox.showerror(title='Invalid Input', message='Please provide a valid input for Vf')
        except:
            if process != 0:
                messagebox.showerror(title='Invalid Input', message='Please provide a valid input')
            return

        LaminaConstants.lamina_const(process, Vf, file_fiber, file_matrix)
        load()

    # Save and Load Buttons
    Label(newWin, bg="#EEE8CD", width=30, height=2, pady=2).grid(row=10, column=1)

    saveButton = Button(newWin, text="Save", bg="#FFF8DC", font='Helvetica 9', width=10,
                        height=2, command=save)
    saveButton.grid(row=11, column = 0)

    loadButton = Button(newWin, text="Load", bg="#FFF8DC", font='Helvetica 9', width=10,
                        height=2, command=load)
    loadButton.grid(row=11, column = 1)

    # Fiber Volume Fraction Definition
    label_Vf = Label(newWin, text='Fiber Volume Fraction: ', bg="#EEE8CD", font='Helvetica 12',
              width=25, height=2, pady=2)
    label_Vf.grid(row=2, column=3)
    entryVf = Entry(newWin, font='Helvetica 12', justify=CENTER, width=27)
    entryVf.grid(row=3, column=3)

    # Calculation Options
    method = newWin.createDropBox(label, options, row=5, column=3)

    method.trace('w', calcMethod)

    calcButton = Button(newWin, text="Calculate", bg="#FFF8DC", font='Helvetica 9', width=10,
                        height=2, command=calculate)
    calcButton.grid(row=8, column=3)

    Label(newWin, bg="#EEE8CD", font='Helvetica 12',
          width=10, height=2, pady=2).grid(row=12, column=4)


def stress():
    newWin = NewWin(winMain, 'Calculate Stress/Strain')
    buttonStress.config(state='disabled')

    def closeWin():
        buttonStress.config(state='normal')
        newWin.destroy()

    newWin.protocol("WM_DELETE_WINDOW", closeWin)

    allLabel = ['Longitudinal Strain, \u03B5x (\u00B5m/m): ',
                'Transverse Strain, \u03B5y (\u00B5m/m): ',
                'Shear Strain, \u03B3xy (\u00B5m/m): ',
                'Longitudinal Stress, \u03c3x (MPa): ',
                'Transverse Stress, \u03c3y (MPa): ',
                'Shear Stress, \u03c4xy (MPa):']

    parameters = newWin.createEntry(allLabel)

    # Disable Entry Box
    for i in parameters:
        i.config(state='disabled')

    strainFile = 'Data/Strains.dat'
    stressFile = 'Data/Stresses.dat'
    laminaFile = 'Data/Lamina.dat'

    label = 'Method of Calculation: '
    options = ['Calculate Strains', 'Calculate Stresses']

    def save(process=0, message=True):
        if process==1:
            # Save Stresses
            stressesSave = parameters[3:]
            newWin.save(stressesSave, fileName=stressFile, message=message)
        elif process==2:
            # Save Strains
            strainsSave = parameters[:3]
            newWin.save(strainsSave, fileName=strainFile, message=message)
        else:
            # Save Strains
            strainsSave = parameters[:3]
            newWin.save(strainsSave, fileName=strainFile, message=message)
            # Save Stresses
            stressesSave = parameters[3:]
            newWin.save(stressesSave, fileName=stressFile, message=message)


    def load():
        # Load Strains
        strainsLoad = parameters[:3]
        newWin.load(strainsLoad, fileName=strainFile)

        # Save Stresses
        stressesLoad = parameters[3:]
        newWin.load(stressesLoad, fileName=stressFile)

    def calcMethod(*args):
        if method.get() == options[0]:
            process = 1
            for i in range(len(parameters)):
                if i > 2:
                    parameters[i].config(state='normal')
                else:
                    parameters[i].config(state='disabled')
        elif method.get() == options[1]:
            process = 2
            for i in range(len(parameters)):
                if i < 3:
                    parameters[i].config(state='normal')
                else:
                    parameters[i].config(state='disabled')

        return process

    def calculate():
        if len(entryPly.get()) == 0:
            entryPly.insert(0, '0.0')
        try:
            Angle = float(entryPly.get())
            if abs(Angle) > 90:
                messagebox.showerror(title='Invalid Input', message='Please provide a valid input')
        except:
            messagebox.showerror(title='Invalid Input', message='Please provide a valid input')
            return
        process = calcMethod()
        save(process, message=False)
        if process == 1:
            LaminaAnalysis.calcStrains(fileStress=stressFile, fileLamina=laminaFile, plyAngle=Angle)
        elif process == 2:
            LaminaAnalysis.calcStresses(fileStrain=strainFile, fileLamina=laminaFile, plyAngle=Angle)
        load()

    def failureCheck():
        if len(entryPly.get()) == 0:
            entryPly.insert(0, '0.0')
        try:
            Angle = float(entryPly.get())
            if abs(Angle) > 90:
                messagebox.showerror(title='Invalid Input', message='Please provide a valid input')
        except:
            messagebox.showerror(title='Invalid Input', message='Please provide a valid input')
            return
        failure = LaminaAnalysis.failureCheck(fileStress=stressFile, fileLamina=laminaFile, plyAngle=Angle)
        failure = failure*2
        failLabel = []
        for i in range(len(parameters)):
            if failure[i]:
                color = '#D22B2B'
                text = 'Fail'
            else:
                color = '#00A36C'
                text = 'Pass'
            failLabel.append(Label(newWin, text=text, bg=color, width=8, height=2))
            failLabel[i].grid(row=i+1, column=2)

    # Save and Load Buttons
    Label(newWin, bg="#EEE8CD", width=30, height=2, pady=2).grid(row=10, column=1)

    saveButton = Button(newWin, text="Save", bg="#FFF8DC", font='Helvetica 9', width=10,
                        height=2, command=save)
    saveButton.grid(row=11, column=0)

    loadButton = Button(newWin, text="Load", bg="#FFF8DC", font='Helvetica 9', width=10,
                        height=2, command=load)
    loadButton.grid(row=11, column=1)

    # Ply Angle Definition
    label_ply = Label(newWin, text='Lamina Orientation Angle (Degree): ', bg="#EEE8CD", font='Helvetica 12',
                      width=28, height=2, pady=2)
    label_ply.grid(row=1, column=3)
    entryPly = Entry(newWin, font='Helvetica 12', justify=CENTER, width=27)
    entryPly.grid(row=2, column=3)

    # Calculation Options
    method = newWin.createDropBox(label, options, row=3, column=3)

    method.trace('w', calcMethod)

    calcButton = Button(newWin, text="Calculate", bg="#FFF8DC", font='Helvetica 9', width=10,
                        height=2, command=calculate)
    calcButton.grid(row=5, column=3)

    # Failure Check Button
    failureButton = Button(newWin, text="Check Failure", bg="#FFF8DC", font='Helvetica 12', width=20,
                        height=2, command=failureCheck)
    failureButton.grid(row=11, column=3)

    Label(newWin, bg="#EEE8CD", font='Helvetica 12',
          width=10, height=2, pady=2).grid(row=12, column=4)


def laminate():
    def laminateDefination():
        definationWin = NewWin(newWin, 'Define Lamina Plies for Laminate', column = 0)
        buttonDefineLaminate.config(state='disabled')

        def closeWin():
            buttonDefineLaminate.config(state='normal')
            definationWin.destroy()

        definationWin.protocol("WM_DELETE_WINDOW", closeWin)

        laminaNoTitle = ['Total No. of Lamina: ']
        laminaNo = definationWin.createEntry(laminaNoTitle, width=7)

        def addLamina():
            buttonDefineLamina.config(state='disabled')
            try:
                # global totalLamina
                totalLamina = int(laminaNo[0].get())
                pickle.dump(totalLamina, open('Data/LaminaCount.dat', 'wb'))
            except:
                messagebox.showerror(title='Invalid Input', message='Please provide a valid input')
                return
            laminaNo[0].config(state='disabled')

            row_index = 2
            Label(definationWin, text='E1 (GPa)', font='Helvetica 12', bg="#EEE8CD", width=10, height=2, pady=2).grid(
                row=row_index, column=1)
            Label(definationWin, text='E2 (GPa)', font='Helvetica 12', bg="#EEE8CD", width=10, height=2, pady=2).grid(
                row=row_index, column=2)
            Label(definationWin, text='\u03BD12', font='Helvetica 12', bg="#EEE8CD", width=10, height=2, pady=2).grid(
                row=row_index, column=3)
            Label(definationWin, text='G12 (GPa)', font='Helvetica 12', bg="#EEE8CD", width=10, height=2, pady=2).grid(
                row=row_index, column=4)
            Label(definationWin, text='\u03B8 (Degree)', font='Helvetica 12', bg="#EEE8CD", width=10, height=2, pady=2).grid(
                row=row_index, column=5)
            Label(definationWin, text='thick (mm)', font='Helvetica 12', bg="#EEE8CD", width=10, height=2,
                  pady=2).grid(
                row=row_index, column=6)

            laminaBox = []
            for i in range(totalLamina):
                row_index += 1
                dummyLabel = [f'Lamina {i+1}: ']
                laminaBox.append(definationWin.createEntry(allLabel=dummyLabel, index=row_index, width=12, boxNo=6))

            def save(message=True):
                for i in range(totalLamina):
                    definationWin.save(parameters= laminaBox[i][:], fileName=f'Data/Lamina{i+1}.dat', message=message)
                    message = False

            def load():
                for i in range(totalLamina):
                    definationWin.load(parameters=laminaBox[i][:], fileName=f'Data/Lamina{i+1}.dat')

            def copy():
                definationWin.save(parameters=laminaBox[0][:], fileName=f'Data/Lamina1.dat', message=False)
                for i in range(totalLamina):
                    definationWin.load(parameters=laminaBox[i][:], fileName=f'Data/Lamina1.dat')

            # Save, Load and Copy to all button
            saveButton = Button(definationWin, text="Save", bg="#FFF8DC", font='Helvetica 9', width=10,
                                height=2, command=save)
            saveButton.grid(row=row_index + 2, column=1)
            loadButton = Button(definationWin, text="Load", bg="#FFF8DC", font='Helvetica 9', width=10,
                                height=2, command=load)
            loadButton.grid(row=row_index + 2, column=2)
            copyButton = Button(definationWin, text="Copy to All", bg="#FFF8DC", font='Helvetica 9', width=10,
                                height=2, command=copy)
            copyButton.grid(row=row_index + 2, column=3)
            Label(definationWin, bg="#EEE8CD", font='Helvetica 12',
                      width=10, height=2, pady=2).grid(row=row_index+3, column=7)

        buttonDefineLamina = Button(definationWin, text="Add Lamina", bg="#FFF8DC", font='Helvetica 12', width=10,
                                      height=1, command=addLamina)
        buttonDefineLamina.grid(row=1, column=2)

    def laminateStiffness():
        stiffnessWin = NewWin(newWin, 'Laminate Stiffness', column=2)
        buttonStiffness.config(state='disabled')

        def closeWin():
            buttonStiffness.config(state='normal')
            stiffnessWin.destroy()

        stiffnessWin.protocol("WM_DELETE_WINDOW", closeWin)

        label = 'Choose an Option: '
        options = ['Define Stiffness', 'Calculate Stiffness']
        labelStiff = ['A', 'B', 'D']
        tempBox = []
        row_idx = 0
        for item in range(3):
            row_idx += 1
            Label(stiffnessWin, font='Helvetica 12', bg="#EEE8CD", width=5, height=1, pady=0).grid(
                row=row_idx, column=0)
            for j in range(3):
                row_idx += 1
                dummyLabel = ['']
                if j == 1:
                    dummyLabel = [f'[{labelStiff[item]}]  = ']
                if j == 2 and item == 0:
                    Label(stiffnessWin, text=f'GPa-mm', font='Helvetica 10', bg="#EEE8CD", width=7, height=1, pady=0).grid(
                        row=row_idx-1, column=9)
                if j == 2 and item == 1:
                    Label(stiffnessWin, text=f'GPa-mm\u00b2', font='Helvetica 10', bg="#EEE8CD", width=7, height=1, pady=0).grid(
                        row=row_idx-1, column=9)
                if j == 2 and item == 2:
                    Label(stiffnessWin, text=f'GPa-mm\u00b3', font='Helvetica 10', bg="#EEE8CD", width=7, height=1, pady=0).grid(
                        row=row_idx-1, column=9)
                tempBox.append(stiffnessWin.createEntry(allLabel=dummyLabel, index=row_idx, width=8, boxNo=3))

        # Disable Entry Box
        for i in tempBox:
            for j in i:
                j.config(state='disabled')

        def save(message=True):
            for i in range(9):
                stiffnessWin.save(parameters=tempBox[i], fileName=f'Data/Stiff{i+1}.dat', message=message)
                message = False

        def load():
            for i in range(9):
                stiffnessWin.load(parameters=tempBox[i], fileName=f'Data/Stiff{i+1}.dat')

        def calcMethod(*args):
            if method.get() == options[0]:
                process = 1
                for i in tempBox:
                    for j in i:
                        j.config(state='normal')
            elif method.get() == options[1]:
                process = 2
                for i in tempBox:
                    for j in i:
                        j.config(state='disabled')
            return process

        def calculate():
            LaminateAnalysis.LaminateStiffness()
            load()

        # Calculation Options
        Label(stiffnessWin, bg="#EEE8CD", font='Helvetica 12',
              width=10, height=2, pady=2).grid(row=row_idx + 1, column=9)
        method = stiffnessWin.createDropBox(label, options, row=2, column=10, width=18)

        method.trace('w', calcMethod)

        calcButton = Button(stiffnessWin, text="Calculate", bg="#FFF8DC", font='Helvetica 9', width=10,
                            height=2, command=calculate)
        calcButton.grid(row=5, column=10)
        Label(stiffnessWin, bg="#EEE8CD", font='Helvetica 12',
              width=10, height=2, pady=2).grid(row=row_idx+1, column=11)

        # Save and Load button
        saveButton = Button(stiffnessWin, text="Save", bg="#FFF8DC", font='Helvetica 9', width=10,
                            height=2, command=save)
        saveButton.grid(row=7, column=10)
        loadButton = Button(stiffnessWin, text="Load", bg="#FFF8DC", font='Helvetica 9', width=10,
                            height=2, command=load)
        loadButton.grid(row=9, column=10)

    def laminateStress():
        stressWin = NewWin(newWin, '', column=0)
        buttonLaminateStress.config(state='disabled')
        Label(stressWin, text='Strains', bg="#EEE8CD", justify=CENTER,
              font='Helvetica 12 bold').grid(row=0, column=1)
        Label(stressWin, text='Forces', bg="#EEE8CD", justify=CENTER,
              font='Helvetica 12 bold').grid(row=0, column=3)

        def closeWin():
            buttonLaminateStress.config(state='normal')
            stressWin.destroy()

        stressWin.protocol("WM_DELETE_WINDOW", closeWin)

        strainLabel = ['Strain in X, \u03B5x (\u00B5m/m): ',
                       'Strain in Y, \u03B5y (\u00B5m/m): ',
                       'X-Y Shear Strain, \u03B3xy (\u00B5m/m): ',
                       'X-Z Bending, \u03BAx (mm/m\u00b2): ',
                       'Y-Z Bending, \u03BAy (mm/m\u00b2): ',
                       'Twisting Curvature, \u03BAxy (mm/m\u00b2): ']

        parameters_strain = stressWin.createEntry(strainLabel, index=1, column=0)

        forceLabel = ['Nx (MPa-mm): ',
                      'Ny (MPa-mm): ',
                      'Nxy (MPa-mm): ',
                      'Mx (MPa-mm\u00b2): ',
                      'My (MPa-mm\u00b2): ',
                      'Mxy (MPa-mm\u00b2): ']

        parameters_force = stressWin.createEntry(forceLabel, index=1, column=2)

        # Disable Entry Box
        for i in parameters_strain:
            i.config(state='disabled')
        for i in parameters_force:
            i.config(state='disabled')

        laminateStrainFile = 'Data/LaminateStrains.dat'
        laminateStressFile = 'Data/LaminateStresses.dat'

        label = 'Method of Calculation: '
        options = ['Calculate Strains', 'Calculate Forces']

        def save(process=0, message=True):
            if process == 1:
                # Save Stresses
                stressWin.save(parameters_force, fileName=laminateStressFile, message=message)
            elif process == 2:
                # Save Strains
                stressWin.save(parameters_strain, fileName=laminateStrainFile, message=message)
            else:
                # Save Strains
                stressWin.save(parameters_strain, fileName=laminateStrainFile, message=message)
                # Save Stresses
                stressWin.save(parameters_force, fileName=laminateStressFile, message=message)

        def load():
            # Load Strains
            stressWin.load(parameters_strain, fileName=laminateStrainFile)
            # Load Stresses
            stressWin.load(parameters_force, fileName=laminateStressFile)

        def calcMethod(*args):
            if method.get() == options[0]:
                process = 1
                for i in range(len(parameters_strain)):
                    parameters_force[i].config(state='normal')
                    parameters_strain[i].config(state='disabled')
            elif method.get() == options[1]:
                process = 2
                for i in range(len(parameters_force)):
                    parameters_strain[i].config(state='normal')
                    parameters_force[i].config(state='disabled')
            return process

        def calculate():
            process = calcMethod()
            save(process, message=False)
            if process == 1:
                LaminateAnalysis.LaminateStrain()
            elif process == 2:
                LaminateAnalysis.LaminateStress()
            load()

        # Save and Load Buttons
        Label(stressWin, bg="#EEE8CD", width=30, height=2, pady=2).grid(row=9, column=2)
        Label(stressWin, bg="#EEE8CD", width=30, height=2, pady=2).grid(row=12, column=2)
        saveButton = Button(stressWin, text="Save", bg="#FFF8DC", font='Helvetica 9', width=10,
                            height=2, command=save)
        saveButton.grid(row=11, column=0)

        loadButton = Button(stressWin, text="Load", bg="#FFF8DC", font='Helvetica 9', width=10,
                            height=2, command=load)
        loadButton.grid(row=11, column=1)

        # Calculation Options
        method = stressWin.createDropBox(label, options, row=10, column=2)

        method.trace('w', calcMethod)

        calcButton = Button(stressWin, text="Calculate", bg="#FFF8DC", font='Helvetica 9', width=10,
                            height=2, command=calculate)
        calcButton.grid(row=11, column=3)

    # Laminate Win Definition
    newWin = NewWin(winMain, 'Determine Laminate Properties')
    buttonLaminate.config(state='disabled')

    def closeWin():
        buttonLaminate.config(state='normal')
        newWin.destroy()

    newWin.protocol("WM_DELETE_WINDOW", closeWin)

    buttonDefineLaminate = Button(newWin, text="Define Laminate", bg="#FFF8DC", font='Helvetica 12', width=30,
                         height=2, command=laminateDefination)
    buttonDefineLaminate.grid(row=2, column=1)

    buttonStiffness = Button(newWin, text="Determine/Define Stiffness", bg="#FFF8DC", font='Helvetica 12', width=30,
                         height=2, command=laminateStiffness)
    buttonStiffness.grid(row=3, column=1)

    buttonLaminateStress = Button(newWin, text="Determine Strains/Forces", bg="#FFF8DC", font='Helvetica 12', width=30,
                         height=2, command=laminateStress)
    buttonLaminateStress.grid(row=4, column=1)

    Label(newWin, bg="#EEE8CD", font='Helvetica 12', width=25,
                         height=2).grid(row=6,column=0)
    Label(newWin, bg="#EEE8CD", font='Helvetica 12', width=25,
          height=2).grid(row=7, column=3)

winMain = Tk()
winMain.title('Composite Material Solver')
winMain.resizable(False, False)


frameMain = Frame(winMain, bg="#EEE8CD")
frameMain.grid(row=0, column=0)

labelMain = Label(frameMain, text='Composite Material Solver', bg="#EEE8CD", font='Helvetica 16 bold', padx=280, pady=30)
labelMain.grid(row=0, column=0)

buttonFiber = Button(frameMain, text="Define Fiber Properties", bg="#FFF8DC", font='Helvetica 12', width=30,
                     height=2, command=fiber)
buttonFiber.grid(row=1, column=0)

buttonMatrix = Button(frameMain, text="Define Matrix Properties", bg="#FFF8DC", font='Helvetica 12', width=30,
                      height=2, command=matrix)
buttonMatrix.grid(row=2, column=0)

buttonLamina = Button(frameMain, text="Define/Analyze Lamina", bg="#FFF8DC", font='Helvetica 12', width=30,
                      height=2, command=lamina)
buttonLamina.grid(row=3, column=0)

buttonStress = Button(frameMain, text="Lamina Strain, Stress and Failure", bg="#FFF8DC", font='Helvetica 12', width=30,
                      height=2, command=stress)
buttonStress.grid(row=4, column=0)

buttonLaminate = Button(frameMain, text="Laminated Plate with Coupling", bg="#FFF8DC", font='Helvetica 12', width=30,
                        height=2, command=laminate)
buttonLaminate.grid(row=5, column=0)

labelRef = Label(frameMain, text='References: \n'
                               '1. Principles of Composite Material Mechanics 4th Edition, By Ronald F. Gibson\n'
                               '2. Mechanics of Composite Materials 2nd Edition, By Autar K. Kaw',
                 font='Helvetica 8 bold', justify=LEFT, bg=	"#EEE8CD", padx=20, pady=50)
labelRef.grid(row=6, sticky = W)
labelDev = Label(frameMain, text='Developed By: \n'
                               'A. K. M. Samiu Haque Barnil',
                 font='Helvetica 8 bold', justify=LEFT, bg=	"#EEE8CD", padx=10, pady=50)
labelDev.grid(row=6, sticky = E)

winMain.mainloop()
