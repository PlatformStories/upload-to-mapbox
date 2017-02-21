# upload-to-mapbox

A GBDX task that uploads raster or vector files to [Mapbox Studio](https://www.mapbox.com/mapbox-studio/).
You need a Mapbox Studio account in order to use this task.
Acceptable file formats and size limits can be found [here](https://www.mapbox.com/api-documentation/#uploads).
You can find an example of using upload-to-mapbox [here](http://gbdxstories.digitalglobe.com/osm-lulc/).

## Run

In a Python terminal:

```python
import gbdxtools
from os.path import join
import uuid

utom = gbdx.Task('upload-to-mapbox')

# Specify input directory
utom.inputs.input = 's3://bucket/prefix/my-directory'

# Specify Mapbox tileset name
utom.inputs.tileset_name = 'my-name'

# Specify access token to upload
utom.inputs.token = 'vkjxvkdfjnvdfkvndfnvkd'

# Run gbdx workflow
wf = gbdx.Workflow([utom])
wf.execute()
```

In order to be able to upload to your account, you need to create [a secret scope token](https://www.mapbox.com/studio/account/tokens/).

If the task completes successfully, your tileset should be present in your account with the name specified
in the corresponding task input.

## Input ports

| Name  | Type |  Description | Required |
|-------|--------------|----------------|----------------|
| input | Directory | Contains input file. Acceptable file formats and size limits can be found at https://www.mapbox.com/api-documentation/#uploads. | True |
|tileset_name | String | The Mapbox tileset name. | True |
| token | String | The Mapbox upload token. | True |

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
docker build -t yourusername/upload-to-mapbox .
```

Then push the image to Docker Hub:

```bash
docker push yourusername/upload-to-mapbox
```

The image name should be the same as the image name under containerDescriptors in upload-to-mapbox.json.

### Try out locally

Create a container in interactive mode and mount the sample input under `/mnt/work/input/`:

```bash
docker run -v full/path/to/sample-input:/mnt/work/input -it yourusername/upload-to-mapbox
```

Then, within the container:

```bash
python /upload-to-mapbox.py
```

Confirm that the tileset is present in your account. 


### Register on GBDX

In a Python terminal:

```python
import gbdxtools
gbdx = gbdxtools.Interface()
gbdx.task_registry.register(json_filename='upload-to-mapbox.json')
```

Note: If you change the task image, you need to reregister the task with a higher version number
in order for the new image to take effect.
