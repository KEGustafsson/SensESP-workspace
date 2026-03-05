# SensESP Workspace

SensESP is a Signal K sensor development toolkit for ESP32-based microcontrollers. This workspace manages multiple independent repositories for convenient development.

## What is SensESP?

SensESP provides a high-level C++ API for building marine sensor devices that connect to [Signal K](https://signalk.org/) servers. Built on the Arduino framework with PlatformIO.

**Use cases:**
- Engine and exhaust temperature monitoring
- Tank level sensors
- Battery and solar monitoring (Victron VE.Direct)
- NMEA 0183 interfacing
- GPS and navigation data
- Switch and relay control

## Repository Structure

This is a **workspace repository** containing multiple independent git repositories. Each can be checked out and worked on independently.

### Core

- **SensESP/** - Signal K sensor toolkit library (C++/PlatformIO)
  - Repository: `git@github.com:SignalK/SensESP.git`
- **ReactESP/** - Event-driven framework for ESP32
  - Repository: `git@github.com:mairas/ReactESP.git`

### Sensor Libraries

- **MAX31856/** - Thermocouple sensor: `git@github.com:SensESP/MAX31856.git`
- **NMEA0183/** - NMEA 0183 parser: `git@github.com:SensESP/NMEA0183.git`
- **OneWire/** - Dallas 1-Wire sensors: `git@github.com:SensESP/OneWire.git`
- **VEDirect/** - Victron VE.Direct: `git@github.com:SensESP/VEDirect.git`

### Examples and Templates

- **SensESP-project-template/** - Project starter: `git@github.com:SensESP/SensESP-project-template.git`
- **Tutorial-BMP280/** - BMP280 tutorial: `git@github.com:SensESP/Tutorial-BMP280.git`
- **SensESP-BN-880/** - GPS module example: `git@github.com:hatlabs/SensESP-BN-880.git`
- **sensesp3-halmet-example/** - HALMET board example: `git@github.com:hatlabs/sensesp3-halmet-example.git`

## Quick Start

```bash
# Clone all component repositories
./run repos:clone

# Update all repositories to latest
./run repos:pull-all-main

# Check status of all repositories
./run repos:status

# List managed repositories
./run repos:list
```

### Working with Individual Components

Each repository has its own build system:

```bash
# SensESP core development
cd SensESP
./run build          # Build frontend + firmware
./run upload         # Upload to device

# See all available commands
cd SensESP
./run help
```

**Always read each repository's `AGENTS.md` or `CLAUDE.md`** for detailed development instructions.

### Adding Local Repositories

To manage additional repositories locally, create a `repos.*.sh` file in the workspace root (e.g., `repos.local.sh`):

```bash
# repos.local.sh (gitignored)
REPOS["my-repo"]="git@github.com:myorg/my-repo.git main"
```

All `repos.*.sh` files are sourced by the `./run` script and can add entries to the `REPOS` array.

## Architecture

SensESP implements a data-flow pipeline:

```
Sensor --> Transform(s) --> Output --> Signal K Server
```

Sensors read hardware inputs, transforms process data (averaging, scaling, filtering), and outputs send results to a Signal K server via WebSocket. A built-in web UI provides configuration and monitoring.

## Resources

- **Signal K**: https://signalk.org/
- **SensESP Documentation**: https://signalk.org/SensESP/
- **PlatformIO**: https://platformio.org/

## License

See individual repository licenses.

## Contributing

Contributions are welcome! Each repository accepts pull requests independently. See individual repository documentation for specific guidelines.
