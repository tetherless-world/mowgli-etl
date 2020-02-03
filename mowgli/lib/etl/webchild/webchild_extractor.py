from mowgli.lib.etl._extractor import _Extractor

class webchildExtractor(_Extractor):
    
    def __init__(self, *, webchild_csv_file_paths:list, **kwds):
        _Extractor.__init__(self)
        self._webchild_memberof_csv_file_path = webchild_csv_file_paths[0]
        self._webchild_physical_csv_file_path = webchild_csv_file_paths[1]
        self._webchild_substanceof_csv_file_path = webchild_csv_file_paths[2]

    def extract(self, **kwds):
        self._logger.info("extract")
        return {"csv_file_paths: {0}\n{1}\n{2}\n".format(self._webchild_memberof_csv_file_path,self._webchild_physical_csv_file_path,self._webchild_substanceof_csv_file_path)}
        #implement extractor