import os
import zipfile
from io import BytesIO

try:
    import ConfigParser as configparser
    from cStringIO import StringIO

except ImportError:
    import configparser
    from io import StringIO


class Resource(object):
    """A zip archive in the resources directory, located by
    supplying a resource category and name.

    Attributes:
      files (dict): Key is file name, value can be one of StringIO,
        BytesIO, or ConfigParser objects.

    """

    def __init__(self, resource_category, resource_name):
        """Load a resource ZIP using a category and zip name.

        Args:
          resource_category (str): E.g., tilesheets, walkabouts.
          resource_name (str): E.g., debug.

        """

        zip_path = os.path.join(
                                'resources',
                                resource_category,
                                resource_name + '.zip'
                               )
        files = {}

        with zipfile.ZipFile(zip_path) as zip_file:

            for file_name in zip_file.namelist():
                file_data = zip_file.open(file_name).read()

                try:
                    file_data = StringIO(file_data.decode('utf-8'))

                    # returns (file path, file extension)
                    if os.path.splitext(file_name)[1] == '.ini':
                        config = configparser.ConfigParser()

                        # NOTE: this still works in python 3, though it was
                        # replaced by config.read_file()
                        config.readfp(file_data)
                        file_data = config

                except ValueError:
                    file_data = BytesIO(file_data)

                files[file_name] = file_data

        self.files = files

    def __getitem__(self, file_name):

        return self.files[file_name]
