#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 07:16:00 2019

@author: danjampro

Run this on the pis (not the main computer).
"""
import os, subprocess
from huntsman.utils import load_config

#==============================================================================

def mount(mountpoint, remote, server_alive_interval=20,
          server_alive_count_max=3, logger=None):
    '''
    Mount remote on local.
    '''
    if logger is None:
        logger = print
        
    if not os.path.isdir(mountpoint):
        try:
            os.makedirs(mountpoint, exist_ok=True)
        except FileExistsError:
            pass #For some reason this is necessary
        
    options = f'ServerAliveInterval={server_alive_interval},' + \
              f'ServerAliveCountMax={server_alive_count_max}'
    options = ['sshfs', remote, mountpoint, '-o', options]
    try:
        subprocess.run(options, shell=False, check=True)
    except Exception as e:
        logger(f'Failed to mount {remote} on {mountpoint}.')
        raise(e)
    
    
def unmount(mountpoint):
    '''
    Unmount remote from local.
    '''
    if os.path.isdir(mountpoint):
        options = ['fusermount', '-u', mountpoint]
        try:
            subprocess.run(options, shell=False, check=True)
        except:
            pass
        
#==============================================================================

def mount_sshfs(logger=None):
    '''
    
    '''
    if logger is None:
        logger = print
        
    #Specify the mount point as ~/Huntsmans-Pro (for huntsman user)
    home = os.path.expandvars('$HOME')
    mountpoint = os.path.join(home, 'Huntsmans-Pro')
    
    #Specify the remote directory
    config = load_config()
    remote_ip = config['messaging']['huntsman_pro_ip']
    remote_dir= config['directories']['base']
    remote = f"huntsman@{remote_ip}:{remote_dir}"
    
    #Check if the remote is already mounted, if so, unmount
    logger(f'Attempting to unmount {mountpoint}...')
    unmount(mountpoint)
    
    #Mount
    logger(f'Mounting {remote} on {mountpoint}...')
    mount(mountpoint, remote)
    
    #Symlink the directories
    original = os.path.join(mountpoint, 'images')
    link = config['directories']['images']
    
    #If link already exists, make sure it is pointing to the right place
    if os.path.exists(link):
        try:
            assert(os.path.islink(link))
            assert(os.path.normpath(os.readlink(link))==os.path.normpath(
                    original))
            logger('Skipping link creation as it already exists.')
        except:
            msg = f'Cannot create link. File already exists: {link}'
            logger(msg)
            raise FileExistsError(msg)
    else:
        logger('Creating symlink to images directory...')
        os.symlink(original, link, target_is_directory=True)
    
    logger('Done mounting SSHFS!')
    
    return mountpoint
    
#==============================================================================
#==============================================================================

if __name__ == '__main__':
    
    mount_sshfs()