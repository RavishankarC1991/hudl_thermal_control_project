# Traceability Matrix

| Requirement ID | Requirement | Test Case ID / Robot Test | Test Type | Priority | Automation Status |
|---|---|---|---|---|---|
| REQ-001 | Firmware shall read temperature from I2C sensor periodically | Simulated Test Rig Sensor Missing Scenario Should Raise I2C Failure | HAL/Fault | High | Automated in Robot Framework |
| REQ-002 | Firmware shall increase PWM when temperature exceeds target | Future thermal-loop system scenario | Unit/System | Critical | Planned |
| REQ-003 | Firmware shall clamp PWM within safe min/max limits | Invalid PWM Command Should Be Reported As Fault | Unit/Boundary | High | Automated in Robot Framework and pytest |
| REQ-004 | Tachometer RPM shall match commanded PWM within tolerance | PWM 60 Percent Should Produce Tachometer RPM Within Tolerance; Simulated Test Rig Normal Scenario Should Pass | Integration | Critical | Automated in Robot Framework and pytest |
| REQ-005 | Firmware shall detect fan stall when PWM is high and RPM is below threshold | Fan Stall Should Be Reported As Fault; Simulated Test Rig Fan Stall Scenario Should Fault | Integration/Fault | Critical | Automated in Robot Framework and pytest |
| REQ-006 | Firmware shall detect tachometer signal loss | Missing Tachometer Signal Should Be Reported As Fault; Simulated Test Rig Tachometer Missing Scenario Should Fault | Integration/Fault | High | Automated in Robot Framework and pytest |
| REQ-007 | Firmware shall enter safe mode on I2C sensor failure | Simulated Test Rig Sensor Missing Scenario Should Raise I2C Failure | Fault | Critical | Automated in Robot Framework and pytest |
| REQ-008 | Firmware shall log fault code and context for failures | CLI fault/log simulation | System/Diagnostics | Medium | Partially automated |
| REQ-009 | Firmware shall recover when transient sensor fault clears | Future recovery scenario | System | High | Planned |
| REQ-010 | Firmware shall maintain target temperature during long-run operation | Future long-run stability suite | System | Critical | Planned |

## Notes

Robot Framework is the primary executable test layer because it provides readable, keyword-driven test cases aligned with the project preference. Pytest is retained as a supporting developer-level suite to verify the Python validation functions used by the Robot Framework keywords.
