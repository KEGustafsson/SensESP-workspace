---
name: review
description: >
  Review firmware code for correctness, hardware compatibility, and best
  practices. Use when user says "review", "check my code", or before
  finalizing a project.
argument-hint: "[optional: project name or specific concern]"
---

# Firmware Code Review

Review the project's firmware for correctness, hardware compatibility, and SensESP best practices.

## Phase 0: Scope

- Identify the project to review (from argument, or ask).
- Read all source files in the project's `src/` directory.
- Read the project's `SPEC.md` to understand what it should do.
- Read the project's `platformio.ini` for build configuration.

## Phase 1: Review Perspectives

Evaluate the code from each of these perspectives. Only report genuine issues -- don't flag things that aren't problems.

### Correctness
- Logic errors, off-by-one, uninitialized variables
- Interrupt safety (shared state accessed from ISRs)
- Memory leaks or unbounded allocations
- Error handling for sensor communication failures
- Does the code match what SPEC.md describes?

### Hardware Compatibility
- Pin numbers match the target board (read `docs/hardware/<board>.md`)
- No pin conflicts (same pin used for two purposes)
- Voltage and current within board limits
- I2C addresses don't collide
- Partition table appropriate for flash size
- Build flags correct for the target MCU

### SensESP Patterns
- Correct use of SensESPAppBuilder
- Proper sensor → transform → output pipelines
- Signal K paths follow conventions (check CLAUDE.md)
- WiFi/connectivity handled by framework, not custom code
- No hardcoded WiFi credentials

### Power and Performance
- No busy-wait loops (use ReactESP timers instead)
- Sensor polling intervals are reasonable (not too fast)
- WiFi traffic not excessive
- RAM usage within limits (ESP32 has ~320KB usable)

## Phase 2: Synthesize

Group findings by severity:

- **Must fix**: Will cause crashes, data corruption, hardware damage, or the firmware won't work at all.
- **Should fix**: Works but incorrectly, or has a reliability problem that will surface eventually.
- **Suggestions**: Style improvements, minor optimizations, better Signal K path naming.

Present findings in plain language. For each issue, explain what's wrong, why it matters, and what the fix looks like.

## Phase 3: Fix

Offer to fix all "must fix" and "should fix" issues. Apply fixes, then re-read the code to verify nothing was introduced. Commit the fixes.

If all issues are addressed, congratulate the user and suggest next steps:
- "Want to upload this to the device and test?" (→ build-flash)
- "Want to push this to GitHub as a backup?"
- "Anything else you'd like to change?"
