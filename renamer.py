import glob
import os
import json


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
path = "./",
filename = "backup.json",
skipConfirmation = False
):
    with open(f"{path}{filename}") as j:
        loaded_backup = j.read()
        loaded_backup = json.loads(loaded_backup)

    

    print(f"Backup successfully loaded from {path + filename}")

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
        if input("Continue replacing files? (this is supposed to be a completely reversible action?)[y/N]\n").lower() != "y":
            exit()
        print("\n" * 3)
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

#get_files_and_rename()
load_backup()