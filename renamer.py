import glob
import os
import json
import pathlib


global username
username = os.getlogin()

def save_backup(
firstentrylist,
secondentrylist,
path = "./",
filename = "backup.json"
):
    backup_dict = {
        "new-filenames": firstentrylist,
        "old-filenames": secondentrylist
    }
    backup_json = json.dumps(backup_dict, indent=4)
    with open(f"{path}{filename}", "w") as file:
        file.write(backup_json)
    return

def load_backup(
path = "./backup.json",
skipConfirmation = False
):
    with open(f"{path}") as j:
        loaded_backup = j.read()
        loaded_backup = json.loads(loaded_backup)

    

    print(f"Backup successfully loaded from {path}")

    if not skipConfirmation:
        if input("Do you want to restore the backup?[y/N]\n").lower() != "y":
            exit()
    
    rename(loaded_backup["new-filenames"], loaded_backup["old-filenames"])

    
    return
    

def get_files_and_rename(
skipConfirmation = False,
logging = True,
backup = True,
path = "/home/v/.minecraft/resourcepacks/",
blacklisted_characters = ["¡", "§", "!", "&"],
file_extension = "*.zip"
):
    def log(text):
        if logging:
            print(text)
    
    blacklisted_files = []
    files = []
        
    for file in glob.glob(path + file_extension):
        files.append(file)

    for filename in files:
        for a in list(filename):
            if a in blacklisted_characters:
                blacklisted_files.append(filename)
    blacklisted_files = list(set(blacklisted_files))


    cleaned_filenames = []


    for file in blacklisted_files:
        file = str(file)
        for char in blacklisted_characters:
            file = file.replace(char, "")
        cleaned_filenames.append(file)
    
    if backup and len(blacklisted_files) > 0:
        save_backup(cleaned_filenames, blacklisted_files)

    log(f"Blacklisted_files len: {len(blacklisted_files)}")
    if not skipConfirmation:
        if input("Replace files? (this is supposed to be a completely reversible action?)[y/N]\n").lower() != "y":
            exit()
        if input("Are you really sure? Type 'I am sure' here to continue\n") != "I am sure":
            exit()

    rename(blacklisted_files, cleaned_filenames, logging=logging)

    print("Done")
    return "Done"

def rename(blacklisted_files, cleaned_filenames, logging=True):
    i = -1
    command = ""
    for file in blacklisted_files:
        i += 1
        command = f'mv "{file}" "{cleaned_filenames[i]}"'
        
        if logging:
            print(command)
        os.system(command)

def main_cli_ui():
    print("""
[resource-pack-renamer]
What do you want to do?
[R] Rename your resource packs to be loaded properly
[B] Load a backup from [R]
""")
    selection = input(">")
    if selection.upper() == "R":
        r_cli_ui()
    elif selection.upper() == "B":
        b_cli_ui()

def file_path_input(text, func):
    path = input(text)
    if not pathlib.Path(path).exists():
        print("invalid path")
        func()
    return path


def b_cli_ui():
    print("")
    s = input("Would you like to use the default path?(./backup.json)")
    if s.lower().startswith("y"):
        path = file_path_input("Enter your custom path: ")
    
    load_backup()
    



def r_cli_ui():
    if input("Do you wish to use simple mode? ").lower().startswith("y"):
        path_thing =  input(f"Path has been set to /home/{username}/.minecraft/resourcepacks. Do you wish to change it? ")
        if path_thing.lower().startswith("y"):
            path = file_path_input()
        else:
            path = "/home/{username}/.minecraft/resourcepacks"
            get_files_and_rename()
        


main_cli_ui()