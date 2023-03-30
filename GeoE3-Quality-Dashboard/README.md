# GeoE3 Quality Dashboard
GeoE3 quality dashboard - a method for scoring services using metadata and monitoring information. 
Read more about the project at https://geoe3.eu/ and https://geoe3platform.eu/geoe3/

## Process

Two steps :
1. Get the data (see folder [Evaluator](https://github.com/opengeospatial/GEOE3/tree/main/GeoE3-Quality-Dashboard/Evaluator)) ;
2. Visualise the quality of the data in a dashboard.

## Operating the quality dashboard on Power BI

You need to have Microsoft Power BI installed.

### Input files

The dashboards expects the following 6 input files :
- CVS interoperability map / maturity model path ;
- CVS file for the quality viewpoint ;
- CVS file for the quality dimensions ;
- CVS file for the quality elements ;
- CVS file for the quality measures ;
- CVS file for the quality metrics.

### Location of input files

The last 5 files are the output of the Evaluator ; they are located in a folder whose name is formatted as follows :  
>*'service ID'_'name of metadata file'_date_time*  

The interoperability map CSV file is located in the src folder (same folder as Python code).

#### Open
