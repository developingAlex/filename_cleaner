# dependencies:
import os # to 'see' files in the executing directory
import re # to use regular expression pattern matching
# constants:
MY_INVALID_CHARS_REGEX = r'[^a-z.A-Z_\-\+\[\]\(\)0-9\ ]'
MY_LIMIT_FOR_FILE_LISTS = 6

# go through the current directory and find any filenames that contain weird
# characters, then for each unique weird character, ask the user a question
# showing the first 15 or however many results of filenames containing that 
# character and asking the user if they want to 'replace all instances of the
# character with another character?', 'ignore the character', 'cycle through
# the list of filenames and ask for a replacement for each one?'. and recurse 
# through all subdirectories

def contains_invalid_chars(filename, invalid_char_regex):
  if re.search(invalid_char_regex, filename) == None:
    return False
  else:
    return True

def reload_bad_files(list_to_update):
  current_directory = os.getcwd()
  files = os.listdir(current_directory)
  list_to_update.clear()
  for file in files:
    if contains_invalid_chars(file, MY_INVALID_CHARS_REGEX):
      list_to_update.append(file)

  

current_directory = os.getcwd()
files = os.listdir(current_directory)
print(os.listdir(current_directory))

##############################################
# determine the files and the bad characters #
##############################################

bad_files = [] # to be populated with offending filenames.
bad_chars = set({}) # set to be populated with only distinct offending chars.
for file in files:
  print(' ') # separate results with a blank line
  print(file, end='')  # the second param requires python3:python3.5 fnclean.py
  if os.path.isdir(file):
    print(" is a directory")
  elif os.path.isfile(file):
    print(" is a file")
    if contains_invalid_chars(file, MY_INVALID_CHARS_REGEX):
      print("filename no good")
      match = re.search(MY_INVALID_CHARS_REGEX, file)
      if match:
        print('The offending character is:' + file[match.start()])
        bad_files.append(file)
        char_matches = list(set(re.findall(MY_INVALID_CHARS_REGEX, file)))
        for char in char_matches:
          bad_chars.add(char)

print("the bad files:")
print(bad_files)
print("the bad characters:")
print(list(bad_chars))

################################################################
# cycle through the bad characters and present offending files #
################################################################


for char in bad_chars:
  print(" the %s character appears in the following files:" %(char,))
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
  option = input("""What do you want to do?
  1. replace all instances
  2. remove all instances
  3. ask me for every single file
  (enter 1 2 or 3)
  """)
  if option == '1':
    replacement = input ("Enter character or text to replace %s with: " %(char,))
    for filename in bad_files:
      if char in filename:
        new_filename = filename.replace(char,replacement)
        os.rename(filename, new_filename)
        print("%s changed to %s" %(filename,new_filename,))
        
    # now since we may have changed filenames our bad_files list may not 
    #reflect reality anymore esp if some files had multiple invalid characters.
    reload_bad_files(bad_files) # to ensure our file lists reflects any changes
  if option == '2':
    print("to be implemented: you chose 2")
  if option == '3':
    print("to be implemented: you chose 3")



# pseudocode would be: begin with a list of filenames (taken from the current
# directory), then as you go through the list, check that each filename consist
# only of characters I consider to be valid: (a-zA-Z0-9.-_()[]+)
#  when an invalid character is found, present to the user the offending 
# filename along with at most 10 or 15 other offending filenames that contain
# the same character, offer the user the options "ignore this special character"
# or "replace all occurances of this special character with a user defined
# string" or "replace occurances case by case asking for a replacement for each"
# repeat above for all other invalid characters.

# [x] find all bad filenames in current directory 
# [x] compile list of bad filenames
# [x] add function to replace all occurances of bad character in string with new string (string inbuilt 'replace' method already does this)
# [ ] work with current directory AND all sub-directories