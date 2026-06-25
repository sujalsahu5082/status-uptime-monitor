import os
import sys
import random
import subprocess
import time
from datetime import datetime

def run_git_cmd(args):
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[WARNING] Git command failed: {' '.join(args)}")
        print(f"Error: {result.stderr}")
    return result.returncode == 0

def main():
    # 1. Random sleep to vary commit times (between 0 and 1800 seconds / 30 mins)
    sleep_seconds = random.randint(0, 1800)
    print(f"[INFO] Randomizing run: sleeping for {sleep_seconds} seconds...")
    time.sleep(sleep_seconds)
    
    # 2. Determine number of commits to make today (realistic distribution)
    # 0 commits: 15% chance (rest days)
    # 1 commit: 45% chance
    # 2 commits: 25% chance
    # 3 commits: 10% chance
    # 4 commits: 5% chance
    choices = [0] * 15 + [1] * 45 + [2] * 25 + [3] * 10 + [4] * 5
    num_commits = random.choice(choices)
    print(f"[INFO] Selected {num_commits} commits for today.")
    
    if num_commits == 0:
        print("[INFO] No contributions selected for today. Enjoy the day off!")
        sys.exit(0)
        
    username = os.environ.get("GITHUB_ACTOR", "sujalsahu5082")
    user_email = f"{username}@users.noreply.github.com"
    
    # Configure Git in the runner env
    run_git_cmd(["git", "config", "user.name", username])
    run_git_cmd(["git", "config", "user.email", user_email])
    
    commit_messages = [
        "chore(status): update uptime logs [heartbeat]",
        "chore(ci): update status heartbeat checkpoints",
        "docs(status): append health logs check",
        "chore(status): log checkpoint status check",
        "fix(status): resolve system logger heartbeat check"
    ]
    
    log_path = "heartbeat.log"
    
    for i in range(num_commits):
        if i > 0:
            # Vary the commit time slightly for multiple commits
            inter_sleep = random.randint(10, 45)
            print(f"[INFO] Sleeping for {inter_sleep}s between commits...")
            time.sleep(inter_sleep)
            
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_id = random.randint(1000, 9999)
        
        # Modify log file
        with open(log_path, "a") as f:
            f.write(f"heartbeat: system check-in at {current_time} - log_id={log_id} status=OK\n")
            
        # Commit changes
        run_git_cmd(["git", "add", log_path])
        commit_msg = random.choice(commit_messages)
        run_git_cmd(["git", "commit", "-m", commit_msg])
        print(f"[SUCCESS] Committed: '{commit_msg}'")
        
    # Push back to repository main branch
    print("[INFO] Pushing commits to GitHub...")
    if run_git_cmd(["git", "push", "origin", "main"]):
        print("[SUCCESS] Contributions pushed successfully!")
    else:
        print("[ERROR] Push failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
