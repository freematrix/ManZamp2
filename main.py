from func import *
#import subprocess as Popen
#import subprocess as sp

#prog = sp.Popen(['runas', '/noprofile', '/user:Administrator', 'NeedsAdminPrivilege.exe'],stdin=sp.PIPE)
#prog.stdin.write('password')
#prog.communicate()

#import subprocess
#subprocess.Popen(['runas', '/noprofile', '/user:Administrator', "notepad.exe","c:\\windows\\system32\\drivers\\etc\\hosts"],stdin=subprocess.PIPE)

def runprogramm_as_admin():
    if not isUserAdmin():
        runAsAdmin(['notepad.exe', "c:\\windows\\system32\\drivers\\etc\\hosts"], False)
    else:
        print("You are an admin!", os.getpid(), "params: ", sys.argv)
        

def checkporta():
    print(portaOccupata(['netstat', '-aon'], 80))

def runMioProgram():
    import sys
    import asyncio
    out, err = asyncio.run(runProgram(["Q:\\SVL\\zamp\\zamp_1.1.2\\Apps\\Apache24\\bin\\httpd.exe"]))
    print("out", out)
    print("err", err)
    


if __name__ == "__main__":
    runMioProgram()