# dependencies:
import os # to 'see' files in the executing directory
import re # to use regular expression pattern matching
import argparse # to parse command line arguments (python >= 3.2)

# constants / default parameters:
MY_INVALID_CHARS_REGEX = r'[^a-z.A-Z_\-\+\[\]\(\)0-9]'
MY_INVALID_CHARS_REGEX_SPACES_VALID = r'[^a-z.A-Z_\-\+\[\]\(\)0-9\ ]'
MY_LIMIT_FOR_FILE_LISTS = 6
VERBOSE = False #turn on/off debugging helper output
RECURSE_HIDDEN_DIRECTORIES = False
RECURSE_SUBDIRECTORIES = False

# go through the current directory (and optionally all subdirectories) and
# find any filenames that contain invalid characters, then for each invalid
# character, show the first X offending files (or optionally all offending files)
# containing that character and ask the user if they want to 
# 'replace all instances of the character with another character', 
# 'delete the character', 
# 'ignore the character', 
# 'cycle through the list of filenames and ask for a replacement for each one
# on a case by case basis'

#############################################
# Inform argparse of command line arguments #
#############################################

parser = argparse.ArgumentParser(
  description='Clean away invalid characters from filenames.'
)

parser.add_argument(
  '-l', '--limit', 
  metavar='NUM',
  type=int, 
  default=MY_LIMIT_FOR_FILE_LISTS, 
  help='Print an initial maximum of NUM filenames before '
    'checking to print the rest'
)
parser.add_argument(
  '-v','--verbose',
  help='Be verbose',
  action='store_true'
)
parser.add_argument(
  '-r',
  '-R',
  dest='recurse',
  help='Recurse through all subdirectories',
  action='store_true'
)
parser.add_argument(
  '-a','--all',
  help='Recurse all subdirectories, even hidden ones',
  action='store_true'
)
parser.add_argument(
  '-s','--spaces',
  help='treat spaces as valid filename characters',
  action='store_true'
)
######################################################
# override parameters according to command line args #
######################################################
invalid_chars_regex = MY_INVALID_CHARS_REGEX
args = parser.parse_args()
RECURSE_SUBDIRECTORIES = args.recurse
RECURSE_HIDDEN_DIRECTORIES = args.all
VERBOSE = args.verbose
MY_LIMIT_FOR_FILE_LISTS = args.limit
 # Take recursion of hidden directories to mean recursion of all directories
if RECURSE_HIDDEN_DIRECTORIES:
  RECURSE_SUBDIRECTORIES = True
if args.spaces:
  invalid_chars_regex = MY_INVALID_CHARS_REGEX_SPACES_VALID

####################
# helper functions #
####################

def get_file_from_path(full_path):
  return full_path[full_path.rfind('/') + 1 : len(full_path)]

def get_invalid_char(full_path, invalid_char_regex):
  filename = get_file_from_path(full_path)
  match = re.search(invalid_char_regex, filename)
  if match:
    return filename[match.start()]
  else:
    return None

def reload_bad_files(list_to_update):
  current_directory = os.getcwd()
  files = []
  identify_files(current_directory, files, RECURSE_SUBDIRECTORIES)
  list_to_update.clear()
  for file in files:
    if get_invalid_char(file, invalid_chars_regex):
      list_to_update.append(file)

reported_paths_recursed = []

def identify_files(path, file_list, recurse):
  # as this function is rerun upon filename updates, keep track of what
  # folders we have already reported to the user that we've checked to
  # avoid repeating ourselves 
  if path not in reported_paths_recursed:
    print("identifying files in %s" %(path,))
    reported_paths_recursed.append(path)
  files = os.listdir(path)
  for file in files:
      if VERBOSE:
        print("considering %s" %(file,))
        print("file[0] = %s" %(file[0],))
      if os.path.isdir(path+'/'+file):
        if recurse:
          if RECURSE_HIDDEN_DIRECTORIES or file[0] != '.':
            if VERBOSE:
              print("checking contents of %s:" %(file))
            identify_files(path + '/' + file, file_list, True)
          else:
            if VERBOSE:
              print("ignoring hidden directories: %s" %(file))
      if os.path.isfile(path+'/'+file) and file[0] != '.':
        if VERBOSE:
          print("adding %s to general file list" %(file,))
        file_list.append(path + '/' + file)

#######################################
# determine all files to be inspected #
#######################################

if VERBOSE:
  print("\n\n###########\ncompiling list of all files to check\n\n")

# get listing of files and directories
current_directory = os.getcwd()
files = []

if RECURSE_SUBDIRECTORIES:
  identify_files(current_directory, files, True)
else:
  identify_files(current_directory, files, False)


##############################################
# determine bad files and the bad characters #
##############################################

if VERBOSE:
  print("\n\n###########\ndetermining bad files and characters\n\n")

bad_files = [] # to be populated with offending filenames.
bad_chars = set({}) # to be populated with only distinct offending chars.
for file in files:
  if VERBOSE:
    print(' ') # separate results with a blank line
    print(file, end='')  # the second param requires python3:python3.5 fnclean.py
  if os.path.isdir(file):
    if VERBOSE:
      print(" is a directory and its name is: %s" %(get_file_from_path(file)))
  elif os.path.isfile(file):
    if VERBOSE:
      print(" is a file and its filename is: %s" %(get_file_from_path(file)))
    match = get_invalid_char(file, invalid_chars_regex)
    if match:
      if VERBOSE:
        print("filename no good")
        print('The offending character is:' + match)
      bad_files.append(file)
      char_matches = list(set(re.findall(invalid_chars_regex, get_file_from_path(file))))
      for char in char_matches:
        bad_chars.add(char)

if VERBOSE:
  print("the bad files:")
  print(bad_files)
  print("the bad characters:")
  print(list(bad_chars))

#####################################
# cycle through the bad characters  #
# present offending files           #
# and ask user how to proceed       #
#####################################

if VERBOSE:
  print("\n\n###########\nCycling through bad characters\n\n")


for char in bad_chars:
  # os.system('cls || clear') ## clear the screen for the user
  reload_bad_files(bad_files) # to ensure our file lists reflects any changes made from previous iterations
  print("the '%s' character appears in the following files:" %(char,))
  files_listed_counter = 0

  for filename in bad_files:
    # print the list of filenames with this character in them:
    if char in filename:
      print (filename)
      files_listed_counter += 1
      if files_listed_counter == MY_LIMIT_FOR_FILE_LISTS and MY_LIMIT_FOR_FILE_LISTS != len(bad_files):
        show_more = input("...show all? (y/n): ") # python3.5 syntax
        if show_more == 'n':
          break
        else:
          continue
    # then ask the user what they want to do:
  option = input("""
  What do you want to do?
  1. replace all instances
  2. remove all instances
  3. ask me for each file
  4. ignore this character
  (enter 1 2 3 or 4):""")
  if option == '1': #replace the character in all filenames
    replacement = input("Enter character or text to replace '%s' with: " %(char,))
    for filename in bad_files:
      if char in filename:
        new_filename = filename.replace(char, replacement)
        os.rename(filename, new_filename)
        if VERBOSE:
          print("%s changed to %s" %(filename, new_filename,))
        
  if option == '2': #delete the character from all filenames
    for filename in bad_files:
      if char in filename:
        new_filename = filename.replace(char,'')
        os.rename(filename, new_filename)
  if option == '3': #ask the user for each filename
    for filename in bad_files:
      if char in filename:
        print("\nfilename: %s" %(filename,))
        file_option = input("""
    What do you want to do?
    1. replace all instances in this filename
    2. remove all instances in this filename
    3. set a new filename
    4. ignore this file
    (enter 1 2 3 or 4):""")
        if file_option == '1': #replace
          replacement = input("Enter character or text to replace '%s' with: " %(char,))
          new_filename = filename.replace(char, replacement)
          os.rename(filename, new_filename)
        if file_option == '2': # remove 
          new_filename = filename.replace(char, '')
          os.rename(filename, new_filename)
        if file_option == '3': # set a new filename
          new_filename = input("Enter the new filename for this file:")
          os.rename(filename, new_filename)

