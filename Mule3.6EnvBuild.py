# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 09:21:05 2015

@author: droy2
"""
import os
import errno
import sys
import subprocess
import shlex
import getpass
import shutil
import subprocess


def main():
    print('This is the Main script that starts the Execution of Mule Enviornment Build\n')
    print('#############################################################################\n')
    print(os.name)
    createDirectories()
    getBinaries()    
    MuleInstallation()
    patchingMule()
    mmcInstall()
    DeploymentScriptInstall()
    cleanUp()
    print('Script Execution Ends Here \n')
    print('#############################################################################\n')
    
def getBinaries():

    path_binaries='/InstallationScript/EBS_EASMule362_Ver1.0/EBS_EASMule362_Ver1.0/'
    dest_dir='/mule'
    print('Getting the Binaries')
    
    ##
    ###
    ##
    print("copying the installation scripts (install_Mule362_1.0.sh , install_MuleDeployMech_1.0.sh) and the installation package (IntuitEBS_EAS_MuleEE362_1.0.tar.gz , IntuitEBS_EAS_MuleDeployMech_1.0.tar.gz) into the /mule folder")
    
    for filename in os.listdir(path_binaries):
        file=path_binaries+filename
        print (file)
        shutil.copy(file,dest_dir)
    
    
    print('The Binaries are sucessfully fetched\n')
    

def MuleInstallation():
    
    #This script installs the basic version EBS_EASMule362_Ver1.0 which is the base install
   
   print('Getting Started with the Installation')
   print( "This script was called by: " , getpass.getuser())
   print ('Now do something as root...')
   subprocess.call(shlex.split('sudo -u root -i sh /mule/install_Mule362_1.0.sh'))
   shutil.copy('/InstallationScript/bash_profile','/home/applmgr/.bash_profile')
   print( "The current user is: " , getpass.getuser())
   #Every space in subprocess.call comes with a , 
   #subprocess.call(shlex.split('sudo id -nu'))
   #sudo -u root -i
   #subprocess.call("sudo","-u","root","i")
   #os.popen("sudo -S /etc/init.d/postifx reload", 'w').write("yourpassword")
#   if os.geteuid() != 0:
#       os.execvp("sudo",["sudo"] + sys.argv)
#       print( "The current user is: " , getpass.getuser())
#       #os.execvp('sh /mule/install_Mule362_1.0.sh') 
#       #os.system('cat /InstallationScript/bash_profile >> /home/applmgr/.bash_profile')
#       #os.system('cat /InstallationScript/bash_profile >> /home/applmgr/.bash_profile')
#       print ("This installation is completed")                    
#      
    
                        
     #print ("Now switch back to the calling user:  ",getpass.getuser()) 
    
    
def createDirectories():
    try :
        
        print('This will create the needed directories')
        # Step 1 make sure applmgr user has access to create directories
        
        os.makedirs(name='/mule',mode=0777)
        os.makedirs(name='/mule_logs',mode=0777)
        print('The Directories are created')
        
        
        
       
        
    except OSError as exception :
        if exception.errno == errno.EEXIST:
            print('The directory already exists')
        
   

def patchingMule():
    print('This will patch Mule from EBS_EASMule362_Ver1.0.1 to 1.0.4')
    #The first Patch 1.0.1 needs to runas rot user
    subprocess.call(shlex.split('sudo -u root -i sh /InstallationScript/EBS_EASMule362_Ver1.0/EBS_EASMule340_Ver1.0.1/install_Mule340_1.0.1.sh'))
    subprocess.call(shlex.split('sh /InstallationScript/EBS_EASMule362_Ver1.0/EBS_EASMule362_Ver1.0.2/install_Mule362_1.0.2.sh'))
    subprocess.call(shlex.split('sh /InstallationScript/EBS_EASMule362_Ver1.0/EBS_EASMule362_Ver1.0.3/install_Mule362_1.0.3.sh'))
    subprocess.call(shlex.split('sh /InstallationScript/EBS_EASMule362_Ver1.0/EBS_EASMule362_Ver1.0.4/install_Mule362_1.0.4.sh'))
    print('The patches are all applied sucessfully')

def mmcInstall():
    
    mmc_install_flag=sys.argv[1]
    
    
    if mmc_install_flag=='N':
        
        
        print('MMC Registration is Not Needed')
        
    else:
        
        print('Doing Host-MMC Console Registration')
        hostname=' '+sys.argv[2]
        env=' '+sys.argv[3]
        pod=' '+sys.argv[4]
        node=' '+sys.argv[5]
        mmc_server=' '+sys.argv[6]
        print('This will install the Host to the MMC Console')
        print('Getting all the parameters')
        print('Registering the host with MMC now')
           
        #parameters=[hostname,env,pod,node,mmc_server]
        cmd='sh /InstallationScript/RegistertoMMC.sh'
        p=''.join(['sh /InstallationScript/RegistertoMMC.sh',hostname,env,pod,node,mmc_server])
        subprocess.call(shlex.split(p))
        #subprocess.call(shlex.split('sh /InstallationScript/RegistertoMMC.sh'.join(parameters)))
        
       # print('The hostname is',hostname)
        
def DeploymentScriptInstall():
    print("Now will install the deployment script")
    subprocess.call(shlex.split('sh /InstallationScript/EBS_EASMule362_Ver1.0/EBS_MuleDeployMech_Ver2.0/install_MuleDeployMech_2.0.sh'))
    print("Now your Mule Enviornment is Ready to use please change properties files accordingly")
    
def cleanUp():
    print('Now will do some basic cleanup')
    subprocess.call(shlex.split('mv /mule/install_Mule362_1.0.sh /mule/cleanup/'))
    print('########################Enjoy your Mule Enviornment#######################')

    
if __name__ == "__main__": main()
    
    
