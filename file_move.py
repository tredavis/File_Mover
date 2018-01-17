import os
from os import walk
from shutil import copyfile
from pathlib import Path

walk_down_tree = False

def grab_inputs():
    """Grabs the file path to write the copied files to"""
    path = input("Where are we moving files from?")    
    new_path = input("Where are we moving files too?")

    walk_down_tree_input = input("*** Important*****\nShould I walk down sub folders and copy those files as well?\nEnter yes or no.\nIf you don't enter anything I will only copy the current folder and not the subfolders? \n")

    walk_down_tree_input = str(walk_down_tree_input).replace(" ", "")
    #now convert to bool
    if str(walk_down_tree_input).lower() == 'yes':
        global walk_down_tree
        walk_down_tree = True

    if not path and not new_path:
        print(".... I need two values to do my work")
        return False

    initialize(path, new_path)

total_files_copied = 0
def initialize (path, new_path):    
    log_file = Path("log.txt")
    # open the log file\
    log = open("log.txt","w+")

    files = []
    dirs = []
    try:
        for (dirpath, dirnames, filenames) in walk(path):
            files.extend(filenames)
            dirs.extend(dirnames)
            print(files)
            log.write("Copying files from {0} to {1}\n".format(path, new_path))

            # all the files in this current directory
            if len(files) > 0:

                counter = 0

                for file in files:
                    print("copying file")
                    #actually copy over the files
                    copy_files(path+'\\'+file, new_path+'\\'+file)

                    # counter used for logging purposes
                    counter += 1
                    if counter == 50:
                        log.write("50 files have been successfully written")
                        coutner = 0

                break
            log.write("{0} files were copied to the {1} directory\n".format(len(files), new_path))
                       

    except Exception as ex:
        print(ex)
        log.write("{0}\n".format(ex))
    
    if walk_down_tree == True:
        if len(dirs) > 0:
            
            for dir in dirs:
                
                print("moving on to the {0} directory".format(dir))
                log.write("moving on to the {0} directory\n".format(dir))
                
                concated_path = path + '\\' + dir
                concated_new_path = new_path + '\\' + dir

                #if we don't have a directory for the new file then make one
                if not os.path.exists(concated_new_path):
                    os.makedirs(concated_new_path)
                    log.write("Making a new directory {0}".format(concated_new_path))            
                
                #recursive call if there is a path currently located in this file
                initialize(concated_path, concated_new_path)
    else:
        print("Done!")
        log.write("Done! {0} files have been successfully copied\n".format(total_files_copied))

    # close the log file
    if log.closed != True:
        log.close()
        
  
def copy_files(src, dst):
    """ Copy a file from one location to another"""
    
    try:
        new_file = Path(dst)
        print(new_file)
        #if the file already exists then don't waste time rewritting it
        if new_file.exists() == False:
            copyfile(src, dst)
            
            #count stricly for logging purposes
            global total_files_copied
            total_files_copied += 1
            print("{0} files have been copied".format(total_files_copied))
            print("File has been copied successfully")
            
        else:
            print("{0} already exists".format(new_file))
 
    except Exception as ex:
        log.write("{0}\n".format(ex))


grab_inputs()

