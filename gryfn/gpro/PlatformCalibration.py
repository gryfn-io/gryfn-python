import yaml


class PlatformCalibration(object):
    def __init__(self, calibration_location, gpro):
        self.path = calibration_location
        self.gpro = gpro
        self.contents = {}
        self.validate()

    def validate(self):
        with open(self.path, "r") as f:
            self.contents = yaml.load(f, Loader=yaml.Loader)

    def get_sensor_calibration(self, sensor_id):
        for sensor in self.contents["sensors"]:
            if sensor["id"] == sensor_id:
                return sensor
