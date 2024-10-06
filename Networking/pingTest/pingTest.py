#!/bin/env python3

# Dependencies


import csv
import os
import platform
import subprocess
import statistics
from datetime import datetime
from argparse import ArgumentParser


# Function to parse ping output and extract the necessary data
def parse_ping_output(output):
    if platform.system().lower() == 'windows':
        # Parse the output for Windows
        lines = output.splitlines()
        rtts = [int(line.split('=')[-1].split('ms')[0]) for line in lines if 'time=' in line]
        packets = [line for line in lines if 'Packets:' in line][0]
        packets_sent = int(packets.split(',')[0].split()[-1])
        packets_received = int(packets.split(',')[1].split()[-1])
        packet_loss = int(packets.split(',')[2].split()[-1].replace('%', ''))
    else:
        # Parse the output for Unix-based systems
        lines = output.splitlines()
        rtts = [float(line.split('time=')[-1].split()[0]) for line in lines if 'time=' in line]
        stats = [line for line in lines if 'packets transmitted' in line][0]
        packets_sent = int(stats.split()[0])
        packets_received = int(stats.split()[3])
        packet_loss = float(stats.split()[5].replace('%', ''))
        
    if rtts:
        min_rtt = min(rtts)
        avg_rtt = statistics.mean(rtts)
        max_rtt = max(rtts)
        jitter = max(rtts) - min(rtts) if len(rtts) > 1 else 0
        is_alive = 1 if packets_received > 0 else 0
    else:
        min_rtt = avg_rtt = max_rtt = jitter = 0
        is_alive = 0
    
    return {
        'rtts': rtts,
        'min_rtt': min_rtt,
        'avg_rtt': avg_rtt,
        'max_rtt': max_rtt,
        'packets_sent': packets_sent,
        'packets_received': packets_received,
        'packet_loss': packet_loss,
        'jitter': jitter,
        'is_alive': is_alive
    }

# Function to perform a ping test
def ping(host):
    # Determine the command based on the operating system
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    
    # Construct the command to ping the host
    command = ['ping', param, '16', host]
    
    # Execute the command
    try:
        output = subprocess.check_output(command, universal_newlines=True)
        return parse_ping_output(output)
    except subprocess.CalledProcessError as e:
        return parse_ping_output(e.output)

# Function to log the results to a CSV file
def log_to_csv(filename, data):
    file_exists = os.path.isfile(filename)
    
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header if the file does not exist
        if not file_exists:
            writer.writerow(['Date Time', 'Address', 'Min RTT', 'Avg RTT', 'Max RTT', 'Packets Sent', 'Packets Received', 'Packet Loss (%)', 'Jitter', 'Is Alive'])
        # Write the data row
        writer.writerow(data)

# Main function
def main():
    host = '1.1.1.1'  # Replace with the host you want to ping (e.g., 'google.com')
    filename = 'results_test.csv'
    
    # Get the current date and time
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Perform the ping test
    ping_data = ping(host)
    
    # Prepare the data to log
    log_data = [
        current_time,
        host,
        ping_data['min_rtt'],
        ping_data['avg_rtt'],
        ping_data['max_rtt'],
        ping_data['packets_sent'],
        ping_data['packets_received'],
        ping_data['packet_loss'],
        ping_data['jitter'],
        ping_data['is_alive']
    ]
    
    # Log the result to the CSV file
    log_to_csv(filename, log_data)
    print(f"Ping result logged: {log_data}")

if __name__ == '__main__':
    main()
