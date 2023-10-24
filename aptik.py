#!/usr/bin/env python
#2023-2023 plasticgaming99 (plsplastic_roblox@protonmail.com)

#EDIT TO YOUR BUILD USER
aptik_user="plastek"

import sys
args = sys.argv
import os
from git import Repo
import urllib.request
import tqdm
import shutil
import subprocess
import pyalpm

dbpath = '/var/lib/pacman'
handle = pyalpm.Handle('/', dbpath)

#init global variables
madenpack = ""

class promptcolor:
    CYAN = '\033[94m'
    GREEN = '\033[92m'
    END = '\033[0m'

def yes_no_input(x):
    while True:
        choice = input(x).lower()
        if choice in ['y', 'ye', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False

def chkdir(x):
    #check directory is avaliable
    while True:
        if os.path.exists(input(x)):
            return True
        else:
            os.makedirs(input(x))
            return False

def makepackage(package, repourl, localdir):
    #make package
        #clone repo with gitpython
        print(f"{promptcolor.GREEN}==>{promptcolor.END} Setting Clone repo to aptik_user_home/.cache/aptik/repo")
        if(urllib.request.urlopen(repourl).getcode() == 404):
            print("package n/a")
            quit()
        repo_dir = localdir + package
        if(os.path.exists(repo_dir) == True):
            shutil.rmtree(repo_dir)
        Repo.clone_from(repo_url, repo_dir)

        subprocess.call('chown -R ' + aptik_user + ":" + aptik_user + " " + repo_dir, shell=True)
        print(f"{promptcolor.GREEN}==>{promptcolor.END} Making package...")
        #subprocess.call('sudo -u ' + aptik_user + ' makepkg', cwd=repo_dir, shell=True)

        return True


if(os.getuid() != 0):
    print("Please run this command with root.")
    quit()

try:
    if(args[1] == "install"):
        from pyalpm import Package
        try:
            #yahhh package
            package = args[2]
            repo_url = "https://gitlab.archlinux.org/archlinux/packaging/packages/" + package
            local_dir = "/home/" + aptik_user + "/.cache/aptik/repo/"
            #create pkg dir when it isnt avaliable
            pkgdir = "/home/" + aptik_user + "/.cache/aptik/pkg"
            #call makepackage
            makepackage(package, repo_url, local_dir)
            #check pkgdir exists
            if(os.path.exists(pkgdir) == False):
                os.makedirs(pkgdir)
            
            print(f"{promptcolor.GREEN}==>{promptcolor.END} Installing...")
            subprocess.call('pacman -U ' + local_dir + package + '/*.tar.zst', cwd=pkgdir, shell=True)
        except IndexError as e:
            print("please input some packages")
except IndexError as e:
    print("input commands plz!!")
