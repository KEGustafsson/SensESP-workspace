# SH-wg Hardware Reference

**Sailor Hat WiFi Gateway**

Online docs: https://docs.hatlabs.fi/sh-wg/

## Microcontroller

- **MCU**: ESP32-WROOM-32E
- **Processor**: Dual-core, 240 MHz
- **WiFi**: 802.11 b/g/n (2.4 GHz), up to 150 Mbps, 20 dBm output power

## Power

- **Input**: 8-32V DC via NMEA 2000 Micro-C connector
- **Consumption**: ~60 mA @ 12V (0.72 W typical)
- **LEN**: 2 (NMEA 2000 Load Equivalence Number)

## Enclosure

- **Material**: Polycarbonate with transparent lid
- **Dimensions**: 64 x 58 x 35 mm (excluding connector)
- **Weight**: 87 g
- **IP rating**: IP65 (waterproof)
- **Temperature**: -20 to +55 C operating

## Pin Assignments

| GPIO | Function | Notes |
|------|----------|-------|
| 25 | CAN RX | NMEA 2000 receive |
| 26 | CAN TX | NMEA 2000 transmit |
| 2 | Blue LED | WiFi status indicator |
| 4 | Yellow LED | Data broadcast indicator |
| 5 | Red LED | Power indicator |
| 18 | Hall Sensor | Magnet-activated input |
| 27 | CAN LED EN | CAN activity LED enable |

## CAN / NMEA 2000

- **Pins**: GPIO 25 (RX), GPIO 26 (TX)
- **Connector**: Single NMEA 2000 Micro-C (provides both power and data)
- **Protocol**: NMEA 2000 at 250 kbps

## User Interface

This is a sealed, waterproof device. There are no buttons -- all user interaction is via a neodymium magnet held against the enclosure.

- **1-second magnet hold**: Restart device
- **10-second magnet hold**: Factory reset

## LED Indicators

- **Red LED**: Power indicator. On when powered, off during magnet detection.
- **Blue LED**: WiFi status. Flashes during config portal, steady when connected.
- **Yellow LED**: UDP broadcast. On normally, flickers on data transmission.
- **Green TX/RX LEDs**: NMEA 2000 bus activity.

## Network Services

| Service | Port | Protocol |
|---------|------|----------|
| NMEA 0183 TCP | 2222 | TCP server |
| YDWG Raw TCP | 2223 | TCP server |
| NMEA 0183 UDP | 2000 | UDP broadcast |
| YDWG Raw UDP | 2002 | UDP broadcast |

WiFi captive portal password: `abcdabcd`

## PlatformIO Configuration

```ini
[env:sh-wg]
platform = espressif32
board = esp32dev
framework = arduino
board_build.partitions = min_spiffs.csv
monitor_speed = 115200

build_flags =
    -D SH_WG
    -D LED_BUILTIN=2

lib_deps =
    mairas/ReactESP @ ^2.1.0
    SignalK/SensESP @ ^2.5.1
    ttlappalainen/NMEA2000-library
    ttlappalainen/NMEA2000_esp32
    bxparks/AceButton @ ^1.9.2
```

## Use Case

The SH-wg is a **dedicated gateway** -- it bridges NMEA 2000 data to WiFi. It receives NMEA 2000 PGNs, converts them to NMEA 0183 sentences and raw YDWG format, and serves them over TCP and UDP to chart plotters, phones, and tablets.

Custom firmware can modify which PGNs are translated, add SeaSmart format output, or add NMEA 0183 to NMEA 2000 conversion.

See `ref/SH-wg-firmware` for the production firmware.

## Gotchas

- **No GPIO header.** This is a sealed device. You can only use the NMEA 2000 connector and WiFi. No external sensors can be connected without hardware modification.
- **Magnet interface**: The hall sensor on GPIO 18 replaces physical buttons. Firmware must handle magnet events.
- **Older SensESP version**: The production firmware uses SensESP 2.x, not 3.x. Check the reference firmware for compatible API patterns.
- **Single connector**: Power and NMEA 2000 data share the same Micro-C connector. The device cannot operate without being connected to an NMEA 2000 network.
