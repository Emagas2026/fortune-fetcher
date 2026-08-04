#!/usr/bin/env python
import os
import sys
import subprocess
from datetime import datetime

BOOKS_DIR = "converted_ebooks"

def run_command(args):
    print(f"Running: {' '.join(args)}")
    env = os.environ.copy()
    env["QT_QPA_PLATFORM"] = "offscreen"
    env["QTWEBENGINE_DISABLE_SANDBOX"] = "1"
    
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                               text=True, env=env)
    full_output = []
    if process.stdout:
        for line in process.stdout:
            print(line, end="")
            full_output.append(line)
    process.wait()
    return "".join(full_output), process.returncode

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <mag_id> [issue_url]")
        sys.exit(1)
    
    mag_id = sys.argv[1]
    issue_url = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != "." else None
    
    if not os.path.exists(BOOKS_DIR):
        os.makedirs(BOOKS_DIR)
    
    print(f"--- Fetching Fortune Magazine ---")
    raw_epub = "temp_output.epub"
    
    recipe_path = "Fortune.recipe"
    if not os.path.exists(recipe_path):
        print("❌ Recipe file not found!")
        sys.exit(1)
    
    cmd = ["ebook-convert", recipe_path, raw_epub]
    
    # 如果提供了 URL，传递给 recipe
    if issue_url:
        cmd.append(f"--recipe-specific-option=issue_url:{issue_url}")
        print(f"Using custom URL: {issue_url}")
    
    output, code = run_command(cmd)
    
    if code != 0 or not os.path.exists(raw_epub):
        print("❌ Conversion failed")
        sys.exit(1)
    
    date_str = datetime.now().strftime("%Y%m%d")
    
    target_dir = os.path.join(BOOKS_DIR, date_str)
    os.makedirs(target_dir, exist_ok=True)
    
    final_epub = os.path.join(target_dir, f"{date_str} - Fortune Magazine.epub")
    os.rename(raw_epub, final_epub)
    
    print(f"✅ Success! Files saved in {target_dir}")

if __name__ == "__main__":
    main()
