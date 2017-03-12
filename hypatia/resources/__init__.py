from hypatia.resources.exceptions import *
from hypatia.resources.bytesio import BytesIO


PATHSEP = "/"
ROOT = "/"

class ResourcePack:
    def __init__(self):
        self.content = {"type": "dir", "content": {}}
        self._modified_since_last_save = []
    
    @staticmethod
    def normalize(path):
        """\
        Normalize a path, removing extraneous path separators and references
        to the current directory, as well as correctly handling '..'.
        """

        starts_with_root = False
        if path.startswith(ROOT): 
            path = path[len(ROOT):]
            starts_with_root = True


        steps = path.split(PATHSEP)

        # filter out empty steps (a // in path) and "."s 
        steps = [a for a in steps if a not in ["", "."]]

        # filter out ".." in path
        for i in range(len(steps)):
            if steps[i] == "..":
                # delete the ".."
                steps[i] = ""

                # and the thing preceding it
                if i > 0:
                    steps[i - 1] = ""

        steps = [a for a in steps if a != ""]

        return (ROOT if starts_with_root else '') + PATHSEP.join(steps) 

    def _parse_tree_for_entry(self, path):
        path = self.normalize(path)
        if path.startswith(ROOT): 
            path = path[len(ROOT):]

        parts = path.split(PATHSEP)

        # Return the root directory if there's no parts
        if len(parts) is 0 or (len(parts) is 1 and parts[0] == ''):
            return self.content

        current = self.content
        collected = []

        while True:
            part = parts.pop(0)

            # collect what parts of the path we've been through so we can
            # reconstruct the current path in the event of an error
            collected.append(part) 

            if part in current['content']:
                entry = current['content'][part]

                if entry['type'] == 'dir':
                    if len(parts) is 0:
                        return entry

                    current = entry

                elif entry['type'] == 'file':
                    if len(parts) is not 0:
                        raise NotADirectory(ROOT + PATHSEP.join(collected))

                    return entry

            else:
                raise FileNotFound(ROOT + PATHSEP.join(collected))

    def exists(self, path):
        try:
            self._parse_tree_for_entry(path)
            return True
        except FileNotFound: 
            return False

    def _update_file_contents(self, path, contents):
        path = self.normalize(path)
        entry = self._parse_tree_for_entry(path)

        if entry['type'] == 'dir':
            raise NotAFile(path)

        entry['content'] = contents
        self._modified_since_last_save.append(path)

    def open(self, path):
        path = self.normalize(path)
        entry = self._parse_tree_for_entry(path)

        if entry['type'] == 'dir':
            raise NotAFile(path)

        file = BytesIO(self, path, entry['content'])

        return file

    def mkdir(self, path):
        """\
        Create a directory at the given path.
        """

        path = self.normalize(path)
        if path.startswith(ROOT): 
            path = path[len(ROOT):]

        split = path.rsplit(PATHSEP, 1)

        if len(split) is 1:
            parent = ''
            newdir = split[0]

        else:
            parent = split[0]
            newdir = split[1]

        prevdir = self._parse_tree_for_entry(ROOT + parent)

        # sanity check
        if prevdir['type'] != 'dir':
            raise NotADirectory(parent)

        # check the new directory doesn't already exist

        if newdir in prevdir['content']:
            raise FileExists(path)

        prevdir['content'][newdir] = {
            'type': 'dir',
            'content': {},
        }
