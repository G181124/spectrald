import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import argparse
from sigunit.checker import run_username_check
from sigunit.utils import color_text

def print_banner():
    banner = r"""
                          __             __    __
    _________  ___  _____/ /__________ _/ /___/ /
   / ___/ __ \/ _ \/ ___/ __/ ___/ __ `/ / __  / 
  (__  ) /_/ /  __/ /__/ /_/ /  / /_/ / / /_/ /  
 /____/ .___/\___/\___/\__/\__/_/   \__,_/_/\__,_/   
     /_/                                          
    """
    print(color_text(banner, 'yellow'))

    # Menambahkan titel di bawah banner dengan warna
    print(color_text("   SpectraLD - Investigative Username OSINT Tool\n", 'blue'))

def main():
    print_banner()
    parser = argparse.ArgumentParser(
        description="SpectraLD RLD - Investigative Username OSINT Tool\n"
                    "SpectraLD is an open-source OSINT tool designed to search usernames across multiple platforms. "
                    "This tool helps to identify whether a particular username exists on various online services, "
                    "and gathers available metadata information when requested. It's optimized for speed and "
                    "allows multithreaded searches to enhance performance.\n\n"
                    "Usage example:\n"
                    "  ./run.sh --username user1 user2 --fast --verbose\n"
                    "This will search for 'user1' and 'user2' on supported platforms."
    )
    
    # Argument for usernames
    parser.add_argument(
        "--username", 
        help="One or more usernames to search for across supported platforms. You can input multiple usernames "
             "separated by spaces (e.g. 'user1 user2 user3').", 
        required=True, 
        nargs='+'
    )
    
    # Argument for verbose mode
    parser.add_argument(
        "--verbose", 
        action="store_true", 
        help="Enable verbose mode. This will display additional metadata, including profile information like "
             "bio, links, and images where available."
    )
    
    # Argument for fast mode
    parser.add_argument(
        "--fast", 
        action="store_true", 
        help="Enable fast mode. This will enable multithreading to speed up the search process by checking "
             "multiple sites concurrently. Use with caution if your network or machine has limited resources."
    )
    
    # Parse arguments
    args = parser.parse_args()

    all_output_lines = []  # Store all results in one file

    # Mengambil timestamp untuk memastikan file hasil unik
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    for username in args.username:
        print(f"\n--- Mencari untuk username: {username} ---")
        username_output_lines = run_username_check(username, verbose=args.verbose)
        all_output_lines.extend(username_output_lines)

        # Menyimpan hasil pencarian berdasarkan username dengan timestamp
        save_path_username = os.path.join("hasil", f"{username}_{timestamp}.txt")
        with open(save_path_username, "w", encoding="utf-8") as f:
            f.write("\n".join(all_output_lines))

        print(f"\n[✓] Hasil untuk username {username} disimpan di: {save_path_username}")

    print(f"\n[✓] Semua hasil disimpan dengan nama file berdasarkan username dan timestamp.")

if __name__ == "__main__":
    main()
