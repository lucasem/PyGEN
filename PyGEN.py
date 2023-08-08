import os
import concurrent.futures
import random
import time
import secp256k1 as ice

# how many cores to use
num_cores = os.cpu_count()

# Define the hexadecimal range. As of now, range of the bitcoin puzzle 66
lower_hex = '0000000000000000000000000000000000000000000000020000000000000000'
upper_hex = '0000000000000000000000000000000000000000000000040000000000000000'

# Convert hex values to integers
lower_int = int(lower_hex, 16)
upper_int = int(upper_hex, 16)


# Function to check if there are more than 3 consecutive characters in a hex string, to avoid checking private keys like '200000015ae3c5b0'
def has_more_than_3_consecutive(hex_string):
    for i in range(len(hex_string) - 3):
        if hex_string[i] == hex_string[i + 1] == hex_string[i + 2] == hex_string[i + 3]:
            return True
    return False


# Define a worker function that generates a batch of addresses and returns them
def worker(start, end, lower_int):
    # Generate a random starting point within the range
    private_key = random.randint(lower_int, upper_int)

    # Initialize the list to hold private keys and corresponding addresses
    private_keys_addresses = []

    # Generate a batch of private keys and corresponding addresses randomly
    for i in range(start, end):
        # Convert the private key to hexadecimal format
        private_key_hex = hex(private_key)[2:]  # [2:] to remove the '0x' prefix

        # Check if the private key has more than 3 consecutive characters in its hex representation
        if not has_more_than_3_consecutive(private_key_hex):
            # Get the addresses from the private key using secp256k1
            address = ice.privatekey_to_address(0, True, private_key)

            # Add the private key (in hex) and address to the list
            private_keys_addresses.append(f"{private_key_hex}:{address}")

        # Increment the private key for the next iteration
        private_key += 1

    return private_keys_addresses


while True:
    # Number of addresses to generate
    num_addresses = 5000000

    # Use a ProcessPoolExecutor to generate the addresses in parallel
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Divide the addresses evenly among the available CPU cores
        addresses_per_core = num_addresses // num_cores

        # Submit a task for each batch of addresses to the executor
        tasks = []
        for i in range(num_cores):
            start = i * addresses_per_core
            end = (i + 1) * addresses_per_core
            tasks.append(executor.submit(worker, start, end, lower_int))

        # Wait for the tasks to complete and retrieve the results
        private_keys_addresses = []
        for task in concurrent.futures.as_completed(tasks):
            private_keys_addresses.extend(task.result())

    # Write the private keys and corresponding addresses to a file
    #with open('private_keys_with_addresses.txt', 'w') as file:
    #    file.write('\n'.join(private_keys_addresses))

        target = '13zb1hQbWV'
        matchers = [target]
        matching = [s for s in private_keys_addresses if any(xs in s for xs in matchers)]
        #print(matching)
        with open('found.txt', 'a') as file:
            file.write('\n'.join(matching))

    # Sleep for a while before the next iteration
    time.sleep(1)  # Sleep for 1 second before running the loop again
