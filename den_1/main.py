name = input("What is your name? ")
age = int(input("What is your age? ")) 


print(f"Hello, {name}! You are {age} years old.")
print(f"Za 5 let mi bude {age + 5} let.")

if age < 13:
    print("You are a child.")
elif age < 18:
    print("You are a teenager.")
elif age == 18:
    print("Congratulations on becoming an adult!")
else:
    print("You are an adult.")

