"""

A helper plugin for downloading executables from the internet to help other 
Plugins which might rely on external executables .

@NOTE remote urls may be tarballs/zips
"""

class DownloadableExecutableUtility:
    """ A helper to help you handle those pesky executables for tools which you need to download """

    def __init(self, name, version, remote):
        """

        Parameters:
        -----------

        name (str) : the name of the executable 

        remote (str) : the remote path for the executable to be downloaded.

        """
        self.name = name
        self.url = remote 

        self.local_path = '' 

        def path(self) -> str:
            """ return a path to a local downloaded bin """
            if not self.local_path:


            return self.local_path
