import pytest

from thermal_qa.fan_model import FanSpec, expected_rpm_from_pwm
from thermal_qa.test_rig import SimulatedTestRig
from thermal_qa.validators import ValidationStatus, validate_pwm_vs_tacho


@pytest.mark.parametrize(
    ("pwm", "expected_rpm"),
    [
        (0, 0),
        (10, 0),
        (20, 1000),
        (50, 2500),
        (100, 5000),
    ],
)
def test_expected_rpm_from_pwm_model(pwm: float, expected_rpm: float) -> None:
    fan_spec = FanSpec(max_rpm=5000, min_start_pwm_percent=20)
    assert expected_rpm_from_pwm(pwm, fan_spec) == expected_rpm


@pytest.mark.parametrize("pwm", [20, 40, 60, 80, 100])
def test_pwm_vs_tacho_passes_when_rpm_is_within_tolerance(pwm: float) -> None:
    fan_spec = FanSpec(max_rpm=5000, rpm_tolerance_percent=10)
    measured_rpm = expected_rpm_from_pwm(pwm, fan_spec)

    result = validate_pwm_vs_tacho(pwm, measured_rpm, fan_spec)

    assert result.status == ValidationStatus.PASS


def test_pwm_vs_tacho_fails_when_rpm_is_above_tolerance() -> None:
    fan_spec = FanSpec(max_rpm=5000, rpm_tolerance_percent=10)
    pwm = 60
    measured_rpm = 4000

    result = validate_pwm_vs_tacho(pwm, measured_rpm, fan_spec)

    assert result.status == ValidationStatus.FAIL
    assert "outside tolerance" in result.message


def test_pwm_vs_tacho_fails_when_rpm_is_below_tolerance_but_not_stalled() -> None:
    fan_spec = FanSpec(max_rpm=5000, rpm_tolerance_percent=10, stall_rpm_threshold=200)
    pwm = 60
    measured_rpm = 2400

    result = validate_pwm_vs_tacho(pwm, measured_rpm, fan_spec)

    assert result.status == ValidationStatus.FAIL
    assert "outside tolerance" in result.message


def test_simulated_test_rig_normal_response_is_within_tolerance() -> None:
    fan_spec = FanSpec(max_rpm=5000, rpm_tolerance_percent=10)
    rig = SimulatedTestRig(fan_spec=fan_spec, noise_percent=3.0)
    rig.set_pwm(60)

    measured_rpm = rig.read_tachometer_rpm()
    result = validate_pwm_vs_tacho(60, measured_rpm, fan_spec)

    assert result.status == ValidationStatus.PASS
