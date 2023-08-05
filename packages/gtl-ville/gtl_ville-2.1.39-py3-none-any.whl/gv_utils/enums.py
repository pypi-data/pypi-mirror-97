#!/usr/bin/env python3


class AttId:
    att = 'att'
    centerxy = 'centerxy'
    datapointeid = 'datapointeid'
    datapointseids = 'datapointseids'
    datatypeeid = 'datatypeeid'
    eid = 'eid'
    ffspeed = 'ffspeed'
    fow = 'fow'
    frc = 'frc'
    fromno = 'fromno'
    geom = 'geom'
    geomxy = 'geomxy'
    id = 'id'
    length = 'length'
    mainroad = 'mainroad'
    maxspeed = 'maxspeed'
    name = 'name'
    nlanes = 'nlanes'
    no = 'no'
    roadeid = 'roadeid'
    roads = 'roads'
    tono = 'tono'
    sample = 'sample'
    validfrom = 'validfrom'
    validto = 'validto'
    webatt = 'webatt'
    zoneeid = 'zoneeid'


class CsvData:
    samples = 'samples'
    timestamp = 'timestamp'

    confidence = 'confidence'
    density = 'density'
    flow = 'flow'
    fluidity = 'fluidity'
    occupancy = 'occupancy'
    speed = 'speed'
    status = 'status'
    traveltime = 'traveltime'


class DataTypeId:
    gka = 'gka'
    karrusrd = 'karrusrd'
    metropme = 'metropme'
    zonepoints = 'zonepoints'
    roads = 'roads'
    tomtomfcd = 'tomtomfcd'
    zones = 'zones'

    dataquality = 'dataquality'
    datapoints = 'datapoints'
    mappingroadsdatapoints = 'mappingroadsdatapoints'
    zonestraveltime = 'zonestraveltime'

    imputedprefixe = 'imputed'


class NetworkObjId:
    datapointsroadsmap = 'datapointsroadsmap'
    frcroadsmap = 'frcroadsmap'
    lonlatnodesmatrix = 'lonlatnodesmatrix'
    mainclustersgeom = 'mainclustersgeom'
    newdpmappings = 'newdpmappings'
    newzonemappings = 'newzonemappings'
    omiteddatapoints = 'omiteddatapoints'
    roadclustermap = 'roadclustermap'
    roadsdatamap = 'roadsdatamap'
    roadsffspeedmap = 'roadsffspeedmap'
    roadszonesmap = 'roadszonesmap'
    voronoiroadmap = 'voronoiroadmap'
    zonesdatamap = 'zonesdatamap'


INDICATORS_DATA_TYPES = (DataTypeId.karrusrd, DataTypeId.metropme, DataTypeId.tomtomfcd, DataTypeId.roads,
                         DataTypeId.zones)

MISSING_VALUE = -1
NO_VALUE = ''
