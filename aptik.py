#!/usr/bin/env python
#2023-2023 plasticgaming99 (plsplastic_roblox@protonmail.com)

#EDIT TO YOUR BUILD USER
aptik_user="plastek"

import sys
args = sys.argv
import os
import git
import urllib.request
import tqdm
import shutil
import subprocess
import pyalpm

handle = pyalpm.Handle("/", "/var/lib/pacman")
localdb = pyalpm.Handle.get_localdb(handle)

#init global variables
madenpack = ""
aptikex = ""

class promptcolor:
    CYAN = '\033[94m'
    GREEN = '\033[92m'
    END = '\033[0m'

def subcall(some,dir):
    subprocess.call(some,cwd=dir,shell=True)

def yes_no_input(dialog,yn):
    while True:
        choice = input().lower()
        if choice in ['y', 'ye', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        elif choice in ['']:
            if yn == "y":
                return True
            elif yn == "n":
                return False
            

def chkdir(x):
    #check directory is avaliable
    while True:
        if os.path.exists(input(x)):
            return True
        else:
            os.makedirs(input(x))
            return False

def makepackage(package, repourl, localdir, asdeps):
    #make package
    while True:
        #init local var
        reqmakedepend=[]
        #clone repo with gitpython
        print(f"{promptcolor.GREEN}==>{promptcolor.END} Setting Clone repo to aptik_user_home/.cache/aptik/repo")
        repo_dir = localdir + package
        if(os.path.exists(repo_dir) == True):
            shutil.rmtree(repo_dir)
        subcall(f"git clone {repourl}", localdir)
        print(f"{promptcolor.GREEN}==>{promptcolor.END} Checking Makedepends...")
        makedependsspace = subprocess.run(["source PKGBUILD ; echo ${makedepends[*]}"], shell=True, stdout=subprocess.PIPE, text=True, check=True, cwd=repo_dir, executable="/usr/bin/bash").stdout
        makedepends = makedependsspace.split()
        checkdependsspace = subprocess.run(["source PKGBUILD ; echo ${checkdepends[*]}"], shell=True, stdout=subprocess.PIPE, text=True, check=True, cwd=repo_dir, executable="/usr/bin/bash").stdout
        checkdepends = checkdependsspace.split()
        makedepends = makedepends + checkdepends
        #make makedepends
        if len(makedepends) > 0:
            #make makedepends
            argsnow = 0
            print(f"{promptcolor.GREEN}==>{promptcolor.END} Preparing for Makedepends...")
            print(makedepends)
            while not (argsnow == len(makedepends)):
                print(localdb.get_pkg(makedepends[argsnow]))
                if localdb.get_pkg(makedepends[argsnow]) == None:
                    reqmakedepend.append(makedepends[argsnow])
                argsnow = argsnow + 1
            #install makedepends
            argsnow = 0
            while not (argsnow == len(reqmakedepend)):
                if reqmakedepend == []:
                    break
                if len(reqmakedepend) == 0:
                    continue
                print(reqmakedepend)
                if localdb.get_pkg(reqmakedepend[argsnow]) != None:
                    continue
                repo_url = f"https://gitlab.archlinux.org/archlinux/packaging/packages/" + package + ".git"
                print(argsnow)
                makepackage(reqmakedepend[argsnow], repo_url, localdir, True)
                argsnow = argsnow + 1
        if asdeps == True:
            print(f"{promptcolor.GREEN}==>{promptcolor.END} Installing Makedepends...")
        subprocess.call('chown -R ' + aptik_user + ":" + aptik_user + " " + repo_dir, shell=True)
        print(f"{promptcolor.GREEN}==>{promptcolor.END} Making package...")
        subprocess.call('sudo -u ' + aptik_user + ' makepkg', cwd=repo_dir, shell=True)

        return True

def chkroot():
    #check that executed by root
    if(os.getuid() != 0):
        print("Please run this command with root.")
        quit(1)

#init var of main
asdepend=False
noconfirm=False
jwpacman=False
needed=False
argtypelist=[]
packagestoins=[]
packagefulldir=[]

if not (len(args) == 1):
    if(args[1] == "install"):
        from pyalpm import Package
        #check root
        chkroot()
        #parse arguments. NO ARGUMENT SANDWICH ALLOWED
        if len(args) <= 2:
            print("Input some packages plz!!")
            quit()
        aargs = len(args) - 1

        #args without 1,2
        argsnow = 2
        argsonlyoptions=[]
        while not (argsnow == len(args)):
            argsonlyoptions.append(args[argsnow])
            argsnow = argsnow + 1

        #check input. packages or options.
        argsnow = 2
        while not (argsnow == len(args)):
            if ("-" == args[argsnow][0]):
                argtypelist.append("1")
            else:
                argtypelist.append("2")
            argsnow = argsnow + 1

        #parse input. like options
        argsnow = 0
        while not (argsnow == len(argsonlyoptions)):
            if (argtypelist[argsnow] == "1"):
                if argsonlyoptions[argsnow] == "--asdeps":
                    asdepend = True
                elif argsonlyoptions[argsnow] == "--yes":
                    noconfirm = True
                elif argsonlyoptions[argsnow] == "--bin":
                    jwpacman = True
                elif argsonlyoptions[argsnow] == "--src":
                    jwpacman = False
                elif argsonlyoptions[argsnow] == "--needed":
                    needed = True
            else:
                packagestoins.append(argsonlyoptions[argsnow])
            argsnow = argsnow + 1

        #yahhh package
        package = packagestoins[0]
        repo_url = f"https://gitlab.archlinux.org/archlinux/packaging/packages/" + package + ".git"
        local_dir = "/home/" + aptik_user + "/.cache/aptik/repo/"
        #create pkg dir when it isnt avaliable
        pkgdir = "/home/" + aptik_user + "/.cache/aptik/pkg"
        #call makepackage
        makepackage(package, repo_url, local_dir, False)
        #check pkgdir exists
        if(os.path.exists(pkgdir) == False):
            os.makedirs(pkgdir)
        print(f"{promptcolor.GREEN}==>{promptcolor.END} Installing...")
        subprocess.call('pacman -U ' + local_dir + package + '/*.tar.zst', cwd=pkgdir, shell=True)
    elif (args[1] == "help" or args[1] == "--help"):
        print (f"usage {args[0]}")
else:
    print("input commands plz!!")

quit(1)
