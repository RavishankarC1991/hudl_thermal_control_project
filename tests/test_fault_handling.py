import pytest

from thermal_qa.fan_model import FanSpec
from thermal_qa.test_rig import SimulatedTestRig
from thermal_qa.validators import ValidationStatus, validate_pwm_vs_tacho


def test_detects_tachometer_signal_loss() -> None:
    fan_spec = FanSpec()
    result = validate_pwm_vs_tacho(pwm_percent=70, measured_rpm=None, fan_spec=fan_spec)

    assert result.status == ValidationStatus.FAULT
    assert "Tachometer signal missing" in result.message


def test_detects_fan_stall_when_pwm_commanded_but_rpm_is_zero() -> None:
    fan_spec = FanSpec(stall_rpm_threshold=200)
    result = validate_pwm_vs_tacho(pwm_percent=80, measured_rpm=0, fan_spec=fan_spec)

    assert result.status == ValidationStatus.FAULT
    assert "fan stall" in result.message.lower()


@pytest.mark.parametrize("invalid_pwm", [-1, 101])
def test_detects_invalid_pwm_command(invalid_pwm: float) -> None:
    fan_spec = FanSpec()
    result = validate_pwm_vs_tacho(
        pwm_percent=invalid_pwm,
        measured_rpm=1000,
        fan_spec=fan_spec,
    )

    assert result.status == ValidationStatus.FAULT
    assert "outside valid range" in result.message


def test_detects_invalid_negative_rpm() -> None:
    fan_spec = FanSpec()
    result = validate_pwm_vs_tacho(pwm_percent=50, measured_rpm=-100, fan_spec=fan_spec)

    assert result.status == ValidationStatus.FAULT
    assert "negative" in result.message


def test_simulated_sensor_failure_raises_timeout() -> None:
    rig = SimulatedTestRig(fan_spec=FanSpec(), sensor_available=False)

    with pytest.raises(TimeoutError):
        rig.read_temperature_celsius()
