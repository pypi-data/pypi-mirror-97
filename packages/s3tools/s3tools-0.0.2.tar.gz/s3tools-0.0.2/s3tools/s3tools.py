import boto3
import os
import glog as log
from concurrent.futures import ThreadPoolExecutor, as_completed


class Profile:
    """Setting up your boto3 resource profile if you have credentials under ~/.aws/credentials. 
    """

    def __init__(self, var=None):
        self.s3session = var

    @property
    def s3session(self):
        return self.__s3session

    @s3session.setter
    def s3session(self, var):
        if var == None:
            if len(boto3.Session().available_profiles):
                profiles = {ix: p for ix, p in enumerate(boto3.session.Session().available_profiles, 1)}
                log.info('\nList of available profiles: \n' + '\n'.join([f'\t{k}: {v}' for k, v in profiles.items()]))
                profile_index = input("Which profile: ")
                self.__s3session = boto3.Session(profile_name=profiles[int(profile_index)]).resource('s3')
            else:
                log.info('No Session profiles found.')
                self.__s3session = boto3.Session().resource('s3')

    def listBuckets(self):
        return [b.name for b in list(self.s3session.buckets.all())]


class Bucket(Profile):
    def __init__(self, bucket_name, s3session=None):
        self.bucket_name = bucket_name
        super().__init__(s3session)

    def listObjects(self, filepath=None):
        """Get list of filepaths to objects in bucket_name, filepath

        Args:
            filepath (str): Path to folder. Default to None if all contents are to be listed.
        """
        try:
            if filepath == None:
                list_object_key = [obj.key for obj in list(self.s3session.Bucket(self.bucket_name).objects.all()) if obj.key[-1] != '/']
                log.info(f'-- Found {len(list_object_key)} objects in {self.bucket_name}/{filepath}')
            else:
                list_object_key = [obj.key for obj in list(self.s3session.Bucket(self.bucket_name).objects.filter(Prefix=filepath)) if obj.key[-1] != '/']
                log.info(f'-- Found {len(list_object_key)} objects in {self.bucket_name}/{filepath}')
            return(list_object_key)
        except Exception as e:
            log.error(f'-- Encountered error when locating objects in {self.bucket_name}/{filepath} -- {e}')
            return([])

    def downloadObject(self, filepath, dst_dir='.'):
        """Download from s3 Bucket

        Args:
            filepath (str): Path to file in s3 Bucket
            dst_dir (str): Path to download destination. Default to current working directory.
        """
        filename = os.path.basename(filepath)
        new_path = os.path.join(dst_dir, filename)
        try:
            self.s3session.Bucket(self.bucket_name).download_file(filepath, new_path)
            return({'file': filename, 'key': filepath, 'downloaded_to': new_path, 'status': 'success'})
        except Exception as e:
            log.error(f'-- Encountered error when downloading {filename} -- {e}')
            return({'file': filename, 'key': filepath, 'status': e})

    def uploadObject(self, filepath, dst_dir):
        """Upload to s3 Bucket

        Args:
            filepath (str): Path to local file that needs to be uploaded
            dst_dir (str): Path to s3 bucket
        """
        filename = os.path.basename(filepath)
        new_path = os.path.join(dst_dir, filename)
        try:
            self.s3session.Bucket(self.bucket_name).upload_file(filepath, new_path)
            return({'filename': filename, 'uploaded_to': new_path, 'status': 'success', 'url': f'https://{self.bucket_name}.s3.amazonaws.com/{new_path}'})
        except Exception as e:
            log.error(f'-- ERROR: For {filename} -- {e}')
            return({'filename': filename, 'status': e})

    def downloadObjectThread(self, list_items, dst_dir='.'):
        """Download from s3 Bucket with ThreadPoolExecutor

        Args:
            list_items (list): List of object paths in s3 Bucket
            dst_dir (str): Path to download destination. Default to current working directory.
        """
        list_results = []
        with ThreadPoolExecutor(max_workers=None) as executor:
            future_to_row = {executor.submit(self.downloadObject, item, dst_dir): item for item in list_items}
            for future in as_completed(future_to_row):
                results = future.result()
                list_results.append(results)
        return(list_results)

    def uploadObjectThread(self, list_items, dst_dir):
        """Upload to s3 Bucket with ThreadPoolExecutor

        Args:
            list_items (list): List of local file paths
            dst_dir (str): Path to s3 bucket
        """
        list_results = []
        with ThreadPoolExecutor(max_workers=None) as executor:
            future_to_row = {executor.submit(self.uploadObject, item, dst_dir): item for item in list_items}
            for future in as_completed(future_to_row):
                results = future.result()
                list_results.append(results)
        return(list_results)

    def copyObject(self, filepath, dst_dir, anotherBucket=None):
        """Copying objects between paths

        Args:
            filepath (str): Path to file in s3 Bucket
            dst_dir (str): Path to where file should be copied in s3 Bucket
            anotherBucket (str): Different bucket name. Default to None to move objects within same bucket.
        """
        filename = os.path.basename(filepath)
        try:
            if filename not in dst_dir:
                dst_dir = os.path.join(dst_dir, filename)
            copy_source = {'Bucket': self.bucket_name, 'Key': filepath}
            if anotherBucket != None:
                copy_source['Bucket'] = anotherBucket
            self.s3session.Bucket(self.bucket_name).copy(copy_source, dst_dir)
            return({'filename': filename, 'copied_to': dst_dir})
        except Exception as e:
            log.error(f'-- ERROR: For {filename} -- {e}')
            return({'filename': filename, 'status': e})
