import uuid
import boto3
from os.path import basename
from pyworks_medialibrary.config import config
from pyworks_medialibrary.interfaces import StorageInterface


class AWSS3Storage(StorageInterface):

    def __init__(self, disk) -> None:
        self.storage = boto3.resource('s3')
        self.bucket_name = disk

    def disk(self, name):
        """Load disk"""
        pass

    def put(self):
        """Put file"""
        pass

    def put_image(self, file_path):
        """Put image file only"""
        try:
            file_content = open(file_path, 'rb')
            file_name = basename(file_path)
            self.storage.Bucket(self.bucket_name).upload_fileobj(
                Fileobj=file_content,
                Key=file_name,
                ExtraArgs={'ACL': 'public-read', 'ContentType': 'image/png'}
            )
            return self.url(file_name=file_name)
        except:
            return None

    def put_image_base64(self):
        """Put image from base64"""
        pass

    def delete(self):
        """Delete one file"""
        pass
    
    def get(self):
        """Get file info"""
        pass

    def url(self, file_name):
        """Return file link"""
        return f"https://{self.bucket_name}.s3.amazonaws.com/{file_name}"

    def copy(self):
        """Copy a file"""
        pass
    
    def copy_from_link(self):
        """Copy a file from link"""
        pass

    def move(self):
        """Move a file"""
        pass

    def exists(self):
        """Check file is exist"""
        pass

    def prepend(self):
        """Prepend data to file"""
        pass

    def append(self):
        """Append data to file"""
        pass