from mowgli.lib.etl._extractor import _Extractor
import os

# I dont think I need this file

class webchildExtractor(_Extractor):
    
    def __init__(self, *, webchild_csv_file_paths:list, **kwds):
        _Extractor.__init__(self)
       