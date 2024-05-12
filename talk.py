import serial
import threading
import time

def read_from_device(ser):
    print("Reading from", ser.name)
    
    try:
        while True:
            # Check if there is data waiting
            if ser.in_waiting > 0:
                print("Waiting:", ser.in_waiting)
                response = ser.read(ser.in_waiting)
                if response:
                    print("Received:", response.decode(errors='replace'))
            time.sleep(0.5)  # Adjust as needed for your device
    except Exception as e:
        print("Read thread error:", str(e))

def write_to_device(ser):
    try:
        while True:
            command = input("Enter command (type 'exit' to quit): ")
            if command.lower() == 'exit':
                break

            # Append newline (CR+LF) if that's how you configure the Arduino IDE serial monitor
            full_command = command + '\r\n'
            ser.write(full_command.encode())
            print(f"Sent: {full_command}")
            time.sleep(0.5)  # Allow time for the device to respond

    except Exception as e:
        print("Write thread error:", str(e))

    finally:
        ser.close()
        print("Closed", ser.name)
        exit(0)

def main():
    # Open serial port with settings often used with Arduino
    ser = serial.Serial(
        port='COM3', 
        baudrate=9600,  # Adjust as necessary, sometimes 115200 is used
        parity=serial.PARITY_NONE, 
        stopbits=serial.STOPBITS_ONE, 
        bytesize=serial.EIGHTBITS,
        timeout=1
    )
    print("Opened", ser.name)
    time.sleep(0.5)
    # Send initialization bytes
    ser.write("C".encode())

    # Create threads for reading and writing
    read_thread = threading.Thread(target=read_from_device, args=(ser,))
    write_thread = threading.Thread(target=write_to_device, args=(ser,))

    # Start threads
    read_thread.start()
    write_thread.start()

    # Wait for the write thread to finish (when user types 'exit')
    write_thread.join()
    read_thread.join()

if __name__ == "__main__":
    main()
