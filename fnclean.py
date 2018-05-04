import os

# go through the current directory and find any filenames that contain weird
# characters, then for each unique weird character, ask the user a question
# showing the first 15 or however many results of filenames containing that 
# character and asking the user if they want to 'replace all instances of the
# character with another character?', 'ignore the character', 'cycle through
# the list of filenames and ask for a replacement for each one?'. and recurse 
# through all subdirectories

current_directory = os.getcwd()
files = os.listdir(current_directory)
print(os.listdir(current_directory))

for file in files:
  print(file, end='')  # the second param requires python3:python3.5 fnclean.py
  if os.path.isdir(file):
    print(" is a directory")
  elif os.path.isfile(file):
    print(" is a file")


# pseudocode would be: begin with a list of filenames (taken from the current
# directory), then as you go through the list, check that each filename consist
# only of characters I consider to be valid: (a-zA-Z0-9.-_()[]+)
#  when an invalid character is found, present to the user the offending 
# filename along with at most 10 or 15 other offending filenames that contain
# the same character, offer the user the options "ignore this special character"
# or "replace all occurances of this special character with a user defined
# string" or "replace occurances case by case asking for a replacement for each"
# repeat above for all other invalid characters.