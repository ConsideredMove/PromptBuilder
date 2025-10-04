import os

# Get user input for maximum number
max_num = int(input("Enter the maximum number: "))

# Generate files
for letter_pos in range(1, max_num + 1):
    letter = chr(64 + letter_pos)  # 65 is 'A', so 64+1 gives us 'A'
    
    for num in range(1, max_num + 1):
        filename = f"or{letter}{num}.txt"
        
        # Skip if file already exists
        if os.path.exists(filename):
            print(f"Skipping {filename} (already exists)")
            continue
        
        # Create file with "__no__" content
        with open(filename, 'w') as f:
            f.write("__no__")
        
        print(f"Created {filename}")

print(f"\nDone! Created files from orA1 to or{chr(64 + max_num)}{max_num}")
