#example 1
#is this a comment
print("    /|")
print("   / |")
print("  /  |")
print(" /   |")
print("/____|")

# hello world basic program
print("Hello World")

# example 2 with variables
# insert variables into text using +variable name+
character_name = "George"
character_age = "1000"

print("some valid python program here where the character "
      "is named " + character_name + " and he is " + character_age +". ")
print("but i now want to change the name "
      "of the character to john... and his age to")

character_name = "Mike" # can rename variables here or later in the code

print("35. so how do i do that")

# types of data that can be stored in variables
# using quotes we can store strings - plain text

# we can also store numbers as seen below:
# character_age  = 50.2

# print("some valid python program here where the character "
#      "is named " +character_name+ " and he is " +character_age+". ")
# print("but i now want to change the name "
#      "of the character to john... and his age to")

# character_name = "Mike" #can rename variables here or later in the code

# print("35. so how do i do that")

# boolean expressions
# is_male = True

# working with strings in python
print("\nwhatever text i want goes here")
# use \n to insert a new line into the code
# creating string variables:
phrase = "giraffe academy"
print(phrase)

# you can concatenate two strings with the +

print(phrase + " is fun")

# functions using strings
print(phrase.lower())
# OR converting to uppercase
print(phrase.upper())

# checking upper or lowercase
print(phrase.isupper())

print(phrase.upper().isupper())

# determining string length
print(len(phrase))

# getting individual characters in the string
print(phrase[6]) # grabs the 6th character in the string
# strings start getting indexed with 0
print(phrase[0] + phrase[3] + phrase.upper())

# passing a parameter
print(phrase.index("g")) # returns the index of the first g in the string
# or
print(phrase.index("acad"))
# if the characer is not found in the string then it trows us an error

# replacing stuff in strings
print(phrase.replace("giraffe", "whatever i want"))

"""can i actually comment things out like this
i tink it does work but its not technically a comment its
just a multi line string but also just gets ignored by the program"""
print("\n")

# working with numbers
