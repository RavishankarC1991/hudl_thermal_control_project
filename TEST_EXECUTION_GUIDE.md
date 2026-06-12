# Test Execution Guide

## Project: Embedded Thermal Control System QA Validation

This document explains how to set up the project locally and execute the automated validation tests. The project uses **Robot Framework** as the primary test automation layer, with Python used for reusable validation logic, simulated test-rig behaviour, and CLI-based fault simulation.

---

## 1. Project Overview

This project validates an embedded thermal control subsystem where firmware reads temperature from an I2C sensor, calculates the required fan PWM duty cycle, applies the PWM output to the fan driver, and validates tachometer RPM feedback.

The automation focuses on:

- PWM vs tachometer RPM validation
- Fan stall detection
- Missing tachometer feedback detection
- Sensor communication fault simulation
- Invalid PWM command handling
- Safe/degraded-mode fault scenarios
- CI-based automated validation using GitHub Actions

---

## 2. Technology Stack

| Area | Tool |
|---|---|
| Unit Testing | Pytest |
| Test automation | Robot Framework |
| Supporting logic | Python |
| Static code checks | Ruff |
| CI/CD | GitHub Actions |
| Documentation | Markdown |
| Test reports | Robot Framework HTML reports |

---

## 3. Repository Structure

```text
hudl_thermal_control_project
├── .github
│   └── workflows
│       └── firmware-validation.yml
├── assets
│   ├── high_level_control_flow.png
│   └── defect_life_cycle.png
├── docs
│   ├── quality_validation_strategy.md
│   ├── traceability_matrix.md
│   └── defect_process.md
├── robot_tests
│   └── thermal_control_validation.robot
├── scripts
├── src
│   └── thermal_qa
│       ├── __init__.py
│       ├── fan_model.py
│       ├── robot_keywords.py
│       ├── simulate_faults.py
│       ├── test_rig.py
│       └── validators.py
├── requirements.txt
├── README.md
└── TEST_EXECUTION_GUIDE.md
```

---

## 4. Prerequisites

Before running the project, ensure the following are installed:

### Required

- Python 3.10 or higher
- Git
- pip

### Recommended

- VS Code or PyCharm
- Robot Framework extension for VS Code

Check Python version:

```bash
python3 --version
```

Expected example:

```text
Python 3.11.x
```

---

## 5. Clone the Repository

Clone the repository from GitHub:

```bash
git clone https://github.com/RavishankarC1991/hudl_thermal_control_project.git
```

Go into the project folder:

```bash
cd hudl_thermal_control_project
```

---

## 6. Create and Activate Virtual Environment

### macOS / Linux

Create virtual environment:

```bash
python3 -m venv .venv
```

Activate virtual environment:

```bash
source .venv/bin/activate
```

Verify Python is coming from the virtual environment:

```bash
which python
```

Expected output should include:

```text
.venv/bin/python
```

### Windows PowerShell

Create virtual environment:

```powershell
python -m venv .venv
```

Activate virtual environment:

```powershell
.venv\Scripts\Activate.ps1
```

If activation is blocked, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again:

```powershell
.venv\Scripts\Activate.ps1
```

---

## 7. Install Dependencies

Install project dependencies:

```bash
pip install -r requirements.txt
```

This installs the required packages such as:

- robotframework
- ruff

---

## 8. Set Python Path

Because the Python source code is inside the `src` folder, set the `PYTHONPATH` before running tests.

### macOS / Linux

```bash
export PYTHONPATH=src
```

Verify:

```bash
echo $PYTHONPATH
```

Expected:

```text
src
```

### Windows PowerShell

```powershell
$env:PYTHONPATH="src"
```

Verify:

```powershell
echo $env:PYTHONPATH
```

Expected:

```text
src
```

---

## Run Python Unit Tests

In addition to Robot Framework validation tests, the project also includes Python unit tests under the `tests/` folder. These tests validate the lower-level Python logic used by the Robot Framework keyword layer, including PWM-to-RPM calculation, tolerance validation, and fault classification.

The unit tests are located here:

```text
tests/
├── test_pwm_tacho_validation.py
└── test_fault_handling.py
```

Run all Python unit tests using Pytest:

```bash
pytest -v
```

Expected result:

```text
19 passed
```

To run a specific unit test file:

```bash
pytest -v tests/test_pwm_tacho_validation.py
```

or:

```bash
pytest -v tests/test_fault_handling.py
```

These unit tests are not the primary validation layer for the submission. Robot Framework is the main test automation layer, while Pytest is used as a supporting developer-level test layer for the reusable Python validation logic.


## 9. Run Robot Framework Validation Tests

Robot Framework is the primary test execution layer for this project.

Run all Robot Framework tests:

```bash
robot -d results/robot robot_tests
```

Expected result:

```text
11 tests, 11 passed, 0 failed
```

Robot Framework will generate reports under:

```text
results/robot
```

Generated report files:

```text
results/robot/report.html
results/robot/log.html
results/robot/output.xml
```

---

## 10. Open Robot Framework Test Report

### macOS

```bash
open results/robot/report.html
```

### Windows PowerShell

```powershell
start results/robot/report.html
```

### Linux

```bash
xdg-open results/robot/report.html
```

The report provides a readable summary of all executed validation scenarios.

---

## 11. Run Static Code Quality Check

Run Ruff against the Python source code:

```bash
ruff check src
```

Expected result:

```text
All checks passed
```

This checks the quality of the supporting Python code used by Robot Framework.

---

## 12. Run CLI Fault Simulation

The project also provides a CLI script to simulate firmware validation scenarios.

### Normal fan behaviour

```bash
python -m thermal_qa.simulate_faults --scenario normal --pwm 60
```

Expected result:

```text
validation_status: PASS
```

### Fan stalled scenario

```bash
python -m thermal_qa.simulate_faults --scenario stalled_fan --pwm 70
```

Expected result:

```text
validation_status: FAULT
```

### Tachometer missing scenario

```bash
python -m thermal_qa.simulate_faults --scenario tacho_missing --pwm 70
```

Expected result:

```text
validation_status: FAULT
```

### Sensor missing scenario

```bash
python -m thermal_qa.simulate_faults --scenario sensor_missing --pwm 70
```

Expected result:

```text
sensor communication fault / TimeoutError
```

---

## 13. Recommended Full Local Execution Sequence

Use this sequence to validate the complete project locally.

### macOS / Linux

```bash
cd hudl_thermal_control_project
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=src

ruff check src
pytest -v  # Pytest Unit Test execution
robot -d results/robot robot_tests # Firmware Validation Tests

python -m thermal_qa.simulate_faults --scenario normal --pwm 60
python -m thermal_qa.simulate_faults --scenario stalled_fan --pwm 70
python -m thermal_qa.simulate_faults --scenario tacho_missing --pwm 70
```

### Windows PowerShell

```powershell
cd hudl_thermal_control_project
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:PYTHONPATH="src"

ruff check src
pytest -v # Pytest Unit Test execution
robot -d results/robot robot_tests # Firmware Validation Tests

python -m thermal_qa.simulate_faults --scenario normal --pwm 60
python -m thermal_qa.simulate_faults --scenario stalled_fan --pwm 70
python -m thermal_qa.simulate_faults --scenario tacho_missing --pwm 70
```

---

## 14. What the Robot Tests Cover

The Robot Framework suite covers the following validation scenarios:

| Area | Scenario |
|---|---|
| Normal behaviour | PWM command produces expected tachometer RPM |
| Boundary behaviour | PWM below fan start threshold expects zero RPM |
| Tolerance validation | RPM above expected tolerance fails |
| Tolerance validation | RPM below expected tolerance fails |
| Fault handling | Missing tachometer signal is reported as FAULT |
| Fault handling | Fan stalled condition is reported as FAULT |
| Input validation | Invalid PWM command is reported as FAULT |
| Test-rig simulation | Normal simulated hardware scenario passes |
| Test-rig simulation | Tachometer missing scenario reports FAULT |
| Test-rig simulation | Fan stall scenario reports FAULT |
| Sensor fault | I2C temperature sensor failure is simulated |

---

## 15. CI/CD Pipeline

The project includes a GitHub Actions workflow:

```text
.github/workflows/firmware-validation.yml
```

The CI pipeline runs automatically on:

- Push to `main`
- Pull request to `main`
- Daily scheduled execution
- Manual execution from GitHub Actions

The CI pipeline performs:

1. Checkout repository
2. Set up Python
3. Install dependencies
4. Run Ruff code quality checks
5. Run Robot Framework firmware validation tests
6. Run CLI fault simulations
7. Upload Robot Framework reports as artifacts

---

## 16. Manually Run CI Pipeline in GitHub

To run the pipeline manually:

1. Open the GitHub repository.
2. Go to the **Actions** tab.
3. Select **Firmware Validation CI**.
4. Click **Run workflow**.
5. Select the `main` branch.
6. Click **Run workflow**.

A green tick means the workflow completed successfully.

---

## 17. CI Output and Reports

After CI execution, GitHub Actions provides:

- Workflow execution logs
- Robot Framework test result summary
- Downloadable Robot Framework report artifacts

The uploaded artifact is usually named:

```text
robot-framework-reports
```

It contains:

```text
report.html
log.html
output.xml
```

---

## 18. Troubleshooting

### Issue: `robot: command not found`

Cause: Virtual environment is not active or dependencies are not installed.

Fix:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

### Issue: `ModuleNotFoundError: No module named 'thermal_qa'`

Cause: `PYTHONPATH` is not set.

Fix on macOS / Linux:

```bash
export PYTHONPATH=src
```

Fix on Windows PowerShell:

```powershell
$env:PYTHONPATH="src"
```

---

### Issue: Robot Framework report not visible

Check whether results were generated:

```bash
ls results/robot
```

Expected files:

```text
log.html
output.xml
report.html
```

Open report on macOS:

```bash
open results/robot/report.html
```

---

### Issue: Virtual environment is active but prompt does not show `(.venv)`

This can happen depending on shell configuration. Verify using:

```bash
which python
```

If the output contains `.venv/bin/python`, the virtual environment is active.

---

## 19. Notes

- Robot Framework is the primary validation layer.
- Python is used as the backend keyword and simulation layer.
- The project uses simulated hardware behaviour so tests can run locally and in CI without physical hardware.
- The structure is designed so that the simulated test rig can later be replaced or extended with real hardware interfaces such as GPIO, I2C, PWM capture, tachometer measurement, or lab instrumentation.

---

## 20. Expected Successful Validation Summary

A successful local validation should show:

```text
Ruff: All checks passed
Robot Framework: 11 tests, 11 passed, 0 failed
CLI normal scenario: PASS
CLI fault scenarios: FAULT as expected
```

This confirms that the core firmware validation logic, fault handling, and Robot Framework test suite are working as expected.
