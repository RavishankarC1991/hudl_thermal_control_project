*** Settings ***
Documentation     Robot Framework validation suite for the embedded thermal control subsystem.
...               It validates PWM command versus tachometer RPM feedback and key fault scenarios.
Library           thermal_qa.robot_keywords.ThermalControlKeywords
Suite Setup       Create Default Fan Spec

*** Variables ***
${MAX_RPM}                 5000
${MIN_START_PWM}           20
${RPM_TOLERANCE_PERCENT}   10
${STALL_THRESHOLD_RPM}     200

*** Test Cases ***
PWM 60 Percent Should Produce Tachometer RPM Within Tolerance
    [Documentation]    Verifies nominal hardware/software integration behaviour: commanded PWM should produce matching tachometer RPM.
    ${result}=    Validate PWM Tacho Response    60    3000
    Validation Status Should Be    ${result}    PASS
    Validation Message Should Contain    ${result}    within tolerance

PWM Below Fan Start Threshold Should Expect Zero RPM
    [Documentation]    Verifies boundary behaviour below the fan start threshold.
    ${expected_rpm}=    Expected RPM For PWM    10
    Should Be Equal As Numbers    ${expected_rpm}    0
    ${result}=    Validate PWM Tacho Response    10    0
    Validation Status Should Be    ${result}    PASS

Measured RPM Above Tolerance Should Fail
    [Documentation]    Verifies that unexpectedly high RPM is reported as validation failure.
    ${result}=    Validate PWM Tacho Response    60    4000
    Validation Status Should Be    ${result}    FAIL
    Validation Message Should Contain    ${result}    outside tolerance

Measured RPM Below Tolerance Should Fail
    [Documentation]    Verifies that low but non-stalled RPM is reported as validation failure.
    ${result}=    Validate PWM Tacho Response    60    2400
    Validation Status Should Be    ${result}    FAIL
    Validation Message Should Contain    ${result}    outside tolerance

Missing Tachometer Signal Should Be Reported As Fault
    [Documentation]    Verifies fail-safe diagnostic behaviour when tacho feedback is unavailable.
    ${result}=    Validate PWM Tacho Response    70    ${None}
    Validation Status Should Be    ${result}    FAULT
    Validation Message Should Contain    ${result}    Tachometer signal missing

Fan Stall Should Be Reported As Fault
    [Documentation]    Verifies fan-stall detection when PWM is commanded but RPM remains near zero.
    ${result}=    Validate PWM Tacho Response    80    0
    Validation Status Should Be    ${result}    FAULT
    Validation Message Should Contain    ${result}    Possible fan stall

Invalid PWM Command Should Be Reported As Fault
    [Documentation]    Verifies input validation for illegal PWM commands.
    ${result}=    Validate PWM Tacho Response    101    5000
    Validation Status Should Be    ${result}    FAULT
    Validation Message Should Contain    ${result}    PWM command outside valid range

Simulated Test Rig Normal Scenario Should Pass
    [Documentation]    Runs a simulated test-rig check suitable for CI where real hardware is unavailable.
    Create Simulated Test Rig    normal    seed=7    noise_percent=2
    Command PWM On Test Rig    60
    ${result}=    Validate Current Test Rig PWM Tacho    60
    Validation Status Should Be    ${result}    PASS

Simulated Test Rig Tachometer Missing Scenario Should Fault
    [Documentation]    Verifies fault injection through the simulated test rig.
    Create Simulated Test Rig    tacho_missing
    Command PWM On Test Rig    70
    ${result}=    Validate Current Test Rig PWM Tacho    70
    Validation Status Should Be    ${result}    FAULT
    Validation Message Should Contain    ${result}    Tachometer signal missing

Simulated Test Rig Fan Stall Scenario Should Fault
    [Documentation]    Verifies fan-stall fault injection through the simulated test rig.
    Create Simulated Test Rig    stalled_fan
    Command PWM On Test Rig    70
    ${result}=    Validate Current Test Rig PWM Tacho    70
    Validation Status Should Be    ${result}    FAULT
    Validation Message Should Contain    ${result}    Possible fan stall

Simulated Test Rig Sensor Missing Scenario Should Raise I2C Failure
    [Documentation]    Verifies I2C temperature sensor failure handling in the simulated test rig.
    Create Simulated Test Rig    sensor_missing
    Run Keyword And Expect Error    *I2C temperature sensor read failed*    Read Temperature From Test Rig
