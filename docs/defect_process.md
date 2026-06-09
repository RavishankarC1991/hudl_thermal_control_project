# Defect Process

## 1. Defect Lifecycle

1. **New**: Defect reported by QA, developer, or CI pipeline.
2. **Triaged**: Severity, priority, owner, and release impact agreed.
3. **Assigned**: Developer or firmware owner begins investigation.
4. **In Progress**: Root cause analysis and fix implementation.
5. **Ready for QA**: Fix is available in a testable build.
6. **Verified**: QA confirms fix and performs targeted regression.
7. **Closed**: Product owner/QA accepts closure.
8. **Reopened**: Issue still reproducible or regression detected.

## 2. Required Defect Fields

- Title
- Requirement ID
- Test case ID
- Firmware version / commit hash
- Hardware revision
- Test environment
- Steps to reproduce
- Expected result
- Actual result
- Logs / screenshots / measurement data
- Severity and priority
- Owner

## 3. Example Defect

**Title:** Fan stall is not detected when PWM is 80% and tachometer RPM is zero

**Severity:** Critical

**Requirement:** REQ-005

**Steps:**
1. Start firmware build `v1.2.0` on hardware revision `EVT-2`.
2. Set thermal target to 35°C.
3. Simulate high temperature of 50°C.
4. Command fan PWM above 70%.
5. Disconnect/block tachometer feedback.

**Expected:** Firmware detects fan stall and enters safe mode within the configured timeout.

**Actual:** Firmware continues operation without fault state.

**Evidence:** Tachometer RPM remains 0 for 10 seconds while PWM remains 80%.

## 4. CI Failure Handling

If the automated PWM/tachometer tolerance check fails in CI:

1. CI marks pipeline failed.
2. Test report is attached as build artifact.
3. Defect is created or linked automatically/manual depending on team tooling.
4. Firmware change is blocked from release branch until fixed or risk accepted.

