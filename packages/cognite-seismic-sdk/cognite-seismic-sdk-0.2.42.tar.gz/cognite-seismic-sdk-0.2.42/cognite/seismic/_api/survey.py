# Copyright 2019 Cognite AS

import os
from typing import *

from cognite.seismic._api.api import API
from google.protobuf.struct_pb2 import Struct

if not os.getenv("READ_THE_DOCS"):

    from cognite.seismic.protos.ingest_service_messages_pb2 import (
        DeleteSurveyRequest,
        EditSurveyRequest,
        RegisterSurveyRequest,
    )
    from cognite.seismic.protos.query_service_messages_pb2 import (
        ListSurveysQueryRequest,
        MetadataFilter,
        SearchSurveyRequest,
        SurveyQueryRequest,
    )
    from cognite.seismic.protos.types_pb2 import CRS, CoverageParameters, GeoJson, Geometry, Wkt


class SurveyAPI(API):
    def __init__(self, query, ingestion, metadata):
        super().__init__(metadata=metadata, query=query, ingestion=ingestion)

    def get(
        self,
        survey_id: Optional[str] = None,
        survey_name: Optional[str] = None,
        list_files: bool = False,
        include_metadata: bool = False,
        crs: Optional[str] = None,
        in_wkt: Optional[bool] = None,
    ):
        """
        Get a survey by either id or name.
        Provide either crs or in_wkt to get survey coverage.

        Args:
            survey_id (str, optional): survey id.
            survey_name (str, optional): survey name.
            list_files (bool): true if the files from this survey should be listed.
            include_metadata (bool): true if metadata should be included in the response.
            crs: the crs in which the survey coverage is returned, default is original survey crs
            in_wkt: survey coverage format, set to true if wkt format is needed, default is geojson format

        Returns:
            GetSurveyResponse: the requested survey, its files and coverage (if requested).
        """
        survey = self.identify(survey_id, survey_name)
        coverageParamCrs = CRS(crs=crs) if crs is not None else None
        coverageParams = (
            CoverageParameters(crs=coverageParamCrs, in_wkt=in_wkt)
            if coverageParamCrs is not None or in_wkt is not None
            else None
        )
        req = SurveyQueryRequest(
            survey=survey, list_files=list_files, include_metadata=include_metadata, include_coverage=coverageParams
        )
        return self.query.GetSurvey(req, metadata=self.metadata)

    def list(self, list_files: bool = False, include_metadata: bool = False):
        """List all the surveys.

        Args:
            list_files (bool): true if the files from the surveys should be listed.
            include_metadata (bool): true if metadata should be included in the response.

        Returns:
            SurveyWithFilesResponse: the requested surveys and their files (if requested).
        """
        return self.query.ListSurveys(
            ListSurveysQueryRequest(list_files=list_files, include_metadata=include_metadata), metadata=self.metadata
        )

    @staticmethod
    def _verify_input(wkt: str = None, geo_json: str = None):
        if not wkt and not geo_json:
            raise Exception("Either `wkt` or `geo_json` needs to be specified")
        if wkt and geo_json:
            raise Exception("Only `wkt` or `geo_json` should be specified")

    def search(
        self,
        crs: str,
        wkt: str = None,
        geo_json: dict = None,
        survey_metadata_filter: dict = None,
        file_metadata_filter: dict = None,
        include_metadata: bool = False,
    ):
        """Finds surveys for which the coverage area intersects with the given set of coordinates or exact metadata key-value match.

        Args:
            crs (str): CRS (Ex.: "EPSG:23031").
            wkt (str): Interested area represented in WKT format. At max one geometry representation should be provided.
            geo_json (dict): Interested area represented in GeoJson format. At max one geometry representation should be provided.
            survey_metadata_filter (dict): survey metadata to filter.
            file_metadata_filter (dict): file metadata to filter.
            include_metadata (bool): true of metadata should be included in the response.

        Returns:
            SurveyWithFilesResponse: the requested surveys and their files (if requested).
        """
        if wkt and geo_json:
            raise Exception("Only one geometry representation should be provided.")

        geo = None

        if geo_json:
            geo_json_struct = Struct()
            geo_json_struct.update(geo_json)
            geo = Geometry(crs=CRS(crs=crs), geo=GeoJson(json=geo_json))
        elif wkt:
            geo = Geometry(crs=CRS(crs=crs), wkt=Wkt(geometry=wkt))

        if survey_metadata_filter and file_metadata_filter:
            request = SearchSurveyRequest(
                polygon=geo,
                survey_metadata=MetadataFilter(filter=survey_metadata_filter),
                file_metadata=MetadataFilter(filter=file_metadata_filter),
                include_metadata=include_metadata,
            )
        elif survey_metadata_filter and not file_metadata_filter:
            request = SearchSurveyRequest(
                polygon=geo,
                survey_metadata=MetadataFilter(filter=survey_metadata_filter),
                include_metadata=include_metadata,
            )
        elif not survey_metadata_filter and file_metadata_filter:
            request = SearchSurveyRequest(
                polygon=geo,
                file_metadata=MetadataFilter(filter=file_metadata_filter),
                include_metadata=include_metadata,
            )
        else:
            request = SearchSurveyRequest(polygon=geo, include_metadata=include_metadata)
        return self.query.SearchSurveys(request, metadata=self.metadata)

    def register(self, survey_name: str, metadata: dict = None):
        """Finds surveys for which the coverage area intersects with the given set of coordinates or exact metadata key-value match.

        Args:
            survey_name (str): survey name.
            metadata (dict): metadata of the survey.

        Returns:
            RegisterSurveyResponse: id, name and metadata of the survey.
        """
        request = RegisterSurveyRequest(name=survey_name, metadata=metadata)
        return self.ingestion.RegisterSurvey(request, metadata=self.metadata)

    def edit(self, survey_id: Optional[str] = None, survey_name: Optional[str] = None, metadata: dict = None):
        """Edit a survey

        Args:
            survey_id (Optional[str]): id of the survey to edit.
            survey_name (Optional[str]): name of the survey to edit.
            metadata (dict): metadata of the survey to edit.

        Returns:
            EditSurveyResponse: id, name and metadata of the survey.

        """
        survey = self.identify(survey_id, survey_name)
        request = EditSurveyRequest(survey=survey, name=survey_name, metadata=metadata)
        return self.ingestion.EditSurvey(request, metadata=self.metadata)

    def delete(self, survey_id: Optional[str] = None, survey_name: Optional[str] = None):
        """Delete a survey

        Args:
            survey_id (Optional[str]): id of the survey to delete.
            survey_name (Optional[str]): name of the survey to delete.

        Returns:
            Nothing

        """
        survey = self.identify(survey_id, survey_name)
        request = DeleteSurveyRequest(survey=survey)
        return self.ingestion.DeleteSurvey(request, metadata=self.metadata)
