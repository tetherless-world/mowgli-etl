from mowgli.lib.etl._pipeline import _Pipeline
from mowgli.lib.etl.webchild.webchild_extractor import webchildExtractor
from mowgli.lib.etl.webchild.webchild_transformer import webchildTransformer
import os


class webchildPipeline(_Pipeline):

    #helper function to gather csvs we want from entire webchild txt folder
    def getFiles():
        mList = os.listdir(os.getcwd()+ r'\WebChildData')
        return mList

    def __init__(self, *, **kwds):
        _Pipeline.__init__(
            self,
            extractor=webchildExtractor(),
            id="webchild",
            transformer=webchildTransformer(getFiles()),
            **kwds
        )
