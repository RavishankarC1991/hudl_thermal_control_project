import argparse
import json

from thermal_qa.fan_model import FanSpec
from thermal_qa.test_rig import SimulatedTestRig
from thermal_qa.validators import validate_pwm_vs_tacho


def build_rig_for_scenario(scenario: str) -> SimulatedTestRig:
    fan_spec = FanSpec()
    if scenario == "normal":
        return SimulatedTestRig(fan_spec=fan_spec)
    if scenario == "stalled_fan":
        return SimulatedTestRig(fan_spec=fan_spec, fan_stalled=True)
    if scenario == "tacho_missing":
        return SimulatedTestRig(fan_spec=fan_spec, tachometer_available=False)
    if scenario == "sensor_missing":
        return SimulatedTestRig(fan_spec=fan_spec, sensor_available=False)
    raise ValueError(f"Unsupported scenario: {scenario}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Simulate thermal control fault data")
    parser.add_argument(
        "--scenario",
        choices=["normal", "stalled_fan", "tacho_missing", "sensor_missing"],
        default="normal",
    )
    parser.add_argument("--pwm", type=float, default=60.0)
    args = parser.parse_args()

    rig = build_rig_for_scenario(args.scenario)
    rig.set_pwm(args.pwm)

    sensor_status = "OK"
    try:
        temperature = rig.read_temperature_celsius()
    except TimeoutError as exc:
        temperature = None
        sensor_status = str(exc)

    measured_rpm = rig.read_tachometer_rpm()
    result = validate_pwm_vs_tacho(args.pwm, measured_rpm, rig.fan_spec)

    output = {
        "scenario": args.scenario,
        "temperature_celsius": temperature,
        "sensor_status": sensor_status,
        "pwm_percent": args.pwm,
        "measured_rpm": measured_rpm,
        "validation_status": result.status.value,
        "validation_message": result.message,
        "expected_rpm": result.expected_rpm,
        "lower_limit": result.lower_limit,
        "upper_limit": result.upper_limit,
    }
    print(json.dumps(output, indent=2))
    return 0 if result.status.value == "PASS" or args.scenario != "normal" else 1


if __name__ == "__main__":
    raise SystemExit(main())
