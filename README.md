# upload-to-mapbox

A GBDX task that uploads raster or vector files to [Mapbox Studio](https://www.mapbox.com/mapbox-studio/).

In the case of a vector file, [tippecanoe](https://github.com/mapbox/tippecanoe) is used to create the corresponding .mbtiles file prior to upload. You need a Mapbox Studio account in order to use this task.
Acceptable file formats and size limits can be found [here](https://www.mapbox.com/api-documentation/#uploads).
Useful tips for uploading can be found [here](https://www.mapbox.com/help/uploads/).
You can find an example of using upload-to-mapbox [here](http://gbdxstories.digitalglobe.com/osm-lulc/).

## Run

In a Python terminal:

```python
import gbdxtools

gbdx = gbdxtools.Interface()

utom = gbdx.Task('upload-to-mapbox')

# Specify input directory
utom.inputs.input = 's3://bucket/prefix/my-directory'

# Specify Mapbox tileset name
utom.inputs.tileset_name = 'buildings'

# Specify access token to upload
utom.inputs.token = 'put valid token here'

# Run gbdx workflow
wf = gbdx.Workflow([utom])
wf.execute()
```

In order to be able to upload to your account, you need to create [a secret scope token](https://www.mapbox.com/studio/account/tokens/).

If there are more than one files in the specified location, then only one will be (arbitrarily) picked by the
task for upload.

If the task completes successfully, your tileset should be present in your account with the name specified
in the corresponding task input.


## Input ports

| Name  | Type |  Description | Required |
|-------|--------------|----------------|----------------|
| input | Directory | Contains input file. Acceptable file formats are tif and geojson. Size limits can be found at https://www.mapbox.com/api-documentation/#uploads. | True |
|tileset_name | String | The Mapbox tileset name. | True |
| token | String | The Mapbox upload token. | True |
| timeout | String | Upload timeout in seconds. Default is 600. | False |
| min_zoom | String | Minimum zoom level for vector tiles. Default is 0. | False |
| max_zoom | String | Maximum zoom level for vector tiles. Default is 14. | False |
| excluded_properties | String | Exclude named properties from all features in input geojson. Property names should be given in string separated by commas. Default is none. | False |
| criteria | String | Filtering criteria for feature properties in input geojson. Criteria should be separated by commas. The format is 'certainty >= 0.99,class == 'building''. Default is none. |
| full_detail | String | Detail in bits at max zoom level. Default is 12. | False |
| low_detail | String | Detail in bits at lower zoom levels. Default is 12. | False |

## Output ports

There are no output ports.

## Development

### Build the Docker image

You need to install [Docker](https://docs.docker.com/engine/installation/).

Clone the repository:

```bash
git clone https://github.com/digitalglobe/upload-to-mapbox
```

Then:

```bash
cd upload-to-mapbox
docker build -t upload-to-mapbox .
```

### Try out locally

Create a container in interactive mode and mount the sample input under `/mnt/work/input/`:

```bash
docker run -v full/path/to/sample-input:/mnt/work/input -it upload-to-mapbox
```

Then, within the container:

```bash
python /upload-to-mapbox.py
```

Confirm that the tileset is present in your account. You can also check the following link

```bash
https://api.mapbox.com/v4/MAP_ID/page.html?access_token=<YOUR ACCESS TOKEN>
```

where MAP_ID is `yourmapboxusername.tileset_name`. Note that this link will work only if the tileset is made public.

### Docker Hub

Login to Docker Hub:

```bash
docker login
```

Tag your image using your username and push it to DockerHub:

```bash
docker tag upload-to-mapbox yourusername/upload-to-mapbox
docker push yourusername/upload-to-mapbox
```

The image name should be the same as the image name under containerDescriptors in upload-to-mapbox.json.

Alternatively, you can link this repository to a [Docker automated build](https://docs.docker.com/docker-hub/builds/).
Every time you push a change to the repository, the Docker image gets automatically updated.

### Register on GBDX

In a Python terminal:

```python
import gbdxtools
gbdx = gbdxtools.Interface()
gbdx.task_registry.register(json_filename='upload-to-mapbox.json')
```

Note: If you change the task image, you need to reregister the task with a higher version number
in order for the new image to take effect. Keep this in mind especially if you use Docker automated build.
