import mapbox
import os
from gbdx_task_interface import GbdxTaskInterface
from time import sleep


class UploadToMapbox(GbdxTaskInterface):

    def invoke(self):

        # Get token
        token = self.get_input_string_port('token')
        os.environ['MAPBOX_ACCESS_TOKEN'] = token

        # Get tileset name
        tileset_name = self.get_input_string_port('tileset_name')

        # Get timeout (in seconds)
        timeout = int(self.get_input_string_port('timeout', default='300'))

        # Get input filename; if there are multiple files, pick one arbitrarily
        input_dir = self.get_input_data_port('input')
        filename = [os.path.join(dp, f) for dp, dn, fn in os.walk(input_dir) for f in fn][0]

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
