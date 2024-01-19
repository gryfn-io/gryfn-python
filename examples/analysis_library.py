import gryfn


def extract_plots(gdal_dataset):
    # Dummy function
    print(gdal_dataset.GetDescription() + " has " + str(gdal_dataset.RasterCount) + " bands!")
    print(gdal_dataset.GetDescription() + " has dimensions " + str(gdal_dataset.RasterXSize) + " x " + str(gdal_dataset.RasterYSize))
    pass


def run_lidar_analysis(lidar_product, plot_file):
    # Dummy function
    # The laspy_dataset calls laspy.open() under the hood, so it just assumes you at least want the header.
    # You need to call .read(), or chunk_iterator() to actually read the point cloud points.

    dataset = lidar_product.laspy_dataset()
    print(str(dataset.header.point_count) + " points in " + lidar_product.data_location())
    # for points in dataset.chunk_iterator(1_000_000):
    #     print(points[0].X)
    pass


def run_hyper_analysis(rasterio_dataset):
    # Dummy function
    print(rasterio_dataset.name + " has " + str(len(rasterio_dataset.indexes)) + " bands!")
    print(rasterio_dataset.name + " has dimensions " + str(rasterio_dataset.width) + " x " + str(rasterio_dataset.height))
    pass


def process_data(gpro, plot_file):
    # Shows off some basic functionality in the GPro class.
    for lidar_product in gpro.lidar_products():
        print(lidar_product.product_type())
        print(lidar_product.acquisition_date())
        print(lidar_product.calibration())

    for vnir_product in gpro.vnir_products():
        print(vnir_product.acquisition_date())

    for rgb_product in gpro.rgb_products():
        print(rgb_product.data_location())
        if rgb_product.data_location().endswith(".tif"):
            ds = rgb_product.gdal_dataset()
            print(dir(ds))
            ds = rgb_product.rasterio_dataset()
            print(dir(ds))
        if rgb_product.data_location().endswith(".laz"):
            ds = rgb_product.laspy_dataset()
            print(dir(ds))
        print(rgb_product.product_params())

    for product in gpro.all_products():
        print(product.data_location() + " --- " + str(product.product_type()) + " --- " + str(product.sensor_type()))

    # The products can be inspected for specific processing parameters, then processed if they
    # fall within whatever criteria are wanted.
    for rgb in gpro.rgb_products():
        if "resolution_cm" in rgb.product_params() and rgb.product_params()["resolution_cm"] <= 1.0:
            print("\nRunning plot extraction on " + rgb.data_location() + " (resolution = %.1f cm)." % float(rgb.product_params()["resolution_cm"]))
            extract_plots(rgb.gdal_dataset())

    for lidar in gpro.lidar_products():
        if lidar.product_type() == "combined_point_cloud":
            print("\nRunning analysis on the lidar's combined point cloud - " + lidar.data_location())
            run_lidar_analysis(lidar, plot_file)

    for hyper in gpro.vnir_products():
        if hyper.product_type() == "orthomosaic":
            print("\nRunning plant indexing on orthomosaic product (resolution = %.1f cm)." % float(hyper.product_params()["resolution_cm"]))
            run_hyper_analysis(hyper.rasterio_dataset())
