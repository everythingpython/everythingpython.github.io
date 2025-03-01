import datetime
import struct
import binascii

def decode_objectid(object_id: str):
    """Decodes a MongoDB ObjectId into its components."""
    # Ensure valid length
    if len(object_id) != 24:
        raise ValueError("Invalid ObjectId. It must be 24 hexadecimal characters.")
    
    # Convert hex string to bytes
    object_id_bytes = bytes.fromhex(object_id)
    
    # Extract components
    timestamp_bytes = object_id_bytes[:4]  # First 4 bytes (UNIX timestamp)
    machine_id_bytes = object_id_bytes[4:9]  # Next 5 bytes (Machine ID)
    process_id_bytes = object_id_bytes[9:11]  # Next 2 bytes (Process ID)
    counter_bytes = object_id_bytes[11:14]  # Last 3 bytes (Counter)
    
    # Convert components to readable format
    timestamp = struct.unpack('>I', timestamp_bytes)[0]  # Convert bytes to int
    human_readable_timestamp = datetime.datetime.utcfromtimestamp(timestamp)
    machine_id = binascii.hexlify(machine_id_bytes).decode()
    process_id = int.from_bytes(process_id_bytes, "big")  # Convert to int
    counter = int.from_bytes(counter_bytes, "big")  # Convert to int
    
    # Print results
    print("Decoded ObjectId Components:")
    print(f"  Timestamp: {human_readable_timestamp} (UTC)")
    print(f"  Machine ID: {machine_id}")
    print(f"  Process ID: {process_id}")
    print(f"  Counter: {counter}")

# Example Usage
if __name__ == "__main__":
    object_id = "67bd3b23c4a560c402966ccd"  # Replace with any ObjectId
    decode_objectid(object_id)
