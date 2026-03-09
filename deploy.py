#!/usr/bin/env python3
"""
Deployment script for MCharts.

This script automates the deployment process by:
1. Syncing the version from package.json to index.html
2. Running `npm test` (Playwright tests)
3. Committing and tagging the version in the source repository
4. Copying index.html, app.js, and style.css to the GitHub Pages repository
5. Committing and pushing the changes in the target repository
"""

import shutil
import os
import subprocess
import sys
import json
import re

def get_version():
    with open("package.json", "r") as f:
        data = json.load(f)
        return data.get("version", "0.0.0")

def update_index_version(version):
    print(f"Updating index.html version to {version}...")
    with open("index.html", "r") as f:
        content = f.read()
    
    # Matches "Version X.Y.Z" or "vX.Y.Z" and replaces it
    new_content = re.sub(r"(Version |v)\d+\.\d+\.\d+", r"\g<1>" + version, content)
    
    if new_content == content:
        print("Warning: Version string not found in index.html or already updated.")
    
    with open("index.html", "w") as f:
        f.write(new_content)

def run_command(command, error_msg):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        print(f"Error: {error_msg}")
        sys.exit(1)

def main():
    # Ensure we are in the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    version = get_version()
    tag = f"v{version}"

    # 1. Sync Version
    update_index_version(version)

    # 2. Run Tests
    print("Running tests...")
    run_command(["npm", "test"], "Tests failed. Aborting deployment.")

    # 3. Commit and Tag Source Repo
    print(f"Committing and tagging source repo with {tag}...")
    try:
        subprocess.run(["git", "add", "-A"], check=True)
        # Commit might fail if no changes
        subprocess.run(["git", "commit", "-m", f"Release {tag}"], check=False)
        # Use -f to overwrite tag locally
        subprocess.run(["git", "tag", "-af", tag, "-m", f"Release {tag}"], check=False)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        subprocess.run(["git", "push", "origin", "--tags", "-f"], check=True)
    except Exception as e:
        print(f"Git source repo operation failed: {e}")

    # 4. Define Source and Destination for Deployment
    # MCharts is simple enough to just copy individual files
    files_to_deploy = ["index.html", "app.js", "style.css"]
    target_repo_dir = "../michael-f-ellis.github.io"
    target_sub_dir = "mcharts"
    destination_full_path = os.path.join(target_repo_dir, target_sub_dir)

    print(f"Deploying to {destination_full_path}...")

    if not os.path.exists(target_repo_dir):
        print(f"Error: Target repository directory '{target_repo_dir}' does not exist.")
        sys.exit(1)

    if not os.path.exists(destination_full_path):
        os.makedirs(destination_full_path, exist_ok=True)

    # 5. Copy Files
    try:
        for filename in files_to_deploy:
            shutil.copy2(filename, os.path.join(destination_full_path, filename))
        print("Files copied successfully.")
    except Exception as e:
        print(f"Error copying files: {e}")
        sys.exit(1)

    # 6. Git Operations in Target Repo
    cwd = os.getcwd()
    try:
        os.chdir(target_repo_dir)
        subprocess.run(["git", "add", target_sub_dir], check=True)
        subprocess.run(["git", "commit", "-m", f"Deploy mcharts {tag}"], check=False)
        subprocess.run(["git", "push"], check=True)
        print("Deployment push complete.")
    except Exception as e:
        print(f"Git target repo operation failed: {e}")
    finally:
        os.chdir(cwd)

if __name__ == "__main__":
    main()
