import os
from cryptography.fernet import Fernet

# Load the encryption key
def load_key(key_file="encryption_key.key"):
    with open(key_file, "rb") as keyfile:
        return keyfile.read()

# Decrypt selected files in a specified directory
def decrypt_files(directory, key):
    cipher = Fernet(key)

    if not os.path.exists(directory):
        print(f"❌ Directory not found: {directory}")
        return

    print(f"\n🔓 Decrypting files in: {directory}")

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)

            # Skip ransom notes
            if file_path.endswith("README_RESTORE_FILES.txt"):
                continue  

            try:
                # Read the encrypted file
                with open(file_path, "rb") as f:
                    encrypted_data = f.read()
                
                # Decrypt the file
                decrypted_data = cipher.decrypt(encrypted_data)
                
                # Overwrite the file with decrypted data
                with open(file_path, "wb") as f:
                    f.write(decrypted_data)
                
                print(f"✔ Decrypted: {file_path}")

            except Exception as e:
                print(f"❌ Failed to decrypt {file_path}: {e}")

    # Remove ransom note after successful decryption
    ransom_note_path = os.path.join(directory, "README_RESTORE_FILES.txt")
    if os.path.exists(ransom_note_path):
        os.remove(ransom_note_path)
        print(f"🗑 Ransom note deleted: {ransom_note_path}")

if __name__ == "__main__":
    key_file = "encryption_key.key"

    # Load the encryption key
    key = load_key(key_file)

    while True:
        # Get a single directory from the user
        directory = input("Enter a directory to decrypt (or type 'exit' to quit): ").strip()
        
        if directory.lower() == "exit":
            print("🔚 Exiting decryption process.")
            break

        # Decrypt only the chosen directory
        decrypt_files(directory, key)
