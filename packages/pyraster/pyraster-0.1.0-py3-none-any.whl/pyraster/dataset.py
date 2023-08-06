from osgeo import gdal, gdalconst, ogr
import os


def polygon_to_raster(
        input_raster,
        shapefile,
        target_raster,
        field_name=None
    ):
    """
    Creates a mask for the polygons in shapefile that coincides with the input_raster. 
    The mask values are set using the 'field_name' attribute in the shapefile if given,
    otherwise a default value of 1 is used as the mask.
    """
    burn_value = 1 # used if field_name is None

    # read the input raster
    try:
        data = gdal.Open(input_raster, gdalconst.GA_ReadOnly)
    except:
        print('Could not read input raster: {}, please make sure it exists!'.format(input_raster))

    # get raster geotransform information and the projection    
    geo_transform = data.GetGeoTransform()
    projection = data.GetProjection()
    # get the no data value, i.e., pixel value for points with no information.
    nodata_value = data.GetRasterBand(1).GetNoDataValue()

    # read the shapefile and get the vector layer
    shape_source = ogr.Open(shapefile)
    shape_layer = shape_source.GetLayer()

    # Create a new raster to save the masks or segmentatio mask withe same dimensions as the input raster
    target_ds = gdal.GetDriverByName('GTiff').Create(target_raster, data.RasterXSize, data.RasterYSize, 1, gdal.GDT_Byte)

    # Set the transformation and projection similar to those of the input raster
    target_ds.SetGeoTransform(geo_transform)
    target_ds.SetProjection(projection)

    # create masks for the polygons coinciding with the input raster
    if field_name is not None:
        # mask values are based on 'field_name' attribute in the shapefile
        gdal.RasterizeLayer(target_ds, [1], shape_layer, options=["ATTRIBUTE=" + field_name])
    else:
        # field_name is not given, mask values are 1.
        gdal.RasterizeLayer(target_ds, [1], shape_layer, None, None, [burn_value], ['ALL_TOUCHED=TRUE'])
    target_ds = None


def get_desired_extent(height, width, extent):
    """ 
    calculates and returns bounding box with the given height and width
    such that the original extent is in the center.
    """
    # parse coordinates from the polygon extent
    minx, maxx, miny, maxy = extent

    # calculate original height and width of the extent
    difx = maxx - minx
    dify = maxy - miny

    # calculate the desired height and width
    extrax = (width - difx) / 2
    extray = (height - dify) / 2
    minx = minx - extrax
    maxx = maxx + extrax
    miny = miny - extray
    maxy = maxy + extray

    # return the corresponding bounding box coordinates
    return minx, maxy,maxx, miny


def isWithin(rect1, rect2):
    """Checks whether rectangle 1 is within rectangle 2
    Parameters:
        rect1: list of coordinates [minx, maxy, maxx, miny]
        rect2: list of coordinates [minx, maxy, maxx, miny]
    Returns:
        True if rect1 within rect2 else False
    """
    minx1, maxy1,maxx1, miny1 = rect1
    minx2, maxy2,maxx2, miny2 = rect2
    if minx1 < minx2 or maxx1 > maxx2 or miny1 < miny2 or maxy1 > maxy2:
        return False
    return True



def create_segmentation_data(
        shapefile,
        raster_file,
        input_folder,
        label_folder,
        height,
        width,
        field_name=None
    ):
    """Create segmentation input/label pairs. Width and height are in pixels.
    Parameters:
        shapefile: path to shapefile
        raster_file: path to raster_file
        input_folder: directory to save input rasters
        label_folder: directory to save target labels
        height: height in pixels for input/target
        width: width in pixels for input/target
        field_name: attribute containing labels in the shapefile
    Returns:
    """

    # Read the large raster data
    try:
        ds = gdal.Open(raster_file, gdalconst.GA_ReadOnly)
    except:
        print('Could not read the raster file: {}, please make sure the path is correct!'.format(raster_file))

    # get raster resolution and coordinates
    geotransform = ds.GetGeoTransform()
    minx, raster_resolution, _, maxy, _, y_res = geotransform
    maxx = minx + ds.RasterXSize*raster_resolution
    miny = maxy + ds.RasterYSize*y_res
    input_raster_extent = [minx, maxy, maxx, miny]
    
    
    # read shapefile
    driver = ogr.GetDriverByName('ESRI Shapefile')
    try:
        shp_source = driver.Open(shapefile, 0)
    except:
        print('Could not read the shapefile: {}, please make sure the path is correct!'.format(shapefile))
    
    # get the vector layer 
    shp_layer = shp_source.GetLayer()

    # create input directories
    if not os.path.exists(input_folder):
        print('Creating input folder: {}'.format(input_folder))
        os.makedirs(input_folder)
    if not os.path.exists(label_folder):
        print('Creating target folder: {}'.format(label_folder))
        os.makedirs(label_folder)

    # start creating input/target pairs 
    for i, feature in enumerate(shp_layer):
        # get the geometry for current feature
        geom = feature.GetGeometryRef()
        # get the bounding box for current feature
        extent = geom.GetEnvelope() # (miny, maxx, miny, maxy)

        # Calculate the desired extent for expected pixel size using the raster resolution
        real_extent = get_desired_extent(height*raster_resolution, width*raster_resolution, extent) # minx, maxy,maxx, miny

        # check if current feature lies within the input raster, if not, we won't crop data from here.
        if not isWithin(real_extent, input_raster_extent):
            continue

        # name each file using the feature/record index (starting from 1)
        segmentation_input_file = os.path.join(input_folder, str(i+1)+'.tif')
        segmentation_label_file = os.path.join(label_folder, str(i+1)+'.tif')

        # crop corresponding patch for current feature from the raster
        gdal.Translate(segmentation_input_file, raster_file, projWin=real_extent)

        """
        create a segmentation ground truth raster for current feature where labels 
        are numbers given in the 'field_name' if given, otherwise labels are 1 
        """ 
        polygon_to_raster(segmentation_input_file, shapefile, segmentation_label_file, field_name=field_name)


