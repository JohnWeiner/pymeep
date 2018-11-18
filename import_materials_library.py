import os
import urllib.request

def download_material_library(folderpath):
    # Download materials library directly from online repository.
    module_name = 'materials_library.py'
    url = ('https://github.com/stevengj/meep/raw/master/python/examples/' +
           module_name)
    filepath = os.path.join(folderpath, module_name)
    if not os.path.exists(filepath):
        try:
            content = urllib.request.urlopen(url).read()
        except urllib.request.URLError:
            print('Failed to download materials library.')
            raise
        with open(filepath, 'bw') as library_file:
            library_file.write(content)
