# Quality & Validation Strategy

## 1. Scope

This strategy covers validation of an embedded thermal control subsystem used in a wearable or IoT product. The subsystem contains an MCU, PWM-controlled fan, I2C temperature sensor, tachometer feedback pin, and firmware control loop.

The main quality objective is to prove that the firmware can maintain the target temperature safely and reliably while handling sensor, fan, and integration edge cases.

## 2. System Overview

The firmware periodically reads temperature from an I2C sensor and compares it with a configured target temperature. Based on the error between measured and target temperature, the firmware adjusts fan speed using PWM. The fan tachometer signal is used as closed-loop feedback to confirm that the physical fan response matches the requested PWM level.

High-level control flow:

1. Read temperature from I2C sensor.
2. Validate sensor reading and detect sensor communication faults.
3. Compare measured temperature against target temperature.
4. Calculate required fan PWM duty cycle.
5. Apply PWM output to fan driver.
6. Read tachometer feedback.
7. Validate that tachometer RPM is consistent with PWM command.
8. Enter degraded or safe mode if sensor/fan feedback is invalid.

## 3. Expected Behaviour

### Normal Behaviour

- When temperature is below target, PWM remains at minimum or low duty cycle.
- When temperature rises above target, PWM increases progressively.
- Tachometer RPM increases approximately proportional to PWM duty cycle.
- The system stabilises around the target temperature without excessive oscillation.
- Firmware logs key events: temperature reading, PWM command, tachometer RPM, and state transitions.

### Boundary Behaviour

- PWM is clamped between configured minimum and maximum limits.
- Sensor readings outside valid physical range are rejected.
- Short temperature spikes should not cause unstable fan behaviour if filtering/debounce is implemented.
- Tachometer RPM tolerance should account for fan variation, supply voltage, measurement noise, and startup delay.

### Fault Behaviour

- I2C sensor read failure should be detected and logged.
- Invalid sensor data should trigger safe fallback behaviour.
- Fan stall should be detected when PWM is high but tachometer RPM is zero or below threshold.
- Tachometer signal loss should be detected when fan is commanded but no valid pulses are received.
- Over-temperature should trigger maximum cooling and a clear fault state.
- The system should recover automatically if the fault clears, or remain latched if safety requirements demand manual reset.

## 4. Test Levels

### Unit Tests

Purpose: Validate firmware logic in isolation. These are implemented as Python/pytest checks to protect the lower-level validation functions used by Robot Framework.

Examples:
- Temperature-to-PWM calculation
- PWM clamping
- Sensor value validation
- Tachometer RPM tolerance calculation
- Fault classification logic

### Hardware Abstraction Layer Tests

Purpose: Validate interactions with abstracted interfaces.

Examples:
- Mock I2C temperature sensor returns valid, invalid, timeout, and noisy readings
- Mock PWM driver receives expected duty cycle
- Mock tachometer returns expected RPM or fault conditions

### Hardware-Software Integration Tests

Purpose: Validate firmware behaviour on development board or test rig. These are represented by Robot Framework scenarios because Robot Framework provides readable, keyword-driven tests that can be understood by QA, firmware, and product stakeholders.

Examples:
- Command PWM values and verify tachometer RPM
- Heat/cool thermal chamber or controlled heat source and verify fan response
- Disconnect sensor and verify safe mode
- Block fan physically in controlled test setup and verify stall detection

### System Tests

Purpose: Validate end-to-end behaviour in representative product conditions.

Examples:
- Long-run thermal stability test
- Startup/shutdown thermal behaviour
- Low battery / low supply fan response
- Environmental variation: cold start, high ambient temperature, enclosure constraints

### Regression Tests

Purpose: Run a stable set of automated Robot Framework checks in CI and, later, on physical test rigs before release.

Examples:
- PWM versus tachometer RPM tolerance check
- Sensor failure handling
- Over-temperature safety behaviour
- Log format and fault code checks

## 5. Automation Strategy

Automation is split into two layers:

1. **CI simulation layer**: runs without hardware using Python simulator/fake HAL. This catches logic regressions early.
2. **Test-rig layer**: runs against actual hardware using the same validation concepts, replacing fake interfaces with real GPIO/I2C/PWM/tachometer measurement adapters.

The sample implementation in this repository demonstrates the CI simulation layer using Robot Framework as the primary validation interface and Python as the reusable keyword/validation layer. In a real product, the same Robot Framework test cases can call a hardware adapter instead of the simulator, while the Python validators can remain reusable across CI and bench-level hardware testing.


## 5.1 Automation Framework Design

The executable validation framework uses a Robot Framework + Python architecture:

- **Robot Framework test suite**: Provides readable acceptance/integration-style scenarios such as nominal PWM-to-RPM validation, missing tachometer feedback, fan stall, invalid PWM command, and I2C sensor failure.
- **Python keyword library**: Exposes reusable Robot Framework keywords and wraps the Python validation logic.
- **Python validation layer**: Contains deterministic fan model, tolerance calculation, and result classification into PASS, FAIL, or FAULT.
- **Simulated test rig**: Allows the same checks to run in CI without physical hardware. In a real rig, this simulator can be replaced by adapters for GPIO, I2C, PWM, tachometer capture, serial, SCPI, or vendor SDKs.
- **Pytest support suite**: Provides developer-level unit tests for the Python functions behind the Robot Framework keywords.

This design keeps the test cases understandable for reviewers while still demonstrating strong Python-based automation and embedded validation design.

## 6. Entry Criteria

- Firmware build is available.
- Requirements and expected behaviours are reviewed.
- Test rig or simulator interface is available.
- Known hardware limitations and fan datasheet limits are documented.
- Logging/fault-code format is agreed.

## 7. Exit Criteria

- All critical and high-priority requirements have automated or documented manual coverage.
- No open critical/high defects affecting thermal safety or fan control.
- PWM versus tachometer validation passes across representative PWM values.
- Fault handling is verified for sensor failure, tachometer loss, and fan stall.
- Regression suite passes in CI and, where applicable, on hardware test rig.

## 8. Key Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Fan RPM is not perfectly linear with PWM | False test failures | Use tolerance bands and fan datasheet calibration |
| Tachometer pulses are noisy | Incorrect RPM calculation | Debounce/filter tachometer input and use averaged measurement windows |
| I2C sensor intermittent failures | Missed thermal events | Retry logic, timeout handling, and fault logging |
| Control-loop oscillation | Poor user experience or thermal instability | Add hysteresis/PID tuning and long-run stability tests |
| Hardware not always available for CI | Late defect discovery | Use simulator in CI and scheduled test-rig regression |

## 9. Defect Severity Guide

- **Critical**: Thermal safety risk, fan does not run during over-temperature, firmware crash, no fault detection.
- **High**: Incorrect PWM/tachometer behaviour, unrecoverable sensor fault, unstable control loop.
- **Medium**: Incorrect logs, non-critical tolerance issue, recovery delay outside target.
- **Low**: Cosmetic issue in diagnostics or minor documentation gap.

