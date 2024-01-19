import os
import logging


class Product(object):
    def __init__(self, manifest_item, gpro):
        self.manifest_item = manifest_item
        self.gpro = gpro

    def data_location(self):
        return os.path.join(self.gpro.path, self.manifest_item["output"])

    def sensor_type(self):
        if "sensor_type" in self.manifest_item:
            return self.manifest_item["sensor_type"]
        else:
            output_filename = os.path.basename(self.manifest_item["output"])
            return self.gpro.latest_pipeline().get_processing_parameters(output_filename)["type"]

    def product_params(self):
        output_filename = os.path.basename(self.manifest_item["output"])
        return self.gpro.latest_pipeline().get_product_parameters(output_filename)

    def processing_params(self):
        output_filename = os.path.basename(self.manifest_item["output"])
        return self.gpro.latest_pipeline().get_processing_parameters(output_filename)

    def calibration(self):
        output_filename = os.path.basename(self.manifest_item["output"])
        return self.gpro.latest_pipeline()\
            .get_calibration(output_filename)\
            .get_sensor_calibration(self.manifest_item["sensor_id"])

    def product_type(self):
        output_filename = os.path.basename(self.manifest_item["output"])
        product_params = self.gpro.latest_pipeline() \
            .get_product_parameters(output_filename)
        if product_params:
            return product_params["type"]
        else:
            return None

    def acquisition_date(self):
        if self.gpro.mission_data:
            return self.gpro.mission_data["acquisition_datetime"]

    @staticmethod
    def gdal_init():
        try:
            try:
                import gdal
            except ImportError:
                from osgeo import gdal
            gdal.AllRegister()
            return gdal
        except ImportError:
            logging.warning("Unable to load GDAL. Cannot provide gdal dataset. Is it installed?")
            return None

    @staticmethod
    def rasterio_init():
        try:
            import rasterio
        except ImportError:
            logging.warning("Unable to load rasterio. Cannot provide rasterio dataset. Is it installed?")
            return None
        return rasterio

    @staticmethod
    def laspy_init():
        try:
            import laspy
        except ImportError:
            logging.warning("Unable to load laspy. Cannot provide laspy dataset. Is it installed?")
            return None
        return laspy

    def gdal_dataset(self):
        gdal = self.gdal_init()
        if not gdal:
            return None
        try:
            return gdal.Open(self.data_location())
        except Exception as e:
            logging.critical("An exception occurred while trying to open " + self.data_location() + " with GDAL.")
            logging.critical(e)

    def rasterio_dataset(self):
        rasterio = self.rasterio_init()
        if not rasterio:
            return None
        try:
            return rasterio.open(self.data_location())
        except Exception as e:
            logging.critical("An exception occurred while trying to open " + self.data_location() + " with rasterio.")
            logging.critical(e)

    def laspy_dataset(self):
        laspy = self.laspy_init()
        if not laspy:
            return None
        try:
            return laspy.open(self.data_location(), "r")
        except Exception as e:
            logging.critical("An exception occurred while trying to open " + self.data_location() + " with laspy.")
            logging.critical(e)