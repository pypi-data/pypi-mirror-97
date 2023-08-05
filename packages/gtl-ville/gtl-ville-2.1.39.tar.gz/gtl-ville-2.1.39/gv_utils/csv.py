#!/usr/bin/env python3

import io
import json
import os

from gv_utils import enums
import numpy as np
import pandas as pd
from pandas.api import types as pdtypes

ENCODING = 'utf8'
CSVSEP = ';'
TEMPCSVSEP = ','

SAMPLES = enums.CsvData.samples
TIMESTAMP = enums.CsvData.timestamp


def dumps_indicators(data):
    csvbuffer = io.BytesIO()
    if isinstance(data, dict):
        timestamp, samples = data[TIMESTAMP], data[SAMPLES]
        metrics = None
        for sampleid, sample in samples.items():
            if metrics is None:
                metrics = list(sample.keys())
                headers = [str(timestamp), ] + metrics
                csvbuffer.write(CSVSEP.join(headers).encode(ENCODING))
            csvbuffer.write(os.linesep.encode(ENCODING))
            values = [str(sampleid), ]
            for metric in metrics:
                value = sample.get(metric, '')
                if isinstance(value, float):
                    value = round(value)
                elif isinstance(value, dict):
                    value = __dump_json(value)
                if value == -1:
                    value = ''
                values.append(str(value))
            csvbuffer.write(CSVSEP.join(values).encode(ENCODING))
    else:
        data.fillna(-1, inplace=True)
        for col in data.columns:
            try:
                if pdtypes.is_numeric_dtype(data[col]):
                    data[col] = data[col].astype('int')
                else:
                    data[col] = data[col].map(__dump_json)
            except:
                pass
        data.replace(-1, '', inplace=True)
        data.to_csv(csvbuffer, sep=CSVSEP)
    csvdata = csvbuffer.getvalue()
    csvbuffer.close()
    return csvdata


def __dump_json(val):
    string = val
    try:
        string = json.dumps(val)
    except:
        pass
    return string


def loads_indicators(csvdata):
    dataframe = pd.read_csv(io.BytesIO(csvdata), sep=CSVSEP, index_col=0)
    for col in dataframe.columns:
        try:
            if not pdtypes.is_numeric_dtype(dataframe[col]):
                dataframe[col] = dataframe[col].map(__load_json)
        except:
            pass
    dataframe.replace(-1, np.NaN, inplace=True)
    dataframe.replace('-1', np.NaN, inplace=True)
    try:
        dataframe.index = dataframe.index.astype('str')
    except:
        pass
    return dataframe


def __load_json(string):
    val = string
    try:
        val = json.loads(string.replace('\'', '"'))
    except:
        pass
    return val


def dumps_zones_travel_time(dictdata, timestamp):
    csvbuffer = io.BytesIO()
    csvbuffer.write(CSVSEP.join([str(timestamp), 'tozonepointeid', 'traveltime', 'path']).encode(ENCODING))
    for fromzpeid, traveltimes in dictdata.items():
        csvbuffer.write(os.linesep.encode(ENCODING))
        for tozpeid, traveltime in traveltimes.items():
            traveltime, path = traveltime
            values = [str(fromzpeid), str(tozpeid)]
            if isinstance(traveltime, float):
                traveltime = round(traveltime)
            values.append(str(traveltime))
            values.append(path)
            csvbuffer.write(CSVSEP.join(values).encode(ENCODING))
    return csvbuffer
