#!/bin/bash

#
# Run "subsample_csv_data.py" for each of the biome.csv files downloaded form EBI_MGnify
# Author: Kai Blumberg <kblumberg@email.arizona.edu>
#

# subsample at most 50 csv rows from the low resolution taxonomic data
#./subsample_csv_data.py -i ../metagenomes/dataset_1/ -o ../metagenomes/dataset_1_subsample -n 50

# subsample at most 38 csv rows from the high resolution taxonomic data
D2=../metagenomes/dataset_2/ 

./subsample_csv_data.py -f $D2/oceanic_sea_surface_microlayer_biome.csv $D2/oceanic_sea_surface_biome.csv $D2/oceanic_epipelagic_zone_biome.csv $D2/oceanic_mesopelagic_zone_biome.csv $D2/marine_coral_reef_biome.csv $D2/oceanic_pelagic_zone_biome.csv $D2/marine_hydrothermal_vent_biome.csv $D2/marine_littoral_zone.csv $D2/marine_benthic_biome.csv $D2/ocean_biome.csv $D2/marine_biome.csv -o ../metagenomes/dataset_2_subsample -m 38
