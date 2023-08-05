#!/usr/bin/env python3
############################################################
## Jose F. Sanchez                                        ##
## Copyright (C) 2019-2020 Lauro Sumoy Lab, IGTP, Spain   ##
############################################################
"""
Shared functions used along ``BacterialTyper`` & ``XICRA`` pipeline.
With different purposes:
    - Print time stamps
  
    - Create system calls

    - Manage/list/arrange files/folders

    - Aesthetics

    - Manage fasta files

    - Other miscellaneous functions
"""
## useful imports
from termcolor import colored
import patoolib ## to extract
import os

##
from HCGB.functions import system_call_functions

############################################################################
########                     FILES/FOLDERS                            ########                     
############################################################################

###############
def is_non_zero_file(fpath):  
    # https://stackoverflow.com/a/15924160
    """Returns TRUE/FALSE if file exists and non zero"""
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

###############
def outdir_project(outdir, project_mode, pd_samples, mode, debug):
    """
    """
    # Group dataframe by sample name
    sample_frame = pd_samples.groupby(["new_name"])
    if (debug):
        print ("+ Dataframe grouby variable 'new_name'")

    dict_outdir = {}    
    for name, cluster in sample_frame:
        if (debug):
            print (cluster)
        if (project_mode):
            #print ("Create subdir for every sample: ", mode)
            sample_dir = create_subfolder('data', outdir)        

            ## create sample
            sample_name_dir = create_subfolder(name, sample_dir)        

            ## create subdir sub sample
            mode_name_dir = create_subfolder(mode, sample_name_dir)        
            dict_outdir[name] = mode_name_dir

        else:
            #print ("All samples share same folder")
            sample_name_dir = create_subfolder(name, outdir)        
            dict_outdir[name] = sample_name_dir

    return (dict_outdir)

###############
#def outdir_subproject(outdir, pd_samples, mode):
#    ## we assume we want to create within a project dir a subdir
#    # Group dataframe by sample name
#    sample_frame = pd_samples.groupby(["name"])
#    dict_outdir = {}    
#    for name, cluster in sample_frame:
#        mode_name_dir = create_subfolder(mode, outdir)        
#        dict_outdir[name] = mode_name_dir
#
#    return (dict_outdir)

###############
def create_subfolder (name, path):
    """Create a subfolder named 'name' in directory 'path'. Returns path created."""
    ## create subfolder  ##    
    subfolder_path = path + "/" + name
    access_rights = 0o755

    # define the access rights
    try:
        os.mkdir(subfolder_path, access_rights)
    except OSError:  
        #print ("\tDirectory %s already exists" % subfolder_path)
        return subfolder_path
    else:  
        print (colored("Successfully created the directory %s " % subfolder_path, 'yellow'))

    return subfolder_path

###############  
def create_folder (path):
    """Create a folder directory 'path'. Returns path created."""

    ## create subfolder  ##    
    access_rights = 0o755

    # define the access rights
    try:
        os.mkdir(path, access_rights)
    except OSError:  
        #print ("\tDirectory %s already exists" %path)
        return path
    else:  
        print (colored("Successfully created the directory %s " %path, 'yellow'))

    return path

############### 
def get_symbolic_link (sample_list, directory):
    """Creates symbolic links, using system call, for list of files given in directory provided"""
    for samplex in sample_list:
        cmd = 'ln -s %s %s' %(samplex, directory)
        system_call_functions.system_call(cmd, returned=False)

    files2return = os.listdir(directory)
    return files2return

###############
def get_symbolic_link_file (file2link, newfile):
    """Creates symbolic link for a file into a new name file"""
    cmd = 'ln -s %s %s' %(file2link, newfile)
    system_call_functions.system_call(cmd, returned=False)


###############
def extract(fileGiven, out, remove=True):
    """
    Extracts archived file
    
    This function extracts the file given in the ``out`` path provided.
    It uses the ``patoolib`` that is able to identify the type of file 
    and compression algorithm to use in each case.
    
    It also removes the compressed file using ``os`` module.
    
    :param fileGiven: Archived file to extract.
    :param out: Output name and absolute path for the extracted archived.
    :param remove: True/False for removing compressed file extracted
    
    :type fileGiven: string
    :type out: string
    :type remove: boolean
    
    """
    ## extract using patoolib
    patoolib.extract_archive(fileGiven, outdir=out, verbosity=0)
    
    if (remove):
        ## remove compress file
        print ("Remove compress file...")
        os.remove(fileGiven)
        print ("\n")

