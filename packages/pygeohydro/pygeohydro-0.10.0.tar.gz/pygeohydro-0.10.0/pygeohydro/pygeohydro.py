"""Accessing data from the supported databases through their APIs."""
import io
import zipfile
from collections import OrderedDict
from typing import Any, Dict, List, Optional, Tuple, Union

import folium
import geopandas as gpd
import numpy as np
import pandas as pd
import pygeoogc as ogc
import pygeoutils as geoutils
import rasterio as rio
import xarray as xr
from pygeoogc import WMS, RetrySession, ServiceURL
from pynhd import NLDI, WaterData
from shapely.geometry import MultiPolygon, Point, Polygon

from . import helpers
from .exceptions import InvalidInputRange, InvalidInputType, InvalidInputValue

DEF_CRS = "epsg:4326"


class NID:
    """Retrieve data from the National Inventory of Dams."""

    def __init__(self) -> None:
        self.session = RetrySession()
        self.base_url = "https://nid.sec.usace.army.mil/ords"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "DNT": "1",
        }

    def get_xlsx(self) -> io.BytesIO:
        """Get the excel file that containes the dam data."""
        self.headers.update({"Cookie": "ORA_WWV_APP_105=ORA_WWV-QM2rrHvxwzROBqNYVD0WIlg2"})
        payload = {"InFileName": "NID2019_U.xlsx"}
        r = self.session.get(
            f"{self.base_url}/NID_R.DOWNLOADFILE", payload=payload, headers=self.headers
        )
        return io.BytesIO(r.content)

    def get_attrs(self, variables: List[str]) -> Dict[str, str]:
        """Get descriptions of the NID variables."""
        self.headers.update({"Cookie": "ORA_WWV_APP_105=ORA_WWV-iaBJjzLW1v3a1s1mXEub0S7R"})

        desc: Dict[str, str] = {}
        for v in variables:
            payload = {"p": f"105:10:10326760693796::NO::P10_COLUMN_NAME:{v}"}
            page = self.session.get(f"{self.base_url}/f", payload=payload, headers=self.headers)
            tables = pd.read_html(page.text)
            desc[v] = tables[0]["Field Definition"].values[0]

        return desc

    def get_codes(self) -> str:
        """Get the definitions of letter codes in NID database."""
        self.headers.update({"Cookie": "ORA_WWV_APP_105=ORA_WWV-Bk16kg_4BwSK2anC36B4XBQn"})
        payload = {"p": "105:21:16137342922753::NO:::"}
        page = self.session.get(f"{self.base_url}/f", payload=payload, headers=self.headers)
        return page.text


def get_nid() -> gpd.GeoDataFrame:
    """Get all dams in the US (over 91K) from National Inventory of Dams 2019.

    Notes
    -----
    This function downloads a 25 MB `xlsx` file and convert it into a
    GeoDataFrame. So, your net speed might be a bottleneck. Another
    bottleneck is data loading since the dataset has more than 91K rows,
    it might take sometime for Pandas to load the data into memory.

    Returns
    -------
    geopandas.GeoDataFrame
        A GeoDataFrame containing all the available dams in the database. This dataframe
        has an ``attrs`` property that contains definitions of all the NID variables including
        their units. You can access this dictionary by, for example, ``nid.attrs`` assuming
        that ``nid`` is the dataframe. For example, ``nli.attrs["VOLUME"]`` returns the definition
        of the ``VOLUME`` column in NID.
    """
    service = NID()
    nid = pd.read_excel(service.get_xlsx(), engine="openpyxl", index_col=0)
    attrs = service.get_attrs(nid.columns)

    nid["INSPECTION_DATE"] = nid.INSPECTION_DATE.str.replace("3018", "2018")
    for c in ["INSPECTION_DATE", "SUBMIT_DATE", "EAP_LAST_REV_DATE"]:
        nid[c] = pd.to_datetime(nid[c])

    for c in ["NUMBER_OF_LOCKS", "YEAR_COMPLETED"]:
        nid[c] = nid[c].astype("Int16")

    nid["geometry"] = [Point(x, y) for x, y in zip(nid.LONGITUDE, nid.LATITUDE)]
    nid = gpd.GeoDataFrame(nid, crs="epsg:4326").drop(columns=["LONGITUDE", "LATITUDE"])
    nid.loc[~nid.is_valid, "geometry"] = pd.NA
    nid.attrs = attrs

    return nid


def get_nid_codes() -> pd.DataFrame:
    """Get the definitions of letter codes in NID database.

    Returns
    -------
    pandas.DataFrame
        A multi-index dataframe where the first index is code categories and the second one is
        letter codes. For example, ``tables.loc[('Core Type',  'A')]`` returns Bituminous Concrete.
    """
    tables_txt = NID().get_codes()

    summary = [
        s.split("summary=")[-1].split('"')[1::2][0]
        for s in tables_txt.split("\n")
        if "summary" in s
    ]

    tables = [
        pd.read_html(tables_txt, attrs={"class": "t-Report-report", "summary": s})[0]
        for s in summary[1:]
    ]
    tables = [
        tb.rename(columns={"CODE": "Code", "VALUE": "Value"}).set_index("Code") for tb in tables
    ]
    return pd.concat(tables, keys=summary[1:]).rename_axis(["Category", "Code"])


def ssebopeta_byloc(
    coords: Tuple[float, float],
    dates: Union[Tuple[str, str], Union[int, List[int]]],
) -> pd.DataFrame:
    """Daily actual ET for a location from SSEBop database in mm/day.

    Parameters
    ----------
    coords : tuple
        Longitude and latitude of the location of interest as a tuple (lon, lat)
    dates : tuple or list, optional
        Start and end dates as a tuple (start, end) or a list of years [2001, 2010, ...].

    Returns
    -------
    pandas.DataFrame
        Daily actual ET for a location
    """
    if not (isinstance(coords, tuple) and len(coords) == 2):
        raise InvalidInputType("coords", "tuple", "(lon, lat)")

    lon, lat = coords

    f_list = _get_ssebopeta_urls(dates)
    session = RetrySession()

    with session.onlyipv4():

        def _ssebop(urls: Tuple[str, str]) -> Dict[str, Union[str, List[float]]]:
            dt, url = urls
            r = session.get(url)
            z = zipfile.ZipFile(io.BytesIO(r.content))

            with rio.MemoryFile() as memfile:
                memfile.write(z.read(z.filelist[0].filename))
                with memfile.open() as src:
                    return {
                        "dt": dt,
                        "eta": [e[0] for e in src.sample([(lon, lat)])][0],
                    }

        eta_list = ogc.utils.threading(_ssebop, f_list, max_workers=4)
    eta = pd.DataFrame.from_records(eta_list)
    eta.columns = ["datetime", "eta (mm/day)"]
    eta = eta.set_index("datetime")
    return eta * 1e-3


def ssebopeta_bygeom(
    geometry: Union[Polygon, Tuple[float, float, float, float]],
    dates: Union[Tuple[str, str], Union[int, List[int]]],
    geo_crs: str = DEF_CRS,
) -> xr.DataArray:
    """Get daily actual ET for a region from SSEBop database.

    Notes
    -----
    Since there's still no web service available for subsetting SSEBop, the data first
    needs to be downloaded for the requested period then it is masked by the
    region of interest locally. Therefore, it's not as fast as other functions and
    the bottleneck could be the download speed.

    Parameters
    ----------
    geometry : shapely.geometry.Polygon or tuple
        The geometry for downloading clipping the data. For a tuple bbox,
        the order should be (west, south, east, north).
    dates : tuple or list, optional
        Start and end dates as a tuple (start, end) or a list of years [2001, 2010, ...].
    geo_crs : str, optional
        The CRS of the input geometry, defaults to epsg:4326.

    Returns
    -------
    xarray.DataArray
        Daily actual ET within a geometry in mm/day at 1 km resolution
    """
    _geometry = geoutils.geo2polygon(geometry, geo_crs, DEF_CRS)

    f_list = _get_ssebopeta_urls(dates)

    session = RetrySession()

    with session.onlyipv4():

        def _ssebop(url_stamped: Tuple[str, str]) -> Tuple[str, xr.DataArray]:
            dt, url = url_stamped
            resp = session.get(url)
            zfile = zipfile.ZipFile(io.BytesIO(resp.content))
            content = zfile.read(zfile.filelist[0].filename)
            ds = geoutils.gtiff2xarray({"eta": content}, _geometry, DEF_CRS)
            return dt, ds.expand_dims({"time": [dt]})

        resp_list = ogc.utils.threading(_ssebop, f_list, max_workers=4)
        data = xr.merge(OrderedDict(sorted(resp_list, key=lambda x: x[0])).values())

    eta = data.eta.copy()
    eta *= 1e-3
    eta.attrs.update({"units": "mm/day", "nodatavals": (np.nan,)})
    return eta


def _get_ssebopeta_urls(
    dates: Union[Tuple[str, str], Union[int, List[int]]]
) -> List[Tuple[pd.DatetimeIndex, str]]:
    """Get list of URLs for SSEBop dataset within a period or years."""
    if not isinstance(dates, (tuple, list, int)):
        raise InvalidInputType(
            "dates", "tuple, list, or int", "(start, end), year, or [years, ...]"
        )

    if isinstance(dates, tuple):
        if len(dates) != 2:
            raise InvalidInputType(
                "dates", "Start and end should be passed as a tuple of length 2."
            )
        start = pd.to_datetime(dates[0])
        end = pd.to_datetime(dates[1])
        if start < pd.to_datetime("2000-01-01") or end > pd.to_datetime("2020-12-31"):
            raise InvalidInputRange("SSEBop database ranges from 2000 to 2020.")
        date_range = pd.date_range(start, end)
    else:
        years = dates if isinstance(dates, list) else [dates]
        seebop_yrs = np.arange(2000, 2020)

        if any(y not in seebop_yrs for y in years):
            raise InvalidInputRange("SSEBop database ranges from 2000 to 2018.")

        d_list = [pd.date_range(f"{y}0101", f"{y}1231") for y in years]
        date_range = d_list[0] if len(d_list) == 1 else d_list[0].union_many(d_list[1:])

    base_url = ServiceURL().http.ssebopeta
    f_list = [
        (d, f"{base_url}/det{d.strftime('%Y%j')}.modisSSEBopETactual.zip") for d in date_range
    ]

    return f_list


def nlcd(
    geometry: Union[Polygon, MultiPolygon, Tuple[float, float, float, float]],
    resolution: float,
    years: Optional[Dict[str, Optional[int]]] = None,
    geo_crs: str = DEF_CRS,
    crs: str = DEF_CRS,
) -> xr.Dataset:
    """Get data from NLCD database (2016).

    Download land use/land cover data from NLCD (2016) database within
    a given geometry in epsg:4326.

    Parameters
    ----------
    geometry : Polygon, MultiPolygon, or tuple of length 4
        The geometry or bounding box (west, south, east, north) for extracting the data.
    resolution : float
        The data resolution in meters. The width and height of the output are computed in pixel
        based on the geometry bounds and the given resolution.
    years : dict, optional
        The years for NLCD data as a dictionary, defaults to
        {'impervious': 2016, 'cover': 2016, 'canopy': 2016}. Set the value of a layer to None,
        to ignore it.
    geo_crs : str, optional
        The CRS of the input geometry, defaults to epsg:4326.
    crs : str, optional
        The spatial reference system to be used for requesting the data, defaults to
        epsg:4326.

    Returns
    -------
     xarray.DataArray
         NLCD within a geometry
    """
    years = {"impervious": 2016, "cover": 2016, "canopy": 2016} if years is None else years
    layers = _nlcd_layers(years)

    _geometry = geoutils.geo2polygon(geometry, geo_crs, crs)

    wms = WMS(ServiceURL().wms.mrlc, layers=layers, outformat="image/geotiff", crs=crs)
    r_dict = wms.getmap_bybox(_geometry.bounds, resolution, box_crs=crs)

    ds = geoutils.gtiff2xarray(r_dict, _geometry, crs)

    if isinstance(ds, xr.DataArray):
        ds = ds.to_dataset()

    for n in ds.keys():
        if "cover" in n.lower():
            ds = ds.rename({n: "cover"})
            ds.cover.attrs["units"] = "classes"
        elif "canopy" in n.lower():
            ds = ds.rename({n: "canopy"})
            ds.canopy.attrs["units"] = "%"
        elif "impervious" in n.lower():
            ds = ds.rename({n: "impervious"})
            ds.impervious.attrs["units"] = "%"

    return ds


def _nlcd_layers(years: Dict[str, Optional[int]]) -> List[str]:
    """Get NLCD layers for the provided years dictionary."""
    nlcd_meta = helpers.nlcd_helper()

    names = ["impervious", "cover", "canopy"]
    avail_years = {n: nlcd_meta[f"{n}_years"] + [None] for n in names}

    if not isinstance(years, dict):
        raise InvalidInputType(
            "years", "dict", "{'impervious': 2016, 'cover': 2016, 'canopy': 2016}"  # noqa: FS003
        )

    if any(yr not in avail_years[lyr] for lyr, yr in years.items()):
        vals = [f"\n{lyr}: {', '.join(str(y) for y in yr)}" for lyr, yr in avail_years.items()]
        raise InvalidInputValue("years", vals)

    layers = [
        f'NLCD_{years["canopy"]}_Tree_Canopy_L48',
        f'NLCD_{years["cover"]}_Land_Cover_Science_product_L48',
        f'NLCD_{years["impervious"]}_Impervious_L48',
    ]

    nones = [lyr for lyr in layers if "None" in lyr]
    for lyr in nones:
        layers.remove(lyr)

    if len(layers) == 0:
        raise InvalidInputRange("At least one of the layers should have a non-None year.")

    return layers


class NWIS:
    """Access NWIS web service."""

    def __init__(self) -> None:
        self.session = RetrySession()
        self.url = ServiceURL().restful.nwis

    @staticmethod
    def query_byid(ids: Union[str, List[str]]) -> Dict[str, str]:
        """Generate the geometry keys and values of an ArcGISRESTful query."""
        if not isinstance(ids, (str, list)):
            raise InvalidInputType("ids", "str or list")

        ids = [str(i) for i in ids] if isinstance(ids, list) else [str(ids)]
        query = {"sites": ",".join(ids)}

        return query

    @staticmethod
    def query_bybox(bbox: Tuple[float, float, float, float]) -> Dict[str, str]:
        """Generate the geometry keys and values of an ArcGISRESTful query."""
        geoutils.check_bbox(bbox)
        query = {"bBox": ",".join(f"{b:.06f}" for b in bbox)}

        return query

    def get_info(self, query: Dict[str, str], expanded: bool = False) -> pd.DataFrame:
        """Get NWIS stations by a list of IDs or within a bounding box.

        Only stations that record(ed) daily streamflow data are returned.
        The following columns are included in the dataframe with expanded
        set to False:

        ==================  ==================================
        Name                Description
        ==================  ==================================
        site_no             Site identification number
        station_nm          Site name
        site_tp_cd          Site type
        dec_lat_va          Decimal latitude
        dec_long_va         Decimal longitude
        coord_acy_cd        Latitude-longitude accuracy
        dec_coord_datum_cd  Decimal Latitude-longitude datum
        alt_va              Altitude of Gage/land surface
        alt_acy_va          Altitude accuracy
        alt_datum_cd        Altitude datum
        huc_cd              Hydrologic unit code
        parm_cd             Parameter code
        stat_cd             Statistical code
        ts_id               Internal timeseries ID
        loc_web_ds          Additional measurement description
        medium_grp_cd       Medium group code
        parm_grp_cd         Parameter group code
        srs_id              SRS ID
        access_cd           Access code
        begin_date          Begin date
        end_date            End date
        count_nu            Record count
        hcdn_2009           Whether is in HCDN-2009 stations
        ==================  ==================================

        Parameters
        ----------
        query : dict
            A dictionary containing query by IDs or BBOX. Use ``query_byid`` or ``query_bbox``
            class methods to generate the queries.
        expanded : bool, optional
            Whether to get expanded sit information for example drainage area.

        Returns
        -------
        pandas.DataFrame
            NWIS stations
        """
        if not isinstance(query, dict):
            raise InvalidInputType("query", "dict")

        output_type = [{"outputDataTypeCd": "dv"}]
        if expanded:
            output_type.append({"siteOutput": "expanded"})

        site_list = []
        for t in output_type:
            payload = {
                **query,
                **t,
                "format": "rdb",
                "parameterCd": "00060",
                "siteStatus": "all",
                "hasDataTypeCd": "dv",
            }

            resp = self.session.post(f"{self.url}/site", payload).text.split("\n")

            r_list = [txt.split("\t") for txt in resp if "#" not in txt]
            r_dict = [dict(zip(r_list[0], st)) for st in r_list[2:]]

            site_list.append(pd.DataFrame.from_dict(r_dict).dropna())

        if expanded:
            sites = pd.merge(
                *site_list, on="site_no", how="outer", suffixes=("", "_overlap")
            ).filter(regex="^(?!.*_overlap)")
        else:
            sites = site_list[0]

        sites.loc[sites.alt_va == "", "alt_va"] = pd.NA
        try:
            sites = sites.drop(sites[sites.parm_cd != "00060"].index)
            sites["begin_date"] = pd.to_datetime(sites["begin_date"])
            sites["end_date"] = pd.to_datetime(sites["end_date"])
        except AttributeError:
            pass

        float_cols = ["dec_lat_va", "dec_long_va", "alt_va", "alt_acy_va"]
        if expanded:
            float_cols += ["drain_area_va", "contrib_drain_area_va"]

        sites[float_cols] = sites[float_cols].apply(lambda x: pd.to_numeric(x, errors="coerce"))

        sites = sites[sites.site_no.apply(len) == 8]

        site_ids = sites.site_no.tolist()
        gii = WaterData("gagesii", DEF_CRS)
        hcdn_dict: Dict[str, str] = {}
        try:
            hcdn = gii.byid("staid", site_ids)
            hcdn_dict.update(hcdn[["staid", "hcdn_2009"]].set_index("staid").hcdn_2009.to_dict())
        except AttributeError:
            for sid in site_ids:
                try:
                    hcdn = gii.byid("staid", sid)
                    hcdn_dict.update(
                        hcdn[["staid", "hcdn_2009"]].set_index("staid").hcdn_2009.to_dict()
                    )
                except AttributeError:
                    hcdn_dict.update({sid: None})

        def hcdn_2009(x: str) -> Optional[bool]:
            _hcdn = hcdn_dict.get(x)
            if _hcdn is not None:
                return len(_hcdn) > 0
            return None

        sites["hcdn_2009"] = sites.site_no.apply(hcdn_2009)

        return sites

    def get_streamflow(
        self, station_ids: Union[List[str], str], dates: Tuple[str, str], mmd: bool = False
    ) -> pd.DataFrame:
        """Get daily streamflow observations from USGS.

        Parameters
        ----------
        station_ids : str, list
            The gage ID(s)  of the USGS station.
        dates : tuple
            Start and end dates as a tuple (start, end).
        mmd : bool
            Convert cms to mm/day based on the contributing drainage area of the stations.

        Returns
        -------
        pandas.DataFrame
            Streamflow data observations in cubic meter per second (cms)
        """
        if not isinstance(station_ids, (str, list)):
            raise InvalidInputType("ids", "str or list")

        station_ids = station_ids if isinstance(station_ids, list) else [station_ids]

        if not isinstance(dates, tuple) or len(dates) != 2:
            raise InvalidInputType("dates", "tuple", "(start, end)")

        start = pd.to_datetime(dates[0])
        end = pd.to_datetime(dates[1])

        siteinfo = self.get_info(self.query_byid(station_ids))
        check_dates = siteinfo.loc[
            (
                (siteinfo.stat_cd == "00003")
                & (start < siteinfo.begin_date)
                & (end > siteinfo.end_date)
            ),
            "site_no",
        ].tolist()
        nas = [s for s in station_ids if s in check_dates]
        if len(nas) > 0:
            raise InvalidInputRange(
                "Daily Mean data unavailable for the specified time "
                + "period for the following stations:\n"
                + ", ".join(nas)
            )

        payload = {
            "format": "json",
            "sites": ",".join(station_ids),
            "startDT": start.strftime("%Y-%m-%d"),
            "endDT": end.strftime("%Y-%m-%d"),
            "parameterCd": "00060",
            "statCd": "00003",
            "siteStatus": "all",
        }

        resp = self.session.post(f"{self.url}/dv", payload)

        time_series = resp.json()["value"]["timeSeries"]
        r_ts = {
            t["sourceInfo"]["siteCode"][0]["value"]: t["values"][0]["value"] for t in time_series
        }

        def to_df(col: str, dic: Dict[str, Any]) -> pd.DataFrame:
            discharge = pd.DataFrame.from_records(dic, exclude=["qualifiers"], index=["dateTime"])
            discharge.index = pd.to_datetime(discharge.index)
            discharge.columns = [col]
            return discharge

        qobs = pd.concat([to_df(f"USGS-{s}", t) for s, t in r_ts.items()], axis=1)

        # Convert cfs to cms
        qobs = qobs.astype("float64") * 0.028316846592

        if mmd:
            nldi = NLDI()
            basins = nldi.get_basins(station_ids)
            eck4 = "+proj=eck4 +lon_0=0 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"
            area = basins.to_crs(eck4).area
            ms2mmd = 1000.0 * 24.0 * 3600.0
            qobs = qobs.apply(lambda x: x / area.loc[x.name.split("-")[-1]] * ms2mmd)
        return qobs


def interactive_map(bbox: Tuple[float, float, float, float]) -> folium.Map:
    """Generate an interactive map including all USGS stations within a bounding box.

    Notes
    -----
    Only stations that record(ed) daily streamflow data are included.

    Parameters
    ----------
    bbox : tuple
        List of corners in this order (west, south, east, north)

    Returns
    -------
    folium.Map
        Interactive map within a bounding box.
    """
    geoutils.check_bbox(bbox)

    nwis = NWIS()
    query = nwis.query_bybox(bbox)
    sites = nwis.get_info(query, expanded=True)
    sites["coords"] = list(sites[["dec_lat_va", "dec_long_va"]].itertuples(name=None, index=False))
    sites["altitude"] = (
        sites["alt_va"].astype("str") + " ft above " + sites["alt_datum_cd"].astype("str")
    )

    sites["drain_area_va"] = sites["drain_area_va"].astype("str") + " square miles"
    sites["contrib_drain_area_va"] = sites["contrib_drain_area_va"].astype("str") + " square miles"

    cols_old = [
        "site_no",
        "station_nm",
        "coords",
        "altitude",
        "huc_cd",
        "drain_area_va",
        "contrib_drain_area_va",
        "begin_date",
        "end_date",
        "hcdn_2009",
    ]

    cols_new = [
        "Site No.",
        "Station Name",
        "Coordinate",
        "Altitude",
        "HUC8",
        "Drainage Area",
        "Contributing Drainage Area",
        "Begin date",
        "End data",
        "HCDN 2009",
    ]
    sites = sites.rename(columns=dict(zip(cols_old, cols_new)))[cols_new]

    msgs = []
    for row in sites.itertuples(index=False):
        msg = ""
        for col in sites:
            msg += "".join(
                ["<strong>", col, "</strong> : ", f"{row[sites.columns.get_loc(col)]}<br>"]
            )
        msgs.append(msg[:-4])

    sites["msg"] = msgs

    west, south, east, north = bbox
    lon = (west + east) * 0.5
    lat = (south + north) * 0.5

    imap = folium.Map(location=(lat, lon), tiles="Stamen Terrain", zoom_start=10)

    for coords, msg in sites[["Coordinate", "msg"]].itertuples(name=None, index=False):
        folium.Marker(
            location=coords, popup=folium.Popup(msg, max_width=250), icon=folium.Icon()
        ).add_to(imap)

    return imap


def cover_statistics(ds: xr.Dataset) -> Dict[str, Union[np.ndarray, Dict[str, float]]]:
    """Percentages of the categorical NLCD cover data.

    Parameters
    ----------
    ds : xarray.Dataset

    Returns
    -------
    dict
        Statistics of NLCD cover data
    """
    nlcd_meta = helpers.nlcd_helper()
    cover_arr = ds.values
    total_pix = np.count_nonzero(~np.isnan(cover_arr))

    class_percentage = dict(
        zip(
            list(nlcd_meta["classes"].values()),
            [
                cover_arr[cover_arr == int(cat)].shape[0] / total_pix * 100.0
                for cat in list(nlcd_meta["classes"].keys())
            ],
        )
    )

    cov = np.floor_divide(cover_arr[~np.isnan(cover_arr)], 10).astype("int")
    cat_list = (
        np.array([np.count_nonzero(cov == c) for c in range(10) if c != 6]) / total_pix * 100.0
    )

    category_percentage = dict(zip(list(nlcd_meta["categories"].keys()), cat_list))

    return {"classes": class_percentage, "categories": category_percentage}
