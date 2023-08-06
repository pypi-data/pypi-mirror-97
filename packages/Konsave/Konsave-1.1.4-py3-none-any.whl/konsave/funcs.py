## IMPORT ##
import os, shutil, argparse, configparser
from random import shuffle
from zipfile import is_zipfile, ZipFile
from konsave.vars import *

from pkg_resources import resource_stream, resource_filename

try:
    import yaml
except ModuleNotFoundError:
    raise ModuleNotFoundError("Please install the module PyYAML using pip: \n"
                              "pip install PyYAML")


## FUNCTIONS ##
def mkdir(path):
    '''
    Creates directory if it doesn't exist
    '''
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def load_config():
    """
    Load the yaml file which contains the files and folder to be saved

    The file should be formatted like this:

    ---
    entries:
        - folder name
        - file name
        - another file name
        - another folder name

    """
    default_config_path = resource_filename('konsave', 'conf.yaml')
    if not os.path.exists(CONFIG_FILE):
        print_msg(f"No config file found! Using default config ({default_config_path}).")
        shutil.copy(default_config_path, CONFIG_FILE)
        print_msg(f"Saved default config to: {CONFIG_FILE}")
        return yaml.load(resource_stream('konsave', 'conf.yaml'), Loader=yaml.FullLoader)["entries"]

    with open(CONFIG_FILE) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    return config["entries"]


# PARSE AND SEARCH IN A CONFIG FILE
def search_config(path, section, option):
    '''
    This function will parse config files and search for specific values
    '''
    config = configparser.ConfigParser(strict=False)
    config.read(path)
    return config[section][option]


# RESTART KDE
def restart_kde():
    '''
    Restarts
    '''
    os.system('plasmashell --replace > /dev/null 2>&1 & disown')

    print("Konsave: Profile applied successfully! Please log-out and log-in to see the changes completely!")


# CHECK FOR ERRORS
def check_error(func, *args):
    '''
    This function runs a function and checks if there are any errors.
    '''
    try:
        f = func(*args)
    except Exception as e:
        print(f"Konsave: {e}\nTry 'konsave -h' for more info!")
    else:
        return f


# PRINT/LOG
def print_msg(msg):
    '''
    Makes any text a little prettier
    '''
    msg = msg[0].capitalize() + msg[1:]
    print(f"Konsave: {msg}")


# COPY FILE/FOLDER
def copy(source, dest):
    '''
    This function was created because shutil.copytree gives error if the destination folder
    exists and the argument "dirs_exist_ok" was introduced only after python 3.8.
    This restricts people with python 3.7 or less from using Konsave.
    This function will let people with python 3.7 or less use Konsave without any issues.
    It uses recursion to copy files and folders from "source" to "dest"
    '''
    assert (type(source) == str and type(dest) == str), "Invalid path"
    assert (source != dest), "Source and destination can't be same"
    assert (os.path.exists(source)), "Source path doesn't exist"
    
    if not os.path.exists(dest):
        os.mkdir(dest)
    
    if os.path.isdir(source):
        for item in os.listdir(source): 
            source_path = os.path.join(source, item)
            dest_path = os.path.join(dest, item)

            if os.path.isdir(source_path):
                copy(source_path, dest_path)
            else:
                if os.path.exists(dest_path):
                    os.remove(dest_path)
                shutil.copy(source_path, dest)
    else:
        shutil.copy(source, dest)


# LIST PROFILES
def list_profiles(list_of_profiles, length_of_lop):
    '''
    Lists all the created profiles
    '''

    # assert
    assert (os.path.exists(PROFILES_DIR) and length_of_lop != 0), "No profile found."

    # run
    print("Konsave profiles:")
    print(f"ID\tNAME")
    for i, item in enumerate(list_of_profiles):
        print(f"{i + 1}\t{item}")


# SAVE PROFILE
def save_profile(name, list_of_profiles, force=False):
    '''
    Saves necessary config files in ~/.config/konsave/profiles/<name>
    '''

    # assert
    assert (name not in list_of_profiles or force), "Profile with this name already exists"

    # run
    print_msg("saving profile...")
    PROFILE_DIR = os.path.join(PROFILES_DIR, name)
    mkdir(PROFILE_DIR)

    entries = load_config()
    for entry in entries:
        source = os.path.join(CONFIG_DIR, entry)
        if os.path.exists(source):
            if os.path.isdir(source):
                check_error(copy, source, os.path.join(PROFILE_DIR, entry))
            else:
                shutil.copy(source, PROFILE_DIR)

    print_msg('Profile saved successfully!')


# APPLY PROFILE
def apply_profile(id, list_of_profiles, length_of_lop):
    '''
    Applies profile of the given id
    '''

    # Lowering id by 1
    id -= 1

    # assert
    assert (length_of_lop != 0), "No profile saved yet."
    assert (id in range(length_of_lop)), "Profile not found :("

    # run
    name = list_of_profiles[id]
    PROFILE_DIR = os.path.join(PROFILES_DIR, name)
    check_error(copy, PROFILE_DIR, CONFIG_DIR)
    restart_kde()


# REMOVE PROFILE
def remove_profile(id, list_of_profiles, length_of_lop):
    '''
    Removes the specified profile
    '''

    # Lowering id by 1
    id -= 1

    # assert
    assert (id in range(length_of_lop)), "Profile not found."

    # run
    item = list_of_profiles[id]
    shutil.rmtree(os.path.join(PROFILES_DIR, item))
    print_msg('removed profile successfully')


# EXPORT PROFILE
def export(id, list_of_profiles, length_of_lop):
    '''
    It will export the specified profile as a ".knsv" file in the home directory
    '''

    # lowering id by 1
    id -= 1

    # assert
    assert (id in range(length_of_lop)), "Profile not found."

    # run
    item = list_of_profiles[id]
    PROFILE_DIR = os.path.join(PROFILES_DIR, item)
    EXPORT_PATH = os.path.join(HOME, item)

    if os.path.exists(EXPORT_PATH):
        rand_str = list('abcdefg12345')
        shuffle(rand_str)
        EXPORT_PATH = EXPORT_PATH + ''.join(rand_str)

    # compressing the files as zip
    print_msg("Exporting profile. It might take a minute or two...")

    CONFIG_EXPORT_PATH = mkdir(os.path.join(EXPORT_PATH, "config"))
    PLASMA_EXPORT_PATH = mkdir(os.path.join(EXPORT_PATH, "plasma"))
    CURSOR_EXPORT_PATH = mkdir(os.path.join(EXPORT_PATH, "cursor"))
    ICON_EXPORT_PATH = mkdir(os.path.join(EXPORT_PATH, "icons"))

    # VARIABLES
    KDE_GLOBALS = os.path.join(PROFILE_DIR, 'kdeglobals')

    icon = search_config(KDE_GLOBALS, 'Icons', 'Theme')
    cursor = search_config(os.path.join(PROFILE_DIR, 'kcminputrc'), 'Mouse', 'cursorTheme')

    PLASMA_DIR = os.path.join(HOME, '.local/share/plasma')
    LOCAL_ICON_DIR = os.path.join(HOME, '.local/share/icons', icon)
    USR_ICON_DIR = os.path.join('/usr/share/icons', icon)
    LOCAL_CURSOR_DIR = os.path.join(HOME, '.icons', cursor)
    USR_CURSOR_DIR = os.path.join('/usr/share/icons', cursor)

    def check_path_and_copy(path1, path2, export_location, name):
        if os.path.exists(path1):
            check_error(copy, path1, os.path.join(export_location, name))
        elif os.path.exists(path2):
            check_error(copy, path2, os.path.join(export_location, name))
        else:
            print_msg(f"Couldn't find {path1} or {path2}. Skipping...")

    check_path_and_copy(LOCAL_ICON_DIR, USR_ICON_DIR, ICON_EXPORT_PATH, icon)
    check_path_and_copy(LOCAL_CURSOR_DIR, USR_CURSOR_DIR, CURSOR_EXPORT_PATH, cursor)
    check_error(copy, PLASMA_DIR, PLASMA_EXPORT_PATH)
    check_error(copy, PROFILE_DIR, CONFIG_EXPORT_PATH)

    shutil.make_archive(EXPORT_PATH, 'zip', EXPORT_PATH)
    shutil.rmtree(EXPORT_PATH)
    shutil.move(EXPORT_PATH + '.zip', EXPORT_PATH + export_extension)

    print_msg(f"Successfully exported to {EXPORT_PATH}{export_extension}")


# IMPORT PROFILE
def import_profile(path):
    '''
    This will import an exported profile
    '''

    # assert
    assert (is_zipfile(path) and path[-5:] == export_extension), "Not a valid konsave file"
    item = os.path.basename(path)[:-5]
    assert (not os.path.exists(os.path.join(PROFILES_DIR, item))), "A profile with this name already exists"

    # run

    print_msg("Importing profile. It might take a minute or two...")

    item = os.path.basename(path).replace(export_extension, '')

    TEMP_PATH = os.path.join(KONSAVE_DIR, 'temp', item)

    with ZipFile(path, 'r') as zip:
        zip.extractall(TEMP_PATH)

    CONFIG_IMPORT_PATH = os.path.join(TEMP_PATH, 'config')
    PLASMA_IMPORT_PATH = os.path.join(TEMP_PATH, 'plasma')
    ICON_IMPORT_PATH = os.path.join(TEMP_PATH, 'icons')
    CURSOR_IMPORT_PATH = os.path.join(TEMP_PATH, 'cursor')

    PLASMA_DIR = os.path.join(HOME, '.local/share/plasma')
    LOCAL_ICON_DIR = os.path.join(HOME, '.local/share/icons')
    LOCAL_CURSOR_DIR = os.path.join(HOME, '.icons')
    PROFILE_DIR = os.path.join(PROFILES_DIR, item)

    print()
    check_error(copy, CONFIG_IMPORT_PATH, PROFILE_DIR)
    check_error(copy, PLASMA_IMPORT_PATH, PLASMA_DIR)
    check_error(copy, ICON_IMPORT_PATH, LOCAL_ICON_DIR)
    check_error(copy, CURSOR_IMPORT_PATH, LOCAL_CURSOR_DIR)

    shutil.rmtree(TEMP_PATH)

    print_msg("Profile successfully imported!")


# WIPE
def wipe():
    '''
    This function will wipe all profiles
    '''
    confirm = input("This will wipe all your profiles. Enter \"WIPE\" Tto continue: ")
    if confirm == 'WIPE':
        shutil.rmtree(PROFILES_DIR)
        print_msg("Removed all profiles!")
    else:
        print_msg("Aborting...")