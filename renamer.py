import glob
import os
import json
import pathlib


global username

# Getting the username for the path

username = os.getlogin()

# backup thing

def save_backup(
firstentrylist,
secondentrylist,
path = "./",
filename = "backup.json"
):
    # the dictionary that will be converted into json
    backup_dict = {
        "new-filenames": firstentrylist,
        "old-filenames": secondentrylist
    }
    # converty
    backup_json = json.dumps(backup_dict, indent=4)
    # putting it into a file
    with open(f"{path}{filename}", "w") as file:
        file.write(backup_json)
    return

# this is for loading backups

def load_backup(
path = "./backup.json",
skipConfirmation = False
):
    # reading the backup
    with open(f"{path}") as j:
        loaded_backup = j.read()
        loaded_backup = json.loads(loaded_backup)

    

    print(f"Backup successfully loaded from {path}")

    # confirmation
    if not skipConfirmation:
        if input("Do you want to restore the backup?[y/N]\n").lower() != "y":
            exit()
    
    # using custom function to rename a bunch of files from the lists provided by the backup
    rename(loaded_backup["new-filenames"], loaded_backup["old-filenames"])

    
    return
    
# this is the main program

def get_files_and_rename(
skipConfirmation = False,
logging = True,
backup = True,
path = "/home/v/.minecraft/resourcepacks/",
blacklisted_characters = ["¡", "§", "!", "&"],
file_extension = "*.zip"
): 
    # this function is used for debugging
    def log(text):
        if logging:
            print(text)
    # some variables that are needed
    blacklisted_files = []
    files = []
    
    # getting all the .zip files from the dir
    for file in glob.glob(path + file_extension):
        # adding them to a list
        files.append(file)

    # checking for all the blacklisted characters defined
    for filename in files:
        # going through all the files
        for a in list(filename):
            if a in blacklisted_characters:
                # adding them to a list
                blacklisted_files.append(filename)
    # removing duplicates because that system to get them is ASS
    blacklisted_files = list(set(blacklisted_files))

    # another variable
    cleaned_filenames = []

    # making a new list with the blacklisted files cleaned up of the characters
    for file in blacklisted_files:
        file = str(file)
        # going through every letter
        for char in blacklisted_characters:
            # replacing them
            file = file.replace(char, "")
        
        # adding them to a new list
        cleaned_filenames.append(file)
    
    # checking if backupping is enabled and backing up the files
    # only if blacklisted_files is not empty
    if backup and len(blacklisted_files) > 0:
        save_backup(cleaned_filenames, blacklisted_files)

    # debug
    log(f"Blacklisted_files len: {len(blacklisted_files)}")
    if not skipConfirmation:
        # confirmations just in case
        if input("Replace files? (this is supposed to be a completely reversible action?)[y/N]\n").lower() != "y":
            exit()
        if input("Are you really sure? Type 'I am sure' here to continue\n") != "I am sure":
            exit()
    # renaming them all with the new filenames and logging at the same state
    rename(blacklisted_files, cleaned_filenames, logging=logging)

    print("Done")
    return "Done"

# the renaming function(linux only btw)
def rename(blacklisted_files, cleaned_filenames, logging=True):
    # this counter is negative because im lazy
    i = -1
    # empty command variable
    command = ""
    # going through all the files
    for file in blacklisted_files:
        # adding to counter
        i += 1
        # creating the command that renames the file(linux only part)
        command = f'mv "{file}" "{cleaned_filenames[i]}"'
        
        # yeah i was too lazy again(if logging is enabled then log)
        if logging:
            print(command)
        # run the command
        os.system(command)

# the user-interface
def main_cli_ui():
    print("""
[resource-pack-renamer]
What do you want to do?
[R] Rename your resource packs to be loaded properly
[B] Load a backup from [R]
""")
    # selection
    selection = input(">")
    if selection.upper() == "R":
        r_cli_ui()
    elif selection.upper() == "B":
        b_cli_ui()
# used for checking and entering a custom file path
def file_path_input(text, func):
    # input
    path = input(text)
    # modern approach to checking if the path is existent
    if not pathlib.Path(path).exists():
        # rerun function
        print("invalid path")
        func()
    return path

# backup ui thing
def b_cli_ui():
    print("")
    s = input("Would you like to use the default path?(./backup.json)")
    # checking if user wants to use default path
    if s.lower().startswith("y"):
        # custom path set
        path = file_path_input("Enter your custom path: ", b_cli_ui)
        # loading backup
        load_backup(path)
        return
    load_backup()
    return
    
    
    


# renamer ui 
def r_cli_ui():
    # asking if the user wants to use simple mode
    if input("Do you wish to use simple mode? ").lower().startswith("y"):
        # shows the user the path and asks if it wants to change it
        path_thing =  input(f"Path has been set to /home/{username}/.minecraft/resourcepacks. Do you wish to change it? ")
        # check
        if path_thing.lower().startswith("y"):
            # custom path
            path = file_path_input("Custom path: ", r_cli_ui)
        else:
            # default path
            path = "/home/{username}/.minecraft/resourcepacks"
            # do the renaming thing
            get_files_and_rename()
        


if __name__ == "__main__":
    main_cli_ui()