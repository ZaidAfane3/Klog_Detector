import pefile 
import os 
import sys

Sus_APIs = ["GetKeyState", "GetKeyboardState", "SetWindowsHookExA", "GetAsyncKeyState"]
Default_Dir = "Keylogger"
result = {
}


def Usage ():
    print ("""

    Usage: klog <command> [option]

    Commands:
        -f "PATH_TO_FILE/file_name.exe"      Use a specific file 
        -d "PATH_TO_DIRECOTRY"               List and choose from a directory 
        -k                                   Use the tools default keylogger directory
    
    Note:
        To use -k, copy and paste the the excutables to test to /Keylogger directory 
    """)

def choose_file (Dir=Default_Dir):
    Malwares = os.listdir(Dir)
    print ('[*] %d executables were found in "%s"'%(len(Malwares), Dir))
    for i in range(len(Malwares)):
        print ("\t%d-"%(i+1), Malwares[i])
    malwre = int(input("[-] Please Choose which Malware to use: "))
    return Dir+"\\"+Malwares[malwre]

def print_list (alist):
    for i in alist:
            print (i)

def export_APIs_from_excutable (exe):
    APIs = list()
    pe = pefile.PE(exe)
    for entry in pe.DIRECTORY_ENTRY_IMPORT: 
        for API in entry.imports:
            APIs.append(API.name.decode())
    APIs.sort()
    return APIs



def get_key_api (alist):
    api = list()
    global Sus_APIs 
    count = 0
    for i in range(len(alist)):
        if "Key" in alist[i]:
            if alist[i] in Sus_APIs:
                count += 1 
            api.append(alist[i])
    
    return api


if len(sys.argv) < 2 or len(sys.argv) > 2 :
    Usage()
    exit(0)
elif sys.argv[1] == "-k":
    f = choose_file()
elif sys.argv[1] == "-d":
    f = choose_file(sys.argv[2])
elif sys.argv[1] == "-f":
    f = sys.argv[2]
else:
    Usage()
    exit(0)
result["File"] = f 
result["APIs"] = export_APIs_from_excutable(f)

print(result)


# APIs_2, count_1, count_2 = get_key_api(APIs)
# if not count_1 : 
#     print ("[-] There is no keyboard APIs here which means mostly this isn't a Keylogger")
# else:
#     print ("[!] %d APIs related to keyboard where found in this excutable"%(count_1))
#     print ("\n##### Keyboard APIs #####")
#     for i in APIs_2:
#         print ("\t=>" , i)
#     print ("#########################\n")
#     if (count_2 >= 2 ):
#         print ("[!] %d of these malwares are detected as suspicious, this is highly to be a Keylogger"%(count_2))
#     else: 
#         print ("[!] None of these APIs detected as suspicious")