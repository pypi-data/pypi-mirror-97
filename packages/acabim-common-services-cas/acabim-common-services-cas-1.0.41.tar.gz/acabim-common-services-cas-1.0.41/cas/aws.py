# noinspection PyUnresolvedReferences
import encodings.idna
import logging
import os
import shutil
import uuid
from enum import IntEnum, unique
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

from cas.concurrency import CallBackThread

_LOGGER = logging.getLogger('cas.model.file')
_BUCKET_NAME = os.getenv('AWS_CURRENT_BUCKET_NAME', 'acabim-testing')


@unique
class AwsFileType(IntEnum):
    CAP = 1  # do not change int values as they are in sync with the .NET clients
    LKM = 2
    LRML = 3
    IFC = 4
    RVT = 5
    BCF = 6
    CSV = 7
    PNG = 8
    PDF = 9
    JPEG = 10
    SVG = 11
    GLB = 12
    Custom = 0

    @property
    def default_file_format(self):
        return self.name.lower()


@unique
class AwsFileCategory(IntEnum):
    General = 0
    BuildingData = 1


class AwsFileDownloader:
    """This class is used to retrieve a file from the AWS S3. When this class goes out of scope, and is garbage
    collected, the downloaded file will automatically be removed from the temporary directory"""

    def __init__(self, file_name, file_type, file_category, auto_download=True, file_available_callback=None,
                 file_unavailable_callback=None):
        if file_available_callback is not None and not callable(file_available_callback):
            raise TypeError('expected callable function, not {0}'.format(type(file_available_callback)))

        if file_unavailable_callback is not None and not callable(file_unavailable_callback):
            raise TypeError('expected callable function, not {0}'.format(type(file_unavailable_callback)))

        self.file_name = file_name
        self.file_type = file_type
        self.file_category = file_category
        self.__download_thread = None
        self.__temp_folder = str(uuid.uuid4())
        self.__file_available_callback = file_available_callback
        self.__file_unavailable_callback = file_unavailable_callback

        _LOGGER.debug('Initialised S3 Access for IFC File "%s"', file_name)
        if auto_download:
            self.download_file()

    def __del__(self):
        self.__cleanup()

    def is_file_downloaded(self):
        return os.path.exists(self.get_local_file_path())

    def is_downloading(self):
        return self.__download_thread is None

    def get_local_file_path(self):
        return os.path.join(self.get_local_file_dir(), self.get_local_file_name())

    def get_local_file_name(self):
        return '{0}.{1}'.format(self.file_name, self.file_type.default_file_format)

    def get_local_file_dir(self):
        return self.__get_temp_path()

    def wait_for_download(self):
        if self.__download_thread is not None:
            self.__download_thread.join()

    def download_file(self):
        if not self.is_file_downloaded():
            if self.__download_thread is None:
                path = generate_bucket_path(self.file_category, self.file_type)
                bucket_path = '{0}.{1}'.format(os.path.join(path, self.file_name), self.file_type.default_file_format)
                file_path = self.get_local_file_path()
                self.__download_thread = CallBackThread(AwsFileDownloader.__download_impl, _BUCKET_NAME, bucket_path,
                                                        file_path, callback=self.__on_download_finished,
                                                        exception_callback=self.__on_download_exception,
                                                        retry_callback=self.__on_download_retry, retry_count=5)
                self.__download_thread.setName('cas_aws_file_dl:{0}'.format(self.file_name))
                self.__download_thread.daemon = True
                self.__download_thread.start()
                _LOGGER.debug('File download started for "%s"', self.file_name)
            else:
                _LOGGER.warning('File is already downloading')
        else:
            _LOGGER.debug('File is already downloaded')

    def __get_temp_path(self):
        folder_path = os.path.join(str(Path.home()), '.local', 'acabim-python', self.__temp_folder)
        if not os.path.exists(folder_path):
            _LOGGER.debug('Creating Path "%s"', folder_path)
            os.makedirs(folder_path)

        return folder_path

    def __on_download_finished(self):
        _LOGGER.info('File "%s" download complete', self.file_name)
        self.__download_thread = None
        if self.__file_available_callback is not None:
            self.__file_available_callback(self)

    def __on_download_exception(self, exception):
        self.__download_thread = None
        if self.__file_unavailable_callback is not None:
            self.__file_unavailable_callback(exception)
        else:
            _LOGGER.error(f'Unable to download file {self.file_name}')
            raise exception

    def __on_download_retry(self, attempt, exception):
        _LOGGER.warning(f'File download {attempt} failed: {str(exception)}')
        self.__cleanup()

    def __cleanup(self):
        _LOGGER.debug('Removing downloaded file "%s" (if available)', self.file_name)
        try:
            if self.is_file_downloaded():
                os.remove(self.get_local_file_path())

            shutil.rmtree(self.__get_temp_path(), ignore_errors=True)
        except OSError as e:
            _LOGGER.exception(e, 'Unable to cleanup data')

    @staticmethod
    def __download_impl(bucket_name, bk_path, f_path):
        _LOGGER.debug(f'Starting S3 File download from bucket {bucket_name} : Path: {bk_path}')
        _LOGGER.debug(f'Downloading to cache file path {f_path}')
        boto3.client('s3').download_file(Bucket=_BUCKET_NAME, Key=bk_path, Filename=f_path)


def upload_file(file_path, file_type, file_category):
    file_name = os.path.basename(file_path)
    obj_name = '{0}/{1}'.format(generate_bucket_path(file_category, file_type), file_name)
    try:
        boto3.client('s3').upload_file(file_path, _BUCKET_NAME, obj_name)
        _LOGGER.info('File %s uploaded to %s successfully', file_name, _BUCKET_NAME)
    except ClientError as e:
        _LOGGER.exception(e, 'Unable to upload file %s to bucket %s', file_path, _BUCKET_NAME)
        return False
    return True


def generate_bucket_path(file_category, file_type):
    if file_category is AwsFileCategory.General:
        return file_type.name
    else:
        return '{0}/{1}'.format(file_category.name, file_type.name)


if __name__ == '__main__':
    import cas.configure as c

    c.configure_logging()
    d = AwsFileDownloader('Linwood', AwsFileType.IFC, AwsFileCategory.BuildingData)
    d.wait_for_download()
