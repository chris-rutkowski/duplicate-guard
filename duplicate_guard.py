import fnmatch
import hashlib
import json
import os
import sys

def load_ignore_patterns(ignore_file):
    with open(ignore_file, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

def should_ignore(file, patterns):
    return any(fnmatch.fnmatch(file, pattern) for pattern in patterns)

def calculate_checksum(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def get_all_repository_files(ignore_patterns):
    repo_files = []
    for root, _, files in os.walk("."):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, ".")
            if not should_ignore(relative_path, ignore_patterns):
                repo_files.append(relative_path)
    return repo_files

def load_files_from_json(file_paths):
    files = []
    for file_path in file_paths:
        with open(file_path, "r") as f:
            files.extend(json.load(f))
    return files

ignore_patterns = load_ignore_patterns(sys.argv[1])
files = load_files_from_json(sys.argv[2:])

# Step 1: Build a checksum map for all existing repository files
print("Calculating checksums for all repository files...")
checksums = {}
for file in get_all_repository_files(ignore_patterns):
    checksum = calculate_checksum(file)
    checksums[checksum] = file
print(f"Done, {len(checksums)} checksums")

# Step 2: Check new/modified files against the repository and themselves
exit_code = 0

for file in files:
    if not file or not os.path.isfile(file):
        continue

    if should_ignore(file, ignore_patterns):
        print(f"Ignoring: '{file}'")
        continue

    print(f"Processing: '{file}'")

    checksum = calculate_checksum(file)

    if checksum in checksums:
        if checksums[checksum] == file:
            continue

        print(f"Error: '{file}' is a duplicate of '{checksums[checksum]}'")
        exit_code = 1
    else:
        checksums[checksum] = file

sys.exit(exit_code)
