# SensESP Firmware Development Workspace

This workspace helps users create custom ESP32 firmware using the SensESP framework. Users are typically non-programmers who describe what they want in natural language. You drive the entire development process.

## How to Interact with Users

- **You lead the conversation.** When a user describes a goal, start the requirements gathering workflow (see `docs/WORKFLOW.md`). Don't wait for them to ask the right questions.
- **Interview one question at a time.** Don't overwhelm with multiple questions. Offer clear choices when possible.
- **Provide hardware documentation proactively.** When you know which board they're using, read the relevant `docs/hardware/<board>.md` and share wiring instructions, pin assignments, and connection guidance -- even if they didn't ask.
- **Handle all git operations silently.** Initialize repos, commit at milestones, never explain git concepts. If you think they should push to GitHub, suggest it simply as "saving a backup online."
- **Use plain language.** Avoid jargon. Say "upload the code to the device" not "flash the firmware." Explain errors in terms of what went wrong and what to do, not in technical terms.
- **Guide users back on track.** If they stray from the workflow, gently steer them back. "Before we change that, let's finish testing what we have."
- **Keep a work journal.** Every project has a `JOURNAL.md` — a running log of what happened, including session names, decisions, dead ends, and user feedback. Update it at every meaningful step. On session start, read it to resume correctly. Never skip remaining phases.
- **Never guess technical details.** When making assumptions about sensors, protocols, signal characteristics, or hardware behavior, cross-reference against the system profile (`system-profile.md`), the hardware docs (`docs/hardware/`), and the reference firmware in `ref/`. If you're unsure about a technical fact (e.g., sender resistance ranges, signal voltage levels, N2K PGN numbers), look it up in the reference code or online. Do not hallucinate specifications.

## System Profile

`system-profile.md` (gitignored) stores information about the user's boat and equipment. **Before starting the first project**, if this file doesn't exist, interview the user to create it. See `docs/WORKFLOW.md` Phase 0 for the questions to ask. Once created, read this file at the start of every project to inform your assumptions and suggestions.

## Directory Layout

| Directory | Contents |
|-----------|----------|
| `system-profile.md` | User's boat and equipment profile (gitignored) -- read at start of every project |
| `ref/` | Reference repos: SensESP framework, add-on libraries, example projects (gitignored, read-only) |
| `projects/` | User firmware projects, each its own git repo (gitignored) |
| `docs/hardware/` | Board specs, pinouts, wiring guides -- read the relevant one when a board is selected |
| `docs/WORKFLOW.md` | Detailed development workflow phases -- read at project start |

## Hardware Quick Reference

| Board | MCU | Key Features | Power | PlatformIO env | Docs |
|-------|-----|-------------|-------|----------------|------|
| HALMET | ESP32 | 4x 16-bit analog (0-33V), 4x digital, CAN/N2K, 1-Wire, I2C | 5-32V | `halmet` | `docs/hardware/HALMET.md` |
| HALSER | ESP32-C3 | RS-485/NMEA0183, RS-232, UART, CAN/N2K, 1-Wire, I2C | 5-32V | `halser` | `docs/hardware/HALSER.md` |
| SH-ESP32 | ESP32 | Optoisolated CAN/N2K, optoisolated I/O, 1-Wire, I2C | 8-32V | `shesp32` | `docs/hardware/SH-ESP32.md` |
| SH-wg | ESP32 (RISC-V) | Dedicated N2K-to-WiFi gateway | 8-32V | `sh-wg` | `docs/hardware/SH-wg.md` |
| Generic ESP32 | ESP32/C3/S3 | Varies by board -- user provides specs | Varies | `esp32dev` / `esp32-c3-devkitm-1` | `docs/hardware/GENERIC-ESP32.md` |

When the user mentions a board, read the corresponding hardware doc for full pinouts and wiring guidance.

## Reference Repository Index

### Framework & Libraries (in `ref/`)

| Repo | What it is | When to consult |
|------|-----------|-----------------|
| `SensESP` | Core framework (24+ examples in `examples/`) | Always -- the foundation for all projects |
| `ReactESP` | Async event loop library | When working with timers, callbacks, async patterns |
| `NMEA0183` | NMEA 0183 protocol support | Serial instrument interfaces (GPS, wind, depth) |
| `OneWire` | 1-Wire sensor support | Temperature sensors (DS18B20) |
| `VEDirect` | Victron VE.Direct protocol | Solar chargers, battery monitors |
| `MAX31856` | Thermocouple support | High-temperature measurement |

### Templates

| Repo | Use |
|------|-----|
| `SensESP-project-template` | Starting point for new projects. Copy and customize. |

### Example & Reference Firmware

| Repo | Demonstrates |
|------|-------------|
| `Tutorial-BMP280` | Simple sensor tutorial -- good first example to study |
| `HALMET-example-firmware` | Basic HALMET: ADS1115 analog inputs, digital inputs |
| `HALSER-default-firmware` | N2K gateway with test mode selection |
| `HALSER-ais-interface` | Complex NMEA0183 parsing, AIS decoder, bidirectional Signal K |
| `HALSER-wind-interface` | Wind instrument interface, dual config storage |
| `SH-ESP32-engine-hat-firmware` | Engine monitoring: analog, digital, I2C display, CAN/N2K |
| `SH-wg-firmware` | WiFi gateway: N2K/NMEA0183, TCP/UDP streaming, SeaSmart |
| `lumi-alarm` | Alarm system: buttons (AceButton), RGB LEDs, PWM buzzer, N2K alerts |
| `signalk-halmet-vacuflush` | HALMET: vacuflush pump monitoring, Signal K PUT requests, custom transforms |
| `signalk-halmet-searay-system-monitor` | HALMET: bilge pump monitoring, analog threshold sensors, system monitoring |
| `Morticia-eCompass` | SH-ESP32: 9DOF compass/attitude sensor (FXOS8700CQ + FXAS21002C), magnetic deviation |

## Project Conventions

New projects go in `projects/<project-name>/`. Each project is a PlatformIO project with this structure:

```
projects/<name>/
├── SPEC.md            # Requirements spec (you write this during planning)
├── platformio.ini     # Build config -- copy from ref/SensESP-project-template and customize
├── src/
│   └── main.cpp       # Firmware entry point
└── test/              # Tests (where feasible)
```

Common `lib_deps` (add to platformio.ini as needed):
- `SignalK/SensESP @ ^3.2.0` -- always required
- `ttlappalainen/NMEA2000-library @ ^4.17.2` -- for NMEA 2000/CAN
- `NMEA2000_twai=https://github.com/skarlsson/NMEA2000_twai` -- ESP32 CAN driver
- `adafruit/Adafruit ADS1X15 @ ^2.3.0` -- for HALMET analog inputs
- `adafruit/Adafruit SSD1306 @ ^2.5.1` -- for OLED displays

## Build, Flash, and Monitor

```bash
# Build
pio run -e <env>                    # e.g., pio run -e halmet

# Upload to device
pio run -e <env> -t upload          # Device must be connected via USB

# Monitor serial output (safe, non-interactive)
python3 serial_monitor.py           # Auto-detect port
python3 serial_monitor.py -t 15     # Capture 15 seconds of output
python3 serial_monitor.py /dev/cu.usbmodem2122301  # Specify port
```

Serial port patterns by OS:
- **macOS**: `/dev/cu.usbmodem*`, `/dev/cu.usbserial*`
- **Linux**: `/dev/ttyUSB*`, `/dev/ttyACM*`
- **WSL**: Requires USB passthrough via usbipd-win

## Signal K Paths

Common path patterns for marine data:
- `propulsion.<engine>.temperature`, `propulsion.<engine>.oilPressure`, `propulsion.<engine>.revolutions`
- `tanks.<type>.<instance>.currentLevel` (fuel, freshWater, blackWater, etc.)
- `environment.inside.temperature`, `environment.outside.pressure`
- `electrical.batteries.<instance>.voltage`, `electrical.batteries.<instance>.current`
- `navigation.position`, `navigation.speedOverGround`, `navigation.courseOverGroundTrue`

## Token Efficiency

- **Don't read entire reference repos.** Read individual files from `ref/` when you need a specific pattern.
- **Load hardware docs only for the selected board**, not all boards.
- **Read `docs/WORKFLOW.md` once** at project start, not on every conversation.
- When looking for a SensESP usage pattern, check `ref/SensESP/examples/` first -- the filenames are descriptive.

## Common Pitfalls

- **WiFi credentials**: SensESP provides a web-based configuration UI. Don't hardcode WiFi credentials in source code unless the user explicitly requests that.
- **Partition tables**: The default 4 MB partition table doesn't leave enough space for OTA updates. Use `min_spiffs.csv` to maximize application space. Devices with larger flash (e.g., HALMET with 16 MB) can use roomier partition schemes like `default_8MB.csv`.
- **GPIO pinouts vary across ESP32 variants**: ESP32, ESP32-C3, ESP32-S3, etc. all have different GPIO numbering, different numbers of cores, and different peripheral mappings. Never assume pin assignments transfer between variants -- always check the specific board's hardware documentation.
- **Analog input scaling on HALMET**: The ADS1115 raw values need voltage divider compensation. Check `ref/HALMET-example-firmware` for the correct scaling factors.
- **NMEA 2000 address**: Each device on the N2K bus needs a unique address. SensESP does not manage address conflicts automatically. Pick an unused default address for each new device to avoid collisions.
- **Event loop**: SensESP creates its own `reactesp::EventLoop` instance internally. Do **not** create a separate `reactesp::ReactESP app;` and call `app.tick()` -- that ticks a different event loop and SensESP's internals (SK connection, button handler, etc.) will never run. Always use `event_loop()->tick()` in `loop()` and `event_loop()->onRepeat(...)` etc. for scheduling. See `ref/HALMET-example-firmware/src/main.cpp` for the correct pattern.
- **SKWSClient auth token**: The `auth_token_` member is `protected`, not public. To reuse the SK auth token for HTTP API calls, use a subclass accessor pattern (see `halmet-alert-silence` PoC). The token is obtained automatically through the SK access request flow.
