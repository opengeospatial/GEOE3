# GeoE3 Quality Dashboard
GeoE3 quality dashboard - a method for scoring services using metadata and monitoring information. 
Read more about the project at https://geoe3.eu/ and https://geoe3platform.eu/geoe3/

## Process
The process is made of two steps :
1. Get the data : this step is detailed in the [Evaluator](https://github.com/opengeospatial/GEOE3/tree/main/GeoE3-Quality-Dashboard/Evaluator) folder ;
2. Visualise the quality of the data in a dashboard : this step is detailed below.

## Operating the quality dashboard on Power BI

You need to have Microsoft Power BI desktop installed.

# 1. Input files

The dashboards expects the following 6 input files :
- CVS interoperability map / maturity model path ;
- CVS file for the quality viewpoint ;
- CVS file for the quality dimensions ;
- CVS file for the quality elements ;
- CVS file for the quality measures ;
- CVS file for the quality metrics.

## Location of input files
The last 5 files are the output of the Evaluator ; they are located in a folder whose name is formatted as follows :  
>*'service ID'_'name of metadata file'_date_time*  

The interoperability map CSV file is located in the src folder (same folder as Python code).

# 2. Setting up the Power BI file

## 2.1. Open the Power BI file
After opening the Quality dashboard Power BI file, the dashboard should be displayed in the software.
The data displayed may not be up to date. You need to rectify that.

## 2.2. Using the right data : 2 parameters to enter
Import of the data is automated. You only have to enter 2 parameters.
- In the "Home" ribbon tag, select the down arrow of the "Transform data" button.
![Screenshot of "Transform data" button in Power BI desktop](https://user-images.githubusercontent.com/114493409/228851429-78dc0f41-f203-400c-9bf9-a180b9c0cc09.png)
- Select "Edit parameters" - a dialog window appears, asking you to enter :
  - the path of the src folder ;
  - the name of the folder created by the Evaluator that contains the 5 CSV files of quality metrics.  
![Screenshot of dialog window for editing parameters in Power BI desktop](https://user-images.githubusercontent.com/114493409/228852754-b875c405-4d35-4089-9c07-199a43aba1d4.png)
- Click "OK".

The quality dashboard should now show the right data.

# 3. Navigating the dashboard 

The GeoE3 quality dashboard is made of 7 windows, which are : 
- Home : displays scores for the 3 viewpoints as well as the menu. Click on those viewpoints to access the next window in the hierarchy, ie. the Viewpoints window. An "information" button is also available to users for further information on how to navigate the dashboard ;
- Viewpoints : displays quality dimensions of one or several selected viewpoints (to select several, ctrl + click). The definition and score of the viewpoint(s) and its dimension(s) are visible on this page.![Screenshot of Viewpoint page in the quality dashboard](https://user-images.githubusercontent.com/114493409/228858962-9e371fb0-57c7-44f8-85a8-01994dce8a63.png)  
  To go see the next level, either click on the right arrow at the top-left corner of the dashboard or directly in the next level in the menu on the left ;
- Dimensions : displays the quality elements of one or several selected dimension(s) (within the previously selected viewpoint(s) ; to see all dimensions of all viewpoints, reset using the curved arrow in the corner) ;
- Elements : displays the measures of one or several selected elements(s) (within the previously selected dimension(s) ;
- Metrics : gives the option to display as many metrics as you want, their description, score and raw value.

- Interoperability Map : Diplays data from the interoperability map created for the GeoE3 project. Use the "select the use case", "select the type of data" and Europe map slicers to display the level of interoperability of relevant datasets. When several datasets are selected, levels of interoperability are averaged (hover to see the averaged value, as the gauge round it) ;
- Tree : this page allows you to navigate through the herarchy tree used to classify quality indicators in this projects, from viewpoints to metric.
![Screenshot of hierarchy tree](https://user-images.githubusercontent.com/114493409/228862308-b7c3d28b-82c2-4bd1-952d-3adb2abeef40.png)

For additionnal information on the metrics and classification, see this index [file](https://github.com/opengeospatial/GEOE3/tree/main/GeoE3-Quality-Dashboard/Evaluator/Quality metrics and where to find them.xlsx )

## Notes on navigating Power BI

- Hovering over elements in the dashboard often displays additionnal information ;
- In the Power BI desktop software, you need to ctrl+click to navigate buttons, as clicking just selects the element ;
- In the Power BI desktop software, in the "Model" tab, make sure that the relationships between the 5 quality indicators table are set as "1 to many", the cross filter is "Both" and the "security filter in both directions" is set as Yes.

# 4. Publish the dashboard

You can publish the quality dashboard created, with the current data, through Power BI.
This published dashboard can then easily be navigated (and shared with a PRO license).
