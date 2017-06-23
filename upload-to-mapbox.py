import mapbox
import os
import subprocess
from time import sleep

from gbdx_task_interface import GbdxTaskInterface


class UploadToMapbox(GbdxTaskInterface):

    def invoke(self):

        # Token
        token = self.get_input_string_port('token')
        os.environ['MAPBOX_ACCESS_TOKEN'] = token

        # Tileset name
        tileset_name = self.get_input_string_port('tileset_name')

        # Timeout (in seconds)
        timeout = int(self.get_input_string_port('timeout', default='600'))

        # The following string inputs apply only to vector tiles

        # Min zoom
        min_zoom = self.get_input_string_port('min_zoom', default='0')

        # Max zoom
        max_zoom = self.get_input_string_port('max_zoom', default='14')

        # Properties to be filtered
        filtered_properties = self.get_input_string_port('filtered_properties', default='').split(',')

        # Max detail at this zoom level
        full_detail = self.get_input_string_port('full_detail', default='')

        # Low detail at this zoom level
        low_detail = self.get_input_string_port('low_detail', default='')

        # Get input filename; if there are multiple files, pick one arbitrarily
        input_dir = self.get_input_data_port('input')
        filename = [os.path.join(dp, f) for dp, dn, fn in os.walk(input_dir) for f in fn if ('tif' in f or 'geojson' in f or 'json' in f)][0]

        if filename is None:
            print 'Invalid filename!'
            return 0

        # convert to mbtiles format if geojson
        if 'geojson' in filename:
            print 'Converting to mbtiles'
            prefix = filename.split('.geojson')[0]
            convert = 'tippecanoe -o {}.mbtiles -Z{} -z{}'.format(prefix, min_zoom, max_zoom)
            if filtered_properties:
                convert += ' ' + ' '.join(len(filtered_properties)*['-x {}']).format(*filtered_properties)
            if full_detail:
                convert += ' -d{}'.format(full_detail)
            if low_detail:
                convert += ' -D{}'.format(low_detail)

            convert += ' -l {} {}'.format(tileset_name, filename)
            proc = subprocess.Popen([convert], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = proc.communicate()
            filename = prefix + '.mbtiles'

        # Create mapbox uploader object
        service = mapbox.Uploader()

        print 'Send upload request'
        with open(filename, 'r') as src:
            upload_response = service.upload(src, tileset=tileset_name, name=tileset_name)
            if upload_response.status_code == 409:
                for i in range(5):
                    sleep(5)
                    with open(filename, 'r') as src:
                        upload_response = service.upload(src, mapid)
                        if upload_response.status_code != 409:
                            break

        if upload_response.status_code != 201:
            print 'Mapbox has not received upload request!'
            return 0

        # Poll the upload API to determine if upload has finished
        # using upload identifier from 201 response
        print 'Uploading'
        upload_id = upload_response.json()['id']
        for i in range(timeout/5):
            status_response = service.status(upload_id).json()
            if status_response['complete']:
                break
            sleep(5)

        if tileset_name not in status_response['tileset']:
            print 'Upload unsuccessful!'
            return 0

        # Now delete completed upload status from upload listing
        print 'Delete upload listing'
        delete_response = service.delete(upload_id)
        for i in range(5):
            if delete_response.status_code == 204:
                break
            else:
                sleep(5)
                delete_response = service.delete(upload_id)


if __name__ == "__main__":
    with UploadToMapbox() as task:
        response = task.invoke()

    if response:
        print 'Done!'
