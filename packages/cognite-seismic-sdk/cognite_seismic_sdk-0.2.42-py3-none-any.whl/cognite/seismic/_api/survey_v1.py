# Copyright 2020 Cognite AS

import os
from typing import *

from cognite.seismic._api.api import API
from cognite.seismic.data_classes.api_types import Survey
from cognite.seismic.data_classes.errors import SeismicServiceError
from grpc import StatusCode

if not os.getenv("READ_THE_DOCS"):

    from cognite.seismic.protos.types_pb2 import CRS, CoverageParameters
    from cognite.seismic.protos.v1.seismic_service_datatypes_pb2 import SearchSpec
    from cognite.seismic.protos.v1.seismic_service_messages_pb2 import SearchSurveysRequest
else:
    from cognite.seismic._api.shims import SearchSpec


class SurveyV1API(API):
    def __init__(self, query, metadata, v0_survey_api):
        super().__init__(metadata=metadata, query=query)
        self.v0_survey_api = v0_survey_api

    def list(
        self,
        list_seismics: bool = False,
        list_seismic_stores: bool = False,
        include_metadata: bool = False,
        crs: Optional[str] = None,
        in_wkt: Optional[bool] = None,
    ):
        """List all the surveys.
        Provide either crs or in_wkt to get surveys' coverage.

        Args:
            list_seismics (bool): true if the seismics ids from the surveys should be listed.
            list_seismic_stores (bool): true if seismic stores ids from the surveys should be listed
            include_metadata (bool): true if metadata should be included in the response.
            crs(str): the crs in which the surveys' coverage is returned, default is original survey crs
            in_wkt(bool): surveys' coverage format, set to true if wkt format is needed, default is geojson format

        Returns:
            List[Survey]: the requested surveys and their files (if requested).
        """

        return self._search_internal([], list_seismics, list_seismic_stores, include_metadata, crs, in_wkt)

    def search(
        self,
        survey_name_substring: Optional[str] = None,
        survey_external_id_substring: Optional[str] = None,
        list_seismics: bool = False,
        list_seismic_stores: bool = False,
        include_metadata: bool = False,
        crs: Optional[str] = None,
        in_wkt: Optional[bool] = None,
    ):
        """Search for subset of surveys.
        Provide either crs or in_wkt to get surveys' coverage.

        Args:
            survey_name_substring (str): find surveys whose name contains this substring
            survey_external_id_substring (str): find surveys whose external id contains this substring
            list_seismics (bool): true if the seismics ids from the surveys should be listed.
            list_seismic_stores (bool): true if seismic stores ids from the surveys should be listed
            include_metadata (bool): true if metadata should be included in the response.
            crs(str): the crs in which the surveys' coverage is returned, default is original survey crs
            in_wkt(bool): surveys' coverage format, set to true if wkt format is needed, default is geojson format

        Returns:
            List[Survey]: the requested surveys and their files (if requested).
        """
        if survey_name_substring is None and survey_external_id_substring is None:
            raise Exception("either survey_name_substring or survey_external_id_substring must be specified")

        search_specs = []
        if survey_name_substring is not None:
            search_specs.append(SearchSpec(name_substring=survey_name_substring))
        if survey_external_id_substring is not None:
            search_specs.append(SearchSpec(external_id_substring=survey_external_id_substring))

        return self._search_internal(search_specs, list_seismics, list_seismic_stores, include_metadata, crs, in_wkt)

    def get(
        self,
        survey_id: Optional[str] = None,
        survey_external_id: Optional[str] = None,
        survey_name: Optional[str] = None,
        list_seismics: bool = False,
        list_seismic_stores: bool = False,
        include_metadata: bool = False,
        crs: Optional[str] = None,
        in_wkt: Optional[bool] = None,
    ):
        """
        Get a survey by either id, external_id or name.
        Provide either crs or in_wkt to get survey coverage.

        Args:
            survey_id (str, optional): survey id.
            survey_external_id (str, optional): survey external id.
            survey_name (str, optional): survey name.
            list_seismics (bool): true if the ids of seismics from this survey should be listed.
            list_seismic_stores (bool): true if the ids of seismic stores from this survey should be listed.
            include_metadata (bool): true if metadata should be included in the response.
            crs(str): the crs in which the survey coverage is returned, default is original survey crs
            in_wkt(bool): survey coverage format, set to true if wkt format is needed, default is geojson format

        Returns:
            Survey: the requested survey, its seismics, seismic stores and metadata (if requested).
        """
        search_spec = None
        if survey_id is None and survey_external_id is None and survey_name is None:
            raise Exception("Must specify either survey_id, survey_name or survey_external_id.")

        if survey_id is not None:
            search_spec = SearchSpec(id_string=survey_id)
        elif survey_external_id is not None:
            search_spec = SearchSpec(external_id=survey_external_id)
        else:
            search_spec = SearchSpec(name=survey_name)

        result = self._search_internal([search_spec], list_seismics, list_seismic_stores, include_metadata, crs, in_wkt)
        if len(result) == 0:
            raise SeismicServiceError(StatusCode.NOT_FOUND, "survey not found")
        else:
            return result[0]

    def register(self, survey_name: str, metadata: dict = None):
        """Finds surveys for which the coverage area intersects with the given set of coordinates or exact metadata key-value match.

        Args:
            survey_name (str): survey name.
            metadata (dict): metadata of the survey.

        Returns:
            RegisterSurveyResponse: id, name and metadata of the survey.
        """
        return self.v0_survey_api.register(survey_name, metadata)

    def edit(self, survey_id: Optional[str] = None, survey_name: Optional[str] = None, metadata: dict = None):
        """Edit a survey

        Args:
            survey_id (Optional[str]): id of the survey to edit.
            survey_name (Optional[str]): name of the survey to edit.
            metadata (dict): metadata of the survey to edit.

        Returns:
            EditSurveyResponse: id, name and metadata of the survey.

        """
        return self.v0_survey_api.edit(survey_id, survey_name, metadata)

    def delete(self, survey_id: Optional[str] = None, survey_name: Optional[str] = None):
        """Delete a survey

        Args:
            survey_id (Optional[str]): id of the survey to delete.
            survey_name (Optional[str]): name of the survey to delete.

        Returns:
            Nothing

        """
        return self.v0_survey_api.delete(survey_id, survey_name)

    def _search_internal(
        self,
        search_specs: List[SearchSpec],
        list_seismics: bool = False,
        list_seismic_stores: bool = False,
        include_metadata: bool = False,
        crs: Optional[str] = None,
        in_wkt: Optional[bool] = None,
    ):
        coverageParamCrs = CRS(crs=crs) if crs is not None else None
        coverageParams = (
            CoverageParameters(crs=coverageParamCrs, in_wkt=in_wkt)
            if coverageParamCrs is not None or in_wkt is not None
            else None
        )
        request = SearchSurveysRequest(
            surveys=search_specs,
            list_seismic_ids=list_seismics,
            list_seismic_store_ids=list_seismic_stores,
            include_metadata=include_metadata,
            include_coverage=coverageParams,
        )
        return [
            Survey.from_proto(survey_proto)
            for survey_proto in self.query.SearchSurveys(request, metadata=self.metadata)
        ]
