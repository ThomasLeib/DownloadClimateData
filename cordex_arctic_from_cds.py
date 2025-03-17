import os
import warnings
import cdsapi
import numpy as np
from plotly.data import experiment


def download(experiment, variable, complete_timespan = True, start_year = False, end_year = False, gcm = "cccma_canesm2", rcm = "cccma_canrcm4", cwd=None):
    """
    https://cds.climate.copernicus.eu/datasets/projections-cordex-domains-single-levels?tab=overview

    valid years:

    rcps: 2006-2100
    historical: 1950-2005

    19x1-19x5, 19x6-19(x+1)0
    20x6-20(x+1)0, 20x1-20x5
    20x6-20(x+1)0, 20x1-20x5

    allowed combinations for 0.44° (not currently implemented); [experiment, gcm, rcm] (alle Angaben ohne Gewähr :D):

    [historical, cccma_canesm2, smhi_rca4]
    [historical, cccma_canesm2, uqam_crcm5]
    [historical, cccma_canesm2, cccma_canrcm4]

    [historical, ichec_ec_earth, smhi_rca4]
    [historical, ichec_ec_earth, dmi_hirham5]
    [historical, ichec_ec_earth, dmi_hirham5]

    [historical, ncc_noresm1_m, smhi_rca4]

    [historical, mpi_m_mpi_esm_lr, mgo_rrcm]
    [historical, mpi_m_mpi_esm_lr, smhi_rca4]
    [historical, mpi_m_mpi_esm_lr, smhi_rca4_sn]


    [rcp_2_6, ichec_ec_earth, smhi_rca4]


    [rcp_4_5, cccma_canesm2, cccma_canrcm4]
    [rcp_4_5, cccma_canesm2, smhi_rca4]

    [rcp_4_5, ichec_ec_earth, dmi_hirham5]
    [rcp_4_5, ichec_ec_earth, smhi_rca4]

    [rcp_4_5, ncc_noresm1_m, smhi_rca4 ]

    [rcp_4_5, mpi_m_mpi_esm_lr, smhi_rca4]


    [rcp_8_5, cccma_canesm2, cccma_canrcm4]
    [rcp_8_5, cccma_canesm2, smhi_rca4]
    [rcp_8_5, cccma_canesm2, uqam_crcm5]

    [rcp_8_5, ichec_ec_earth, dmi_hirham5]
    [rcp_8_5, ichec_ec_earth, smhi_rca4]
    [rcp_8_5, ichec_ec_earth, smhi_rca4_sn]

    [rcp_8_5, mpi_m_mpi_esm_mr, uqam_crcm5]

    [rcp_8_5, ncc_noresm1_m, smhi_rca4]

    [rcp_8_5, mpi_m_mpi_esm_lr, smhi_rca4]
    [rcp_8_5, mpi_m_mpi_esm_lr, smhi_rca4_sn]
    [rcp_8_5, mpi_m_mpi_esm_lr, mgo_rrcm]

    """

    dataset = "projections-cordex-domains-single-levels"
    domain = "arctic"
    temporal_resolution = "daily_mean"
    ensemble = "r1i1p1"
    horizonal_resolution = "0_22_degree_x_0_22_degree"

    horizontal_resolutions = ["0_22_degree_x_0_22_degree", "0_44_degree_x_0_44_degree"]
    experiments = ["rcp_4_5", "rcp_8_5", "historical"]

    gcms = ["cccma_canesm2"] # more options for 0.44° but need to find out which combinations are allowed
    rcms = ["cccma_canrcm4"] # more options to 0.44° but need to find out which combinations are allowed

    variables = [
        "2m_air_temperature", "2m_surface_specific_humidity", "10m_u_component_of_the_wind",
        "10m_v_component_of_the_wind", "10m_wind_speed", "maximum_2m_temperature_in_the_last_24_hours",
        "minimum_2m_temperature_in_the_last_24_hours", "evaporation", "mean_sea_level_pressure",
        "mean_precipitation_flux", "surface_pressure", "surface_solar_radiation_downwards",
        "surface_thermal_radiation_downward", "total_cloud_cover"
    ]
    start_year_list, end_year_list = create_year_range(experiment, start_year, end_year)

    if cwd == None:
        cwd = os.getcwd()

    if all(x in variables for x in variable)\
        and experiment in experiments\
        and gcm in gcms\
        and rcm in rcms:

        if not os.path.exists(cwd + '/data'):
            os.mkdir(cwd + '/data')
        #TODO: Implement some naming scheme
        target = cwd + '/data/test.zip'
        #TODO: Implement check if data is already downloaded
        print("Data download started (it might take several minutes)")
        client = cdsapi.Client()

        request = {
            "domain": domain,
            "experiment": experiment,
            "horizontal_resolution": horizonal_resolution,
            "temporal_resolution": temporal_resolution,
            "variable": variable,
            "gcm_model": gcm,
            "rcm_model": rcm,
            "ensemble_member": ensemble,
            "start_year": start_year_list,
            "end_year": end_year_list
        }
        client = cdsapi.Client()
        client.retrieve(dataset, request).download(target)
        print("Data download completed")
    else:
        warnings.warn('The data download was cancelled. At least one of the provided input variables does not exist'
                      ' or was misspelled. Please check.')
        return



def create_year_range(experiment, start_year, end_year, full_timespan = True):
    if experiment == "historical":
        earliest_year = 1951
        latest_year = 2005
    elif experiment == "rcp_4_5" or experiment == "rcp_8_5":
        earliest_year = 2006
        latest_year = 2100


    if full_timespan:
        start_year = earliest_year
        end_year = latest_year
    if not earliest_year <= start_year <= end_year <= latest_year:
        warnings.warn("Invalid year range. Please check.")
    if full_timespan:
        start_year_list = np.arange(start_year, end_year, 5)
        end_year_list = np.arange(start_year + 4, end_year + 1, 5)
    else:
        start = np.array([1951,1956,1961,1966,1971,1976,1981,1986,1991,1996,2001,2006,2011,2016,2021,2026,2031,2036,2041,2046,2051,2056,2061,2066,2071,2076,2081,2086,2091,2096])
        finish = np.array([1955,1960,1965,1970,1975,1980,1985,1990,1995,2000,2005,2010,2015,2020,2025,2030,2035,2040,2045,2050,2055,2060,2065,2070,2075,2080,2085,2090,2095,2100])
        start_year_list = start[(start >= start_year) & (start <= end_year)]
        end_year_list = start[(finish >= start_year) & (finish <= end_year)]

    return list(start_year_list.astype(str)), list(end_year_list.astype(str))

experiment = "historical"
variable = ["2m_air_temperature"]
#download(experiment, variable)

