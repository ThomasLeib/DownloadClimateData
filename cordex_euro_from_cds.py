import os
import warnings
import cdsapi


def download(origin, experiment, variable, area, cwd=None):
    """
    Downloads data from the CDS API for the EURO-CORDEX/CORDEX-CORE project
    origin: str
        Which dataset to download from. Either CORDEX-CORE or EURO-CORDEX
    experiment: str
        Historical, RCP_2_6, RCP_4_5 or RCP_8_5
    variable: str
        Climate data variable to download. Only one can be downloaded at a time. Find names below.
    subarea: list of int
        [N,W,S,E] borders of a rectangular area to download data for
    cwd: str
        current working directory, i.e. where data is supposed to be stored

    Returns: Nothing. Downloaded file is directly stored.
    """
    dataset = "multi-origin-c3s-atlas"
    origins = ["cordex_core", "cordex_eur_11"]
    experiments = ["historical", "rcp_2_6", "rcp_8_5"]
    variables = ["monthly_mean_of_daily_accumulated_precipitation", "monthly_mean_of_daily_mean_temperature",
                          "monthly_surface_solar_radiation_downwards", "monthly_mean_of_daily_minimum_temperature",
                          "monthly_mean_of_daily_maximum_temperature","monthly_surface_thermal_radiation_downwards",
                          "monthly_near_surface_specific_humidity"] # there are more variables available but they should suffice for now

    #Test some cases which will lead to failed or faulty download

    warnings.warn("Be certain that the selected area is within the domain of the selected origin. The data download will work but the file will contain no data.")

    if type(variable) == list and len(variable) > 1:
        variable = variable[0]
        warnings.warn("Only one variable can be downloaded at a time. The first variable in the list will be used.")

    if origin == "cordex_core" and experiment == "rcp_4_5":
            warnings.warn("The combination of origin cordex_core and experiment rcp_4_5 is not available. "
                          "The data download was cancelled.")
            return


    if cwd is None:
        cwd = os.getcwd()


    if origin == "cordex_core":
        domain = "global_mosaic"
    elif origin == "cordex_eur_11":
        domain = "eur_cordex"

    if experiment == "historical":
        period = "1970-2005"
    elif experiment == "rcp_2_6" or experiment == "rcp_4_5" or experiment == "rcp_8_5":
        period = "2006-2100"

    #  Check for correct spelling of the input variables and legal year range and area

    if variable  in variables\
        and experiment in experiments\
        and -180 <= area[1] <= area[3] <= 180 \
        and -90 <= area[2] <= area[0] <= 90\
        and origin in origins:

        #TODO: Talk to Alex about the folder structure in which to store the data

        if not os.path.exists(cwd + '/data'):
            os.mkdir(cwd + '/data')
        #TODO: Implement some naming scheme
        target = cwd + '/data/test.zip'
        #TODO: Implement check if data is already downloaded
        print("Data download started (it might take several minutes)")
        client = cdsapi.Client()
        request = {
            "origin": origin,
            "experiment": experiment,
            "domain": domain,
            "period": period,
            "variable": variable,
            "area": area
        }
        client = cdsapi.Client()
        client.retrieve(dataset, request).download(target)
        print("Data download completed")
    else:
        warnings.warn('The data download was cancelled. At least one of the provided input variables does not exist'
                      ' or was misspelled. Please check.')


origin = "cordex_eur_11"
variable = "monthly_mean_of_daily_mean_temperature"
experiment = "rcp_2_6"
area = [50, 15, 48, 16]
download(origin, experiment,variable,area)
# request = {
#     "origin": "cordex_core",
#     "experiment": "rcp_2_6",
#     "domain": "global_mosaic",
#     "period": "2006-2100",
#     "variable": ["monthly_mean_of_daily_accumulated_precipitation","monthly_mean_of_daily_mean_temperature"],
#     "area": [90, 179, 89, 180]
# }
#
# client = cdsapi.Client()
# client.retrieve(dataset, request).download()
