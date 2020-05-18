import pefile 
import os 
import sys

Sus_APIs = ["GetKeyState", "GetKeyboardState", "SetWindowsHookExA", "GetAsyncKeyState", "GetKeyboardLayout"]
Default_Dir = "Keylogger"
result = {}


def Usage ():
    print ("""

    Usage: klog <command> [option]

    Commands:
        -f "PATH_TO_FILE/file_name.exe"      Use a specific file 
        -d "PATH_TO_DIRECOTRY"               List and choose from a directory  
        -k                                   Use the tools default keylogger directory
    
    Note:
        - To use -k, copy and paste the the excutables to test to /Keylogger directory 
        - To use -d and -f, the path should be between double quotation marks 
    """)

def choose_file (Dir=Default_Dir):
    Malwares = os.listdir(Dir+"\\")
    print ('[*] %d executables were found in "%s"'%(len(Malwares), Dir))
    for i in range(len(Malwares)):
        print ("\t%d-"%(i+1), Malwares[i])
    malwre = int(input("[-] Please Choose which Malware to use: "))
    return Dir+"\\"+Malwares[malwre-1]

def print_list (alist):
    for i in alist:
            print (i)

def export_APIs_from_excutable ():
    global result
    APIs = list()
    pe = pefile.PE(result["File"])
    for entry in pe.DIRECTORY_ENTRY_IMPORT: 
        for API in entry.imports:
            APIs.append(API.name.decode())
    APIs.sort()
    result["APIs"] = {"All":APIs}

def get_key_api ():
    global result 
    api = result["APIs"]["All"]
    result["APIs"]["Suspicious"] = {"Count":0,"Keyboard":[],"None-Keyboard":[]}
    global Sus_APIs
    for i in range(len(api)):
        if api[i] in Sus_APIs:
            result["APIs"]["Suspicious"]["Count"] +=1 
            if "Key" in api[i]:
                result["APIs"]["Suspicious"]["Keyboard"].append(api[i])
                continue
            result["APIs"]["Suspicious"]["None-Keyboard"].append(api[i])


if len(sys.argv) < 2 :
    Usage()
    print (sys.argv)
    exit(0)
elif sys.argv[1] == "-k":
    f = choose_file()
elif sys.argv[1] == "-d":
    print ()
    f = choose_file("".join(sys.argv[2::]))
elif sys.argv[1] == "-f":
    f = "".join(sys.argv[2::])
else:
    print (sys.argv)
    Usage()
    exit(0)

result["File"] = f 
export_APIs_from_excutable()
get_key_api()
# print(result)

print ()

if  result["APIs"]["Suspicious"]["Count"] == 0: 
    print ("[*] There is no suspicious APIs here which means mostly this isn't a Keylogger or it maybe it's Obfuscated")
else:
    print ("[!] %d APIs has been detected as suspicious and might be used in KEYLOGGERS"%(len(result["APIs"]["Suspicious"])))
    if len(result["APIs"]["Suspicious"]["Keyboard"]) > 0:
        print ("[!] ITS A KEYLOGGER !!!")
    else: 
        print ("[!] There is keystrokes APIs detected but there is a WindowsHook intercepts interrupts in the system")
print ()
print (result["APIs"]["Suspicious"])
