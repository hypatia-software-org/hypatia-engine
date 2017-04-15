import os

from hypatia import class_default, class_get

@class_default
class FilesystemResourcePack(class_get("ResourcePack")):
    def __init__(self, path):
        super().__init__()

        self._filesystem_path = path

        for root, dirs, files in os.walk(self._filesystem_path):
            _, _, actualroot = root.partition(self._filesystem_path)
            
            if actualroot != "":
                # we're not in the root directory, so mkdir this directory
                self.mkdir(actualroot)

            # get directory entry
            dirent = self._parse_tree_for_entry(actualroot)

            for file in files:
                newpath = os.path.join(root, file)
                with open(newpath, 'rb') as fh:
                    content = fh.read()
                    dirent['content'][file] = {
                        "type": "file",
                        "content": content,
                    }

