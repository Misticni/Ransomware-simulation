# Ransomware Simulation

## 📌 Overview
This project is a **ransomware simulation** designed for cybersecurity research and educational purposes. It demonstrates the **encryption and decryption** process of ransomware attacks in a **controlled environment**. 

**⚠ Disclaimer:**  
This project is intended **only for ethical research and educational purposes**. Misuse of this code for malicious activities is **strictly prohibited**.

---

## 🔍 Features
- **File Encryption**: Encrypts files using AES-based **Fernet** encryption.
- **Key Management**: Generates an encryption key and uploads it to **Dropbox**.
- **Ransom Note Generation**: Creates a ransom note mimicking real-world ransomware behavior.
- **File Decryption**: Allows decryption of files with the correct key.

---

## 🛠 Technologies Used
- **Python** 🐍
- **Cryptography (Fernet encryption)**
- **Dropbox API** (for remote key storage)
- **VirtualBox** (for safe testing)

---

## 🚀 How to Use

### Encryption Process
1. Run the **ransomware simulation script**:
   ```bash
   python ransomware_simulation.py
