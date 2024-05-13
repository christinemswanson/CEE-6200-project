# CEE-6200-project
This repository houses my final project for CEE-6200 to perform a model diagnostic assessment of the Plan 2014 simulation model. The goal of Phase I of the project is to determine how well the simulated and observed water levels correspond to each other, particularly during January - May 2017 when the International Lake Ontario St. Lawrence River Board (ILOSLRB) was not making major deviations from Plan 2014. The second phase of this project is to perform a climate change impact assessment to determine roughly how extreme water levels could get on Lake Ontario to the end of the century. 

Please note, you will need to change the file path directories to run the R and Python scripts on your local machine, described below. 

**Requirements:**

* To run the R scripts: `rnoaa` (v = 1.3.4), `remotes`, `tidyverse`

* To run the Python scripts: `pandas`, `os`, `numpy`, `matplotlib`, `datetime`, `sklearn`, `scipy`, `calendar`

## Repository overview:

* `README`: this file
* `finalProject`: folder that contains sub-folders for the project. 

**Folders overview:**

1: `data`

* Contains the historical observed data on water levels on Lake Ontario and various locations along the St. Lawrence River (Alexandria Bay, Ogdensburg, and Pointe Claire) in the `historic` folder. Contains the Plan 2014 simulation model output, which simulates water levels and flows, in the `simulation_output` folder. The simulation output is from this respository: github.com/ksemmendinger/Plan-2014-Python. The three climate change driven water supply data sets are provided in the `climate_scenarios` folder. 

2: `documentation`

* Contains the metadata for where the observed data were obtained for this project. Also contains metadata on the three climate change projections.  

3: `figs`

* Contains all figures produced from this project. 

4: `py-scripts`

* Contain the Python scripts to load and clean the observed water level data, as well as perform the analysis. 

5: `scripts`

* Contains the R files to query observed water level data from NOAA at Ogdensburg and Alexandria Bay. These R files do not need to be run if you choose to use the provided historic data at Ogdensburg and Alexandria Bay located in the `data/historic` folder. 

6: `simulation`

* Contains the required input data files and scripts to run the Plan 2014 simulation
