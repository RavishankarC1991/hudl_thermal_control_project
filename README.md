# End-to-End Quality Strategy & Test Framework for Embedded Thermal Control System

This repository contains a take-home technical project for a wearable / IoT embedded thermal control subsystem.

The device includes:

- MCU firmware controlling a PWM fan
- I2C temperature sensor
- Fan tachometer feedback pin
- Firmware control loop that adjusts fan speed dynamically to maintain a target temperature

## Deliverables

1. **Quality & Validation Strategy**
   - Firmware control-loop overview
   - Expected behaviours
   - Test strategy
   - Traceability matrix
   - Defect process

2. **Firmware Test Code Sample**
   - Robot Framework acceptance/integration tests as the primary executable test layer
   - Python keyword library wrapping reusable validation logic
   - Python simulator/fake test rig for running without hardware
   - Pytest unit tests as supporting developer-level checks

3. **Bonus Items**
   - CLI simulator for fault/log data generation
   - GitHub Actions CI step to run Robot Framework, pytest, lint checks, and sample fault simulations
   - Scheduled CI execution for regular validation

## Repository Structure

```text
.
├── docs/
│   ├── quality_validation_strategy.md
│   ├── traceability_matrix.md
│   └── defect_process.md
├── src/thermal_qa/
│   ├── fan_model.py
│   ├── robot_keywords.py
│   ├── test_rig.py
│   ├── validators.py
│   └── simulate_faults.py
├── robot_tests/
│   └── thermal_control_validation.robot
├── tests/
│   ├── test_pwm_tacho_validation.py
│   └── test_fault_handling.py
├── .github/workflows/firmware-validation.yml
├── requirements.txt
└── README.md
```

## Quick Start on macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=src
robot -d results/robot robot_tests
pytest -v
```

## Quick Start on Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:PYTHONPATH="src"
robot -d results/robot robot_tests
pytest -v
```

## Primary Test Suite: Robot Framework

The main test suite is:

```text
robot_tests/thermal_control_validation.robot
```

It validates:

- Nominal PWM versus tachometer RPM behaviour
- Boundary behaviour below fan start threshold
- RPM above tolerance
- RPM below tolerance
- Missing tachometer signal
- Fan stall
- Invalid PWM command
- Simulated hardware test-rig scenarios
- I2C temperature sensor failure injection

Run it with:

```bash
export PYTHONPATH=src
robot -d results/robot robot_tests
```

Robot Framework reports are generated under:

```text
results/robot/report.html
results/robot/log.html
results/robot/output.xml
```

## Supporting Developer Tests: Pytest

The pytest suite validates the lower-level Python logic used by the Robot Framework keywords.

```bash
export PYTHONPATH=src
pytest -v
```

## Run CLI Simulation

Normal scenario:

```bash
python -m thermal_qa.simulate_faults --scenario normal --pwm 60
```

Fault scenario:

```bash
python -m thermal_qa.simulate_faults --scenario stalled_fan --pwm 70
```

## Key Validation Idea

The core validation checks whether measured tachometer RPM is consistent with the commanded PWM duty cycle within tolerance.

Example:

- PWM duty cycle: 60%
- Fan max RPM: 5000 RPM
- Expected RPM: 3000 RPM
- Acceptable tolerance: ±10%
- Pass range: 2700–3300 RPM

This represents the kind of check that can run on a physical test rig using GPIO/PWM/tachometer capture, or in CI using a simulator/fake HAL.

## Why Robot Framework + Python?

Robot Framework is used as the readable, interview-friendly validation layer because the assignment prefers Robot Framework and/or Python. Python is used underneath for reusable validation logic, fan modelling, simulator behaviour, and CLI fault injection. This keeps the tests readable for QA stakeholders while still allowing engineering-level reuse in CI and hardware rigs.
