# Template for material definition
class DefMaterial:
    def __init__(self, dataList=[]):
        self.E1 = dataList[0]       # Also represents eps1 (Strain) or sigma1 (Stress) or Nx
        self.E2 = dataList[1]       # Also represents eps2 (Strain) or sigma2 (Stress) or Ny
        self.neu12 = dataList[2]    # Also represents gamma12 (Strain) or tow12 (Stress) or Nxy
        if len(dataList) > 3:
            self.G = dataList[3]            # Also represents X-Z Bending or Mx
            self.sig1T_ult = dataList[4]    # Also represents Ply Angle (theta) or Y-Z Bending or My
            self.sig1C_ult = dataList[5]    # Also represents Ply thickness and Twisting or Mxy
            if len(dataList) > 6:
                self.sig2T_ult = dataList[6]
                self.sig2C_ult = dataList[7]
                self.tow12_ult = dataList[8]
                self.neu21 = (self.neu12 * self.E2) / self.E1
