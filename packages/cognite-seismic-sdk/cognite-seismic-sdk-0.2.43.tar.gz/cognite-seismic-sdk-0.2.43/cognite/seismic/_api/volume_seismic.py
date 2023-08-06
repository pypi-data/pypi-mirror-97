# Copyright 2019 Cognite AS

import os
from typing import *

import numpy as np
from cognite.seismic._api.api import API
from cognite.seismic._api.utility import Direction, LineRange, MaybeString, get_identifier, get_search_spec
from cognite.seismic.data_classes.api_types import RangeInclusive, Trace, VolumeDef

try:
    from tqdm.auto import tqdm
except ImportError:
    tqdm = None

if not os.getenv("READ_THE_DOCS"):
    from cognite.seismic.protos.types_pb2 import GeoJson
    from cognite.seismic.protos.types_pb2 import Geometry as GeometryProto
    from cognite.seismic.protos.types_pb2 import LineDescriptor, Wkt
    from cognite.seismic.protos.v1.seismic_service_datatypes_pb2 import LineBasedVolume, OptionalMap
    from cognite.seismic.protos.v1.seismic_service_messages_pb2 import (
        VolumeRequest,
        SearchSeismicStoresRequest,
        SearchSeismicsRequest,
    )
    from google.protobuf.wrappers_pb2 import Int32Value as i32
    from google.protobuf.wrappers_pb2 import StringValue
else:
    from cognite.seismic._api.shims import LineDescriptor


class ArrayData(NamedTuple):
    """Encapsulates the array returned from :py:meth:`VolumeSeismicAPI.get_array`, along with metadata about coordinates.

    Attributes:
        volume_data: 3D Array containing the requested volume data
        crs: The coordinate system used
        coord_x: 2D array containing the x coordinate of each (inline, xline) pair
        coord_y: 2D array containing the y coordinate of each (inline, xline) pair
        inline_range: The range of inline ids described by the first dimension of the array
        xline_range: The range of xline ids described by the second dimension of the array
        z_range: The range of depth indices described by the third dimension of the array
        """

    volume_data: np.ma.MaskedArray
    crs: str
    coord_x: np.ma.MaskedArray
    coord_y: np.ma.MaskedArray
    inline_range: RangeInclusive
    xline_range: RangeInclusive
    z_range: RangeInclusive

    def __repr__(self) -> str:
        return (
            f"ArrayData(volume_data=<array of shape {self.volume_data.shape}>, "
            f"crs={repr(self.crs)}, "
            f"coord_x=<array of shape {self.coord_x.shape}>, "
            f"coord_y=<array of shape {self.coord_x.shape}>, "
            f"inline_range={repr(self.inline_range)}, "
            f"xline_range={repr(self.xline_range)}, "
            f"z_range={repr(self.z_range)})"
        )


class VolumeSeismicAPI(API):
    def __init__(self, query, ingestion, metadata):
        super().__init__(query=query, ingestion=ingestion, metadata=metadata)

    def get_volume(
        self,
        *,
        id: Optional[int] = None,
        external_id: MaybeString = None,
        seismic_store_id: Optional[int] = None,
        inline_range: Optional[LineRange] = None,
        xline_range: Optional[LineRange] = None,
        z_range: Optional[LineRange] = None,
        include_trace_header: bool = False,
    ) -> Iterable[Trace]:
        """Retrieve traces from a seismic or seismic store

        Provide one of: the seismic id, the seismic external id, the seismic store id.
        The line ranges are specified as tuples of either (start, end) or (start, end, step).
        If a line range is not specified, the maximum ranges will be assumed.

        Args:
            id (int | None): The id of the seismic to query
            external_id (str | None): The external id of the seismic to query
            seismic_store_id (int | None): The id of the seismic store to query
            inline_range ([int, int] | [int, int, int] | None): The inline range
            xline_range ([int, int] | [int, int, int] | None): The xline range
            z_range ([int, int] | [int, int, int]): The zline range
            include_trace-header (bool): Whether to include trace header info in the response.

        Returns:
            Iterable[:py:class:`~cognite.seismic.data_classes.api_types.Trace`]: The traces for the specified volume
        """
        inline = into_line_range(inline_range)
        xline = into_line_range(xline_range)
        zline = into_line_range(z_range)
        lbs = LineBasedVolume(iline=inline, xline=xline, z=zline)
        req = VolumeRequest(volume=lbs, include_trace_header=include_trace_header)
        if seismic_store_id:
            req.seismic_store_id = seismic_store_id
        else:
            req.seismic.MergeFrom(get_identifier(id, external_id))

        for proto in self.query.GetVolume(req, metadata=self.metadata):
            yield Trace.from_proto(proto)

    # Refuse to allocate arrays larger than this
    # FIXME(audunska): Figure out the right limit here, or maybe just use numpy's memory limit
    ARR_LIM = 1e8

    def get_array(
        self,
        *,
        id: Optional[int] = None,
        external_id: MaybeString = None,
        seismic_store_id: Optional[int] = None,
        inline_range: Optional[LineRange] = None,
        xline_range: Optional[LineRange] = None,
        z_range: Optional[LineRange] = None,
        progress: Optional[bool] = False,
    ) -> ArrayData:
        """Store traces from a seismic or seismic store into a numpy array

        Provide one of: the seismic id, the seismic external id, the seismic store id.
        The line ranges are specified as tuples of either (start, end) or (start, end, step).
        If a line range is not specified, the maximum ranges will be assumed.

        Args:
            id (int | None): The id of the seismic to query
            external_id (str | None): The external id of the seismic to query
            seismic_store_id (int | None): The id of the seismic store to query
            inline_range ([int, int] | [int, int, int] | None): The inline range
            xline_range ([int, int] | [int, int, int] | None): The xline range
            z_range ([int, int] | [int, int, int]): The zline range
            progress: (bool): If set to true, display a progress bar. Default: False

        Returns:
            An :py:class:`~ArrayData` object encapsulating the retrieved array (see below)
        """

        z_size = None
        # Fetch the corresponding VolumeDef
        if seismic_store_id:
            spec = get_search_spec(id=seismic_store_id)
            req = SearchSeismicStoresRequest(seismic_store=spec)
            req.include_volume_definitions = True
            req.include_headers = True
            [store] = self.query.SearchSeismicStores(req, metadata=self.metadata)
            volumedef = VolumeDef.from_proto(store.inline_volume_def)
            z_size = volumedef.parsed.get("sample_count")
            if z_size is None and store.binary_header is not None:
                z_size = store.binary_header.samples
        else:
            spec = get_search_spec(id, external_id)
            req = SearchSeismicsRequest(seismic=spec)
            req.include_volume_definition = True
            req.include_binary_header = True
            [seismic] = self.query.SearchSeismics(req, metadata=self.metadata)
            volumedef = VolumeDef.from_proto(seismic.volume_def)
            z_size = volumedef.parsed.get("sample_count")
            if z_size is None and seismic.binary_header is not None:
                z_size = seismic.binary_header.samples

        # Compute optimal ranges
        if inline_range is None:
            inline_res = volumedef.common_inline_range()
        else:
            inline_res = RangeInclusive.from_linerange(inline_range)
        if xline_range is None:
            xline_res = volumedef.common_xline_range()
        else:
            xline_res = RangeInclusive.from_linerange(xline_range)
        inline_size = len(inline_res)
        xline_size = len(xline_res)
        if z_range is not None:
            z_res = RangeInclusive.from_linerange(z_range)
            z_size = len(z_res)
        elif z_size is not None:
            z_res = RangeInclusive(0, z_size - 1)
        else:
            z_res = None

        def alloc(z_size):
            if inline_size * xline_size * z_size > self.ARR_LIM:
                raise ValueError(
                    f"Array of size ({inline_size},{xline_size},{z_size}) has more than {self.ARRAY_LIM} elements. Consider restricting the array using inline_range etc."
                )
            return np.ma.masked_all((inline_size, xline_size, z_size), dtype="float")

        if z_size is not None:
            volume_data = alloc(z_size)

        crs = None
        coord_x = np.ma.masked_all((inline_size, xline_size), dtype="float")
        coord_y = np.ma.masked_all((inline_size, xline_size), dtype="float")
        # Fetch data
        traces = self.get_volume(
            id=id,
            external_id=external_id,
            seismic_store_id=seismic_store_id,
            inline_range=inline_range,
            xline_range=xline_range,
            z_range=z_range,
            include_trace_header=False,
        )
        if progress:
            if tqdm is None:
                raise Exception("progress=True requires the tqdm package. Install with 'pip install tqdm'.")
            # Due to SBS-3251, the number of traces streamed is > inline_size*xline_size:
            traces = tqdm(
                traces,
                total=volumedef.count_total_traces(
                    (inline_res.start, inline_res.stop), (xline_res.start, xline_res.stop)
                ),
            )
        for trace in traces:
            if z_size is None:
                z_size = len(trace.trace)
                z_res = RangeInclusive(0, z_size - 1)
                # Now we know the trace length, so allocate
                volume_data = alloc(z_size)

            # TODO: This slicing should go away once SBS-3251 is fixed
            trace_slice = trace.trace[:: z_res.step]
            if len(trace_slice) != z_size:
                raise Exception(f"Trace length {len(trace.trace)} incompatible with {z_res}")
            try:
                inline_ind = inline_res.index(trace.inline)
                xline_ind = xline_res.index(trace.xline)
            # TODO: This exception-catching should not be necessary once SBS-3251 is fixed
            except ValueError as e:
                if "incompatible" in e.args[0]:
                    continue
                else:
                    raise
            volume_data[inline_ind, xline_ind, :] = trace_slice
            if crs is None:
                crs = trace.coordinate.crs
            elif trace.coordinate.crs != crs:
                raise Exception("Incompatible coordinate systems between traces")
            coord_x[inline_ind, xline_ind] = trace.coordinate.x
            coord_y[inline_ind, xline_ind] = trace.coordinate.y
        return ArrayData(
            volume_data=volume_data,
            crs=crs,
            coord_x=coord_x,
            coord_y=coord_y,
            inline_range=inline_res,
            xline_range=xline_res,
            z_range=z_res,
        )


def into_line_range(linerange: Optional[LineRange]) -> LineDescriptor:
    "Converts a tuple of two or three values into a LineDescriptor"
    if linerange is None:
        return None
    if len(linerange) == 2:
        start, stop = linerange
        return LineDescriptor(min=i32(value=start), max=i32(value=stop))
    if len(linerange) == 3:
        start, stop, step = linerange
        return LineDescriptor(min=i32(value=start), max=i32(value=stop), step=i32(value=step))
    raise Exception("A line range should be None, (int, int), or (int, int, int).")
