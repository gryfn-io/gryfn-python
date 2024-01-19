import logging
from .Product import Product


class Hyperspectral(Product):
    pass

    def laspy_dataset(self):
        logging.warning("LAS/LAZ is not a supported format for hyperspectral data.")
