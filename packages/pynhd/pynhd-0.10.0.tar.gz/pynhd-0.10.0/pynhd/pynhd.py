"""Access NLDI and WaterData databases."""
import logging
import os
import re
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import cytoolz as tlz
import geopandas as gpd
import numpy as np
import pandas as pd
import pygeoogc as ogc
import pygeoutils as geoutils
from pygeoogc import WFS, ArcGISRESTful, MatchCRS, RetrySession, ServerError, ServiceURL
from requests import Response
from shapely.geometry import MultiPolygon, Polygon
from simplejson import JSONDecodeError

from .exceptions import InvalidInputType, InvalidInputValue, MissingItems, ZeroMatched

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
DEF_CRS = "epsg:4326"
ALT_CRS = "epsg:4269"


class WaterData:
    """Access to `Water Data <https://labs.waterdata.usgs.gov/geoserver>`__ service.

    Parameters
    ----------
    layer : str
        A valid layer from the WaterData service. Valid layers are:
        ``nhdarea``, ``nhdwaterbody``, ``catchmentsp``, ``nhdflowline_network``
        ``gagesii``, ``huc08``, ``huc12``, ``huc12agg``, and ``huc12all``. Note that
        the layers' worksapce for the Water Data service is ``wmadata`` which will
        be added to the given ``layer`` argument if it is not provided.
    crs : str, optional
        The target spatial reference system, defaults to ``epsg:4326``.
    """

    def __init__(
        self,
        layer: str,
        crs: str = DEF_CRS,
    ) -> None:
        self.layer = layer if ":" in layer else f"wmadata:{layer}"
        self.crs = crs
        self.wfs = WFS(
            ServiceURL().wfs.waterdata,
            layer=self.layer,
            outformat="application/json",
            version="2.0.0",
            crs=ALT_CRS,
        )

    def bybox(
        self, bbox: Tuple[float, float, float, float], box_crs: str = DEF_CRS
    ) -> gpd.GeoDataFrame:
        """Get features within a bounding box."""
        resp = self.wfs.getfeature_bybox(bbox, box_crs, always_xy=True)
        return self._to_geodf(resp)

    def bygeom(
        self,
        geometry: Union[Polygon, MultiPolygon],
        geo_crs: str = DEF_CRS,
        xy: bool = True,
        predicate: str = "INTERSECTS",
    ) -> gpd.GeoDataFrame:
        """Get features within a geometry.

        Parameters
        ----------
        geometry : shapely.geometry
            The input geometry
        geom_crs : str, optional
            The CRS of the input geometry, default to epsg:4326.
        xy : bool, optional
            Whether axis order of the input geometry is xy or yx.
        predicate : str, optional
            The geometric prediacte to use for requesting the data, defaults to
            INTERSECTS. Valid predicates are:
            EQUALS, DISJOINT, INTERSECTS, TOUCHES, CROSSES, WITHIN, CONTAINS,
            OVERLAPS, RELATE, BEYOND

        Returns
        -------
        geopandas.GeoDataFrame
            The requested features in the given geometry.
        """
        resp = self.wfs.getfeature_bygeom(geometry, geo_crs, always_xy=not xy, predicate=predicate)
        return self._to_geodf(resp)

    def bydistance(
        self, coords: Tuple[float, float], distance: int, loc_crs: str = DEF_CRS
    ) -> gpd.GeoDataFrame:
        """Get features within a radius (in meters) of a point."""
        if isinstance(coords, (list, tuple)) and len(coords) != 2:
            raise InvalidInputType("coords", "tuple or list of length 2.")

        _coords = MatchCRS.coords(((coords[0],), (coords[1],)), loc_crs, ALT_CRS)
        cql_filter = (
            f"DWITHIN(the_geom,POINT({_coords[1][0]:.6f} {_coords[0][0]:.6f}),{distance},meters)"
        )
        resp = self.wfs.getfeature_byfilter(cql_filter, "GET")
        return self._to_geodf(resp)

    def byid(self, featurename: str, featureids: Union[List[str], str]) -> gpd.GeoDataFrame:
        """Get features based on IDs."""
        resp = self.wfs.getfeature_byid(featurename, featureids)
        return self._to_geodf(resp)

    def byfilter(self, cql_filter: str, method: str = "GET") -> gpd.GeoDataFrame:
        """Get features based on a CQL filter."""
        resp = self.wfs.getfeature_byfilter(cql_filter, method)
        return self._to_geodf(resp)

    def _to_geodf(self, resp: Response) -> gpd.GeoDataFrame:
        """Convert a response from WaterData to a GeoDataFrame.

        Parameters
        ----------
        resp : Response
            A response from a WaterData request.

        Returns
        -------
        geopandas.GeoDataFrame
            The requested features in a GeoDataFrames.
        """
        return geoutils.json2geodf(resp.json(), ALT_CRS, self.crs)


class AGRBase:
    """Base class for accessing NHD(Plus) HR database through the National Map ArcGISRESTful.

    Parameters
    ----------
    layer : str
        A valid service layer. For a list of available layers pass an empty string to
        the class.
    outfields : str or list, optional
        Target field name(s), default to "*" i.e., all the fields.
    crs : str, optional
        Target spatial reference, default to EPSG:4326
    """

    def __init__(
        self,
        layer: str,
        outfields: Union[str, List[str]] = "*",
        crs: str = DEF_CRS,
        service: Optional[ArcGISRESTful] = None,
    ) -> None:
        self.layer = layer
        self.outfields = outfields
        self.crs = crs
        self.service = service

    def _check_service(self) -> None:
        """Check if service is set."""
        if self.service is None:
            raise ValueError("First you should use _init_service(url) to initialize the service.")

    def _init_service(self, url: str) -> ArcGISRESTful:
        service = ArcGISRESTful(
            url,
            outformat="json",
            outfields=self.outfields,
            crs=self.crs,
        )
        valid_layers = {v.lower(): k for k, v in service.valid_layers.items()}
        if self.layer not in valid_layers:
            raise InvalidInputValue("layer", list(valid_layers))
        service.layer = valid_layers[self.layer]
        return service

    def connect_to(self, service: str, service_list: Dict[str, str], auto_switch: bool) -> None:
        """Connect to a web service.

        Parameters
        ----------
        service : str, optional
            Name of the preferred web service to connect to from the list provided in service_list.
        service_list: dict
            A dict where keys are names of the web services and values are their URLs.
        auto_switch : bool, optional
            Automatically switch to other services' URL if the first one doesn't work, default to False.
        """
        if service not in service_list:
            raise InvalidInputValue("service", list(service_list.keys()))

        url = service_list.pop(service)
        try:
            self.service = self._init_service(url)
        except (ServerError, ConnectionError):
            if not auto_switch:
                raise ServerError(url)

            while len(service_list) > 0:
                next_service = next(iter(service_list.keys()))
                logger.warning(f"Connection to {url} failed. Will try {next_service} next ...")
                try:
                    url = service_list.pop(next_service)
                    self.service = self._init_service(url)
                    logger.info(f"Connected to {url}.")
                except (ServerError, ConnectionError):
                    continue

        if self.service is None:
            raise ServerError(url)

    def bygeom(
        self,
        geom: Union[Polygon, List[Tuple[float, float]], Tuple[float, float, float, float]],
        geo_crs: str = DEF_CRS,
        sql_clause: str = "",
        distance: Optional[int] = None,
        return_m: bool = False,
    ) -> gpd.GeoDataFrame:
        """Get feature within a geometry that can be combined with a SQL where clause.

        Parameters
        ----------
        geom : Polygon or tuple
            A geometry (Polygon) or bounding box (tuple of length 4).
        geo_crs : str
            The spatial reference of the input geometry.
        sql_clause : str, optional
            A valid SQL 92 WHERE clause, defaults to an empty string.
        distance : int, optional
            The buffer distance for the input geometries in meters, default to None.
        return_m : bool, optional
            Whether to activate the Return M (measure) in the request, defaults to False.

        Returns
        -------
        geopandas.GeoDataFrame
            The requested features as a GeoDataFrame.
        """
        self._check_service()

        self.service.oids_bygeom(  # type: ignore
            geom, geo_crs=geo_crs, sql_clause=sql_clause, distance=distance
        )
        return self._getfeatures(return_m)

    def byids(
        self, field: str, fids: Union[str, List[str]], return_m: bool = False
    ) -> gpd.GeoDataFrame:
        """Get features based on a list of field IDs.

        Parameters
        ----------
        field : str
            Name of the target field that IDs belong to.
        fids : str or list
            A list of target field ID(s).
        return_m : bool
            Whether to activate the Return M (measure) in the request, defaults to False.

        Returns
        -------
        geopandas.GeoDataFrame
            The requested features as a GeoDataFrame.
        """
        self._check_service()

        self.service.oids_byfield(field, fids)  # type: ignore
        return self._getfeatures(return_m)

    def bysql(self, sql_clause: str, return_m: bool = False) -> gpd.GeoDataFrame:
        """Get feature IDs using a valid SQL 92 WHERE clause.

        Notes
        -----
        Not all web services support this type of query. For more details look
        `here <https://developers.arcgis.com/rest/services-reference/query-feature-service-.htm#ESRI_SECTION2_07DD2C5127674F6A814CE6C07D39AD46>`__

        Parameters
        ----------
        sql_clause : str
            A valid SQL 92 WHERE clause.
        return_m : bool
            Whether to activate the Return M (measure) in the request, defaults to False.

        Returns
        -------
        geopandas.GeoDataFrame
            The requested features as a GeoDataFrame.
        """
        self._check_service()

        self.service.oids_bysql(sql_clause)  # type: ignore
        return self._getfeatures(return_m)

    def _getfeatures(self, return_m: bool = False) -> gpd.GeoDataFrame:
        """Send a request for getting data based on object IDs.

        Parameters
        ----------
        return_m : bool
            Whether to activate the Return M (measure) in the request, defaults to False.

        Returns
        -------
        geopandas.GeoDataFrame
            The requested features as a GeoDataFrame.
        """
        self._check_service()

        resp = self.service.get_features(return_m)  # type: ignore
        return geoutils.json2geodf(resp)


class NHDPlusHR(AGRBase):
    """Access NHDPlus HR database through the National Map ArcGISRESTful.

    Parameters
    ----------
    layer : str
        A valid service layer. For a list of available layers pass an empty string to
        the class.
    outfields : str or list, optional
        Target field name(s), default to "*" i.e., all the fields.
    crs : str, optional
        Target spatial reference, default to EPSG:4326
    service : str, optional
        Name of the web service to use, defaults to hydro. Supported web services are:
        * hydro: https://hydro.nationalmap.gov/arcgis/rest/services/NHDPlus_HR/MapServer
        * edits: https://edits.nationalmap.gov/arcgis/rest/services/NHDPlus_HR/NHDPlus_HR/MapServer
    auto_switch : bool, optional
        Automatically switch to other services' URL if the first one doesn't work, default to False.
    """

    def __init__(
        self,
        layer: str,
        outfields: Union[str, List[str]] = "*",
        crs: str = DEF_CRS,
        service: str = "hydro",
        auto_switch: bool = False,
    ):
        super().__init__(layer, outfields, crs)
        service_list = {
            "hydro": ServiceURL().restful.nhdplushr,
            "edits": ServiceURL().restful.nhdplushr_edits,
        }
        self.connect_to(service, service_list, auto_switch)


class NLDI:
    """Access the Hydro Network-Linked Data Index (NLDI) service."""

    def __init__(self) -> None:
        self.base_url = ServiceURL().restful.nldi
        self.session = RetrySession()

        resp = self.session.get("/".join([self.base_url, "linked-data"])).json()
        self.valid_fsources = {r["source"]: r["sourceName"] for r in resp}

        resp = self.session.get("/".join([self.base_url, "lookups"])).json()
        self.valid_chartypes = {r["type"]: r["typeName"] for r in resp}

    @staticmethod
    def _missing_warning(n_miss: int, n_tot: int) -> None:
        """Show a warning if there are misssing features."""
        logger.warning(
            " ".join(
                [
                    f"{n_miss} of {n_tot} inputs didn't return any features.",
                    "They are returned as a list.",
                ]
            )
        )

    def getfeature_byid(
        self, fsource: str, fid: Union[str, List[str]]
    ) -> Union[gpd.GeoDataFrame, Tuple[gpd.GeoDataFrame, List[str]]]:
        """Get feature(s) based ID(s).

        Parameters
        ----------
        fsource : str
            The name of feature(s) source. The valid sources are:
            comid, huc12pp, nwissite, wade, wqp
        fid : str or list
            Feature ID(s).

        Returns
        -------
        geopandas.GeoDataFrame or (geopandas.GeoDataFrame, list)
            NLDI indexed features in EPSG:4326. If some IDs don't return any features
            a list of missing ID(s) are returnd as well.
        """
        self._validate_fsource(fsource)
        fid = fid if isinstance(fid, list) else [fid]
        urls = {f: "/".join([self.base_url, "linked-data", fsource, f]) for f in fid}
        features, not_found = self._get_urls(urls)

        if len(not_found) > 0:
            self._missing_warning(len(not_found), len(fid))
            return features, not_found

        return features

    def comid_byloc(
        self,
        coords: Union[Tuple[float, float], List[Tuple[float, float]]],
        loc_crs: str = DEF_CRS,
    ) -> Union[gpd.GeoDataFrame, Tuple[gpd.GeoDataFrame, List[Tuple[float, float]]]]:
        """Get the closest ComID(s) based on coordinates.

        Parameters
        ----------
        coords : tuple or list
            A tuple of length two (x, y) or a list of them.
        loc_crs : str, optional
            The spatial reference of the input coordinate, defaults to EPSG:4326.

        Returns
        -------
        geopandas.GeoDataFrame or (geopandas.GeoDataFrame, list)
            NLDI indexed ComID(s) in EPSG:4326. If some coords don't return any ComID
            a list of missing coords are returnd as well.
        """
        coords = coords if isinstance(coords, list) else [coords]
        coords_4326 = list(zip(*MatchCRS.coords(tuple(zip(*coords)), loc_crs, DEF_CRS)))

        base_url = "/".join([self.base_url, "linked-data", "comid", "position"])
        urls = {
            (coords[i][0], coords[i][1]): f"{base_url}?coords=POINT({lon} {lat})"
            for i, (lon, lat) in enumerate(coords_4326)
        }
        comids, not_found = self._get_urls(urls)
        comids = comids.reset_index(level=2, drop=True)

        if len(not_found) > 0:
            self._missing_warning(len(not_found), len(coords))
            return comids, not_found

        return comids

    def get_basins(
        self, station_ids: Union[str, List[str]]
    ) -> Union[gpd.GeoDataFrame, Tuple[gpd.GeoDataFrame, List[str]]]:
        """Get basins for a list of station IDs.

        Parameters
        ----------
        station_ids : str or list
            USGS station ID(s).

        Returns
        -------
        geopandas.GeoDataFrame or (geopandas.GeoDataFrame, list)
            NLDI indexed basins in EPSG:4326. If some IDs don't return any features
            a list of missing ID(s) are returnd as well.
        """
        station_ids = station_ids if isinstance(station_ids, list) else [station_ids]
        urls = {s: f"{self.base_url}/linked-data/nwissite/USGS-{s}/basin" for s in station_ids}
        basins, not_found = self._get_urls(urls)
        basins = basins.reset_index(level=1, drop=True)
        basins.index.rename("identifier", inplace=True)

        if len(not_found) > 0:
            self._missing_warning(len(not_found), len(station_ids))
            return basins, not_found

        return basins

    def getcharacteristic_byid(
        self,
        comids: Union[List[str], str],
        char_type: str,
        char_ids: Union[str, List[str]] = "all",
        values_only: bool = True,
    ) -> Union[pd.DataFrame, Tuple[pd.DataFrame, pd.DataFrame]]:
        """Get characteristics using a list ComIDs.

        Parameters
        ----------
        comids : str or list
            The ID of the feature.
        char_type : str
            Type of the characteristic. Valid values are ``local`` for
            individual reach catchments, ``tot`` for network-accumulated values
            using total cumulative drainage area and ``div`` for network-accumulated values
            using divergence-routed.
        char_ids : str or list, optional
            Name(s) of the target characteristics, default to all.
        values_only : bool, optional
            Whether to return only ``characteristic_value`` as a series, default to True.
            If is set to False, ``percent_nodata`` is returned as well.

        Returns
        -------
        pandas.DataFrame or tuple of pandas.DataFrame
            Either only ``characteristic_value`` as a dataframe or
            or if ``values_only`` is Fale return ``percent_nodata`` as well.
        """
        if char_type not in self.valid_chartypes:
            valids = [f'"{s}" for {d}' for s, d in self.valid_chartypes.items()]
            raise InvalidInputValue("char", valids)

        comids = comids if isinstance(comids, list) else [comids]
        v_dict, nd_dict = {}, {}

        if char_ids == "all":
            payload = None
        else:
            _char_ids = char_ids if isinstance(char_ids, list) else [char_ids]
            valid_charids = self.get_validchars(char_type)

            idx = valid_charids.index
            if any(c not in idx for c in _char_ids):
                vids = valid_charids["characteristic_description"]
                raise InvalidInputValue("char_id", [f'"{s}" for {d}' for s, d in vids.items()])
            payload = {"characteristicId": ",".join(_char_ids)}

        for comid in comids:
            url = "/".join([self.base_url, "linked-data", "comid", comid, char_type])
            rjson = self._get_url(url, payload)
            char = pd.DataFrame.from_dict(rjson["characteristics"], orient="columns").T
            char.columns = char.iloc[0]
            char = char.drop(index="characteristic_id")

            v_dict[comid] = char.loc["characteristic_value"]
            if values_only:
                continue

            nd_dict[comid] = char.loc["percent_nodata"]

        def todf(df_dict: Dict[str, pd.DataFrame]) -> pd.DataFrame:
            df = pd.DataFrame.from_dict(df_dict, orient="index")
            df[df == ""] = np.nan
            df.index = df.index.astype("int64")
            return df.astype("f4")

        chars = todf(v_dict)
        if values_only:
            return chars

        return chars, todf(nd_dict)

    def get_validchars(self, char_type: str) -> pd.DataFrame:
        """Get all the avialable characteristics IDs for a give characteristics type."""
        resp = self.session.get("/".join([self.base_url, "lookups", char_type, "characteristics"]))
        c_list = ogc.utils.traverse_json(resp.json(), ["characteristicMetadata", "characteristic"])
        return pd.DataFrame.from_dict(
            {c.pop("characteristic_id"): c for c in c_list}, orient="index"
        )

    def navigate_byid(
        self,
        fsource: str,
        fid: str,
        navigation: str,
        source: str,
        distance: int = 500,
    ) -> gpd.GeoDataFrame:
        """Navigate the NHDPlus databse from a single feature id up to a distance.

        Parameters
        ----------
        fsource : str
            The name of feature source. The valid sources are:
            comid, huc12pp, nwissite, wade, WQP.
        fid : str
            The ID of the feature.
        navigation : str
            The navigation method.
        source : str, optional
            Return the data from another source after navigating
            the features using fsource, defaults to None.
        distance : int, optional
            Limit the search for navigation up to a distance in km,
            defaults is 500 km. Note that this is an expensive request so you
            have be mindful of the value that you provide.

        Returns
        -------
        geopandas.GeoDataFrame
            NLDI indexed features in EPSG:4326.
        """
        self._validate_fsource(fsource)

        url = "/".join([self.base_url, "linked-data", fsource, fid, "navigation"])

        valid_navigations = self._get_url(url)
        if navigation not in valid_navigations.keys():
            raise InvalidInputValue("navigation", list(valid_navigations.keys()))

        url = valid_navigations[navigation]

        r_json = self._get_url(url)
        valid_sources = {s["source"].lower(): s["features"] for s in r_json}  # type: ignore
        if source not in valid_sources:
            raise InvalidInputValue("source", list(valid_sources.keys()))

        url = f"{valid_sources[source]}?distance={int(distance)}"

        return geoutils.json2geodf(self._get_url(url), ALT_CRS, DEF_CRS)

    def navigate_byloc(
        self,
        coords: Tuple[float, float],
        navigation: Optional[str] = None,
        source: Optional[str] = None,
        loc_crs: str = DEF_CRS,
        distance: int = 500,
    ) -> gpd.GeoDataFrame:
        """Navigate the NHDPlus databse from a coordinate.

        Parameters
        ----------
        coords : tuple
            A tuple of length two (x, y).
        navigation : str, optional
            The navigation method, defaults to None which throws an exception
            if comid_only is False.
        source : str, optional
            Return the data from another source after navigating
            the features using fsource, defaults to None which throws an exception
            if comid_only is False.
        loc_crs : str, optional
            The spatial reference of the input coordinate, defaults to EPSG:4326.
        distance : int, optional
            Limit the search for navigation up to a distance in km,
            defaults to 500 km. Note that this is an expensive request so you
            have be mindful of the value that you provide. If you want to get
            all the available features you can pass a large distance like 9999999.

        Returns
        -------
        geopandas.GeoDataFrame
            NLDI indexed features in EPSG:4326.
        """
        _coords = MatchCRS().coords(((coords[0],), (coords[1],)), loc_crs, DEF_CRS)
        lon, lat = _coords[0][0], _coords[1][0]

        url = "/".join([self.base_url, "linked-data", "comid", "position"])
        payload = {"coords": f"POINT({lon} {lat})"}
        rjson = self._get_url(url, payload)
        comid = geoutils.json2geodf(rjson, ALT_CRS, DEF_CRS).comid.iloc[0]

        if navigation is None or source is None:
            raise MissingItems(["navigation", "source"])

        return self.navigate_byid("comid", comid, navigation, source, distance)

    def _validate_fsource(self, fsource: str) -> None:
        """Check if the given feature source is valid."""
        if fsource not in self.valid_fsources:
            valids = [f'"{s}" for {d}' for s, d in self.valid_fsources.items()]
            raise InvalidInputValue("feature source", valids)

    def _get_urls(self, urls: Dict[Any, str]) -> Tuple[gpd.GeoDataFrame, List[str]]:
        """Get basins for a list of station IDs.

        Parameters
        ----------
        urls_dict : dict
            A dict with keys as feature ids and values as corresponsing url.

        Returns
        -------
        (geopandas.GeoDataFrame, list)
            NLDI indexed features in EPSG:4326 and list of ID(s) that no feature was found.
        """
        not_found = []
        resp = []
        for f, u in urls.items():
            try:
                rjson = self._get_url(u)
                resp.append((f, geoutils.json2geodf(rjson, ALT_CRS, DEF_CRS)))
            except (ZeroMatched, JSONDecodeError, ConnectionError):
                not_found.append(f)

        if len(resp) == 0:
            raise ZeroMatched("No feature was found with the provided inputs.")

        resp_df = gpd.GeoDataFrame(pd.concat(dict(resp)))

        return resp_df, not_found

    def _get_url(self, url: str, payload: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Send a request to the service using GET method."""
        if payload:
            payload.update({"f": "json"})
        else:
            payload = {"f": "json"}

        try:
            return self.session.get(url, payload).json()
        except JSONDecodeError:
            raise ZeroMatched("No feature was found with the provided inputs.")
        except ConnectionError:
            raise ConnectionError("NLDI server cannot be reached at the moment.")


class ScienceBase:
    """Access NHDPlus V2.1 Attributes from ScienceBase over CONUS.

    More info can be found `here <https://www.sciencebase.gov/catalog/item/5669a79ee4b08895842a1d47>`_.

    Parameters
    ----------
    save_dir : str
        Directory to save the staged data frame containing metadata for the database,
        defaults to system's temp directory. The metadata dataframe is saved as a feather
        file, nhdplus_attrs.feather, in save_dir that can be loaded with Pandas.
    """

    def __init__(self, save_dir: Optional[str] = None) -> None:
        self.save_dir = Path(save_dir) if save_dir else Path(tempfile.gettempdir())
        if not self.save_dir.exists():
            os.makedirs(self.save_dir)
        self.session = RetrySession()
        self.nhd_attr_item = "5669a79ee4b08895842a1d47"
        self.char_feather = Path(self.save_dir, "nhdplus_attrs.feather")

    def get_children(self, item: str) -> Dict[str, Any]:
        """Get childern items of an item."""
        url = "https://www.sciencebase.gov/catalog/items"
        payload = {
            "filter": f"parentIdExcludingLinks={item}",
            "fields": "title,id",
            "format": "json",
        }
        return self.session.get(url, payload=payload).json()

    def get_files(self, item: str) -> Dict[str, Tuple[str, str]]:
        """Get all the available zip files in an item."""
        url = "https://www.sciencebase.gov/catalog/item"
        payload = {"fields": "files,downloadUri", "format": "json"}
        r = self.session.get(f"{url}/{item}", payload=payload).json()
        files_url = zip(tlz.pluck("name", r["files"]), tlz.pluck("url", r["files"]))
        meta = list(tlz.pluck("metadataHtmlViewUri", r["files"], default=""))[-1]
        return {f.replace("_CONUS.zip", ""): (u, meta) for f, u in files_url if ".zip" in f}

    def stage_data(self) -> pd.DataFrame:
        """Stage the NHDPlus Attributes database and save to nhdplus_attrs.feather."""
        r = self.get_children(self.nhd_attr_item)

        titles = tlz.pluck("title", r["items"])
        titles = tlz.concat(tlz.map(tlz.partial(re.findall, "Select(.*?)Attributes"), titles))
        titles = tlz.map(str.strip, titles)

        main_items = dict(zip(titles, tlz.pluck("id", r["items"])))

        files = {}
        soil = main_items.pop("Soil")
        for i, item in main_items.items():
            r = self.get_children(item)

            titles = tlz.pluck("title", r["items"])
            titles = tlz.map(lambda s: s.split(":")[1].strip() if ":" in s else s, titles)

            child_items = dict(zip(titles, tlz.pluck("id", r["items"])))
            files[i] = {t: self.get_files(c) for t, c in child_items.items()}

        r = self.get_children(soil)
        titles = tlz.pluck("title", r["items"])
        titles = tlz.map(lambda s: s.split(":")[1].strip() if ":" in s else s, titles)

        child_items = dict(zip(titles, tlz.pluck("id", r["items"])))
        stat = child_items.pop("STATSGO Soil Characteristics")
        ssur = child_items.pop("SSURGO Soil Characteristics")
        files["Soil"] = {t: self.get_files(c) for t, c in child_items.items()}

        r = self.get_children(stat)
        titles = tlz.pluck("title", r["items"])
        titles = tlz.map(lambda s: s.split(":")[1].split(",")[1].strip(), titles)
        child_items = dict(zip(titles, tlz.pluck("id", r["items"])))
        files["STATSGO"] = {t: self.get_files(c) for t, c in child_items.items()}

        r = self.get_children(ssur)
        titles = tlz.pluck("title", r["items"])
        titles = tlz.map(lambda s: s.split(":")[1].strip(), titles)
        child_items = dict(zip(titles, tlz.pluck("id", r["items"])))
        files["SSURGO"] = {t: self.get_files(c) for t, c in child_items.items()}

        chars = []
        types = {"CAT": "local", "TOT": "upstream_acc", "ACC": "div_routing"}
        for t, dd in files.items():
            for d, fd in dd.items():
                for f, u in fd.items():
                    chars.append(
                        {
                            "name": f,
                            "type": types.get(f[-3:], "other"),
                            "theme": t,
                            "description": d,
                            "url": u[0],
                            "meta": u[1],
                        }
                    )
        char_df = pd.DataFrame(chars, dtype="category")
        char_df.to_feather(self.char_feather)
        return char_df


def nhdplus_attrs(name: Optional[str] = None, save_dir: Optional[str] = None) -> pd.DataFrame:
    """Access NHDPlus V2.1 Attributes from ScienceBase over CONUS.

    More info can be found `here <https://www.sciencebase.gov/catalog/item/5669a79ee4b08895842a1d47>`_.

    Parameters
    ----------
    name : str, optional
        Name of the NHDPlus attribute, defaults to None which returns a dataframe containing
        metadata of all the available attributes in the database.
    save_dir : str, optional
        Directory to save the staged data frame containing metadata for the database,
        defaults to system's temp directory. The metadata dataframe is saved as a feather
        file, nhdplus_attrs.feather, in save_dir that can be loaded with Pandas.

    Returns
    -------
    pandas.DataFrame
        Either a dataframe containing the database metadata or the requested attribute over CONUS.
    """
    sb = ScienceBase(save_dir)
    if sb.char_feather.exists():
        char_df = pd.read_feather(sb.char_feather)
    else:
        char_df = sb.stage_data()

    if name is None:
        return char_df

    try:
        url = char_df[char_df.name == name].url.values[0]
    except IndexError:
        raise ValueError("The given characteristic name is not in the database.")

    return pd.read_csv(url, compression="zip")
