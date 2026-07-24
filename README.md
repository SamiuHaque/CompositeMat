# CompositeMat

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-Tkinter-informational)](https://docs.python.org/3/library/tkinter.html)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

**CompositeMat** is a Python-based desktop application for analyzing the engineering properties and mechanical response of unidirectional composite laminae and laminated plates. It provides a graphical user interface for material definition, micromechanical property estimation, lamina stress–strain analysis, failure checking, and laminate stiffness calculations based on Classical Lamination Theory (CLT).

The program is intended primarily for educational use, preliminary engineering calculations, and verification of hand calculations.

## Features

### Constituent material definition

- Define the elastic properties of fiber and matrix materials.
- Define longitudinal, transverse, and shear strengths.
- Save and reload material data for later calculations.

### Lamina property calculation

Determine equivalent orthotropic lamina properties using:

- Manual property definition
- Strength-of-materials approach
- Semi-empirical approach using Halpin–Tsai-type relations

Calculated properties include:

- Longitudinal modulus, `E1`
- Transverse modulus, `E2`
- Major and minor Poisson's ratios, `ν12` and `ν21`
- In-plane shear modulus, `G12`
- Longitudinal tensile and compressive strengths
- Transverse tensile and compressive strengths
- In-plane shear strength

### Lamina stress, strain, and failure analysis

- Calculate lamina strains from applied stresses.
- Calculate lamina stresses from applied strains.
- Account for lamina orientation through transformed stiffness matrices.
- Check individual stress components against tensile, compressive, and shear limits using a maximum-stress-type criterion.

### Laminated plate analysis

- Define an arbitrary number of lamina plies.
- Assign elastic properties, orientation angle, and thickness to each ply.
- Copy a common lamina definition to all plies when required.
- Calculate the laminate extensional, coupling, and bending stiffness matrices:
  - `[A]` — extensional stiffness
  - `[B]` — extension–bending coupling stiffness
  - `[D]` — bending stiffness
- Calculate mid-plane strains and curvatures from applied force and moment resultants.
- Calculate force and moment resultants from prescribed strains and curvatures.

## Governing Relationship

The laminate calculations are based on the Classical Lamination Theory relationship:

```text
┌ N ┐   ┌ A  B ┐ ┌ ε⁰ ┐
│   │ = │      │ │    │
└ M ┘   └ B  D ┘ └ κ  ┘
```

where:

- `N` is the vector of in-plane force resultants.
- `M` is the vector of moment resultants.
- `ε⁰` is the vector of laminate mid-plane strains.
- `κ` is the vector of laminate curvatures.

## Requirements

- Python 3
- NumPy 1.25.2
- Tkinter
- A desktop environment capable of displaying Tk windows

Tkinter is included with most standard Python installations. It should not be replaced by the unrelated `tk` package from PyPI. The recommended contents of `requirements.txt` are therefore:

```text
numpy==1.25.2
```

You can verify that Tkinter is available by running:

```bash
python -m tkinter
```

A small demonstration window should open if Tkinter is installed correctly.

## Installation

Clone the repository:

```bash
git clone https://github.com/SamiuHaque/CompositeMat.git
cd CompositeMat
```

Create and activate a virtual environment.

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install NumPy:

```bash
python -m pip install --upgrade pip
python -m pip install numpy==1.25.2
```

Create the runtime data directory used by the application:

```bash
mkdir Data
```

On Debian- or Ubuntu-based Linux systems, install Tkinter separately if it is unavailable:

```bash
sudo apt install python3-tk
```

## Running the Program

From the repository root, run:

```bash
python CompositeSolver.py
```

The main **Composite Material Solver** window will open.

## Recommended Workflow

1. Select **Define Fiber Properties** and enter the fiber engineering constants and strengths.
2. Select **Define Matrix Properties** and enter the matrix properties.
3. Open **Define/Analyze Lamina**.
4. Select a lamina calculation method and enter the fiber volume fraction where required.
5. Save the calculated or manually defined lamina properties.
6. Use **Lamina Strain, Stress and Failure** for transformed stress–strain calculations and failure checking.
7. Use **Laminated Plate with Coupling** to define a stacking sequence, calculate the `[A]`, `[B]`, and `[D]` matrices, and solve for laminate forces or deformations.

## Input Units

Use the units displayed in the interface consistently.

| Quantity | Unit |
|---|---:|
| Elastic and shear moduli | GPa |
| Material strengths and stresses | MPa |
| Lamina orientation | degrees |
| Ply thickness | mm |
| Normal and shear strains | µm/m |
| Curvatures | mm/m², as displayed in the GUI |
| In-plane force resultants | MPa·mm |
| Moment resultants | MPa·mm² |

## Project Structure

```text
CompositeMat/
├── CompositeSolver.py     # Tkinter GUI and application entry point
├── DefMaterial.py         # Shared data container for material and result values
├── LaminaConstants.py     # Micromechanical lamina-property calculations
├── LaminaAnalysis.py      # Lamina stiffness, transformations, and failure checks
├── LaminateAnalysis.py    # Classical Lamination Theory calculations
├── requirements.txt       # Python dependency list
├── LICENSE                # GNU General Public License v3.0
├── README.md
└── Data/                  # Runtime calculation data generated by the program
```

## Data Storage

The application stores material definitions, stiffness matrices, loads, strains, and other intermediate results as Python pickle files in the `Data/` directory.

> **Security note:** Do not load `.dat` files obtained from untrusted sources. Python pickle files may execute malicious code when opened.

## Current Limitations

- The tool is intended for linear-elastic lamina and laminate calculations.
- Failure checking is limited to direct comparison of transformed stress components with allowable strengths.
- Advanced criteria such as Tsai–Hill, Tsai–Wu, Hashin, Puck, progressive damage, and nonlinear response are not currently included.
- Laminate-level ply stress recovery and ply-by-ply failure analysis are not currently provided.
- Hygrothermal effects, manufacturing defects, and interlaminar stresses are outside the present scope.
- Input validation and automated report generation are limited.

Results should be independently checked before being used for design, certification, manufacturing, or other safety-critical engineering decisions.

## References

The implementation was developed with reference to:

1. Ronald F. Gibson, *Principles of Composite Material Mechanics*, 4th Edition.
2. Autar K. Kaw, *Mechanics of Composite Materials*, 2nd Edition.

## Contributing

Contributions, corrections, and feature suggestions are welcome. To contribute:

1. Fork the repository.
2. Create a feature branch.
3. Make and test your changes.
4. Submit a pull request with a clear description of the modification.

## License

This project is distributed under the **GNU General Public License v3.0**. See the [LICENSE](LICENSE) file for details.

## Author

Developed by **A. K. M. Samiu Haque Barnil**.

GitHub: [SamiuHaque](https://github.com/SamiuHaque)
