# Run the program

Run the **__main__.py** program. It will ask for :
- the path of source files ;
- a service ID.

The data from the availability API is downloaded into a temp file located in the temp folder. This file should be automatically deleted after the program is run.

## Demonstration files

Files used for a demonstration are included in this repository :
- MD_Bui_EX_1.xml is a dataset metadata file with added reccomended data between `<!-- Added : ` markers. Originally from a buildings dataset from the Norwegian Mapping Authority ;
- SMD_Bui_EX_1.xml is a service metadata file. Originally from a buildings dataset from the Norwegian Mapping Authority (no modification in this file ; same dataset as MD_Bui_EX_1.xml) ;
- interoperability_maturityModel.csv is the interoperability map produced by GeoE3 updated before 2023 ;
- 164572_MD_Bui_EX_1_20230331_045258 is a file that contains the results of an evaluation of the previous file. It can be used directly in the dashboard ;
- buildings_and_errors/results_NO_cc.csv is the CSV results  file of the evaluation of the dataset by the GeoE3 Quality Software (dataset from the Norwegian Mapping Authority (same dataset as MD_Bui_EX_1.xml).
