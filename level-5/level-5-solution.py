from pwn import *

# Set up the remote connection
conn = remote('chals.tisc24.ctf.sg', 61622)

# Function to interact with the device
def interact_with_device():
    # Loop through and wait for 5 instances of the prompt '>' before proceeding
    for _ in range(5):
        conn.recvuntil(b'>')
    
    # Send the first command 'SEND d2 46' after the 5th prompt is encountered
    conn.sendline(b'SEND d2 46')

    # Wait for the next prompt '>'
    conn.recvuntil(b'>')
    # Send the next command 'SEND d3' after receiving the next prompt
    conn.sendline(b'SEND d3')

    # Wait for the next prompt '>' before sending the receive command
    conn.recvuntil(b'>')
    # Send 'RECV 16', asking the device to send 16 bytes of data
    conn.sendline(b'RECV 16')
    
    # Capture the response from the device until the next prompt '>'
    response = conn.recvuntil(b'>', drop=True)  # Read the response and stop at the next prompt
    response = response.decode().strip()  # Decode the response from bytes to a string, and strip leading/trailing whitespace
    print(f'Captured response: {response}')
    return response

# Function to simulate PRNG outputs (based on the logic derived from function FUN_400d1508)
def prng_function(x):
    x = x & 0xFFFF  # Ensure x is limited to 16 bits
    uVar1 = ((x << 7) ^ x) & 0xFFFF  # Left shift x by 7 bits and XOR with the original value, then mask to 16 bits
    uVar1 = ((uVar1 >> 9) ^ uVar1) & 0xFFFF  # Right shift by 9 bits and XOR with itself, then mask to 16 bits
    x = ((uVar1 << 8) ^ uVar1) & 0xFFFF  # Left shift by 8 bits and XOR with itself, then mask to 16 bits
    return x  # Return the final transformed value

# Function to generate a sequence of pseudorandom numbers based on a seed
def compute_prng_sequence(seed, length=16):
    sequence = []  # Initialize an empty list to store the PRNG sequence
    x = seed  # Start with the given seed
    for _ in range(length):  # Loop for the specified sequence length
        x = prng_function(x)  # Apply the PRNG function to generate the value
        sequence.append(x & 0xFF)  # Append only the lower 8 bits of the generated value to the sequence
    return sequence  # Return the full sequence of generated PRNG values

# Function to validate the decoded data array (checks if all values are printable ASCII characters)
def is_valid_data_array(data_array):
    # Check if each byte in the data array is within the printable ASCII range (32 to 127)
    return all(32 <= byte <= 127 for byte in data_array)

# Main function
def main():
    # Interact with the device to get the data
    data = interact_with_device()

    # Parse the response from the device: convert each pair of hex characters to an integer
    xor_data = [int(data[i:i+2], 16) for i in range(0, len(data), 3)]  # Interpret the response as a list of integers (parsed as hex)

    flag = None  # Initialize the flag variable as None, in case no valid flag is found

    # Loop through possible seed values
    for seed in range(0, 4096):
        # Compute the PRNG sequence for the current seed
        prng_output = compute_prng_sequence(seed)

        # XOR each byte in the received data with the corresponding byte from the PRNG sequence
        data_array_candidate = [xor_data[i] ^ prng_output[i] for i in range(16)]

        # Check if the resulting data array is valid (printable characters)
        if is_valid_data_array(data_array_candidate):
            # If valid, convert the data array to characters and form the flag
            flag = ''.join([chr(x) for x in data_array_candidate])
            break

    # Output the obtained flag (if found), or print an error message if no valid flag is found
    if flag:
        print(f'Flag obtained: {flag}')
    else:
        print('No valid flag found.')

# Call the main function when the script is executed
if __name__ == '__main__':
    main()

# Close the connection once the interaction with the device is complete
conn.close()