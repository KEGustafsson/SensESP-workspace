# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## SensESP Workspace

SensESP is a Signal K sensor development toolkit for ESP32-based microcontrollers. It provides a high-level API for building marine sensor devices that connect to Signal K servers.

This workspace manages multiple independent repositories for convenient development. Each repository must work independently and can have no directory-level cross-dependencies.

## Local Environment Setup

**For additional project context, see @CLAUDE.private.md and @CLAUDE.local.md** (optional, not included in this repository).

## Contributing Guidelines

### Code Standards

- Follow YAGNI, SOLID, DRY, and KISS principles
- Write self-documenting code; comments explain "why", not "what"
- Keep functions small and focused on a single responsibility
- Prefer composition over inheritance
- No magic numbers; use named constants
- Use strict type checking; avoid `any` or equivalent escape hatches
- C++ code follows `.clang-format` style (Google base with 2-space indent)
- All new code requires tests -- test behavior, not implementation details
- Documentation describes current state, not development history

### Git Workflow

- Branch from main for new work; never push directly to main
- Branch naming: `<type>/<description>` where type = feat|fix|docs|chore|refactor|test
- Conventional commits: `<type>(<scope>): <subject>` -- 50 char subject max, imperative mood
- Atomic commits: one logical change per commit
- Clean up history via rebase before creating a PR
- Use rebase to update branches with upstream changes, never merge commits

### Pull Requests

- One logical change per PR; refactoring and behavior changes belong in separate PRs
- Descriptive titles suitable for release notes (under 70 characters)
- Descriptions explain motivation (why) and approach (how), not mechanics (what)
- Reference issues with `closes`, `fixes`, or `resolves` (e.g., "closes #18")
- All CI checks must pass before merging -- no exceptions
- Use merge commits (not squash) to preserve commit history

## Independent Repositories

### SensESP Core

**SensESP/** - Signal K sensor toolkit library (C++/PlatformIO)
- Repository: `git@github.com:SignalK/SensESP.git`
- Core library with sensor pipeline architecture
- Has its own `AGENTS.md` and `./run` script
- Build: `cd SensESP && ./run build-pio`
- Frontend: `cd SensESP && ./run build-frontend`

**ReactESP/** - Event-driven framework for ESP32 (C++)
- Repository: `git@github.com:mairas/ReactESP.git`
- Cooperative multitasking library used by SensESP

### Sensor Libraries

**MAX31856/** - Thermocouple sensor library
- Repository: `git@github.com:SensESP/MAX31856.git`

**NMEA0183/** - NMEA 0183 parser for SensESP
- Repository: `git@github.com:SensESP/NMEA0183.git`

**OneWire/** - Dallas 1-Wire temperature sensors
- Repository: `git@github.com:SensESP/OneWire.git`

**VEDirect/** - Victron VE.Direct protocol for SensESP
- Repository: `git@github.com:SensESP/VEDirect.git`

### Examples and Templates

**SensESP-project-template/** - Project starter template
- Repository: `git@github.com:SensESP/SensESP-project-template.git`

**Tutorial-BMP280/** - BMP280 barometer tutorial
- Repository: `git@github.com:SensESP/Tutorial-BMP280.git`

**SensESP-BN-880/** - BN-880 GPS module example
- Repository: `git@github.com:hatlabs/SensESP-BN-880.git`

**sensesp3-halmet-example/** - HALMET board example
- Repository: `git@github.com:hatlabs/sensesp3-halmet-example.git`

## Architecture

### Sensor Pipeline

The core SensESP architecture is a data-flow pipeline:

```
Sensor --> Transform(s) --> Output --> Signal K Server
```

- **Sensors** (`src/sensesp/sensors/`): Read hardware inputs (analog, digital, 1-Wire, I2C)
- **Transforms** (`src/sensesp/transforms/`): Process data (moving average, linear, lambda, debounce)
- **Outputs** (`src/sensesp/signalk/`): Send data to Signal K server via WebSocket
- **Net** (`src/sensesp/net/`): WiFi management, mDNS, HTTP server, WebSocket client
- **UI** (`src/sensesp/ui/`): Web-based configuration interface (Preact/Bootstrap)
- **System** (`src/sensesp/system/`): Core infrastructure, observable values, task queues
- **Controllers** (`src/sensesp/controllers/`): Control logic (e.g., PID, digital output)

### Build System

PlatformIO with multiple environments:
- **Platforms**: arduino, pioarduino (recommended), espidf
- **Devices**: esp32, esp32c3 (and custom boards: SHESP32, HALMET, HALSER)
- **Frontend**: Preact + Bootstrap, built with pnpm, embedded via `pio run -t frontend`

### CI

GitHub Actions matrix builds SensESP against combinations of:
- 6 example programs
- 2 devices (esp32, esp32c3)
- 2 platforms (arduino, pioarduino)

## Quick Start

```bash
# Clone all component repositories
./run repos:clone

# Update all repositories to latest
./run repos:pull-all-main

# Check status of all repositories
./run repos:status

# Work in a specific repository
cd SensESP
./run build-pio
```

**Each repository may have its own AGENTS.md or CLAUDE.md** -- read the appropriate one for detailed context.

### Per-Repository Operations

Each repository has its own:
- Git history and remote
- Build system and dependencies
- `./run` script (where applicable)

**Always `cd` into the specific repository directory first** before running commands.

### SensESP Core Development

```bash
cd SensESP

# Build firmware
./run build-pio

# Build web frontend
./run build-frontend

# Full build (frontend + firmware)
./run build

# Upload to device
./run upload

# Format code
./run format

# Run all checks
./run checks
```

### Frontend Development

The SensESP web UI uses Preact and Bootstrap:

```bash
cd SensESP
./run install-frontend    # Install pnpm dependencies
./run build-frontend      # Compile CSS + build + embed
```

Frontend source is in `SensESP/frontend/`.

## Repository Management

```bash
# Clone all missing repositories
./run repos:clone

# Update all to latest main branches
./run repos:pull-all-main

# Check status of all repos
./run repos:status

# List all managed repos
./run repos:list
```

Additional repositories can be added via `repos.*.sh` files (gitignored) -- see README.md for details.
