import os
import warnings
import cdsapi

#TODO: The list of valid combinations can at least be in part found here:
# EURO-CORDEX: https://www.euro-cordex.net/imperia/md/content/csc/cordex/20180130-eurocordex-simulations.pdf
# MED-CORDEX: https://www.medcordex.eu/search/index.php
# ARCTIC-CORDEX: https://climate-cryosphere.org/arctic-cordex/ (maybe)
def download(clim_var, domain, experiment, horizontal_resolution,temporal_resolution, gcm, rcm, ensemble, year_start, year_finish, cwd=None):
    dataset = "projections-cordex-domains-single-levels"
    domains = ["arctic", "europe", "mediterranean"]
    experiments = ["evaluation","historical","rcp_2_6", "rcp_4_5", "rcp_8_5"]
    horizontal_resolutions = ["0_11_degree_x_0_11_degree","0_22_degree_x_0_22_degree","0_44_degree_x_0_44_degree"]
    temporal_resolutions = ["daily_mean","monthly_mean","seasonal_mean"] # there's also 3 and 6 hours
    cor_variables = [
            "2m_air_temperature", "2m_relative_humidity", "2m_surface_specific_humidity",
            "10m_u_component_of_the_wind", "10m_v_component_of_the_wind", "10m_wind_speed",
            "maximum_2m_temperature_in_the_last_24_hours", "minimum_2m_temperature_in_the_last_24_hours",
            "200hpa_temperature", "200hpa_u_component_of_the_wind", "200hpa_v_component_of_the_wind",
            "500hpa_geopotential_height", "850hpa_u_component_of_the_wind", "850hpa_v_component_of_the_wind",
            "evaporation", "land_area_fraction", "mean_sea_level_pressure", "mean_precipitation_flux",
            "orography", "surface_pressure", "surface_solar_radiation_downwards",
            "surface_thermal_radiation_downward", "surface_upwelling_shortwave_radiation",
            "total_cloud_cover", "total_run_off_flux"
        ]

    gcms = [
        "cccma_canesm2", "cnrm_cerfacs_cm5", "csiro_bom_access1_0", "csiro_bom_access1_3",
        "csiro_qccce_csiro_mk3_6_0", "era_interim", "ichec_ec_earth", "ipsl_cm5a_lr",
        "ipsl_cm5a_mr", "miroc_miroc5", "mohc_hadgem2_es", "mpi_m_mpi_esm_lr",
        "mpi_m_mpi_esm_mr", "ncar_ccsm4", "ncc_noresm1_m", "noaa_gfdl_gfdl_esm2g"
    ]

    rcms = [
        "awi_hirham5", "bccr_wrf331", "boun_regcm4_3", "cccma_canrcm4", "clmcom_btu_cclm4_8_17",
        "clmcom_clm_cclm4_8_17", "clmcom_cclm4_8_17_clm3_5", "clmcom_cclm5_0_2", "clmcom_eth_cosmo_crclim",
        "clmcom_hzg_cclm5_0_15", "clmcom_kit_cclm5_0_15", "cmcc_cclm4_8_19", "cnrm_aladin52", "cnrm_aladin53",
        "cnrm_aladin63", "csiro_ccam_2008", "cyi_wrf351", "dmi_hirham5", "elu_regcm4_3", "gerics_remo2009",
        "gerics_remo2015", "guf_cclm4_8_18", "ictp_regcm4_3", "ictp_regcm4_4", "ictp_regcm4_6", "ictp_regcm4_7",
        "iitm_regcm4_4", "inpe_eta", "ipsl_wrf381p", "isu_regcm4", "knmi_racmo21p", "knmi_racmo22e", "knmi_racmo22t",
        "lmd_lmdz4nemomed8", "mgo_rrcm", "mohc_hadrem3_ga7_05", "mohc_hadrm3p", "mpi_csc_remo2009", "ncar_regcm4",
        "ncar_wrf", "ornl_regcm4_7", "ouranos_crcm5", "rmib_ugent_alaro_0", "ru_core_regcm4_3", "smhi_rca4",
        "smhi_rca4_sn", "ua_wrf", "ucan_wrf341i", "uhoh_wrf361h", "ulg_mar311", "ulg_mar36", "unsw_wrf360j",
        "unsw_wrf360k", "unsw_wrf360l", "uqam_crcm5", "uqam_crcm5_sn"
    ]
    ensemble_members = ["r1i1p1","r2i1p1","r3i1p1","r6i1p1","r12i1p1","r0i0p0"]
    earliest_year = 1950
    latest_year = 2100

    # Get current working directory if no string was provided
    if cwd is None:
        cwd = os.getcwd()

    # Set default climate variable to '2m_temperature' if none were provided
    if clim_var is None:
        clim_var = ['2m_air_temperature']

    if all(x in cor_variables for x in clim_var)\
        and gcm in gcms\
        and rcm in rcms\
        and domain in domains\
        and experiment in experiments\
        and horizontal_resolution in horizontal_resolutions\
        and temporal_resolution in temporal_resolutions\
        and ensemble in ensemble_members\
        and earliest_year <= year_start <= year_finish <= latest_year: #TODO: implement multi-year requests

            if not os.path.exists(cwd + '/data'):
                os.mkdir(cwd + '/data')
            #TODO: Implement some naming scheme
            target = cwd + '/data/test.grib'
            #TODO: Implement check if data is already downloaded
            print("Data download started (it might take several minutes)")

            client = cdsapi.Client()
            request = {
                "domain": domain,
                "experiment": experiment,
                "horizontal_resolution": horizontal_resolution,
                "temporal_resolution": temporal_resolution,
                "variable": clim_var,
                "gcm_model": gcm,
                "rcm_model": rcm,
                "ensemble_member": ensemble,
                "start_year": [str(year_start)],
                "end_year": [str(year_finish)]
            }
            client = cdsapi.Client()
            client.retrieve(dataset, request).download(target)

            print("Data download completed")

    else:
        warnings.warn('The data download was cancelled. At least one of the provided input variables does not exist'
                      ' or was misspelled. Please check.')

clim_var = ['2m_air_temperature']
domain = "arctic"
experiment = "rcp_2_6"
horizontal_resolution = "0_11_degree_x_0_11_degree"
temporal_resolution = "seasonal_mean"
gcm = "cnrm_cerfacs_cm5"
rcm = "gerics_remo2015"
ensemble = "r1i1p1"
year_start = 2005
year_finish = 2010
download(clim_var, domain, experiment, horizontal_resolution,temporal_resolution, gcm, rcm, ensemble, year_start, year_finish)
