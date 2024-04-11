import os

def rename_files_to_lowercase(directory):
    # Define the set of desired file extensions
    target_extensions = {'pdf', 'xls', 'xlsx', 'doc', 'docx'}
    
    # List all files in the given directory
    files = os.listdir(directory)
    for filename in files:
        # Extract the file extension and convert it to lowercase
        file_extension = filename.split('.')[-1].lower()
        
        # Check if the file has the desired extension
        if file_extension in target_extensions:
            # Construct the full file path
            old_file = os.path.join(directory, filename)
            new_file = os.path.join(directory, filename.lower())
            
            # Check if the filename contains uppercase characters
            if filename != filename.lower():
                # Rename the file to its lowercase version
                os.rename(old_file, new_file)
                print(f'Renamed: {filename} -> {filename.lower()}')
            else:
                # The file is already in lowercase, no need to rename
                print(f"Skipping (already lowercase): {filename}")

if __name__ == "__main__":
    # Expand the '~' to the full path of the user's home directory
    directory = os.path.expanduser('~/Downloads/01')
    rename_files_to_lowercase(directory)
