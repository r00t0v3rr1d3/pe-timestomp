#!/usr/bin/env python3

import sys
import struct
import datetime
import random

def print_help(argv0):
    print(f"""Usage: {argv0} <pe_file> [-p | --print | timestamp]

View / Modify PE file timestamp

Arguments:
  <pe_file>       Path to the PE file to modify
  [-p | --print]  Optional:
                  - Display the PE file's current timestamp without modification
  [timestamp]     Optional timestamp in this format:
                  - Human-readable date: "YYYY-MM-DD HH:MM:SS"

Examples:
  {argv0} myfile.exe -p                     # Print timestamp, no modifications
  {argv0} myfile.exe                        # Set random timestamp within last 10 years
  {argv0} myfile.exe "2025-10-02 19:05:47"  # Set timestamp to specific date/time
""")

def modify_pe_timestamp(filename, timestamp=None):
    with open(filename, 'rb+') as f:
        # Read PE header offset
        f.seek(60)
        pe_offset = struct.unpack('<I', f.read(4))[0]
        
        # Move to timestamp location
        f.seek(pe_offset + 8)
        
        # Read original timestamp
        orig_ts = struct.unpack('<I', f.read(4))[0]
        orig_date = datetime.datetime.fromtimestamp(orig_ts).strftime('%Y-%m-%d %H:%M:%S')
        
        # Determine new timestamp
        if timestamp is None:
            # Generate random timestamp between 10 years ago and now
            current_time = int(datetime.datetime.now().timestamp())
            ten_years_ago = current_time - (10 * 365 * 24 * 60 * 60)  # 10 years in seconds
            timestamp = random.randint(ten_years_ago, current_time)
        elif timestamp == 'print':
            print(f"Original: {orig_ts} ({orig_date})")
            exit(0)
        elif isinstance(timestamp, str):
            try:
                timestamp = int(datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').timestamp())
            except ValueError:
                print("Error: Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'")
                sys.exit(1)
        
        # Write new timestamp
        f.seek(pe_offset + 8)
        f.write(struct.pack('<I', timestamp))
    
    # Confirm and print changes
    new_date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    print(f"Original: {orig_ts} ({orig_date})")
    print(f"New:      {timestamp} ({new_date})")

def main():
    if len(sys.argv) < 2 or sys.argv[1].lower() in ['-h', '--help']:
        print_help(sys.argv[0])
        sys.exit(1)
    
    filename = sys.argv[1]
    timestamp = sys.argv[2] if len(sys.argv) > 2 else None

    if len(sys.argv) > 2 and sys.argv[2].lower() in ['-p', '--print']:
        timestamp = "print"
    
    modify_pe_timestamp(filename, timestamp)

if __name__ == '__main__':
    main()

