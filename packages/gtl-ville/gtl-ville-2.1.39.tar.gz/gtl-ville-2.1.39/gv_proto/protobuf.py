#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import asyncio
from concurrent.futures import ProcessPoolExecutor
import json

import pandas as pd
import shapely.wkt

from gv_proto.proto.archivist_pb2 import DataQuality, Indicators, LocationData, ZonesTravelTime
from gv_proto.proto.geographer_pb2 import FreeflowSpeeds, Locations, Mapping
from gv_utils import csv, enums, geometry

ATT = enums.AttId.att
DATATYPE_EID = enums.AttId.datatypeeid
EID = enums.AttId.eid
GEOM = enums.AttId.geom
WEBATT = enums.AttId.webatt


async def encode_indicators(indicators):
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as executor:
        indicators = await loop.run_in_executor(executor, _encode_indicators, indicators)
    return Indicators(indicators=indicators)


def _encode_indicators(indicators):
    try:
        bdata = csv.dumps_indicators(indicators)
    except:
        bdata = b''
    return bdata


def sync_decode_indicators(pbindicators):
    return _decode_indicators(pbindicators.indicators)


async def decode_indicators(pbindicators):
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as executor:
        indicators = await loop.run_in_executor(executor, _decode_indicators, pbindicators.indicators)
    return indicators


def _decode_indicators(indicators):
    try:
        indicators = csv.loads_indicators(indicators)
    except:
        indicators = pd.DataFrame()
    return indicators


async def encode_data_quality(dataquality):
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as executor:
        dataquality = await loop.run_in_executor(executor, _encode_data_quality, dataquality)
    return DataQuality(dataquality=dataquality)


def _encode_data_quality(dataquality):
    return __encode_json(dataquality)


async def decode_data_quality(pbdataquality):
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as executor:
        dataquality = await loop.run_in_executor(executor, _decode_data_quality, pbdataquality.dataquality)
    return dataquality


def sync_decode_data_quality(pbdataquality):
    return _decode_data_quality(pbdataquality.dataquality)


def _decode_data_quality(dataquality):
    return __decode_json(dataquality)


async def encode_location_data(locationdata):
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as executor:
        bdata = await loop.run_in_executor(executor, _encode_location_data, locationdata)
    return LocationData(locationdata=bdata)


def _encode_location_data(locationdata):
    return __encode_json(locationdata)


async def decode_location_data(pblocationdata):
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as executor:
        locationdata = await loop.run_in_executor(executor, _decode_location_data, pblocationdata.locationdata)
    return locationdata


def sync_decode_location_data(pblocationdata):
    return _decode_zones_travel_time(pblocationdata.locationdata)


def _decode_location_data(locationdata):
    return __decode_json(locationdata)


async def encode_zones_travel_time(traveltimes):
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as executor:
        bdata = await loop.run_in_executor(executor, _encode_zones_travel_time, traveltimes)
    return ZonesTravelTime(traveltimes=bdata)


def _encode_zones_travel_time(traveltimes):
    return __encode_json(traveltimes)


async def decode_zones_travel_time(pbtraveltimes):
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as executor:
        traveltimes = await loop.run_in_executor(executor, _decode_zones_travel_time, pbtraveltimes.traveltimes)
    return traveltimes


def sync_decode_zones_travel_time(pbtraveltimes):
    return _decode_zones_travel_time(pbtraveltimes.traveltimes)


def _decode_zones_travel_time(traveltimes):
    return __decode_json(traveltimes)


def __encode_json(data):
    try:
        bdata = json.dumps(data).encode(csv.ENCODING)
    except:
        bdata = b''
    return bdata


def __decode_json(bdata):
    return json.loads(bdata.decode(csv.ENCODING))


async def encode_locations(locations):
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as executor:
        pblocations = await loop.run_in_executor(executor, _encode_locations, locations)
    return pblocations


def _encode_locations(locations, pblocations=None):
    if pblocations is None:
        pblocations = Locations()
    for eid, loc in locations.items():
        geom = loc[GEOM]
        if isinstance(geom, str):
            geom = shapely.wkt.loads(geom)
        pblocations.locations[eid].geom = geom.wkb
        pblocations.locations[eid].att.FromJsonString(json.dumps(loc.get(ATT, {})))
        pblocations.locations[eid].webatt.FromJsonString(json.dumps(loc.get(WEBATT, {})))
        pblocations.locations[eid].datatype = loc.get(DATATYPE_EID, '')
    return pblocations


def sync_decode_locations(response):
    return _decode_locations(response.locations)


async def decode_locations(pblocations):
    loop = asyncio.get_event_loop()
    locations = await loop.run_in_executor(None, _decode_locations, pblocations.locations)
    return locations


def _decode_locations(pblocations):
    locations = {}
    for eid in pblocations:
        loc = pblocations[eid]
        locations[eid] = {EID: eid, GEOM: geometry.decode_geometry(loc.geom),
                          ATT: json.loads(loc.att.ToJsonString()), WEBATT: json.loads(loc.webatt.ToJsonString()),
                          DATATYPE_EID: loc.datatype}
    return locations


async def encode_mapping(mapping, validat):
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as executor:
        pbmapping = await loop.run_in_executor(executor, _encode_mapping, mapping, validat)
    return pbmapping


def _encode_mapping(mapping, validat):
    pbmapping = Mapping()
    for fromeid, toeidsorlocations in mapping.items():
        if not isinstance(toeidsorlocations, dict):
            pbmapping.mapping[fromeid].eids.eids.extend(toeidsorlocations)
        else:
            _encode_locations(toeidsorlocations, pbmapping.mapping[fromeid].locations)
    pbmapping.validat.FromSeconds(validat)
    return pbmapping


async def decode_mapping(pbmapping):
    loop = asyncio.get_event_loop()
    mapping = await loop.run_in_executor(None, _decode_mapping, pbmapping.mapping)
    return mapping, pbmapping.validat.ToSeconds()


def _decode_mapping(pbmapping):
    mapping = {}
    for eid in pbmapping:
        if pbmapping[eid].HasField('eids'):
            mapping[eid] = pbmapping[eid].eids.eids
        else:
            mapping[eid] = _decode_locations(pbmapping[eid].locations.locations)
    return mapping


async def encode_ffspeeds(eidsffspeeds):
    return FreeflowSpeeds(freeflowspeeds=eidsffspeeds)


async def decode_ffspeeds(pbffspeeds):
    return dict(pbffspeeds.freeflowspeeds)
