"""
Copyright (c) 2020 MEEO s.r.l.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import os
import logging
logger=logging.getLogger('adamapi')

from . import AdamApiError

class Datasets():
    def __init__(self, client):
        self.client = client
        self.LOG = logger

    def getDatasets( self, datasetId=None,**kwargs ):
        """
        getDataset convention:
        1. without parametes returns all datasets present over the adam endpoint;
        2. with datasetId paramenter returns a specific description of this dataset

        @  {ID:datasetId}: the datasetId
        @  page: Indicats a specific page
        @  maxRecords: Max number of results in output
        """
        params={ 'datasetId':datasetId }
        if 'page' in kwargs:
            params['page']=kwargs['page']
        else:
            params['page']=0
        if 'maxRecords' in kwargs:
            params['maxRecords']=kwargs['maxRecords']
        else:
            params['maxRecords']=10

        r = self.client.client( os.path.join( 'datasets', 'api', 'datasets' ), params, 'GET' )
        self.LOG.info( 'Datasets request executed' )
        response = r.json()
        if 'errors' in response:
            raise AdamApiError( response[ 'errors' ] )
        return response[ 'response' ]
