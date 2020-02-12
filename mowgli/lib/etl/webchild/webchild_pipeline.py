from _pipeline import _Pipeline
from mowgli.lib.webchild.webchild_extractor import webchildExtractor
from mowgli.lib.webchild.webchild_transformer import webchildTransformer
import os


class WebchildPipeline(_Pipeline):

    #helper function to gather csvs we want from entire webchild txt folder
    def get_files():
        os.chdir("../../../../Data/WebChildData")
        file_list = os.listdir(os.getcwd())
        return file_list

    def __init__(self):
        _Pipeline.__init__(
            self,
            extractor= webChildExtractor(csv_file_paths = get_files()),
            id="webchild",
            transformer=webchildTransformer(),
            **kwds
        )
 