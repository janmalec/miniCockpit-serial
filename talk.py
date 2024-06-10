import serial
import threading
import time

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL


# for cpu usage
import psutil

# Get the default audio device
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

def get_volume():
    # Get the current volume level
    current_volume = volume.GetMasterVolumeLevelScalar()
    print(f"Current volume is {current_volume * 100:.1f}%")
    return current_volume

def set_master_volume(volume_level):
    # Print the current volume
    #print_current_volume(volume)
    
    # Calculate the volume level (0.0 to 1.0)
    volume_level = max(0.0, min(1.0, volume_level))  # Ensure volume is within bounds

    # Set the volume
    volume.SetMasterVolumeLevelScalar(volume_level, None)
    print(f"Volume set to {volume_level * 100}%")

def read_from_device(ser):
    print("Reading from", ser.name)
    
    try:
        buffer = ""
        while True:
            # Check if there is data waiting
            if ser.in_waiting > 0:
                #print("Waiting:", ser.in_waiting)
                response = ser.read(ser.in_waiting).decode(errors='replace')
                print("Received:", response)
                
                commands = response.split(';')
                
                # Process all complete commands
                for cmd in commands[:-1]: 
                    process_command(ser, cmd.strip())
                if len(commands):
                    process_command(ser, commands[0].strip(), set=False)
                
            time.sleep(0.01)  # Adjust as needed for your device
    except Exception as e:
        print("Read thread error:", str(e))

def process_command(ser, cmd, set=False):
    if cmd == '13':
        newvol = min(get_volume() + 0.05, 1)
        set_master_volume(newvol)
        # set volume display
        volstr = f"S{int(100 * newvol)}"
        print(volstr)
        #time.sleep(0.05)
        if set:
            ser.write(volstr.encode())
    elif cmd == '14':
        newvol = max(get_volume() - 0.05, 0)
        set_master_volume(newvol)
        # set volume display
        volstr = f"S{int(100 * newvol)}"
        print(volstr)
        #time.sleep(0.05)
        if set:
            ser.write(volstr.encode())

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

# TODO finish
def write_stuff(ser):
    try:
        while True:
            #print("CPU:", psutil.cpu_percent())
            cpustr = f"H{int(psutil.cpu_percent())};"
            print("writing", cpustr)
            ser.write(cpustr.encode())
            time.sleep(0.5)
            volstr = f"S{int(100 * get_volume())}"
            print(volstr)
            ser.write(volstr.encode())
            time.sleep(0.5)
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
    print("Opened", ser.name, "wait for init")
    time.sleep(3)
    # Send initialization bytes
    ser.write("C;".encode())
    ser.write("C".encode())
    ser.write("C".encode())

    time.sleep(0.5)

    volstr = f"S{int(100 * get_volume())}"
    print(volstr)
    ser.write(volstr.encode())

    # Create threads for reading and writing
    read_thread = threading.Thread(target=read_from_device, args=(ser,))
    #write_thread = threading.Thread(target=write_to_device, args=(ser,))
    write_stuff_thread = threading.Thread(target=write_stuff, args=(ser,))

    # Start threads
    read_thread.start()
    #write_thread.start()
    write_stuff_thread.start()

    # Wait for the write thread to finish (when user types 'exit')
    #write_thread.join()
    read_thread.join()
    write_stuff_thread.join()

if __name__ == "__main__":
    main()
