#!/usr/bin/env python3

import asyncio
import time
import traceback

from grpclib.client import Channel

from gv_proto import protobuf
from gv_proto.proto.broadcaster_pb2 import PubRequest, SubRequest
from gv_proto.proto.archivist_pb2 import DataQuality, Indicators, ZonesTravelTime, ZonesTravelTimeRequest
from gv_proto.proto.geographer_pb2 import Locations, LocationsRequest, Mapping, MappingRequest
from gv_proto.grpclib.interface_grpc import InterfaceStub
from gv_utils import enums
from gv_utils.asyncio import check_event_loop


DATA_TYPE_EID = enums.AttId.datatypeeid

METRO_PME = enums.DataTypeId.metropme
TOMTOM_FCD = enums.DataTypeId.tomtomfcd
KARRUS_RD = enums.DataTypeId.karrusrd

DATA_QUALITY = enums.DataTypeId.dataquality
DATA_POINTS = enums.DataTypeId.datapoints
MAPPING_ROADS_DATA_POINTS = enums.DataTypeId.mappingroadsdatapoints
ZONES_TRAVEL_TIME = enums.DataTypeId.zonestraveltime
IMPUTED_PREF = enums.DataTypeId.imputedprefixe


class Service:
    samplings = {KARRUS_RD: 1 * 60, METRO_PME: 1 * 60, TOMTOM_FCD: 1 * 60}

    def __init__(self, logger, futures=None, callbacks=None):
        if futures is None:
            futures = []
        if callbacks is None:
            callbacks = {}

        self.logger = logger
        self.futures = futures
        self.callbacks = callbacks
        self.interface = None
        self._channel = None
        self._mainfut = None

    async def async_init(self):
        pass

    def start(self, rpchost, rpcport):
        check_event_loop()  # will create a new event loop if needed (if we are not in the main thread)
        self.logger.info('RPC client is starting.')
        try:
            asyncio.run(self._run(rpchost, rpcport))
        except KeyboardInterrupt:
            pass
        self.logger.info('RPC client has stopped.')

    async def _run(self, rpchost, rpcport):
        try:
            self._channel = Channel(rpchost, rpcport)
            self.interface = InterfaceStub(self._channel)
            await self.async_init()
            self.logger.info('RPC client has started.')
            while True:
                try:
                    self._mainfut = asyncio.gather(
                        *self.futures,
                        *[self._subscribe(datatype, callback) for datatype, callback in self.callbacks.items()]
                    )
                    self._mainfut.add_done_callback(self._close)
                    await self._mainfut
                except KeyboardInterrupt:
                    self._cancel()
                except:
                    time.sleep(1)
                else:
                    time.sleep(1)
        except:
            self._close()

    def _close(self, _=None):
        if self._channel is not None:
            self._channel.close()
            self._channel = None

    def _cancel(self):
        if self._mainfut is not None:
            self._mainfut.cancel()
            self._mainfut = None

    async def _publish(self, data, datatype, datatimestamp):
        success = False
        try:
            originaldatatype = datatype
            datatype = self._is_message_prefixed(datatype)
            if datatype == DATA_POINTS:
                encode_func, args = self.__publish_data_points(data)
            elif datatype == MAPPING_ROADS_DATA_POINTS:
                encode_func, args = self.__publish_mapping_roads_data_points(data, datatimestamp)
            elif datatype in enums.INDICATORS_DATA_TYPES:
                encode_func, args = self.__publish_indicators(data)
            elif IMPUTED_PREF in datatype:
                encode_func, args = self.__publish_indicators(data)
            elif datatype == DATA_QUALITY:
                encode_func, args = self.__publish_data_quality(data)
            elif datatype == ZONES_TRAVEL_TIME:
                encode_func, args = self.__publish_zones_travel_time(data)
            else:
                raise Exception

            try:
                pbdata = await encode_func(*args)
            except:
                self.logger.error(traceback.format_exc())
                self.logger.error('An error occurred while encoding {}.'.format(originaldatatype))
            else:
                request = PubRequest(datatype=originaldatatype)
                request.data.Pack(pbdata)
                request.timestamp.FromSeconds(datatimestamp)
                response = await self.interface.publish(request)
                success = response.success
        except:
            self.logger.error(traceback.format_exc())
            self.logger.error('An error occurred while publishing {}.'.format(datatype))
        finally:
            return success

    @staticmethod
    def __publish_data_points(data):
        return protobuf.encode_locations, (data,)

    @staticmethod
    def __publish_mapping_roads_data_points(data, datatimestamp):
        return protobuf.encode_mapping, (data, datatimestamp)

    @staticmethod
    def __publish_indicators(data):
        return protobuf.encode_indicators, (data,)

    @staticmethod
    def __publish_data_quality(data):
        return protobuf.encode_data_quality, (data,)

    @staticmethod
    def __publish_zones_travel_time(data):
        return protobuf.encode_zones_travel_time, (data,)

    async def _subscribe(self, datatype, callback):
        async with self.interface.subscribe.open() as stream:
            await stream.send_message(SubRequest(datatype=datatype))
            self.logger.info('RPC client has subscribed to {} data.'.format(datatype))
            try:
                originaldatatype = datatype
                datatype = self._is_message_prefixed(datatype)
                if datatype == DATA_POINTS:
                    pbdata, decode_func = self.__subscribe_data_points()
                elif datatype == MAPPING_ROADS_DATA_POINTS:
                    pbdata, decode_func = self.__subscribe_mapping_roads_data_points()
                elif datatype in enums.INDICATORS_DATA_TYPES:
                    pbdata, decode_func = self.__subscribe_indicators()
                elif datatype == DATA_QUALITY:
                    pbdata, decode_func = self.__subscribe_data_quality()
                elif datatype == ZONES_TRAVEL_TIME:
                    pbdata, decode_func = self.__subscribe_zones_travel_time()
                else:
                    raise Exception

                async for response in stream:
                    self.logger.debug('Got new {} data.'.format(originaldatatype))
                    try:
                        response.Unpack(pbdata)
                        data = await decode_func(pbdata)
                    except:
                        self.logger.error(traceback.format_exc())
                        self.logger.error('An error occurred while decoding {} data.'.format(originaldatatype))
                    else:
                        asyncio.create_task(callback(data))
            finally:
                await stream.end()
                self.logger.info('RPC client has unsubscribed from {} data.'.format(datatype))

    @staticmethod
    def __subscribe_data_points():
        return Locations(), protobuf.decode_locations

    @staticmethod
    def __subscribe_mapping_roads_data_points():
        return Mapping(), protobuf.decode_mapping

    @staticmethod
    def __subscribe_indicators():
        return Indicators(), protobuf.decode_indicators

    @staticmethod
    def __subscribe_data_quality():
        return DataQuality(), protobuf.decode_data_quality

    @staticmethod
    def __subscribe_zones_travel_time():
        return ZonesTravelTime(), protobuf.decode_zones_travel_time

    @staticmethod
    def _is_message_prefixed(datatype):
        sep = '-'
        splited = datatype.split(sep)
        return datatype if splited[0] not in ('PAST', 'OFFLINE') else sep.join(splited[1:])

    async def _get_data_points(self, datapointeids=None, datatypeeid=None):
        lr = LocationsRequest()
        if datapointeids is not None:
            lr.eids.eids.extend(datapointeids)
        if datatypeeid is not None:
            lr.datatype = datatypeeid
        return await protobuf.decode_locations(await self.interface.get_data_points(lr))

    async def _get_zone_points(self):
        lr = LocationsRequest()
        return await protobuf.decode_locations(await self.interface.get_zone_points(lr))

    async def _get_zones_travel_time(self, frompointeid, topointeid, period, fromdatetime, todatetime=None):
        request = ZonesTravelTimeRequest(fromPoint=frompointeid, toPoint=topointeid, period=period)
        request.fromdate.FromSeconds(int(fromdatetime.timestamp()))
        if todatetime is not None:
            request.todate.FromSeconds(int(todatetime.timestamp()))
        return await protobuf.decode_zones_travel_time(await self.interface.get_zones_travel_time(request))

    async def _get_roads(self, roadeids=None):
        lr = LocationsRequest()
        if roadeids is not None:
            lr.eids.eids.extend(roadeids)
        return await protobuf.decode_locations(await self.interface.get_roads(lr))

    async def _get_mapping_roads_data_points(self):
        return (await protobuf.decode_mapping(await self.interface.get_mapping_roads_data_points(MappingRequest())))[0]

    @staticmethod
    def _get_data_type_eid_from_data_points(datapoints):
        datapointeid, datapoint = datapoints.popitem()
        datatype = datapoint[DATA_TYPE_EID]
        datapoints[datapointeid] = datapoint
        return datatype


def start(Application, threaded=False):
    if threaded:
        import threading
        threading.Thread(target=start, args=(Application, False), daemon=True).start()
        print('Starting application in a background thread...')
    else:
        Application()
