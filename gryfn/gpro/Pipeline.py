import os

import yaml


class Pipeline(object):
    def __init__(self, pipeline_path, gpro):
        self.path = pipeline_path
        self.gpro = gpro
        self.name = os.path.basename(self.path)
        self.contents = {}
        self.validate()

    def validate(self):
        with open(self.path, "r") as f:
            self.contents = yaml.load(f, Loader=yaml.Loader)

    def get_product_parameters(self, product_name):
        for task in self.contents["tasks"]:
            if "products" not in task:
                continue
            for product in task["products"]:
                if product["filename"] == product_name:
                    return product
        return {}

    def get_processing_parameters(self, product_name):
        for task in self.contents["tasks"]:
            if "products" not in task:
                continue
            for product in task["products"]:
                if product["filename"] == product_name:
                    task_copy = task.copy()
                    del task_copy["products"]
                    return task_copy
        return {}

    def get_calibration(self, product_name):
        for task in self.contents["tasks"]:
            if "products" not in task:
                continue
            for product in task["products"]:
                if product["filename"] == product_name:
                    if task["calibration"] == "nominal":
                        nominal = self.gpro.mission_data["nominal_calibration"]
                        return self.gpro.calibrations[nominal]
                    else:
                        return self.gpro.calibrations[task["calibration"]]
