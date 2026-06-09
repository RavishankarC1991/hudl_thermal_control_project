from dataclasses import dataclass
from enum import Enum

from thermal_qa.fan_model import FanSpec, expected_rpm_from_pwm, rpm_tolerance_band


class ValidationStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    FAULT = "FAULT"


@dataclass(frozen=True)
class ValidationResult:
    status: ValidationStatus
    message: str
    pwm_percent: float
    measured_rpm: float | None
    expected_rpm: float | None
    lower_limit: float | None
    upper_limit: float | None


def validate_pwm_vs_tacho(
    pwm_percent: float,
    measured_rpm: float | None,
    fan_spec: FanSpec,
) -> ValidationResult:
    """Validate tachometer RPM response for a commanded PWM value."""
    if pwm_percent < 0 or pwm_percent > 100:
        return ValidationResult(
            status=ValidationStatus.FAULT,
            message="PWM command outside valid range 0-100%",
            pwm_percent=pwm_percent,
            measured_rpm=measured_rpm,
            expected_rpm=None,
            lower_limit=None,
            upper_limit=None,
        )

    if measured_rpm is None:
        return ValidationResult(
            status=ValidationStatus.FAULT,
            message="Tachometer signal missing",
            pwm_percent=pwm_percent,
            measured_rpm=None,
            expected_rpm=None,
            lower_limit=None,
            upper_limit=None,
        )

    if measured_rpm < 0:
        return ValidationResult(
            status=ValidationStatus.FAULT,
            message="Invalid negative tachometer RPM",
            pwm_percent=pwm_percent,
            measured_rpm=measured_rpm,
            expected_rpm=None,
            lower_limit=None,
            upper_limit=None,
        )

    expected_rpm = expected_rpm_from_pwm(pwm_percent, fan_spec)
    lower_limit, upper_limit = rpm_tolerance_band(
        expected_rpm, fan_spec.rpm_tolerance_percent
    )

    if pwm_percent >= fan_spec.min_start_pwm_percent and measured_rpm < fan_spec.stall_rpm_threshold:
        return ValidationResult(
            status=ValidationStatus.FAULT,
            message="Possible fan stall: PWM commanded but RPM below stall threshold",
            pwm_percent=pwm_percent,
            measured_rpm=measured_rpm,
            expected_rpm=expected_rpm,
            lower_limit=lower_limit,
            upper_limit=upper_limit,
        )

    if lower_limit <= measured_rpm <= upper_limit:
        return ValidationResult(
            status=ValidationStatus.PASS,
            message="Measured tachometer RPM is within tolerance for commanded PWM",
            pwm_percent=pwm_percent,
            measured_rpm=measured_rpm,
            expected_rpm=expected_rpm,
            lower_limit=lower_limit,
            upper_limit=upper_limit,
        )

    return ValidationResult(
        status=ValidationStatus.FAIL,
        message="Measured tachometer RPM is outside tolerance for commanded PWM",
        pwm_percent=pwm_percent,
        measured_rpm=measured_rpm,
        expected_rpm=expected_rpm,
        lower_limit=lower_limit,
        upper_limit=upper_limit,
    )
