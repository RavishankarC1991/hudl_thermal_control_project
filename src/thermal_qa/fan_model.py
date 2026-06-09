from dataclasses import dataclass


@dataclass(frozen=True)
class FanSpec:
    """Fan characteristics used for validation.

    In a real project these values should come from the fan datasheet or
    from calibration data measured on the product test rig.
    """

    max_rpm: int = 5000
    min_start_pwm_percent: int = 20
    rpm_tolerance_percent: float = 10.0
    stall_rpm_threshold: int = 200


def expected_rpm_from_pwm(pwm_percent: float, fan_spec: FanSpec) -> float:
    """Return expected RPM for a commanded PWM duty cycle.

    This simple model assumes an approximately linear fan response above the
    minimum start PWM. Below the start threshold the expected RPM is zero.
    """
    if pwm_percent <= 0:
        return 0.0
    if pwm_percent < fan_spec.min_start_pwm_percent:
        return 0.0
    if pwm_percent > 100:
        raise ValueError("PWM percent cannot be greater than 100")
    return fan_spec.max_rpm * (pwm_percent / 100.0)


def rpm_tolerance_band(expected_rpm: float, tolerance_percent: float) -> tuple[float, float]:
    delta = expected_rpm * (tolerance_percent / 100.0)
    return expected_rpm - delta, expected_rpm + delta
