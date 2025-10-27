# 🚀 COMPLETE INSTALLATION GUIDE - E2E Encrypted Messenger

## 📋 Table of Contents
1. [Prerequisites Check](#prerequisites-check)
2. [Download & Setup](#download--setup)
3. [Install Dependencies](#install-dependencies)
4. [Test the System](#test-the-system)
5. [Run CLI Application](#run-cli-application)
6. [Run Web UI](#run-web-ui)
7. [Troubleshooting](#troubleshooting)
8. [Demo Preparation](#demo-preparation)

---

## 1. Prerequisites Check

### Step 1.1: Check if Python is Installed

**On Windows:**
1. Press `Windows Key + R`
2. Type `cmd` and press Enter
3. In the black window, type:
   ```
   python --version
   ```
4. You should see something like: `Python 3.9.7` or `Python 3.10.0`

**On Mac:**
1. Press `Command + Space`
2. Type `terminal` and press Enter
3. In the terminal, type:
   ```
   python3 --version
   ```
4. You should see something like: `Python 3.9.7`

**On Linux:**
1. Open Terminal (usually Ctrl+Alt+T)
2. Type:
   ```
   python3 --version
   ```

### ✅ What You Need:
- Python 3.7 or higher
- If you see "Python 3.X.X" where X is 7 or higher, you're good!

### ❌ If Python is NOT installed:

**Windows:**
1. Go to https://www.python.org/downloads/
2. Click "Download Python 3.11.X" (big yellow button)
3. Run the installer
4. **IMPORTANT:** Check the box "Add Python to PATH"
5. Click "Install Now"
6. Restart your computer

**Mac:**
1. Python 3 is usually pre-installed
2. If not, install Homebrew first: https://brew.sh/
3. Then run: `brew install python3`

**Linux:**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

---

## 2. Download & Setup

### Step 2.1: Create Project Folder

**Windows:**
1. Open File Explorer
2. Go to your Documents folder
3. Right-click → New → Folder
4. Name it: `E2E-Messenger`
5. Open this folder

**Mac/Linux:**
```bash
cd ~
mkdir E2E-Messenger
cd E2E-Messenger
```

### Step 2.2: Save Your Python Files

You need to save these files in your `E2E-Messenger` folder:

Note: This is for Running as A CLI program, This and all the Depandancies

1. **auth.py** - Copy from your document #1
2. **encryption.py** - Copy from your document #2
3. **main.py** - Copy from your document #3
4. **message_storage.py** - **USE THE FIXED VERSION** from my artifacts above
5. **messaging.py** - Copy from your document #5
6. **requirements.txt** - Dependencies list

### Step 2.3: Save New Files I Created

For Running webui also get:

7. **test_system.py** - The complete test script
8. **api.py** - Flask API for web UI
9. **index.html** - Web UI (save this one!)

### Step 2.4: Verify Your Files

**Windows:**
1. Open your `E2E-Messenger` folder
2. You should see these files:
   - auth.py
   - encryption.py
   - main.py
   - message_storage.py (FIXED version!)
   - messaging.py
   - test_system.py (NEW)
   - api.py (NEW)
   - requirements.txt (NEW)
   - index.html (NEW)

**Mac/Linux:**
```bash
ls -la
```

You should see all 9 files listed above.

---

## 3. Install Dependencies

### Step 3.1: Open Terminal/Command Prompt in Project Folder

**Windows Method 1:**
1. Open your `E2E-Messenger` folder in File Explorer
2. Hold Shift and right-click in empty space
3. Click "Open PowerShell window here" or "Open Command Prompt here"

**Windows Method 2:**
1. Press `Windows Key + R`
2. Type `cmd` and press Enter
3. Type: `cd Documents\E2E-Messenger` and press Enter

**Mac:**
1. Open Finder, go to your E2E-Messenger folder
2. Right-click the folder → Services → New Terminal at Folder

**Linux:**
1. Open Terminal
2. Navigate to folder: `cd ~/E2E-Messenger`

### Step 3.2: Install Core Dependencies

**Copy and paste this EXACT command:**

**Windows (in Command Prompt or PowerShell):**
```
pip install cryptography filelock
```

**Mac/Linux (in Terminal):**
```
pip3 install cryptography filelock
```

**What you should see:**
```
Collecting cryptography
Downloading cryptography-XX.X.X...
Installing collected packages: cryptography, filelock
Successfully installed cryptography-XX.X.X filelock-X.X.X
```

### ⏱️ This takes 1-2 minutes

### Step 3.3: Install Optional Web Dependencies

**If you want to run the web UI with real encryption:**

**Windows:**
```
pip install flask flask-cors
```

**Mac/Linux:**
```
pip3 install flask flask-cors
```

### ✅ Installation Complete!

If you see "Successfully installed..." you're ready to go!

---

## 4. Test the System

### Step 4.1: Run the Test Suite

**Make sure you're still in the E2E-Messenger folder!**

**Windows:**
```
python test_system.py
```

**Mac/Linux:**
```
python3 test_system.py
```

### Step 4.2: What You Should See

The test will run for about 10-15 seconds. You should see:

```
============================================================
E2E ENCRYPTED MESSENGER - SYSTEM TEST & DEMO
============================================================

[1/7] Testing imports...
✓ auth.py imported successfully
✓ encryption.py imported successfully
✓ message_storage.py imported successfully
✓ messaging.py imported successfully

[2/7] Testing directory setup...
✓ Directories created successfully
  - Users/ directory exists
  - Keys/ directory exists
  - messages/ directory exists

[3/7] Testing password hashing...
✓ Password hashed successfully
✓ Correct password verification works
✓ Wrong password correctly rejected

[4/7] Testing RSA key generation...
✓ RSA keypair generated (2048-bit)
✓ Public key serialized to PEM format

[5/7] Testing user creation...
✓ User 'alice' created and saved
✓ User 'bob' created and saved
✓ Users loaded successfully from files
✓ Found 2 users: alice, bob

[6/7] Testing E2E encryption...
✓ Message encrypted with Bob's public key
✓ Message decrypted with Bob's private key
✓ Encryption/Decryption successful - messages match!

[7/7] Testing message storage...
✓ Message saved to storage
✓ Retrieved 1 message(s) for Bob
✓ Retrieved message decrypted
✓ Full round-trip successful!
✓ get_user_public_key() works correctly

============================================================
✓ ALL TESTS PASSED!
============================================================

System Status:
  ✓ Authentication system working
  ✓ RSA-2048 key generation working
  ✓ AES-256-GCM encryption working
  ✓ End-to-end encryption working
  ✓ Message storage working
  ✓ User management working

Demo users created:
  - alice (password: AlicePassword123)
  - bob (password: BobPassword123)

============================================================
READY FOR HACKATHON DEMO!
============================================================
```

### ✅ If You See This: YOU'RE READY!

### ❌ If You See Errors:

**Error: "No module named 'cryptography'"**
```
Solution: pip install cryptography filelock
```

**Error: "No module named 'filelock'"**
```
Solution: pip install filelock
```

**Error: "File not found"**
```
Solution: Make sure you're in the E2E-Messenger folder
Check: dir (Windows) or ls (Mac/Linux)
```

---

## 5. Run CLI Application

### Step 5.1: Start the Application

**Windows:**
```
python main.py
```

**Mac/Linux:**
```
python3 main.py
```

### Step 5.2: What You Should See

```
=== E2E Encrypted Messaging App ===

========================================
1. Login
2. Sign Up
3. Exit
========================================

Choose an option (1-3):
```

### Step 5.3: Login as Demo User

1. Type `1` and press Enter (Login)
2. Enter username: `alice`
3. Enter password: `AlicePassword123`

You should see:
```
✓ Logged in as alice
✓ Private key loaded

=== E2E Encrypted Messaging App ===

Welcome, alice!

========================================
1. Send Message
2. Check Inbox
3. Logout
========================================

Choose an option (1-3):
```

### Step 5.4: Send a Test Message

1. Type `1` and press Enter (Send Message)
2. To: `bob`
3. Message: `Hey Bob! This is encrypted! 🔒`
4. You should see: `✓ Message sent successfully!`

### Step 5.5: Check Messages as Bob

1. Type `3` to logout
2. Type `1` to login
3. Username: `bob`
4. Password: `BobPassword123`
5. Type `2` to Check Inbox
6. You should see the decrypted message!

### ✅ If This Works: Your System is Perfect!

---

## 6. Run Web UI

### Option A: Quick Demo Mode (No Backend Needed)

**Step 6A.1: Open the HTML File**

1. Find `index.html` in your E2E-Messenger folder
2. Double-click it
3. It should open in your web browser

**Step 6A.2: Login to Demo**

1. Click "Log In" button
2. Username: `alice`
3. Password: `demo`
4. Click "Log In"

**Step 6A.3: Explore the Interface**

- You'll see a beautiful interface with:
  - Send Message panel (left)
  - Inbox panel (right)
  - Demo messages showing encryption indicators

**This is perfect for showing the UI to judges!**

---

### Option B: Full Mode with Real Encryption

**Step 6B.1: Start Python API**

**Open a NEW terminal/command prompt window** (keep the old one open if you want)

**Windows:**
1. Navigate to folder: `cd Documents\E2E-Messenger`
2. Run: `python api.py`

**Mac/Linux:**
```bash
cd ~/E2E-Messenger
python3 api.py
```

**What you should see:**
```
============================================================
E2E Encrypted Messenger - API Server
============================================================

Starting Flask API server...
API will be available at: http://localhost:5000

Endpoints:
  POST /api/signup    - Create account
  POST /api/login     - Login
  POST /api/logout    - Logout
  POST /api/send      - Send message
  POST /api/inbox     - Get inbox
  GET  /api/users     - List users
  GET  /api/health    - Health check

Press Ctrl+C to stop
============================================================

 * Running on http://127.0.0.1:5000
```

**✅ Leave this window OPEN! The API needs to keep running!**

**Step 6B.2: Open Web UI**

1. Open `index.html` in your browser (double-click)
2. You should see at the top:
   ```
   ✓ Connected to Python Backend
   ```

**Step 6B.3: Create a Real Account**

1. Click "Sign Up"
2. Choose username (min 3 characters): `testuser`
3. Choose password (min 8 characters): `password123`
4. Confirm password: `password123`
5. Click "Create Account"
6. You should see: "Account created! Please log in."

**Step 6B.4: Login**

1. Username: `testuser`
2. Password: `password123`
3. Click "Log In"

**Step 6B.5: Send Real Encrypted Message**

1. In "Send Message" panel:
   - To: `alice` (or `bob`)
   - Message: Type anything!
2. Click "Send Encrypted Message"
3. You should see: "Message sent to alice!"

**Step 6B.6: Check Inbox as Another User**

1. Click "Logout"
2. Login as `alice` / `AlicePassword123`
3. Click the refresh button (🔄)
4. You should see your encrypted message, now decrypted!

**✅ This is the FULL SYSTEM with real RSA+AES encryption!**

---

## 7. Troubleshooting

### Problem: "pip is not recognized"

**Windows Solution:**
```
python -m pip install cryptography filelock
```

**Mac/Linux Solution:**
```
python3 -m pip install cryptography filelock
```

### Problem: "Permission denied"

**Mac/Linux Solution:**
```
sudo pip3 install cryptography filelock
```
(You'll need to enter your password)

### Problem: API won't start - "Address already in use"

**Solution:** Another program is using port 5000

**Windows:**
1. Open Command Prompt as Administrator
2. Run: `netstat -ano | findstr :5000`
3. Find the PID (last number)
4. Run: `taskkill /PID [that number] /F`

**Mac/Linux:**
```bash
lsof -ti:5000 | xargs kill -9
```

Or change the port in `api.py`:
```python
app.run(debug=True, port=5001)  # Use 5001 instead
```

### Problem: Web UI shows "Demo Mode" even with API running

**Solutions:**
1. Make sure API is actually running (check terminal)
2. Refresh the web page (F5)
3. Check browser console for errors (F12 → Console tab)
4. Make sure `flask-cors` is installed: `pip install flask-cors`

### Problem: Test fails with "FileNotFoundError"

**Solution:** You're not in the right folder

**Check where you are:**
- Windows: `cd` (shows current folder)
- Mac/Linux: `pwd` (shows current path)

**Navigate to correct folder:**
- Windows: `cd Documents\E2E-Messenger`
- Mac/Linux: `cd ~/E2E-Messenger`

### Problem: "ModuleNotFoundError: No module named 'filelock'"

**Solution:**
```
pip install filelock
```

or

```
pip3 install filelock
```

### Problem: Messages not showing in inbox

**Check:**
1. Are you logged in as the recipient?
2. Is the recipient's username spelled correctly?
3. Did you use an existing user (alice/bob) or create a new one?

**Reset everything:**
```bash
# Windows
rmdir /s Users Keys messages

# Mac/Linux
rm -rf Users/ Keys/ messages/

# Then run tests again
python test_system.py
```

---

## 8. Demo Preparation

### 15 Minutes Before Demo

**Checklist:**
- [ ] All dependencies installed (`pip list` shows cryptography, filelock)
- [ ] Test passed (run `python test_system.py`)
- [ ] CLI works (test `python main.py`, login as alice)
- [ ] Web UI opens (double-click `index.html`)
- [ ] Terminal font is LARGE (16pt+)
- [ ] Have 2 terminal windows ready
- [ ] Close unnecessary programs

### Terminal Setup

**Windows - Make Font Larger:**
1. Right-click terminal title bar
2. Properties → Font
3. Choose size 18 or 20

**Mac - Make Font Larger:**
1. Terminal → Preferences
2. Profiles → Text
3. Change font size to 18pt

**Linux:**
1. Terminal → Preferences
2. Increase font size to 18

### Have These Commands Ready

**Terminal 1 (Main Demo):**
```bash
python test_system.py
python main.py
```

**Terminal 2 (Show Encryption):**
```bash
# Windows
type messages\bob.json

# Mac/Linux
cat messages/bob.json
```

**Terminal 3 (Optional - API):**
```bash
python api.py
```

### Practice Run-Through

**Do this ONCE before judges:**

1. Run `python test_system.py` (15 seconds)
2. Run `python main.py` (30 seconds)
   - Login: alice / AlicePassword123
   - Send message to: bob
   - Logout
3. Show encrypted file (10 seconds)
4. Login as bob, check inbox (20 seconds)
5. Open web UI (15 seconds)

**Total: 90 seconds** ✅

---

## 9. Quick Reference Commands

### Windows Commands
```batch
# Navigate to folder
cd Documents\E2E-Messenger

# Install dependencies
pip install cryptography filelock flask flask-cors

# Run tests
python test_system.py

# Run CLI app
python main.py

# Run API
python api.py

# Show encrypted messages
type messages\bob.json

# List files
dir

# Check Python version
python --version
```

### Mac/Linux Commands
```bash
# Navigate to folder
cd ~/E2E-Messenger

# Install dependencies
pip3 install cryptography filelock flask flask-cors

# Run tests
python3 test_system.py

# Run CLI app
python3 main.py

# Run API
python3 api.py

# Show encrypted messages
cat messages/bob.json

# List files
ls -la

# Check Python version
python3 --version
```

---

## 10. File Structure Reference

After setup, your folder should look like this:

```
E2E-Messenger/
├── auth.py                  # User authentication
├── encryption.py            # RSA + AES encryption
├── main.py                  # Main CLI app
├── message_storage.py       # Storage (FIXED version!)
├── messaging.py             # Messaging UI
├── test_system.py          # Test suite (NEW)
├── api.py                  # Flask API (NEW)
├── requirements.txt        # Dependencies (NEW)
├── index.html              # Web UI (NEW)
├── Users/                  # Created automatically
│   ├── alice.json
│   └── bob.json
├── Keys/                   # Created automatically
│   ├── alice.key
│   └── bob.key
└── messages/               # Created automatically
    └── bob.json
```

---

## ✅ FINAL VERIFICATION

**Run this checklist RIGHT NOW:**

```bash
# 1. Check Python
python --version
# Should show: Python 3.X.X

# 2. Install dependencies
pip install cryptography filelock flask flask-cors

# 3. Run tests
python test_system.py
# Should show: ✓ ALL TESTS PASSED!

# 4. Test CLI
python main.py
# Login: alice / AlicePassword123

# 5. Test Web UI
# Double-click index.html
# Login: alice / demo
```

**If all 5 steps work: YOU'RE READY! 🎉**

---

## 🆘 EMERGENCY HELP

### Still Having Problems?

**Check these in order:**

1. **Python installed?**
   ```
   python --version
   ```
   If not, reinstall Python (see Section 1.1)

2. **In correct folder?**
   ```
   dir    # Windows
   ls     # Mac/Linux
   ```
   Should see all 9 .py files

3. **Dependencies installed?**
   ```
   pip list
   ```
   Should see: cryptography, filelock

4. **Files saved correctly?**
   - Check file sizes (each should be > 1 KB)
   - Make sure no ".txt" extension added

5. **Try fresh start:**
   ```bash
   # Delete everything
   rm -rf Users/ Keys/ messages/
   
   # Run tests
   python test_system.py
   ```

---

## 🎉 SUCCESS!

If you made it here and everything works:

**YOU NOW HAVE:**
- ✅ Working E2E encrypted messenger
- ✅ Beautiful web interface  
- ✅ Complete test suite
- ✅ Ready for demo

**GO WIN THAT HACKATHON! 🏆**

---

## 📞 Quick Help Summary

| Problem | Solution |
|---------|----------|
| "pip not found" | `python -m pip install ...` |
| "permission denied" | Use `sudo` on Mac/Linux |
| "module not found" | `pip install [module]` |
| "port in use" | Change port or kill process |
| Tests fail | Check you're in right folder |
| Web UI doesn't load | Try different browser |
| API won't connect | Install flask-cors |

---

**You're all set! Follow this guide step-by-step and you'll have a working demo in 15-20 minutes!** 🚀