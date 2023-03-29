# geoe3-quality-dashboard
GeoE3 quality dashboard - method for scoring services using metadata and monitoring information. You can read more about the project at https://geoe3.eu/ and https://geoe3platform.eu/geoe3/

## Data flow of the program, from Python to Power BI

The program requires the following input :
- JSON structure file path;
- service ID number ;
- xml metadata file path ;
- cvs quality evaluation file from GeoE3 quality software path ;
- cvs interoperability map / maturity model path.

Output of the program is :
- 5 cvs files for the metrics / measures / elements / dimensions / viewpoints.

Input in the Power BI dashboard : 
- 5 cvs files for the metrics / measures / elements / dimensions / viewpoints ;
- cvs interoperability map / maturity model path.

## Starting point

Start implementation with a subset of metrics and a single service. The service chosen is the Norwegian building service.

Service metadata: `https://www.geonorge.no/geonetwork/srv/nor/xml_iso19139?uuid=dc0f80e3-3f4d-486b-9393-da8244f37e47`

Dataset metadata: `https://www.geonorge.no/geonetwork/srv/nor/xml_iso19139?uuid=8b4304ea-4fb0-479c-a24d-fa225e2c6e97`

Endpoint: `https://wfs.geonorge.no/skwms1/wfs.inspire-bu-core2d_limited?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetCapabilities`

Spatineo Directory: `https://directory.spatineo.com/service/164572/`


## Source of the dashboard data

1. Dataset metadata (data provider)
2. Service metadata OR Service description Capabilities document (data or service provider)
3. Quality evaluation results (part of the GeoE3 project)
4. Service availability information (Spatineo)

Sources 1 and 2 are XML files that can be downloaded from wherever catalogues they reside from.

Source 3 data is provided by a Quality Software. The Quality software is based on FME and the workbench which analyses the actual contenst of the dataset. It could produce a machine readable file that the dashboard could read in. Currently, for each dataset, we are interested in the produced CSV result file that puts together the list and count of errors the software has identified. The products of the software should be downloaded from 'somewhere' - still undetermined where the software would run from and where the data would be stored.

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
$ conda config --add channels conda-forge
$ cd c:\whereever\this\project\is\geoe3-quality-dashboard\
$ conda install pytest lxml isodate==0.6.1
```
Then run "pip install XXX" with XXX being the modules listed in the requirements. 