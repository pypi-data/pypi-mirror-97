# Copyright 2020 Cognite AS

import os
from typing import *

from cognite.seismic._api.api import API
from cognite.seismic._api.utility import MaybeString, get_identifier
from google.protobuf.struct_pb2 import Struct

if not os.getenv("READ_THE_DOCS"):
    from cognite.seismic.protos.types_pb2 import CRS, GeoJson, Geometry, LineBasedRectangle, PositionQuery, Wkt
    from cognite.seismic.protos.v1.seismic_service_messages_pb2 import SegYSeismicRequest, SegYSeismicResponse


class FileSeismicAPI(API):
    def __init__(self, query, ingestion, metadata):
        super().__init__(query=query, ingestion=ingestion, metadata=metadata)

    def get_segy(
        self, *, id: Union[int, None] = None, external_id: MaybeString = None, seismic_store_id: Union[int, None] = None
    ) -> Iterable[SegYSeismicResponse]:
        """
        Get SEGY file

        Provide one of: the seismic id, the seismic external id, the seismic store id.

        Args:
            id (int | None): The id of the seismic to query
            external_id (str | None): The external id of the seismic to query
            seismic_store_id (int | None): The id of the seismic store to query

        Returns: SegYSeismicResponse: SEGY file
        """
        request = SegYSeismicRequest()
        if seismic_store_id:
            request.seismic_store_id = seismic_store_id
        else:
            request.seismic.MergeFrom(get_identifier(id, external_id))

        return (i for i in self.query.GetSegYFile(request, metadata=self.metadata))

    def get_segy_by_lines(
        self,
        *,
        id: Union[int, None] = None,
        external_id: MaybeString = None,
        seismic_store_id: Union[int, None] = None,
        top_left_inline: int,
        top_left_xline: int,
        bottom_right_inline: int,
        bottom_right_xline: int,
    ) -> Iterable[SegYSeismicResponse]:
        """
        Get a part of a SEGY file with data inside a given range of inlines and xlines

        Provide one of: the seismic id, the seismic external id, the seismic store id.

        Args:
            id (int | None): The id of the seismic to query
            external_id (str | None): The external id of the seismic to query
            seismic_store_id (int | None): The id of the seismic store to query
            top_left_inline (int | None): Top left inline.
            top_left_xline (int | None): Top left xline.
            bottom_right_inline (int | None): Bottom right inline.
            bottom_right_xline (int | None): Bottom right xline.

        Returns: SegYSeismicResponse: SEGY file
        """
        top_left = PositionQuery(iline=top_left_inline, xline=top_left_xline)
        bottom_right = PositionQuery(iline=bottom_right_inline, xline=bottom_right_xline)
        rectangle = LineBasedRectangle(top_left=top_left, bottom_right=bottom_right)
        request = SegYSeismicRequest(lines=rectangle)
        if seismic_store_id:
            request.seismic_store_id = seismic_store_id
        else:
            request.seismic.MergeFrom(get_identifier(id, external_id))

        return (i for i in self.query.GetSegYFile(request, metadata=self.metadata))

    def get_segy_by_geometry(
        self,
        *,
        id: Union[int, None] = None,
        external_id: MaybeString = None,
        seismic_store_id: Union[int, None] = None,
        crs: str = None,
        wkt: str = None,
        geo_json=None,
    ) -> Iterable[SegYSeismicResponse]:
        """
        Get a part of a SEGY file with data inside an arbitrary 2D polygon.

        Provide one of: the seismic id, the seismic external id, the seismic store id.
        Provide one of: wkt, geo_json.

        Args:
            id (int | None): The id of the seismic to query
            external_id (str | None): The external id of the seismic to query
            seismic_store_id (int | None): The id of the seismic store to query
            crs (str): CRS
            wkt (str): polygon in WKT format
            geo_json (dict): polygon in geoJson format

            Returns: SegYSeismicResponse: SEGY file
        """
        self._verify_input(crs, wkt, geo_json)
        if geo_json:
            geo_json_struct = Struct()
            geo_json_struct.update(geo_json)
            geo = Geometry(crs=CRS(crs=crs), geo=GeoJson(json=geo_json_struct))
        else:
            geo = Geometry(crs=CRS(crs=crs), wkt=Wkt(geometry=wkt))
        request = SegYSeismicRequest(polygon=geo)
        if seismic_store_id:
            request.seismic_store_id = seismic_store_id
        else:
            request.seismic.MergeFrom(get_identifier(id, external_id))

        return (i for i in self.query.GetSegYFile(request, metadata=self.metadata))

    @staticmethod
    def _verify_input(crs: str = None, wkt: str = None, geo_json: str = None):
        if not crs:
            raise Exception("CRS is required")
        if not wkt and not geo_json:
            raise Exception("Either `wkt` or `geo_json` needs to be specified")
        if wkt and geo_json:
            raise Exception("Only `wkt` or `geo_json` should be specified")
