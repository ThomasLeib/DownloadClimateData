import os
import warnings
import cdsapi
import numpy as np

def download(clim_var=None, product_type="monthly_averaged_reanalysis",year_start = 1950, year_finish = 2024,area = [90,-180,-90,180], cwd=None, data_format = "grib", download_format = "zip"):
    dataset = "reanalysis-era5-land-monthly-means"

    # providing months is currently not implemented, maybe TODO
    month = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

    #providing time is currently not implemented, TODO if reanalysis by hour of day is to be implemented
    time = ["00:00"]
    era5_formats = ["grib", "netcdf"]
    download_formats = ["unarchived", "zip"]
    era5_variables = [
        "2m_dewpoint_temperature", "2m_temperature", "skin_temperature",
        "soil_temperature_level_1", "soil_temperature_level_2", "soil_temperature_level_3", "soil_temperature_level_4",
        "lake_bottom_temperature", "lake_ice_depth", "lake_ice_temperature", "lake_mix_layer_depth", "lake_mix_layer_temperature",
        "lake_shape_factor", "lake_total_layer_temperature", "snow_albedo", "snow_cover", "snow_density", "snow_depth",
        "snow_depth_water_equivalent", "snowfall", "snowmelt", "temperature_of_snow_layer", "skin_reservoir_content",
        "volumetric_soil_water_layer_1", "volumetric_soil_water_layer_2", "volumetric_soil_water_layer_3", "volumetric_soil_water_layer_4",
        "forecast_albedo", "surface_latent_heat_flux", "surface_net_solar_radiation", "surface_net_thermal_radiation",
        "surface_sensible_heat_flux", "surface_solar_radiation_downwards", "surface_thermal_radiation_downwards",
        "evaporation_from_bare_soil", "evaporation_from_open_water_surfaces_excluding_oceans", "evaporation_from_the_top_of_canopy",
        "evaporation_from_vegetation_transpiration", "potential_evaporation", "runoff", "snow_evaporation", "sub_surface_runoff",
        "surface_runoff", "total_evaporation", "10m_u_component_of_wind", "10m_v_component_of_wind", "surface_pressure",
        "total_precipitation", "leaf_area_index_high_vegetation", "leaf_area_index_low_vegetation", "high_vegetation_cover",
        "glacier_mask", "lake_cover", "low_vegetation_cover", "lake_total_depth", "geopotential", "land_sea_mask", "soil_type",
        "type_of_high_vegetation", "type_of_low_vegetation"
        ]

    #pruduct type monthly_averaged_reanalysis_by_hour_of_day is not implemented currently, maybe TODO
    era5_product_types = ["monthly_averaged_reanalysis"]
    earliest_year = 1950
    latest_year = 2024 # actually 2025 is the latest available year but this is for simplicity

    # Get current working directory if no string was provided
    if cwd is None:
        cwd = os.getcwd()

    # Set default climate variable to '2m_temperature' if none were provided
    if clim_var is None:
        clim_var = ['2m_temperature']

    #  Check for correct spelling of the input variables and legal year range and area
    if all(x in era5_variables for x in clim_var) \
            and all(x in era5_product_types for x in [product_type]) \
            and earliest_year <= year_start <= year_finish <= latest_year \
            and -180 <= area[1] <= area[3] <= 180 \
            and -90 <= area[2] <= area[0] <= 90:

        #generate list of all years in range
        year = list(np.arange(year_start, year_finish + 1, 1).astype(str))
        #TODO: Talk to Alex about the folder structure in which to store the data
        if not os.path.exists(cwd + '/data'):
            os.mkdir(cwd + '/data')
        #TODO: Implement some naming scheme
        target = cwd + '/data/test.grib'
        #TODO: Implement check if data is already downloaded
        print("Data download started (it might take several minutes)")

        client = cdsapi.Client()
        request = {
            'product_type': product_type,
            'variable': clim_var,
            "year": year,
            "month": month,
            "time": time,
            "data_format": data_format,
            "download_format": download_format,
            "area": area}
        client.retrieve(dataset, request, target)

        print("Data download completed")


    else:
        warnings.warn('The data download was cancelled. At least one of the provided input variables does not exist'
                      ' or was misspelled. Please check.')

clim_var = ['2m_temperature']
year_start = 1990
year_finish = 2000
product_type = "monthly_averaged_reanalysis"
area = [49, 8, 47, 10]
download(clim_var, product_type, year_start, year_finish, area)
