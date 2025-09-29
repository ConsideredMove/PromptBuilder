import os

def create_text_files():
    """Creates 100 text files named ext1.txt through ext100.txt"""
    
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create 100 text files
    for i in range(1, 101):
        filename = f"ext{i}.txt"
        filepath = os.path.join(script_dir, filename)
        
        try:
            with open(filepath, 'w') as file:
                file.write(f"This is text file number {i}\n")
                file.write(f"Created by the text file generator script\n")
            
            print(f"Created: {filename}")
            
        except IOError as e:
            print(f"Error creating {filename}: {e}")

if __name__ == "__main__":
    print("Creating 100 text files...")
    create_text_files()
    print("Done!")