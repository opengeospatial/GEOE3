# Geoe3 Quality Software

## Introduction

This repository contain two version of the FME-based quality software. The purpose of these workspaces is to automatically points out errors of the given LoD2-level CityGML or CityJSON data sets. Both workspaces perform several checks for the geometry, attributes and relations of the features. Results can be written either to CSV, CityGML or CityJSON file.

At the moment, workspaces can support only buildings of CityJSON up to version 1.0.1 and CityGML up to version 2.0. 

In addition of FME workspaces, this repository contains also Excel files related to quality rules in FME implementations. The Excel files contain more detailed information about all implemented rules.

## Installation

To use these workspaces, you need at least FME version 2021.2. To get the licence and the software please visit [www.safe.com](https://www.safe.com/). 

If you are new to FME environment, see [Safe Community](https://community.safe.com/s/article/batch-processing-method-1-command-line-or-batch-fi).

## How to run the model?
The workspaces can be run in multiple ways. The most easiest way is to use FME Workbench desktop application itself, where you can just click 'run' and set the input parameters. The another way is to use command line for which you can find instructions [here](https://community.safe.com/s/article/batch-processing-method-1-command-line-or-batch-fi). The third option is to automatize or schedule running. Instructions are provided [here](https://community.safe.com/s/article/getting-started-with-automations).

When you run the workspace, FME ask user to define multiple input parameters. These input or so called user parameters affect functionality of the rules ie. they are kind of thresholds. Also input and output datasets are defined as user parameters. It is possible and even recommendable to modify default values of user parameters before running the model. This can be done by running the whole workspace (FME will ask parameters in that case) or by right-clicking the parameters from Navigator -> User Parameters and selecting Manage User Parameters... 

You can see explanations of user parameters below:

<img src="https://github.com/opengeospatial/GEOE3/blob/main/wiki_images/user_parameters.PNG" alt="User parameters image" width="60%">

| No. 	|     USER PARAMETER 	|     DESCRIPTION 	|
|---	|---	|---	|
| 1. 	| [INPUT_CITYGML3] Source CityGML File(s) 	| One or multiple input file(s).  	|
| 2. 	| [OUTPUT_CSV]   Destination CSV File 	| Output CSV (Comma Separated Values) file containing errors. If file with the same name already exist in this folder, it will be overwritten. 	|
| 3. 	| [OUTPUT_CITYGML] Destination CityGML file 	| Output CityGML file containing geometry and errors. If the file with same name already exist, it be overwritten. 	|
| 4. 	| [RULE_CATEGORIES]   Rule categories to be checked 	| This parameter defined which rule categories are applied to data automatically. 	|
| 5. 	| [CRS] Destination Coordinate System 	| Coordinate Reference System in which all datasets will be converted.  	|
| 6. 	| [CHECK_NORMALS]   Check vertex normals for every feature 	| If this is chosen, the model adds an error to every feature, which doesn't contain normal vectors. 	|
| 7.  	| [OVERLAP] Maximum overlappiing percentage of the whole area (0-100 %) 	| Threshold, which determine the maximum overlapping area of one surface. 	|
| 8. 	| [PLAN_DIST] Planar surface distance tolerance ie. 'thickness' 	| This parameter describes the maximum “thickness” a face can have before it is considered non-planar. A planar polygon has a thickness of 0. 	|
| 9. 	| [PLAN_ANG]   Planar surface normal deviation tolerance (degrees) 	| This parameter describes the maximum deviation between the average surface normal of a face and the surface normals resulting from a triangulation of that face, before it is considered non-planar. A planar polygon has a surface normal deviation of 0. 	|
| 10. 	| [MIN_VERTEX_COUNT] Minimum vertex count per feature 	| The model checks that every feature has enough vertices. If some feature has too few vertices, it causes an error. 	|
| 11. 	| [MIN_AREA]   Minimum area of the surface (crs unit) 	| The model checks that every surface has bigger area than the given threshold. If the area is smaller than threshold, it causes an error. 	|
| 12. 	| [COORD_PREC]   Coordinate rounding precision (number of decimal places) 	| The model rounds off coordinates of the feature to a specified number of decimal places.	|
| 13. 	| [SPIKE_ANGLE] Maximum spike angle 	| If the angle (in degrees) between two line segments is less than or equal to this parameter, then the middle point is a spike and is notified. The value must be between 0 and 180 degrees. 	|

## How to interpret the results?
Tabular results can be stored to CSV (Comma Separated Values) -file. In addition of basic information of features, CSV file includes names, details and severity levels of every errors detected. You can group, aggregate or analyze the results based on the unique identifier or the dataset name. This can be done by any software / programming language that can handle CSV data, like Excel.

Geometrical results ie. invalid parts of the features can be stored to CityGML or CityJSON file. This output file contain errorneous geometry parts of the buildings and the basic information of errors. Error names, desciptions, counts and severity levels are included. Note, that all features has their original geometry without any modified or deleted parts. You can analyze and process geometrical results via any application or programming language that can handle CityJSON or CityGML data, like FME Inspector. 
 
**Note 1:** If you run the model multiple times with the same output names, the files will be overwritten without separate warning.

**Note 2: **You can also see the results from workspace itself by enabling feature caching (Run -> Enable Feature Caching).

## How to edit workspace?

You can edit workspace easily from FME Workbench desktop application. The workspace might be a quite complicated. It consists of several tabs, bookmarks, transformers and embedded transformers. The main tab is the only view you need, if you just want to run the model. Other tabs are customized transformers, which are embedded in the main tab. The only purpose of the bookmarks is to make the model clearer by grouping rules. 

Do not change the given order of the FME workflow without proper reason. That is because some upstream transformers modify data to ensure that transformers in downstream can process it without false errors. One error may affect to other errors. For example, all invalid solid boundaries are fixed automatically before detecting invalid solid voids because error in boundaries may cause errors in voids. So without repairing (or discarding) data automatically, error located in boundary may be listed as error in void. 

Some rules can discard the feature (severity level = FAIL), in which case the feature is not passed on towards other rules in downstream. For that reason, be careful when interpreting quality results. One feature might contain more than one FAIL-level quality errors, but only one is reported as the feature is discarded. Sometimes failed features are fixed automatically, if that is possible (severity level = FIXED).

You can temporarily disable some rules by right-clicking corresponding transformer in FME and selecting "disable". Note that when you disable some transformers in upstream, data does not flow into downstream transformers. Sometimes you should re-route the flow and skip transformer in that way.

As said earlier, some rules are hierarchically connected to each other. In the picture below, you can see how rules affect to each other in CityGML workspace. Red rules may discard some features and orange rules tries to repair invalid parts of the features. Both red and orange rules may stop the data flow and thus the transformers after these may not process all features.

<img src="https://github.com/opengeospatial/GEOE3/blob/main/wiki_images/Flowchart_CityGML.jpg" alt="Workflow of the CityGML workspace" width="90%">

**Note 1:** The principles and hierarchy between CityGML and CityJSON workspaces differ due to different encoding of formats. 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

## Notes
At the moment, both workspaces are under construction and thus might contain some inconsistencies. 

See also the project [wiki pages](https://github.com/opengeospatial/GEOE3/wiki).

Disable feature caching for faster processing. Also also also..

## Authors
Alpo Turunen
alpo.turunen@maanmittauslaitos.fi
