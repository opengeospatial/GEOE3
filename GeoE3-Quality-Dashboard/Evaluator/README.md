# Extraction and evaluation of the data

## Required input 

The program will ask for the following input (6):
- JSON structure file path ;
- Service ID number (for service availability evaluation, provided by Spatineo API) ;
- XML dataset metadata file path ;
- XML service metadata file path ;
- CVS quality evaluation file from GeoE3 quality software path ;
- CVS interoperability map / maturity model path.

## Output

The output of the program is 5 files located in one folder:
- CVS file for the quality viewpoint ;
- CVS file for the quality dimensions ;
- CVS file for the quality elements ;
- CVS file for the quality measures ;
- CVS file for the quality metrics.

Name of the folder is formatted as follow :  
> *'service ID'_'name of metadata file'_date_time*  

## Source of the dashboard data

1. Dataset metadata (data provider)
2. Service metadata OR Service description Capabilities document (data or service provider)
3. Quality evaluation results (see [GeoE3 Quality Software](https://github.com/opengeospatial/GEOE3/tree/main/Geoe3-Quality-Software))
4. Service availability information (Spatineo)

Sources 1 and 2 are XML files that can be downloaded from wherever catalogues they reside from.

Source 3 data is provided by a Quality Software. The Quality software is based on FME and the workbench which analyses the actual contenst of the dataset. It could produce a machine readable file that the dashboard could read in. Currently, for each dataset, we are interested in the produced CSV result file that puts together the list and count of errors the software has identified.

Source 4 data is downloaded from an API provided by Spatineo.

## The evaluation process

1. Start with a list of datasets, the each dataset includes the following information:
    - link to dataset metadata
    - link to service metadata for a (single) service that is used to disseminate the dataset
    - linkage to the Quality evaluation results (TBD)
    - linkage to the service availability information (TBD)
2. Configuration file that includes viewpoints, their dimensions, all the way up to metrics. Each metric includes extraction rules on how to extract information to evaluate that metric for a particular dataset
    - an exatraction rule may target one of the sources (dataset metadata, service metadata, quality software output, or availability information)
3. Configuration also includes the evaluation criteria used to assess whether the extraction output meets requirements => gives a score for that metric
4. Scores are then combined up the quality hierarchy with weights applied (weights are stored in the configuration file)
5. Output in tabular format (for example CSV) so that it is easily usable in the dashboard application (for example Power BI)

## Configuration file format

The configuration file is named 'Dashboard_structure.json' and is in a JSON format.
It is in the form of noded dictionaries with keys and values.

`"viewpoint1": {
    "type": "viewpoint",
    "name": "name of viewpoint",
    "weight": 1,
    "description": "Description of viewpoint.",
    "nodes": {
        "dimension1":{
            "type": "dimension",
            "name": "name of dimension",
            "weight": 6,
            "description": "Description of dimension.",
            "nodes": {
                "element1": {
                    "type": "qualityElement",
                    "name": "name of element",
                    "weight": 5,
                    "description": "Description of quality element.",
                    "nodes": {
                        "measure1": {
                            "type": "measure",
                            "name": "name of measure",
                            "weight": 5,
                            "description": "Description of measure.",
                            "nodes": {
                                "metric1": {
                                    "type": "metric",
                                    "name": "name of metric",
                                    "weight": 0,
                                    "description": "Description of metric",
                                    "extractionRule": {
                                        "type": "xpath",
                                        "source": "service-availability",
                                        "url_start": "https://xxxxx",
                                        "rule": "//xpathxxxxxx",
                                        "value": "text"                                        
                                    },
                                    "evaluationRule": {
                                        "type": "presence",
                                        "description": "Checks presence"
                                    }`
### Extraction rules

```
  ... 
  "extractionRule": {
    "source": "dataset-metadata", 
    "type": "xpath",
    "rule": ".//gmd:MD_Metadata/gmd:contact/gmd:CI_ResponsibleParty/gmd:individualName/gco:CharacterString"
  }
```

`source` = one of `dataset-metadata`, `service-metadata`, `quality-evaluation`, `service-description` (e.g. WFS Capabilities document), or `service-availability`

## Adding extractors / evaluators

When you need a new type of extractor:
1. Choose a keyword for it (for example "***xpath***")
2. Write a function in `src/extract.py` that follows the format `def execute_[your_chosen_keyword_with_underscores]_rule(rule, model):`
3. Register the keyword in the dict `extractor_by_type` in `src/extract.py`
4. Write tests for that extractor in a new file `test/test_extractor_[your_chosen_keyword_with_underscores].py`

Similar thing with evaluators, choose a keyword, write the function in `src/evaluate.py` and write tests in a new file.

## Testing

To run tests:

`$ pytest`

## Miniconda3 help

1. Start "Anaconda Powershell Prompt (Miniconda3)" from the start menu
2. In the shell, run `conda activate geoe3`
3. In the shell, run `cd c:\whereever\this\project\is\geoe3-quality-dashboard\`
4. Use the project as normal

When using miniconda for the first time, run these commands

```
$ conda create --name geoe3
$ conda activate geoe3
$ conda config --add chanels conda-forge
$ cd c:\whereever\this\project\is\geoe3-quality-dashboard\
$ conda install pytest lxml isodate==0.6.1
```
