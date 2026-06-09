"""Robot Framework keyword library for thermal control validation.

The keywords wrap the Python validation layer so the same business logic can be
executed from Robot Framework or from pytest.
"""

from thermal_qa.fan_model import FanSpec, expected_rpm_from_pwm, rpm_tolerance_band
from thermal_qa.test_rig import SimulatedTestRig
from thermal_qa.validators import validate_pwm_vs_tacho


class ThermalControlKeywords:
    """Robot Framework keywords for PWM/tachometer and fault validation."""

    def __init__(self) -> None:
        self.fan_spec = FanSpec()
        self.rig: SimulatedTestRig | None = None
        self.last_result = None

    def create_default_fan_spec(
        self,
        max_rpm: int = 5000,
        min_start_pwm_percent: int = 20,
        rpm_tolerance_percent: float = 10.0,
        stall_rpm_threshold: int = 200,
    ) -> dict:
        """Create a fan specification used by validation keywords."""
        self.fan_spec = FanSpec(
            max_rpm=int(max_rpm),
            min_start_pwm_percent=int(min_start_pwm_percent),
            rpm_tolerance_percent=float(rpm_tolerance_percent),
            stall_rpm_threshold=int(stall_rpm_threshold),
        )
        return self._fan_spec_as_dict()

    def expected_rpm_for_pwm(self, pwm_percent: float) -> float:
        """Return expected fan RPM for a PWM duty cycle."""
        return expected_rpm_from_pwm(float(pwm_percent), self.fan_spec)

    def rpm_tolerance_band_for_pwm(self, pwm_percent: float) -> dict:
        """Return lower and upper RPM tolerance limits for a PWM command."""
        expected_rpm = self.expected_rpm_for_pwm(float(pwm_percent))
        lower_limit, upper_limit = rpm_tolerance_band(
            expected_rpm, self.fan_spec.rpm_tolerance_percent
        )
        return {
            "expected_rpm": expected_rpm,
            "lower_limit": lower_limit,
            "upper_limit": upper_limit,
        }

    def validate_pwm_tacho_response(
        self, pwm_percent: float, measured_rpm: float | None
    ) -> dict:
        """Validate the measured tachometer RPM against commanded PWM."""
        normalized_rpm = None if measured_rpm in (None, "${None}", "None") else float(measured_rpm)
        result = validate_pwm_vs_tacho(float(pwm_percent), normalized_rpm, self.fan_spec)
        self.last_result = result
        return {
            "status": result.status.value,
            "message": result.message,
            "pwm_percent": result.pwm_percent,
            "measured_rpm": result.measured_rpm,
            "expected_rpm": result.expected_rpm,
            "lower_limit": result.lower_limit,
            "upper_limit": result.upper_limit,
        }

    def validation_status_should_be(self, result: dict, expected_status: str) -> None:
        """Assert validation result status."""
        actual_status = result["status"]
        if actual_status != expected_status:
            raise AssertionError(
                f"Expected validation status {expected_status}, got {actual_status}. "
                f"Full result: {result}"
            )

    def validation_message_should_contain(self, result: dict, expected_text: str) -> None:
        """Assert validation message contains the expected text."""
        if expected_text not in result["message"]:
            raise AssertionError(
                f"Expected message to contain {expected_text!r}, got {result['message']!r}"
            )

    def create_simulated_test_rig(
        self,
        scenario: str = "normal",
        seed: int = 42,
        noise_percent: float = 3.0,
    ) -> None:
        """Create a simulated hardware test rig for normal or fault scenarios."""
        scenario = scenario.lower()
        self.rig = SimulatedTestRig(
            fan_spec=self.fan_spec,
            seed=int(seed),
            noise_percent=float(noise_percent),
            sensor_available=scenario != "sensor_missing",
            tachometer_available=scenario != "tacho_missing",
            fan_stalled=scenario == "stalled_fan",
        )

    def command_pwm_on_test_rig(self, pwm_percent: float) -> None:
        """Command PWM duty cycle on the simulated test rig."""
        self._require_rig().set_pwm(float(pwm_percent))

    def read_tachometer_from_test_rig(self) -> float | None:
        """Read tachometer RPM from the simulated test rig."""
        return self._require_rig().read_tachometer_rpm()

    def read_temperature_from_test_rig(self) -> float:
        """Read temperature from the simulated test rig."""
        return self._require_rig().read_temperature_celsius()

    def validate_current_test_rig_pwm_tacho(self, pwm_percent: float) -> dict:
        """Read the current tachometer RPM and validate it against PWM."""
        measured_rpm = self.read_tachometer_from_test_rig()
        return self.validate_pwm_tacho_response(float(pwm_percent), measured_rpm)

    def _require_rig(self) -> SimulatedTestRig:
        if self.rig is None:
            raise RuntimeError("No simulated test rig exists. Call Create Simulated Test Rig first.")
        return self.rig

    def _fan_spec_as_dict(self) -> dict:
        return {
            "max_rpm": self.fan_spec.max_rpm,
            "min_start_pwm_percent": self.fan_spec.min_start_pwm_percent,
            "rpm_tolerance_percent": self.fan_spec.rpm_tolerance_percent,
            "stall_rpm_threshold": self.fan_spec.stall_rpm_threshold,
        }
