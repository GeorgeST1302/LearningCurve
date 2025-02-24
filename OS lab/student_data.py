import os
file_name = "student_data.txt"
with open(file_name, "w") as file:
    # Step 2: Write the required lines into the file
    file.write("Name: Jane Doe\n")
    file.write("Roll Number: 67890\n")
    file.write("Department: AI-DS\n")

# Step 3: Read and print the file contents
with open(file_name, "r") as file:
    print("File Contents:")
    print(file.read())

# Step 4: Rename the file to `ai_ds_data.txt`
new_file_name = "ai_ds_data.txt"
os.rename(file_name, new_file_name)
print(f"File renamed to: {new_file_name}")

# Step 5: Delete the file
os.remove(new_file_name)
print(f"File {new_file_name} deleted.")
