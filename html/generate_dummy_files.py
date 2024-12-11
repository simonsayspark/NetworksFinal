import os
import random
import string

# Define the folder where the dummy files will be created
OUTPUT_FOLDER = "dummy_files"

# Ensure the folder exists
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Function to generate random content
def generate_random_content(length=100):
    return ''.join(random.choices(string.ascii_letters + string.digits + " ", k=length))

# Function to create dummy files
def create_dummy_files(num_files=10):
    for i in range(1, num_files + 1):
        filename = f"file_{i}.txt"
        filepath = os.path.join(OUTPUT_FOLDER, filename)
        
        with open(filepath, "w") as file:
            file.write(f"This is file {i}\n")
            file.write(generate_random_content())

    print(f"Created {num_files} dummy files in '{OUTPUT_FOLDER}' folder.")

# Call the function to create dummy files
if __name__ == "__main__":
    create_dummy_files(10)  # Change the number to generate more or fewer files
