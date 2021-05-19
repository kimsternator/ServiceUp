from google.cloud import storage

BUCKET_NAME = 'service-up-312720.appspot.com'
PATH_TO_KEY = 'key.json'
IMAGE_LINK_BASE = 'http://storage.googleapis.com/service-up-312720.appspot.com/{}'

class ImageUpload:
    def upload(self, file, curr_name, new_name):
        storage_client = storage.Client.from_service_account_json(PATH_TO_KEY)
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(new_name)
        blob.upload_from_file(file, content_type='image/jpeg')

        link = IMAGE_LINK_BASE.format(new_name)
        print(
            "File {} uploaded to {} with link: {}.".format(
                curr_name, new_name, link
            )
        )
        return link
    
    def get_blobs(self):
        storage_client = storage.Client()
        blobs = storage_client.bucket(BUCKET_NAME).list_blobs()
        return blobs
    
    def get_link(self, blob):
        storage_client = storage.Client()
        return IMAGE_LINK_BASE.format(blob.name)

if __name__ == '__main__': 
    up = ImageUpload()
    for i in up.get_blobs():
        print(up.get_link(i))