# SensESP Development Workflow

This document defines the phases Claude follows when helping users create firmware projects. Each phase has clear entry conditions, actions, and exit conditions.

## Phase 1: Requirements Gathering

**Entry**: User describes a goal ("I want to monitor my engine temperature").

**Actions**:
1. Ask about the goal -- what do they want to measure, control, or connect?
2. Ask about the hardware -- which board? What sensors?
3. Ask about outputs -- where should data go? (Signal K, NMEA 2000, display, alarms)
4. Ask about the environment -- marine, automotive, indoor?

**Guidelines**:
- One question at a time. Offer choices when possible.
- If the user doesn't know what sensors they need, suggest common options for their goal.
- If the user has a Hat Labs board, use the board's capabilities to guide suggestions.
- If the user has a generic ESP32, ask about its specific features.

**Exit**: You have enough information to write a specification.

## Phase 2: Hardware Documentation

**Entry**: Board is known.

**Actions**:
1. Read `docs/hardware/<board>.md` for the selected board.
2. Present wiring instructions for the user's specific sensors and connections.
3. Include pin numbers, connector positions, jumper settings.
4. Warn about any gotchas (voltage limits, isolation, required components).

**Guidelines**:
- This phase is mandatory even if the user didn't ask about wiring.
- For generic boards, ask the user to describe or link to their board's pinout.
- Use plain language: "Connect the temperature sensor's signal wire to pin 23" not "Wire GPIO23 to the NTC output."

**Exit**: User understands how to physically connect their sensors.

## Phase 3: Specification

**Entry**: Requirements gathered, hardware documented.

**Actions**:
1. Create the project directory: `projects/<project-name>/`
2. Write `SPEC.md` summarizing: goal, hardware, sensors, connections, Signal K paths, expected behavior, dependencies.
3. Present the spec to the user for review.

**Guidelines**:
- The spec is the contract. Don't proceed until the user confirms it.
- Keep it readable by non-technical users.
- Include a connections table with physical pin numbers.

**Exit**: User confirms the specification.

## Phase 4: Architecture

**Entry**: Specification confirmed.

**Actions**:
1. Study relevant reference examples in `ref/` for patterns that match the use case.
2. Design the SensESP signal flow: sensor → transform → output.
3. Identify required libraries (lib_deps for platformio.ini).
4. Plan the main.cpp structure.

**Guidelines**:
- Check `ref/SensESP/examples/` for matching patterns first.
- Then check the product-specific examples (HALMET-example-firmware, etc.).
- Prefer simple, linear pipelines. Avoid unnecessary complexity.
- Note which example files you're drawing from so you can reference them during implementation.

**Exit**: You have a clear plan for the code structure.

## Phase 5: Implementation

**Entry**: Architecture planned.

**Actions**:
1. Copy `ref/SensESP-project-template/` as the starting point.
2. Configure `platformio.ini` for the target board and dependencies.
3. Write `src/main.cpp` following the planned architecture.
4. Where feasible, write tests for transforms and logic in `test/`.
5. Initialize git repo and commit the initial implementation.

**Guidelines**:
- Follow test-driven development where practical. SensESP transforms and custom logic can be unit tested.
- Keep the code simple. A non-programmer should be able to read it and roughly understand what's happening.
- Add brief comments explaining what each section does (for the user's benefit).
- Commit at meaningful milestones, not after every line.

**Exit**: Code compiles and is ready to flash.

## Phase 6: Build and Flash

**Entry**: Code written or modified.

**Actions**:
1. Build with `pio run -e <env>`.
2. Fix any compilation errors (explain them in plain language).
3. Upload with `pio run -e <env> -t upload`.
4. Handle upload failures (device not found, bootloader mode, wrong port).

**Guidelines**:
- If the build fails, fix the code -- don't ask the user to fix it.
- If the upload fails, guide the user through the physical steps (press BOOT, reconnect USB).
- Report binary size so the user knows if they're close to limits.
- **Build failures often reveal issues in the implementation.** After fixing, return to Phase 5 if the fix requires rethinking the approach, or stay in Phase 6 if it's a simple correction.

**Exit**: Firmware is running on the device.

## Phase 7: Hardware Testing

**Entry**: Firmware uploaded.

**Actions**:
1. Monitor serial output with `python3 serial_monitor.py -t 30`.
2. Interpret the output:
   - Boot messages (WiFi, Signal K connection, sensor init)
   - Sensor readings (are values plausible?)
   - Error messages (stack traces, watchdog resets)
3. Report findings in plain language.
4. **Ask the user for feedback.** Does the device behave as they expected? Is the data meaningful to them? Is anything missing, surprising, or wrong? Encourage them to describe what they see and how it compares to what they had in mind.
5. If issues are found -- technical or expectation-based -- diagnose and address them.

**Guidelines**:
- Plausibility checks: room temperature should be 15-30°C, not 0 or 1000. Oil pressure at idle should be non-zero.
- If sensor reads zero or constant, likely a wiring issue.
- If device reboots, look for stack traces.
- WiFi configuration happens through SensESP's built-in web portal, not in code.

**User feedback is the most valuable signal in this phase.** Users often can't fully express what they want until they see something working. It's common and perfectly fine for the user to say things like "this works, but actually I also need..." or "I thought I wanted X but now I realize I need Y." This isn't a problem -- it's the normal process of discovering real requirements through hands-on experience. Encourage it.

**Iteration**: Testing and user feedback frequently reveal issues that require going back to earlier phases:
- **Wiring or sensor issues** → return to Phase 2 (Hardware Documentation) to re-check connections.
- **"This isn't quite what I wanted"** or **missing features** → return to Phase 3 (Specification) to update requirements based on what the user has learned, then Phase 4-5 to redesign and reimplement.
- **Code bugs** → return to Phase 5, fix, then Phase 6 to rebuild and reflash.
- **Plausible readings but wrong values** → may need scaling or calibration adjustments in Phase 5.
- **"Can we also add..."** → welcome it. Update SPEC.md, return to the appropriate phase.

This iteration is normal and expected. Don't treat it as failure -- it's how firmware development works. Each cycle narrows the gap between intended and actual behavior. When updating SPEC.md based on feedback, note what changed and why so the evolution of requirements is visible.

**Exit**: The user confirms the device works as they expect -- sensor readings are plausible, data flows to the intended outputs, no crashes or errors, and the user is satisfied with the behavior.

## Phase 8: Review

**Entry**: Hardware testing passed.

**Actions**:
1. Review code for correctness, hardware compatibility, SensESP best practices.
2. Check Signal K path naming against conventions.
3. Verify pin assignments match the hardware doc.
4. Ensure no hardcoded WiFi credentials (unless user explicitly requested them).
5. Fix any issues found.

**Guidelines**:
- Keep the review proportional to the project size.
- **If the review reveals significant issues**, return to Phase 5 (Implementation) to fix them, then Phase 6-7 to rebuild and retest. Don't ship code with known problems.

**Exit**: Code is correct and follows best practices.

## Phase 9: Cleanup and Documentation

**Entry**: Review passed.

**Actions**:
1. Clean up: remove debug prints, organize code, ensure comments are helpful.
2. Final commit.
3. **Capture learnings**: Write down anything surprising, non-obvious, or useful for future projects:
   - Hardware quirks discovered during testing (e.g., "this sensor needs a 4.7k pull-up to work reliably")
   - Workarounds for framework limitations
   - Calibration values or scaling factors that were hard to find
   - Save these to `CLAUDE.local.md` (project-specific notes) or to Claude Code memory (for cross-project learnings).
4. Suggest pushing to GitHub as a backup.

**Guidelines**:
- Learnings are valuable. Even small observations ("HALMET analog input 3 has slightly higher noise than the others") can save hours on future projects.
- Don't write learnings that merely restate what the code does. Focus on what was surprising or non-obvious.

**Exit**: Project is complete, clean, and learnings are preserved.

## Resuming Work

When a user returns to an existing project:
1. Check `projects/` for their project.
2. Read the SPEC.md and source code to recall the context.
3. Ask where they want to pick up: "Last time we got the temperature sensor working. Want to add the pressure sensor next?"
