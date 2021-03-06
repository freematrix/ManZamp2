#import subprocess as Popen
#import subprocess as sp

#prog = sp.Popen(['runas', '/noprofile', '/user:Administrator', 'NeedsAdminPrivilege.exe'],stdin=sp.PIPE)
#prog.stdin.write('password')
#prog.communicate()

#import subprocess
#subprocess.Popen(['runas', '/noprofile', '/user:Administrator', "notepad.exe","c:\\windows\\system32\\drivers\\etc\\hosts"],stdin=subprocess.PIPE)


import sys, os, traceback, types
import typing



def check_port_occupata(porta: int) -> bool:
    import socket, errno
    bok = False

    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind(('', porta)) ## Try to open port
        except OSError as e:
            if e.errno == 98: ## Errorno 98 means address already bound
                bok = True
            raise e
        s.close()
        bok = False
        
    
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", porta))
        bok = True
    except socket.error as e:
        if e.errno == errno.EADDRINUSE:
            print("Port is already in use")
        else:
            # something else raised the socket.error exception
            print(e)

    s.close()
    """
    return bok

def portaOccupata(listaProgrammaEParams, porta):
    import re
    out, err = runProgram(listaProgrammaEParams)
    x = re.search("0\\.0\\.0\\.0:" + str(porta) + ".+LISTENING", str(out))
    if x:
        return True
    else:
        return False


async def runProgram(listaProgrammaEParams):
    #import subprocess
    import asyncio
    proc = await asyncio.create_subprocess_exec(listaProgrammaEParams,stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE)
    #p = subprocess.Popen(listaProgrammaEParams, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #out, err = p.communicate()
    out, err = await proc.communicate()
    return out, err
    


def isUserAdmin():

    if os.name == 'nt':
        import ctypes
        # WARNING: requires Windows XP SP2 or higher!
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            traceback.print_exc()
            print ("Admin check failed, assuming not an admin.")
            return False
    elif os.name == 'posix':
        # Check for root on Posix
        return os.getuid() == 0
    else:
        raise RuntimeError("Unsupported operating system for this module: %s" % (os.name,))

def runAsAdmin(cmdLine=None, wait=True):

    if os.name != 'nt':
        raise RuntimeError("This function is only implemented on Windows.")

    import win32api, win32con, win32event, win32process
    from win32com.shell.shell import ShellExecuteEx
    from win32com.shell import shellcon


    cmd = '"%s"' % (cmdLine[0],)
    #print("programma", cmd)
    params = " ".join(['"%s"' % (x,) for x in cmdLine[1:]])
    #print("params", params)
    showCmd = win32con.SW_SHOWNORMAL
    #showCmd = win32con.SW_HIDE
    lpVerb = 'runas'  # causes UAC elevation prompt.

    # print "Running", cmd, params

    # ShellExecute() doesn't seem to allow us to fetch the PID or handle
    # of the process, so we can't get anything useful from it. Therefore
    # the more complex ShellExecuteEx() must be used.

    # procHandle = win32api.ShellExecute(0, lpVerb, cmd, params, cmdDir, showCmd)

    procInfo = ShellExecuteEx(nShow=showCmd,fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,lpVerb=lpVerb,lpFile=cmd,lpParameters=params)

    if wait:
        procHandle = procInfo['hProcess']    
        obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
        rc = win32process.GetExitCodeProcess(procHandle)
        #print "Process handle %s returned code %s" % (procHandle, rc)
    else:
        rc = None

    return rc

"""
def test111():
    rc = 0
    if not isUserAdmin():
        print("You're not an admin.", os.getpid(), "params: ", sys.argv)
        #rc = runAsAdmin(["c:\Windows\notepad.exe"])
        rc = runAsAdmin(['notepad.exe', "c:\\windows\\system32\\drivers\\etc\\hosts"], False)
    else:
        print("You are an admin!", os.getpid(), "params: ", sys.argv)
        rc = 0
    x = input('Press Enter to exit.')
    return rc
"""

if __name__ == "__main__":
    pass
    #print(type(['lis','aas']))
    #exit()
    