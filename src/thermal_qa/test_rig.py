from dataclasses import dataclass
from random import Random

from thermal_qa.fan_model import FanSpec, expected_rpm_from_pwm


@dataclass
class SimulatedTestRig:
    """Simulation of a thermal-control hardware test rig.

    In a real system this class can be replaced with an adapter that controls
    hardware through GPIO, serial, SCPI, vendor SDK, or a board debug interface.
    """

    fan_spec: FanSpec
    seed: int = 42
    noise_percent: float = 3.0
    sensor_available: bool = True
    tachometer_available: bool = True
    fan_stalled: bool = False

    def __post_init__(self) -> None:
        self._rng = Random(self.seed)
        self._pwm_percent = 0.0

    def set_pwm(self, pwm_percent: float) -> None:
        if pwm_percent < 0 or pwm_percent > 100:
            raise ValueError("PWM must be between 0 and 100")
        self._pwm_percent = pwm_percent

    def read_tachometer_rpm(self) -> float | None:
        if not self.tachometer_available:
            return None
        if self.fan_stalled:
            return 0.0

        nominal_rpm = expected_rpm_from_pwm(self._pwm_percent, self.fan_spec)
        noise = self._rng.uniform(-self.noise_percent, self.noise_percent) / 100.0
        return round(nominal_rpm * (1.0 + noise), 2)

    def read_temperature_celsius(self) -> float:
        if not self.sensor_available:
            raise TimeoutError("I2C temperature sensor read failed")
        return 42.0
