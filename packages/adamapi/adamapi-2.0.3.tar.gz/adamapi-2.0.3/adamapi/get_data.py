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


from datetime import timedelta, datetime, timezone
import os
import time
from osgeo import ogr
import imageio
import json
import requests
import errno
import csv

import logging
logger=logging.getLogger('adamapi')

from . import AdamApiError

class GetData(object):
    def __init__(self,client):
        self.LOG=logger
        self.client=client

    def getData(self,datasetId,startDate=None,endDate=None,**kwargs):
        """
        Method to retrive:
        1) the complete product
        2) a geographic subset of the product
        3) a timeseries on a point
        @datasetId required
        @startDate required for point 2 and 3, invalid for point 1
        @endDate required for point 2 and 3, invalid for point 1
        @outputFname optional
        @geometry invalid in the case 1 but required in the case 2 and 3
        @productid invalid in the case 2 and 3 but required in the case 1
        """
        params,fname=self.checkParams(datasetId,startDate,endDate,kwargs)
        if fname is None:
            self.LOG.error("Unprocessable requests with productId and geometry. Execute a request with only once of two params")
            raise AdamApiError( "Unprocessable requests with productId and geometry. Execute a request with only once of two params")
        self._checkDirFile(fname)
        if "productId" in params:
            url = os.path.join("apis","v2","opensearch",datasetId.split(":",1)[0],"records/",params["productId"]+"/","download")
            method = "GET"
            isorder=False
        if "geometry" in params:
            isorder=True
            method = "POST"
            try:
                geom = ogr.CreateGeometryFromJson(params["geometry"])
            except:
                geom = ogr.CreateGeometryFromJson(json.dumps(params["geometry"]))
            if geom.GetGeometryName() == "POINT":
                url = os.path.join("apis","v2","chart","order",datasetId.split(":",1)[0]+"/")
                is_timeseries=True
            else:
                is_timeseries=False
                url = os.path.join("apis","v2","subset","order",datasetId.split(":",1)[0]+"/")
        try:
            response_order = self.client.client(url,params,method,force_raise = True,enable_stream=False)
            response_order.raise_for_status()
            if isorder:
                if response_order.json()["status"] == "started":
                    status = self._checkStatus(response_order.json()["pk"])
                    if status == "completed":
                        if is_timeseries:
                            url_download = os.path.join("apis","v2","chart","order",str(response_order.json()["pk"]),"download")
                        else:
                            url_download = os.path.join("apis","v2","subset","order",str(response_order.json()["pk"]),"download")
                        try:
                            response_download = self.client.client(url_download,{},"GET",force_raise=True,enable_stream=True)
                            response_download.raise_for_status()
                            with open(fname,"wb") as f:
                                for chunk in response_download.iter_content(chunk_size=128):
                                    f.write(chunk)
                        except requests.exceptions.HTTPError as er:
                            raise AdamApiError( response_download.json())
                        except Exception as e:
                            self.LOG.exception("Un error occurd : %s"%(e))
                            raise AdamApiError( e )

                if status == "failed":
                    self.LOG.error("Failed request")
                    raise AdamApiError(status)
            else:
                with open( fname+".tif", 'wb' ) as f:
                    f.write( response_order.content )
        except requests.exceptions.HTTPError as er:
            raise AdamApiError(response_order.json())
        except Exception as e:
            self.LOG.exception("Un error occurd : %s"%(e))
            raise AdamApiError( e )

        return fname

    def checkParams(self,datasetId,start_date,end_date,kwargs):
        params={}
        fname=None
        op_kwargs = kwargs.copy()
        if "productId" in kwargs and "geometry" in kwargs:
            return params , None

        if "outputFname" in kwargs and kwargs["outputFname"] is not None:
            fname = kwargs["outputFname"]
            del(op_kwargs["outputFname"])
        else:
            fname="adamapiresults/%s"%(datasetId.split(":")[-1])

        for(key,value)in op_kwargs.items():
            if key == "geometry":
                if isinstance(value,str):
                    params[key]=value
                else:
                    params[key]=json.dumps(value)
            else:
                params[key]=value

        if "productId" not in kwargs:
            if start_date > end_date:
                raise AdamApiError("Invalid Temporal Filter: startDate > endDate")
            params["start_date"]=start_date
            params["end_date"]=end_date
        return params,fname

    def _checkStatus(self,oid,):
        """
        wrap /status/order
        """
        animation = "|/-\\"
        idx = 0
        params={}
        url = os.path.join("apis","v2","subset","order",str(oid),"status")
        status = "running"
        while status == "running":
            time.sleep(2)
            r = self.client.client(url,params,"GET",force_raise=True)
            status = r.json()["status"]
            if status == "running":
                print(animation[idx % len(animation)], end="\r")
                idx += 1
            else:
                break
        return status



    def _checkDirFile(self,filename):
        dirname = os.path.dirname( filename )
        if dirname.strip():
            try:
                os.makedirs( dirname )
            except OSError as ose:
                if ose.errno!=errno.EEXIST:
                    raise AdamApiError( ose )
