from pykeepass import PyKeePass
import os

# --- Configuration ---

# 1. This MUST be the correct UUID for your specific server.
# (See previous message on how to find this if you're not sure)
GITLAB_SERVER_UUID = "224be9a9-8758-4e0d-bf74-271ebf2f5269" 

# 2. Your token
GITLAB_API_TOKEN = "glpat-your-token-here"

# 3. Your new database settings
DB_PATH = 'gitlab_creds.kdbx'
DB_PASSWORD = 'your-strong-master-password' # Master password for the file

# --- Script ---

# This is the entry title IntelliJ will look for
ENTRY_TITLE = f"IntelliJ Platform GitLab — {GITLAB_SERVER_UUID}"

kp = None

if not os.path.exists(DB_PATH):
    print(f"Creating new KDBX v4 database: {DB_PATH}")
    # This is the fix:
    # We explicitly create a KDBX version 4 file.
    # This matches modern IntelliJ and uses ChaCha20 for protection.
    kp = PyKeePass(DB_PATH, password=DB_PASSWORD, kdbx_version=4)
else:
    print(f"Opening existing database: {DB_PATH}")
    # If file exists, just open it
    kp = PyKeePass(DB_PATH, password=DB_PASSWORD)


# Find the entry
entry = kp.find_entries(title=ENTRY_TITLE, first=True)

if entry:
    print(f"Found existing entry, updating token...")
    entry.username = GITLAB_SERVER_UUID
    entry.password = GITLAB_API_TOKEN # This setter automatically protects it
else:
    print(f"No entry found, creating new one...")
    entry = kp.add_entry(
        destination_group=kp.root_group,
        title=ENTRY_TITLE,
        username=GITLAB_SERVER_UUID,
        password=GITLAB_API_TOKEN # This uses the protected setter
    )

# Save the database
kp.save()

print("\n-------------------------------------------------")
print(f"Successfully saved credentials to {DB_PATH}")
print("You can now point IntelliJ to this file:")
print("Settings > Appearance & Behavior > System Settings > Passwords")
