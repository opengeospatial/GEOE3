# Geoe3 Quality Software

# Introduction

This repository contains two versions of the FME-based quality software. The purpose of these workspaces is to automatically point out errors of the given LoD2-level CityGML and CityJSON data sets. Both workspaces perform several checks on the geometry, attributes and relations of the features. Results can be written either to CSV, CityGML or CityJSON file.

At the moment, workspaces can only support buildings of CityJSON up to version 1.0.1 and CityGML up to version 2.0. 

In addition to FME workspaces, this repository also contains Excel files related to quality rules in FME implementations. The Excel files contain more detailed information about all implemented rules. 

The rules are mainly based on SIG3D Modelling Guide and the OGC CityGML Standards (links below). Some rules are invented by the GeoE3 team of the National Land Survey of Finland. 

# Installation

To use these workspaces, you need at least FME version 2021.2. To get the licence and the software please visit [www.safe.com](https://www.safe.com/). 

If you are new to the FME environment, see [Safe Community](https://community.safe.com/s/article/batch-processing-method-1-command-line-or-batch-fi).

# How to run the model?
The workspaces can be run in multiple ways. The easiest way is to use the FME Workbench desktop application, where you can just click 'run' and set the input parameters. An another way is to use the command line for which you can find instructions [here](https://community.safe.com/s/article/batch-processing-method-1-command-line-or-batch-fi). The third option is to automatize or schedule running. Instructions are provided [here](https://community.safe.com/s/article/getting-started-with-automations).

## User parameters
When you run the workspace, FME will ask the user to define multiple **user parameters.** as an input. These parameters affect functionality of the rules, which are kinds of thresholds. Both input and output datasets are defined as user parameters. It is possible and even recommendable to modify default values of user parameters before running the model. This can be done by running the whole workspace or by right-clicking the parameters from Navigator -> User Parameters -> Manage User Parameters... 

You can see explanations of user parameters **for CityGML version** below:

<img src="https://github.com/opengeospatial/GEOE3/blob/main/wiki_images/user_parameters.png" alt="User parameters image" width="60%">

| No. 	|     USER PARAMETER 	|     OPTIONS 	|     DESCRIPTION 	|     MANDATORY 	|
|---	|---	|---	|--- |--- |
| 1. 	| [INPUT_CITYGML3] Source CityGML File(s) 	|Full or relative path of files. Also wildcards ('*') are supported.| One or multiple input file(s). Multiple files are all read and processed together, which enables eg. checking duplicate IDs against features in all data sets.	| Yes |
| 2. 	| [OUTPUT_CSV]   Destination CSV File 	|File name without path. No extensions needed. | Output CSV (Comma Separated Values) file contains only errors aggregated per feature. If a file with same name already exists in the same folder, it will be overwritten. 	| If empty, no output csv |
| 3. 	| [OUTPUT_CITYGML] Destination CityGML file |File name without path. No extensions needed. | Output CityGML file contains invalid geometry parts and corresponding errors as an attributes. If the file with the same name already exists, it will be overwritten. 	| If empty, no output CityGML |
| 4. 	| [RULE_CATEGORIES]   Rule categories to be checked 	| ValidateGeometry, ValidateAttributes, ValidateXlinks, ValidateHierarchy, ValidateAddress | This parameter defines which rule categories are applied to data automatically. For example, if you only choose ValidateGeometry, then the model does not process other rules. This is especially useful, when the input dataset is very large and thus processing would take a lot of time. | If empty, only duplicates and CRS will be checked |
| 5. 	| [CRS] Destination Coordinate System 	| All suitable coordinate reference systems, like EPSG registries. | Coordinate Reference System in which all datasets will be converted. If empty, original input CRSs is used.	Note that used CRS defines the measurement units for many thresholds (eg. meter or foot)| If empty, original CRS remains |
| 6. 	| [CHECK_NORMALS]   Check vertex normals for every feature 	| Yes/No | If this is chosen, the model adds an error to every feature, which doesn't contain normal vectors. 	| Yes |
| 7.  	| [OVERLAP] Maximum overlappiing percentage of the whole area	|  Float 0-100 | Threshold, which determines the maximum overlapping area of one surface. 	| If empty, skip overlap checks|
| 8. 	| [PLAN_DIST] Planar surface distance tolerance i.e. 'thickness' 	| Float >= 0| This parameter describes the maximum “thickness” a face can have before it is considered non-planar. A planar polygon has a thickness of 0. 	| Yes |
| 9. 	| [PLAN_ANG]   Planar surface normal deviation tolerance | Float 0-180 degrees| This parameter describes the maximum deviation between the average surface normal of a face and the surface normals resulting from a triangulation of that face, before it is considered non-planar. A planar polygon has a surface normal deviation of 0. 	| Yes |
| 10. 	| [MIN_VOLUME] Minimum volume of the solid 	| Integer > 0 | The model checks that every solid has larger volume than this threshold. If the volume is too small, it causes an error. 	| If empty, skip volume checks |
| 11. 	| [MIN_AREA]   Minimum area of the surface (crs unit) 	| Float >= 0 | The model checks that every surface has a bigger area than the given threshold. If the area is smaller than the threshold, it causes an error. 	| If empty, skip area checks |
| 12. 	| [SPIKE_ANGLE] Maximum spike angle 	| Float 0-180 degrees | If the angle (in degrees) between two line segments is less than or equal to this parameter, then the middle point is a spike and is notified. The value must be between 0 and 180 degrees. 	| If empty, skip spike checks |
| 13. 	| [COORD_PREC]   Coordinate rounding precision (number of decimal places) 	| Integer 0-20 | The model rounds coordinates of the feature to a specified number of decimal places.	| If empty, no rounding |
| 14. 	| [TOLERANCE] Tolerance for duplicate concecutive points 	| Float >= 0 | If two concecutive points are located in the same coordinates within this tolerance, they are considered as an duplicate points. 	| Yes |





**Note 1:** User parameters slightly differ between CityGML and CityJSON workspaces and might be in different order. 

# How to interpret the results?
The explanations for all implemented rules are in the Excel file located in this repository. The excel table corresponds with the FME workspace.

**1. CSV Results**

Tabular results can be stored in the CSV (Comma Separated Values) file. In addition to the basic attributes of features, CSV file includes names, details and severity levels of every error detected. You can group, aggregate or analyze the results based on the unique identifier or the dataset name. This can be done by any software / programming language that can handle CSV data.

Example of results opened in Excel:

![Example image of CSV results](https://user-images.githubusercontent.com/60340933/150500173-276a39c0-bade-4dfd-b201-8d0fba137a16.png)

**2. CityJSON and CityGML Results**

Geometrical results i.e. invalid parts of the features can be stored to CityGML or CityJSON file. This output file contains errorneous geometry parts of the buildings and the basic information of errors. Number of errors, their names, descriptions and severity levels are included. Note that all features have their original geometry without any modified or deleted parts. You can analyze and process geometrical results via any application or programming language that can handle CityJSON or CityGML data, like the FME Inspector. 

**3. Results in the FME Workspace**

You can also inspect, group and aggregate the results from the FME workspace itself when you add inspectors or enable feature caching ('Run' -> 'Enable Feature Caching'). That might be especially useful, when encountering problems.

![kuva](https://user-images.githubusercontent.com/60340933/150511861-668b84b9-9c02-4e05-be0e-045bb4ba9da3.png)

# How to edit the workspace?

You can edit workspaces easily with the FME Workbench desktop application. The workspace might seem quite complicated. It consists of several tabs, bookmarks, transformers and embedded transformers. The main tab is the only view you need, if you just want to run the model. Other tabs are customized transformers, which are embedded in the main tab. The only purpose of the bookmarks is to make the model clearer and group rules according to their theme. 

Some rules can discard failed features (severity level = FAIL), in which case the feature is not passed on towards other rules in downstream. For that reason, be careful when interpreting quality results. In theory, one feature might contain more than one FAIL-level quality error, but only one is reported because the feature is discarded after that. In some cases, transformer tries to repair features automatically (severity level = FIXED).

For that reason, do not change the given order of the FME workflow without proper knowledge. Changing order of transformers might lead to false errors because fixing one error may affect other errors. For example, all invalid solid boundaries are fixed automatically before detecting invalid solid voids because errors in boundaries may cause errors in voids. So without repairing (or discarding) data automatically, errors located in solid boundaries may be listed as errors in solid voids. 

You can temporarily disable some rules by right-clicking the corresponding transformer in the workspace and selecting 'disable'. Note that when you disable some transformers upstream, data does not flow to downstream transformers. Sometimes you should re-route the flow and skip transformers in that way.

In the picture below, you can see how rules are connected to each other in the **CityGML** workspace. Red rules may discard some features and orange rules try to repair invalid parts of the features. This might prevent transformers downstream from processing data. Blue rules only raise a warning. 

<img src="https://github.com/opengeospatial/GEOE3/blob/main/wiki_images/Flowchart_CityGML.jpg" alt="Workflow of the CityGML workspace" width="90%">

**Note 1:** The principles and hierarchy between CityGML and CityJSON workspaces differ due to different encoding of formats. 

**Note 2:** Implemented rules are described in the corresponding Excel sheet. The purpose of the Excel is to be an updated version of all rules in the FME workspace.

## Tips for performance tuning
If the datasets are very large, processing all rules will take a lot of time. If you don't have to find all possible errors, you can select executable rules from user parameters named RULE_CATEGORIES. In addition, ensure that feature caching and feature counting are disabled (from 'Run' menu). More possible solutions for perfomance problems can be found [here](https://community.safe.com/s/article/performance-tuning-fme). 


# Contributing
If you have any ideas, questions or recommendations, please open an issue or contact me directly by email.

# Notes
At the moment, both workspaces are under construction and therefore might contain some inconsistencies. 

See also the project [wiki](https://github.com/opengeospatial/GEOE3/wiki) and [web pages](https://geoe3.eu/).

# Authors
Alpo Turunen

National Land Survey of Finland

alpo.turunen@maanmittauslaitos.fi
