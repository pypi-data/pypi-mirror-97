# region_estimators package

[![Build Status](https://travis-ci.org/UoMResearchIT/region_estimators.svg?branch=master)](https://travis-ci.org/UoMResearchIT/region_estimators)

region_estimators is a Python library to calculate regional estimations of scalar quantities, based on some known scalar quantities at specific locations.
For example, estimating the NO2 (pollution) level of a postcode/zip region, based on site data nearby.
This first version of the package is initialised with 2 estimation methods:
1. ConcentricRegions: look for actual data points in gradually wider rings, starting with sites within the region, and then working in rings outwards, until sites are found. If more than one site is found at the final stage, it takes the mean.
2. Simple Distance measure: This is a very basic implementation... Find the nearest site to the region and use that value.
If sites exist within the region, take the mean.
   
The sections below are:
- [Repository Structure](#repository-structure)
- [Requirements](#requirements)
- [Usage](#usage) 
- [Unit Testing](#unit-testing)
- [Contributing](#contributing)  
- [Copyright and licensing](#copyright--licensing)


<!-- toc -->

## Repository Structure

The `region_estimators` directory contains the python modules used by the tools. 
The `sample_input_files` directory contains examples of the input files required to test installation.
Operational scripts are stored within the `scripts` directory. 
A set of python unittest test files can be found in the `test` directory.


```
.
├── region_estimations
├── sample_input_files
├── scripts
│   └── outputs
├── test

```

## Requirements

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install region_estimators.
```bash
pip install shapely
pip install pandas
pip install geopandas
pip install region_estimators
```

## Usage
An example python script that uses the region_estimators package can be found in the `scripts` directory.
The required parts are highlighted in the following shortened excerpt:

```python
from shapely import wkt
import pandas as pd
from region_estimators import RegionEstimatorFactory, EstimationData


if __name__ == '__main__':
    # obtain inputs arguments 
    #... [See scripts for obtaining via commandline arguments (argparse)]    

    # Prepare input files  (For sample input files, see the 'sample_input_files' folder)
    df_regions = pd.read_csv(regions_filespec, index_col='region_id')
    df_sites = pd.read_csv(sites_filespec, index_col='site_id')
    df_actuals = pd.read_csv(actuals_filespec)

    # Convert the regions geometry column from string to wkt format using wkt
    df_regions['geometry'] = df_regions.apply(lambda row: wkt.loads(row.geometry), axis=1)

    # Create estimator, the first parameter is the estimation method.

    estimation_data = EstimationData(df_sites, df_regions, df_actuals)

    estimator = RegionEstimatorFactory.region_estimator(method, estimation_data, verbose, max_processors)

    # Make estimations
    if method == 'concentric-regions':
        estimator.max_ring_count = max_rings
    df_estimates = estimator.get_estimations(measurement, region_id, timestamp)

    print(df_estimates)

    # Convert dataframe result to (for example) a csv file:
    if args.save_to_csv:
        df_estimates.to_csv(os.path.join(outdir_name, 'estimates_{}.csv'.format(outfile_suffix)))

```

##### Details of estimation_data class creation / parameters:
```
├── Constructor
│   ├── 3 pandas.Dataframe objects:  
│   │   └── regions (metadata)
│   │   │    └── required columns
│   │   │   │    └── 'region_id' (INDEX): identifier for region (must be unique to each region)
│   │   │   │    └── 'geometry' (shapely.wkt/geom.wkt):  Multi-polygon representing regions location and shape.

│   │   └── sites (metadata)
│   │   │    └── required columns
│   │   │   │    └── 'site_id' (INDEX): identifier for site (must be unique to each site)
│   │   │   │    └── 'latitude' (numeric): latitude of site location
│   │   │   │    └── 'longitude' (numeric): longitude of site location
│   │   │    └── optional columns
│   │   │   │    └── 'name' (string): Human readable name of site

│   │   └── actuals (data)
│   │   │    └── required columns
│   │   │   │    └── 'timestamp' (string): timestamp of actual reading
│   │   │   │    └── 'site_id': (string) ID of site which took actua in sites (in value and type))
│   │   │   │    └── [one or more value columns] (float):    value of actual measurement readings.

├── Returns
│   ├── Initialised instance of EstimationData class
```

##### Details of region_estimators factory class parameters: #####
```
├── Required inputs
│   ├── method_name (string): The estimation method to be uesed
                              In the first version the options are 'concentric-regions' or 'distance-simple'
│   ├── estimation_data (EstimationData instance - see above): data required to make estimations

├── Optional inputs
│   ├── verbose: (int) Verbosity of output level. zero or less => No debug output. Default=0
│   ├── max_processors (int) Maximum number of processors to use. Default=1
│                     (Maximum: Number of processor available)

├── Returns
│   ├── Initialised instance of subclass of RegionEstimator class
```

##### Details of RegionEstimator (subclass) get_estimations method parameters
```
├── Required inputs
│   ├── measurement: which measurement to be estimated (e.g. 'urtica')

├── Optional inputs
│   ├── region_id: region identifier (string (or None to get all regions))
│   ├── timestamp: timestamp identifier (string (or None to get all timestamps))
│   ├── ignore_site_ids: (list of str) Site IDs to be ignored. Default=[]

├── Returns
│   ├── pandas dataframe, with columns:
│   │   └── measurement
│   │   └── region_id
│   │   └── timestamp
│   │   └── value: (float or empty) The estimated value
│   │   └── extra_data: (dict string) Extra info about the estimation calculation

WARNING! - estimator.get_estimates('urtica', None, None) will calculate every region at every timestamp.
```

## Unit testing
A set of python unittest test files can be found in the `test` directory, and can be run from the shell 
(once the necessary requirements are installed) with the command:
```bash
python -m unittest
```

## Contributing
### Improvements to code
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### Extending the RegionEstimator class 
with further method classes:
* Add the new class name (str) to the available_methods list in region_estimator_factory.py:
   ```python
   available_methods = {'concentric-regions': ConcentricRegionsEstimator,
                         'distance-simple': DistanceSimpleEstimator}
   ```
* Create the new RegionEstimator subclass, following the layout in other current subclasses. 
  E.g. ConcentricRegionsEstimator (concentric_regions_estimator.py) and
     DistanceSimpleEstimator (distance_simple_estimator.py)

## Copyright & Licensing

This software has been developed by the [Research IT](https://research-it.manchester.ac.uk/) group at the [University of Manchester](https://www.manchester.ac.uk/) for an [Alan Turing Institute](https://www.turing.ac.uk/) project.

(c) 2019-2021 University of Manchester.
Licensed under the MIT license (https://opensource.org/licenses/MIT)
