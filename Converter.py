
import subprocess
import pyperclip
string = ""
counter = 0
def replace(old:str, new:str):
    global string, counter
    if string.find(old) != -1:
        string = string.replace(old, new)
        counter += 1
    # change all instances of old to new

        


def translatetoPython():
    
    global counter, string
    string= "  " + string + "  "
    string = string.replace("=", "")
    string = string.replace("ROT", "sqrt")
    string = string.replace("^2", "**2 ")
    string = string.replace("(", " ( ")
    string = string.replace(")", " ) ")
    string = string.replace("-", " - ")
    string = string.replace("+", " + ")
    string = string.replace("/", " / ")
    string = string.replace("*", " * ")
    string = string.replace(" $O$9 ", " self.Mass ")
    string = string.replace(" $O$10 "," self.Radius ")
    string = string.replace(" $O$2 ", " self.Gravity ")
    string = string.replace(" $O$12 "," self.MomentsOfInertia.x ")
    string = string.replace(" $O$13 "," self.MomentsOfInertia.y ")
    string = string.replace(" $O$14 "," self.MomentsOfInertia.z ")
    string = string.replace(" $E$6 ", " self.r0.x ")
    string = string.replace(" $E$7 ", " self.r0.y ")
    string = string.replace(" $E$8 ", " self.r0.z ")
    string = string.replace(" I23 ",  " self._r_factor ")
    string = string.replace(" J23 ",  " self._mag.x ")
    string = string.replace(" K23 ",  " self._mag.y ")
    string = string.replace(" L23 ",  " self._mag.z ")
    string = string.replace(" AA22 ", " self.angularVelocity.y ")
    string = string.replace(" AB22 ", " self.angularVelocity.z ")
    string = string.replace(" AC22 ", " self.velocity.x ")
    string = string.replace(" AD22 ", " self.velocity.y ")
    string = string.replace(" AE22 ", " self.theta[0] ")
    string = string.replace(" AF22 ", " self.theta[1] ")
    string = string.replace(" AG22 ", " self.theta[2] ")
    string = string.replace(" AH22 ", " self.theta[3] ")
    string = string.replace(" AI22 ", " self.theta[4] ")
    string = string.replace(" AJ22 ", " self.theta[5] ")
    string = string.replace(" AK22 ", " self.a1 ")
    string = string.replace(" AL22 ", " self.b1 ")
    string = string.replace(" AM22 ", " self.c1 ")
    string = string.replace(" AN22 ", " self.d1 ")
    string = string.replace(" AO22 ", " self.a2 ")
    string = string.replace(" AP22 ", " self.b2 ")
    string = string.replace(" AQ22 ", " self.c2 ")
    string = string.replace(" AR22 ", " self.d2 ")
    string = string.replace(" AS22 ", " self.a3 ")
    string = string.replace(" AT22 ", " self.b3 ")
    string = string.replace(" AU22 ", " self.c3 ")
    string = string.replace(" AV22 ", " self.d3 ")
    string = string.replace(" AW22 ", " self.angularAcceleration.x ")
    string = string.replace(" AX22 ", " self.angularAcceleration.y ")
    string = string.replace(" AY22 ", " self.angularAcceleration.z ")
    string = string.replace(" AZ22 ", " self.globalAcceleration.x ")
    string = string.replace(" BA22 ", " self.globalAcceleration.y ")
    string = string.replace(" BB22 ", " self.fs.x ")
    string = string.replace(" BC22 ", " self.fs.y ")
    string = string.replace(" BD22 ", " self.N ")
    string = string.replace(" BG22 ", " self.k_friction ")
    string = string.replace(" BK23 ", " self._r_factor ")
    string = string.replace(" BL23 ", " self._mag.x ")
    string = string.replace(" BM23 ", " self._mag.y ")
    string = string.replace(" BN23 ", " self._mag.z ")
    string = string.replace(" BO22 ", " self.Time ")
    string = string.replace(" BP22 ", " self.lmnX.x ")
    string = string.replace(" BQ22 ", " self.lmnX.y ")
    string = string.replace(" BR22 ", " self.lmnX.z ")
    string = string.replace(" BS22 ", " self.lmnY.x ")
    string = string.replace(" BT22 ", " self.lmnY.y ")
    string = string.replace(" BU22 ", " self.lmnY.z ")
    string = string.replace(" BV22 ", " self.lmnZ.x ")
    string = string.replace(" BW22 ", " self.lmnZ.y ")
    string = string.replace(" BX22 ", " self.lmnZ.z ")
    string = string.replace(" BY22 ", " self.r.x ")
    string = string.replace(" BZ22 ", " self.r.y ")
    string = string.replace(" CA22 ", " self.r.z ")
    string = string.replace(" CB22 ", " self.angularVelocity.x ")
    string = string.replace(" CC22 ", " self.angularVelocity.y ")
    string = string.replace(" CD22 ", " self.angularVelocity.z ")
    string = string.replace(" CE22 ", " self.velocity.x ")
    string = string.replace(" CF22 ", " self.velocity.y ")
    string = string.replace(" CG22 ", " self.theta[0] ")
    string = string.replace(" CH22 ", " self.theta[1] ")
    string = string.replace(" CI22 ", " self.theta[2] ")
    string = string.replace(" CJ22 ", " self.abcd1.a ")
    string = string.replace(" CK22 ", " self.abcd1.b ")
    string = string.replace(" CL22 ", " self.abcd1.c ")
    string = string.replace(" CM22 ", " self.abcd1.d ")
    string = string.replace(" CN22 ", " self.abcd2.a ")
    string = string.replace(" CO22 ", " self.abcd2.b ")
    string = string.replace(" CP22 ", " self.abcd2.c ")
    string = string.replace(" CQ22 ", " self.abcd2.d ")
    string = string.replace(" CR22 ", " self.abcd3.a ")
    string = string.replace(" CS22 ", " self.abcd3.b ")
    string = string.replace(" CT22 ", " self.abcd3.c ")
    string = string.replace(" CU22 ", " self.abcd3.d ")
    string = string.replace(" CV22 ", " self.angularAcceleration.x ")
    string = string.replace(" CW22 ", " self.angularAcceleration.y ")
    string = string.replace(" CX22 ", " self.angularAcceleration.z ")
    string = string.replace(" CY22 ", " self.acceleration.x ")
    string = string.replace(" CZ22 ", " self.acceleration.y ")
    string = string.replace(" DA22 ", " self.forces.x ")
    string = string.replace(" DB22 ", " self.forces.y ")
    string = string.replace(" DC22 ", " self.N ")
    string = string.replace(" DG22 ", " self.position.x ")
    string = string.replace(" DH22 ", " self.position.y ")
    string = string.replace(" DI22 ", " self.s_friction ")
    string = string.replace(" $N$16 "," self.timestep ")
    string = string.replace(" N22 ",  " self.lmnX.x ")
    string = string.replace(" O22 ",  " self.lmnX.y ")
    string = string.replace(" P22 ",  " self.lmnX.z ")
    string = string.replace(" Q22 ",  " self.lmnY.x ")
    string = string.replace(" R22 ",  " self.lmnY.y ")
    string = string.replace(" S22 ",  " self.lmnY.z ")
    string = string.replace(" T22 ",  " self.lmnZ.x ")
    string = string.replace(" U22 ",  " self.lmnZ.y ")
    string = string.replace(" V22 ",  " self.lmnZ.z ")
    string = string.replace(" W22 ",  " self.r.x ")
    string = string.replace(" X22 ",  " self.r.y ")
    string = string.replace(" Y22 ",  " self.r.z ")
    string = string.replace(" Z22 ",  " self.angularVelocity.x ")
    string = string.replace("   ",  "  ")
    string = string.replace("  ",  " ")
    string = string.replace(" ",  "")
    
    print("Copied to clipboard:\n",string)

def getClipboardData():
    # Open the clipboard with tkinter
    data = pyperclip.paste()

    return data

def setClipboardData(data:str):
    pyperclip.copy(data)
if __name__ == "__main__":
    # string = input("Enter the string: ")
    string = getClipboardData()

    translatetoPython()
    setClipboardData(string.strip())

    # cmd='echo '+string.strip()+'|clip'
    # subprocess.check_call(cmd, shell=True)
    # (-u_k*mass*(angularacceleration.x*r.y-angularacceleration.y*r.x+gravity+theta1)*(velocity.x-radius*angularvelocity.y)/sqrt((velocity.x-radius*angularvelocity.y)**2+(velocity.y+radius*angularvelocity.x)**2))/mass-(angularacceleration.y*r.z-angularacceleration.z*r.y)-theta3
