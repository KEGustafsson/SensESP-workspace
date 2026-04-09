#!/usr/bin/env python3
"""Non-interactive serial monitor that doesn't toggle DTR/RTS.

Reads serial output without resetting the device, making it safe for
use in non-interactive contexts (scripts, CI, Claude Code).

Supports macOS, Linux, and WSL port auto-detection.

Requires: pyserial (pip install pyserial)
"""

import argparse
import platform
import sys
import time

import serial


def main():
    parser = argparse.ArgumentParser(
        description="Read serial output without resetting the device"
    )
    parser.add_argument(
        "port",
        nargs="?",
        help="Serial port (default: auto-detect)",
    )
    parser.add_argument(
        "-b", "--baud", type=int, default=115200, help="Baud rate (default: 115200)"
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        default=0,
        help="Exit after N seconds (default: 0 = run until interrupted)",
    )
    args = parser.parse_args()

    port = args.port
    if port is None:
        port = auto_detect_port()
        if port is None:
            print("Error: no USB serial device found", file=sys.stderr)
            if is_wsl():
                print(
                    "\nWSL detected. USB devices require usbipd-win to pass through.",
                    file=sys.stderr,
                )
                print(
                    "See: https://learn.microsoft.com/en-us/windows/wsl/connect-usb",
                    file=sys.stderr,
                )
            sys.exit(1)
        print(f"Auto-detected port: {port}", file=sys.stderr)

    ser = serial.Serial()
    ser.port = port
    ser.baudrate = args.baud
    ser.timeout = 1
    ser.dtr = False
    ser.rts = False
    ser.dsrdtr = False
    ser.rtscts = False
    ser.open()

    try:
        deadline = time.time() + args.timeout if args.timeout > 0 else None
        while deadline is None or time.time() < deadline:
            line = ser.readline()
            if line:
                sys.stdout.write(line.decode("utf-8", errors="replace"))
                sys.stdout.flush()
    except KeyboardInterrupt:
        pass
    finally:
        ser.close()


def is_wsl():
    """Detect if running under Windows Subsystem for Linux."""
    try:
        with open("/proc/version", "r") as f:
            return "microsoft" in f.read().lower()
    except FileNotFoundError:
        return False


def auto_detect_port():
    import glob

    ports = []

    system = platform.system()
    if system == "Darwin":
        # macOS
        ports = glob.glob("/dev/cu.usbmodem*") + glob.glob("/dev/cu.usbserial*")
    elif system == "Linux":
        # Linux and WSL (if USB passthrough is configured)
        ports = glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*")

    if len(ports) == 1:
        return ports[0]
    if len(ports) > 1:
        print(f"Multiple ports found: {ports}", file=sys.stderr)
        print(f"Using first: {ports[0]}", file=sys.stderr)
        return ports[0]
    return None


if __name__ == "__main__":
    main()
