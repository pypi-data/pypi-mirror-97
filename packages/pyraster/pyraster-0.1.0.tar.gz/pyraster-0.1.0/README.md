# PyRaster

PyRaster is a package for processing raster and vector files and preparing training/test data for deep learning applications. PyRaster depends on the python library called `GDAL` with versions after `2.2`. The `GDAL` library does not however simply get installed using `pip`. You have to run the following commands in the terminal and then install the version that your system supports. Please note that this is tested and works on Ubuntu:

```
sudo apt-get install libgdal-dev
export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal
gdal-config --version
```

The last command above prints out the `GDAL` version that you could install on your system. You could install version `2.2.3` for example as follows:


```
pip install GDAL==2.2.3
```

After install GDAL, you could isntall `PyRaster` as follows:

```
pip install PyRaster
```

