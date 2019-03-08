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
This is the script I used for mcmillan.


    #!/bin/bash

    set -x
    # TOp left: 35.747585, -120.798966
    # Bottom Right: 35.692125, -120.735120

    SOUTH=35.692125
    NORTH=35.755904
    EAST=-120.735120
    WEST=-120.798966

    LAT_OFFSET=-0.0055
    ADJ_SOUTH=$(echo "$SOUTH+$LAT_OFFSET" | bc)
    ADJ_NORTH=$(echo "$NORTH+$LAT_OFFSET" | bc)

    LON_OFFSET=0.005
    ADJ_EAST=$(echo "$EAST+$LON_OFFSET" | bc)
    ADJ_WEST=$(echo "$WEST+$LON_OFFSET" | bc)

    rm -f mcmillan_color.tif mcmillan_elevation.tif

    gdalwarp -te $WEST $SOUTH $EAST $NORTH  n35_w121_1arc_v3.tif mcmillan_elevation.tif

    gdalwarp -t_srs '+proj=longlat +datum=WGS84 +no_defs ' -ts 6000 0 -te $ADJ_WEST $ADJ_SOUTH $ADJ_EAST $ADJ_NORTH 5724_2452.tif 5724_2462.tif 5724_2472.tif 5734_2452.tif 5734_2462.tif 5734_2472.tif 5744_2452.tif 5744_2462.tif 5744_2472.tif mcmillan_color.tif
    convert mcmillan_color.tif mcmillan_color.png

Save these files into your gazebo resource path that's exported by the package.

Note that the 6000 is the resolution of the file laterally. 

# Generate World

Then create a world that references them.

I pushed the pose down such that the airfield is at zero height in gazebo.
The size of the texture is the width of the content in meters.

Note that there seemed to be an offset due to possibly NAD1983 vs WGS1984 I'm not sure exactly where it came from.
I had gdal fix the dataum, but I think there might be registration errors.

Gazebo also seems to force the heightmap content to be square.

# Developmet tip

If you are changing any textures on the height map.
Whether content or meta data it is all cached.
To change anything you will need to remove the cached paging content in `~/.gazebo/paging/VISUAL_ELEMENT`

