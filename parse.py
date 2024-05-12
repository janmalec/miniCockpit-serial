import json
import pandas as pd

def parse_usb_payload(hex_data):
    """Extract readable ASCII data from hex USB payloads."""
    try:
        # Remove colons and convert hex data to bytes
        hex_data = hex_data.replace(':', '')
        byte_data = bytes.fromhex(hex_data)
        return byte_data.decode('ascii', errors='ignore')  # Decode bytes to ASCII
    except ValueError as e:
        return f"Invalid data - {e}"

def main():
    file_path = 'capture.json'  # Update this to your actual file path

    # Load JSON data
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    
    # Convert JSON data to DataFrame
    df = pd.json_normalize(json_data)

    # Check for the USB capdata column
    if '_source.layers.usb.capdata' in df.columns:
        # Drop rows with missing USB capdata values
        df_filtered = df.dropna(subset=['_source.layers.usb.capdata'])

        # Add readable ASCII data
        df_filtered['Readable Data'] = df_filtered['_source.layers.usb.capdata'].apply(parse_usb_payload)

        # Display the processed data
        print(df_filtered[['_source.layers.usb.capdata', 'Readable Data']])
    else:
        print("No USB capdata found in the JSON.")

if __name__ == "__main__":
    main()
