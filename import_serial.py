import serial
import time
import os
import signal  # Import signal module

# Replace 'COM3' with the appropriate serial port for your Arduino
# On Linux, it might be something like '/dev/ttyUSB0'
# On macOS, it might be something like '/dev/tty.usbserial-XXXX'

# permanent device name for the Arduino USB port:
# https://inegm.medium.com/persistent-names-for-usb-serial-devices-in-linux-dev-ttyusbx-dev-custom-name-fd49b5db9af1
arduino_port = '/dev/arduino'
baud_rate = 115200

rgb_color = "#FF0000"  # Red color

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def set_rgb_color_from_hex(hex_color):
    red, green, blue = hex_to_rgb(hex_color)
    set_rgb_color(red, green, blue)
    print(f"Setting RGB LED to color: {hex_color} (R: {red}, G: {green}, B: {blue})")

def set_rgb_color(red, green, blue):
    with serial.Serial(arduino_port, baud_rate, timeout=1) as ser:
        ser.write(f"{red},{green},{blue}\n".encode())

def parse_arduino_data(line):
    try:
        data = line.split()
        d2 = int(data[0].split(':')[1])
        d3 = int(data[1].split(':')[1])
        a0 = int(data[2].split(':')[1])
        a1 = int(data[3].split(':')[1])
        voltage1 = (a0 / 1023.0) * 3.3
        voltage2 = (a1 / 1023.0) * 3.3
        return d2, d3, voltage1, voltage2
    except (ValueError, IndexError):
        return None

def read_arduino_data():
    print("Starting to read data from Arduino...")
    while True:
        try:
            with serial.Serial(arduino_port, baud_rate, timeout=1) as ser:
                print("Connection established")
                while True:
                    try:
                        if ser.in_waiting > 0:
                            line = ser.readline().decode('utf-8').rstrip()
                            parsed_data = parse_arduino_data(line)
                            if parsed_data:
                                d2, d3, voltage1, voltage2 = parsed_data
                                print(f"\rD2: {d2}, D3: {d3}, A0: {voltage1:.2f} V, A1: {voltage2:.2f} V", end='')
                            else:
                                print("\rInvalid data received", end='')
                        time.sleep(0.1)
                    except (serial.SerialException, OSError) as e:
                        print(f"\rNo new data from serial port or I/O error: {e}", end='')
                        time.sleep(5)
                        break  # Exit inner loop to retry connection
                    except TypeError as e:
                        print(f"\rDisconnect of USB->UART occurred: {e}", end='')
                        break
        except (serial.SerialException, OSError) as e:
            print(f"\rCable detached or I/O error: {e}", end='')
            time.sleep(5)
        except KeyboardInterrupt:
            print("\rExiting...", end='')
            break
        except Exception as e:
            print(f"\rUnexpected error: {e}", end='')
        print("\rRestarting read_arduino_data...", end='')
        time.sleep(1)

if __name__ == "__main__":
    # Example usage: Set RGB LED to red color using hex code
    set_rgb_color_from_hex(rgb_color)
    while True:
        try:
            read_arduino_data()
        except Exception as e:
            print(f"\rError: {e}. Restarting main loop...", end='')
            time.sleep(1)