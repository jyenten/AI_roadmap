# This program asks the user for their name and age, and then categorizes them based on their age group.

print("Welcome to the Age Categorizer!")

name = input("What is your name? ")

# The input function returns a string, so we need to convert it to an integer using int() for age.
try:
    age = int(input("What is your age? "))

    # We can use f-strings to format the output and include variables directly in the string.
    if age < 0 or age > 120:
        print("Age cannot be negative or greater than 120.")
    else:    
        current_year = 2026
        birth_year = current_year - age
        
        print(f"Hello, {name}! You were born in {birth_year}.")

    # We can use if-elif-else statements to categorize the user based on their age.
    if age < 13:
        print(f"Hello, {name}! You are a child.")

    elif 13 <= age < 18:
        print(f"Hello, {name}! You are a teenager.")

    elif age == 18:
        print(f"Hello, {name}! You are {age} years old. Congratulations on becoming an adult!")

    elif age < 65:
        print(f"Hello, {name}! You are an adult.")

    
except ValueError:
    print("Please enter a valid number for age.")