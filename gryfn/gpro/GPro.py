import os
import yaml
import logging
import glob
from gryfn import products
from gryfn import Pipeline
from gryfn import PlatformCalibration


class GPro(object):
    def __init__(self, gpro_location):
        self.path = gpro_location
        self.manifest_location = os.path.join(gpro_location, "manifest.yaml").strip()
        self.products_location = os.path.join(gpro_location, "products.yaml").strip()
        self.manifest = []
        self.products = []
        self.mission_data_location = os.path.normpath(os.path.join(gpro_location, "mission_data.yaml"))
        self.mission_data = None
        self.calibrations = {}
        self.pipelines = []
        self.validate()

    def validate(self):
        if not self._products_present():
            logging.warning("Unable to load products.yaml from gpro.")
        if not self._manifest_present():
            raise Exception("Unable to find GPro manifest from %s." % self.manifest_location)
        if not self._mission_data_present():
            logging.warning("Unable to load mission data from gpro.")
        self._search_for_pipelines()
        self._search_for_calibration_files()

    def all_products(self):
        data_products = self.hyperspectral_products()
        data_products.extend(self.lidar_products())
        data_products.extend(self.rgb_products())
        data_products.extend(self.gnss_products())
        return data_products

    def lidar_products(self):
        return self._products("LiDAR", products.LiDAR)

    def vnir_products(self):
        return self._products("VNIR", products.VNIR)

    def swir_products(self):
        return self._products("SWIR", products.SWIR)

    def rgb_products(self):
        return self._products("RGB", products.RGB)

    def gnss_products(self):
        return self._products("GNSS", products.RGB)

    def hyperspectral_products(self):
        data_products = self._products("Hyperspectral", products.Hyperspectral)
        data_products.extend(self._products("SWIR", products.SWIR))
        data_products.extend(self._products("VNIR", products.VNIR))
        return data_products

    def _products(self, sensor_type, clazz):
        data_products = []
        if self.products:
            for item in self.products:
                if item["sensor_type"] == sensor_type:
                    data_products.append(clazz(item, self))
        else:
            self._load_manifest()
            for item in self.manifest:
                if "sensor_type" in item:
                    if item["sensor_type"] == sensor_type:
                        data_products.append(clazz(item, self))
                elif self._find_product_in_pipeline(sensor_type, item):
                    data_products.append(clazz(item, self))
        return data_products

    def latest_pipeline(self):
        return self.pipelines[-1]

    def _mission_data_present(self):
        if not os.path.exists(self.mission_data_location):
            return False
        try:
            with open(self.mission_data_location, "r") as mission_data:
                self.mission_data = yaml.load(mission_data, Loader=yaml.Loader)
            return True
        except Exception as e:
            return False

    def _manifest_present(self):
        return os.path.exists(self.manifest_location)

    def _load_manifest(self):
        try:
            with open(self.manifest_location, "r") as manifest:
                self.manifest = yaml.load(manifest, Loader=yaml.Loader)
            return True
        except Exception as e:
            logging.warning("Unable to load manifest.yaml.")
            logging.warning(str(e))
            return False

    def _products_present(self):
        if not os.path.exists(self.products_location):
            return False
        try:
            with open(self.products_location, "r") as products_manifest:
                self.products = yaml.load(products_manifest, Loader=yaml.Loader)
            return True
        except Exception as e:
            return False

    def _search_for_pipelines(self):
        yamls = glob.glob(os.path.join(self.path, "*.y*ml"))
        for y in yamls:
            with open(y, "r") as f:
                contents = yaml.load(f, Loader=yaml.Loader)
                if "tasks" in contents:
                    self.pipelines.append(Pipeline(y, self))
        self.pipelines.sort(key=lambda p: p.name)

    def _search_for_calibration_files(self):
        yamls = glob.glob(os.path.join(self.path, "*.y*ml"))
        for y in yamls:
            with open(y, "r") as f:
                contents = yaml.load(f, Loader=yaml.Loader)
                if "sensors" in contents:
                    self.calibrations[os.path.basename(y)] = PlatformCalibration(y, self)

    def _find_product_in_pipeline(self, sensor_type, item):
        output_filename = os.path.basename(item["output"])
        for task in self.latest_pipeline().contents["tasks"]:
            if "products" in task:
                for product in task["products"]:
                    if product["filename"] == output_filename and sensor_type == task["type"]:
                        return True
        return False
