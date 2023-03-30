# GeoE3 Quality Dashboard
GeoE3 quality dashboard - a method for scoring services using metadata and monitoring information. 
Read more about the project at https://geoe3.eu/ and https://geoe3platform.eu/geoe3/

## Process

Two steps :
1. Get the data (see folder [Evaluator](https://github.com/opengeospatial/GEOE3/tree/main/GeoE3-Quality-Dashboard/Evaluator)) ;
2. Visualise the quality of the data in a dashboard.

## Operating the quality dashboard on Power BI

You need to have Microsoft Power BI desktop installed.

### 1. Input files

The dashboards expects the following 6 input files :
- CVS interoperability map / maturity model path ;
- CVS file for the quality viewpoint ;
- CVS file for the quality dimensions ;
- CVS file for the quality elements ;
- CVS file for the quality measures ;
- CVS file for the quality metrics.

#### Location of input files
The last 5 files are the output of the Evaluator ; they are located in a folder whose name is formatted as follows :  
>*'service ID'_'name of metadata file'_date_time*  

The interoperability map CSV file is located in the src folder (same folder as Python code).

### 2. Setting up the Power BI file

#### Open the Power BI file
After opening the Quality dashboard Power BI file, the dashboard should be displayed in the software.
The data displayed may not be up to date. You need to rectify that.

#### Using the right data : 2 parameters to enter
Import of the data is automated. You only have to enter 2 parameters.
- In the "Home" ribbon tag, select the down arrow of the "Transform data" button.![Screenshot of "Transform data" button in Power BI desktop](https://user-images.githubusercontent.com/114493409/228851429-78dc0f41-f203-400c-9bf9-a180b9c0cc09.png)

- Select "Edit parameters"

