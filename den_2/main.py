print("=== Day 2: Loops ===")
# For Loops


try:

    number = int(input("Enter the final number: "))
   

    if number < 1:
        print("Please enter a positive integer.")
    else:
        total = 0
        even_count = 0
        odd_count = 0
        even_sum = 0
        odd_sum = 0
        

   

        for i in range(1, number + 1):
            total += i
            print(f"Adding {i}, current total: {total}")
            
            if i % 2 == 0:
                    even_count += 1
                    even_sum += i
            else:
                odd_count += 1
                odd_sum += i
                
           # print(f"i = {i}, even_count = {even_count}, odd_count = {odd_count}")
        average = total / number

        print(f"Sum of numbers from 1 to {number} is: {total}")     
        print(f"Even numbers count: {even_count}")
        print(f"Odd numbers count: {odd_count}")
        print(f"Sum of even numbers: {even_sum}")
        print(f"Sum of odd numbers: {odd_sum}")
        print(f"Average of numbers from 1 to {number} is: {round(average, 2)}")

except ValueError:
    print("Please enter a valid integer.")




print("\n=== While Loops ===")


counter = 5

while counter >= 1:
    print(counter)
    counter -= 1

print("Done.")

print("\n===Password Check===")

password = ""
attempts = 0
max_attempts = 3

while password != "python" and attempts < max_attempts:
    password = input("Enter the password: ")
    attempts += 1

    if password != "python":
        remaining_attempts = max_attempts - attempts
        print(f"Attempts remaining: {remaining_attempts}")

if password == "python":
    print("Access granted.")
    print(f"Number of attempts: {attempts}")
else:
    print("Access denied.")

