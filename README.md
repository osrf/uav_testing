This is a repository with example worlds generated from real world examples.

Here are some notes 


# Download content

Go to 
https://earthexplorer.usgs.gov/

Create an account

Find the region of interest. Select a point or set of points.


Select Data Set(s):

 * Aerial Imagry -> High Resolution Orthoimagery
 * Digital Elevation -> SRTM -> SRTM 1 Arc-Second Global

Go to the Results and download all the tiles.
You can download them individually or in a bulk download.

Alternative data sources should be fine as well.

There will be a lot of data.
The 9 tiles I used for McMillan were each approximately 400MB
And the height map arc tile is ~ 25MB.


# Isolate area of interest

Once you have the region of interest use gdalwarp to extract the regions of interest.
This is the script I used for mcmillan and yosemite


    #!/bin/bash                                                                     

    set -x

    # Yosemite                                                                      
    SOUTH=37.6993
    NORTH=37.7690
    EAST=-119.5285
    WEST=-119.5978
    NAME=yosemite
    RESOLUTION=5000
    SOURCE_DIR=/data/temp_gis
    PACKAGE_DIR=/tmp/ws/src/uav_testing/yosemite_valley
    SOURCE_DEM=n37_w120_1arc_v3.tif
    SOURCE_IMAGES='m_3711912_se_11_h_20160701.tif m_3711912_sw_11_h_20160701.tif m_\
    3711920_ne_11_h_20160701.tif m_3711920_nw_11_h_20160701.tif'

    # mcmillan                                                                      
    SOUTH=35.692125
    NORTH=35.755904
    EAST=-120.735120
    WEST=-120.798966
    NAME=mcmillan
    RESOLUTION=5000
    SOURCE_DIR=/data/temp_gis/mcmillan
    PACKAGE_DIR=/tmp/ws/src/uav_testing/mcmillan_airfield
    SOURCE_DEM=n35_w121_1arc_v3.tif
    SOURCE_IMAGES='5724_2452.tif 5724_2462.tif 5724_2472.tif 5734_2452.tif 5734_246\
    2.tif 5734_2472.tif 5744_2452.tif 5744_2462.tif 5744_2472.tif'


    OUTPUT_IMAGE=${NAME}_color.tif
    OUTPUT_DEM=${PACKAGE_DIR}/media/${NAME}_elevation.tif
    OUTPUT_PNG=${PACKAGE_DIR}/media/textures/${NAME}_color.png


    cd $SOURCE_DIR

    rm -f $OUTPUT_DEM $OUTPUT_IMAGE $OUTPUT_PNG


    gdalwarp -te $WEST $SOUTH $EAST $NORTH $SOURCE_DEM  $OUTPUT_DEM

    gdalwarp -t_srs '+proj=longlat +datum=WGS84 +no_defs ' -ts $RESOLUTION 0 -te $W\
    EST $SOUTH $EAST $NORTH $SOURCE_IMAGES $OUTPUT_IMAGE
    convert $OUTPUT_IMAGE $OUTPUT_PNG



Save these files into your gazebo resource path that's exported by the package.

Note that the 5000 is the resolution of the file laterally.

# Generate World

Then create a world that references them.

I pushed the pose down such that the airfield is at zero height in gazebo.
The size of the texture is the width of the content in meters.

Note that there's a scaling issue with the textures. I have ticketed it here: https://bitbucket.org/osrf/gazebo/issues/2603/texture-scaling-on-heightmaps-does-not

It looks like a rendering of about 80% width is necessary.


Gazebo also seems to work better with square content, this might have been an artifact from before validating the above ratio.

# Developmet tip

If you are changing any textures on the height map.
Whether content or meta data it is all cached.
To change anything you will need to remove the cached paging content in `~/.gazebo/paging/VISUAL_ELEMENT`

Ticketed at: https://bitbucket.org/osrf/gazebo/issues/2604/the-default-caching-behavior-of-caching



# Resources:

A potential other approach is to overlay in QGIS: https://opengislab.com/blog/2018/3/20/3d-dem-visualization-in-qgis-30

gdalwarp docs: https://www.gdal.org/gdalwarp.html

SDF geometry documentation: http://sdformat.org/spec?elem=geometry&ver=1.6
