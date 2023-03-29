"""Function to extract results from the model"""

import logging
import json 
import os
import pandas as pd
import lxml
from lxml import etree
from xml_ import *
from loader import load_API, load_dataset_metadata, load_cvs
from evaluate import evaluate, evaluate_categories




def read_rules_from_json(json_file):
    try:
        with open(json_file, "r") as f:
            structure_file = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error in {json_file} at line {e.lineno}, column {e.colno}: {e.msg}")
    return structure_file

def execute_load_API(rule,serviceId):
    """Executes the load_API function returns the apth to the XML temp file"""
    url = rule['url_start'] + serviceId
    api_data_path = load_API(url,serviceId)
    return api_data_path

# This function extracts values from the JSON structure file and applies execute_xpath_rule to the xpath rules. Returns a table.
def extract_all_info(my_dict, metadata_file, service_metadata_file, serviceId, qualityEvaluation_file, interoperability_file, func = None):
    model = {
        'dataset-metadata': load_dataset_metadata(metadata_file),
        'service-availability' : "",
        'service-metadata': load_dataset_metadata(service_metadata_file),
        'quality-evaluation': qualityEvaluation_file,
        'interoperability-maturity-model': interoperability_file
    }
    result = []
    table_data_Metrics = []
    table_data_VP = []
    table_data_Dimensions = []
    table_data_Elements = []
    table_data_Measures = []
    table_data_scores = []
    url_start_previous = ""
    for key1, value1 in my_dict.items():
        rowVP = {
            "Viewpoint": value1["name"],
            "Viewpoint_Weight": value1["weight"],
            "Viewpoint_Description": value1["description"]
        }
        table_data_VP.append(rowVP)
        for key2, value2 in value1.items():
            if key2 == "nodes":
                for key3, value3 in value2.items():
                    rowDimension = {
                        "Viewpoint": value1["name"],
                        "Dimension": value3["name"],
                         "Dimension_Weight": value3["weight"],
                         "Dimension_Description": value3["description"]
                    }
                    table_data_Dimensions.append(rowDimension)
                    for key4, value4 in value3.items():
                        if key4 == "nodes":
                            for key5, value5 in value4.items():
                                rowElement = {
                                    "Dimension": value3["name"],
                                    "Element": value5["name"],
                                    "Element_Weight": value5["weight"],
                                    "Element_Description": value5["description"],
                                }
                                table_data_Elements.append(rowElement)
                                for key6, value6 in value5.items():
                                    if key6 == "nodes":
                                        for key7, value7 in value6.items():
                                            rowMeasure = {
                                                "Element": value5["name"],
                                                "Measure": value7["name"],
                                                "Measure_Weight": value7["weight"],
                                                "Measure_Description": value7["description"]
                                            }
                                            table_data_Measures.append(rowMeasure)
                                            for key8, value8 in value7.items():
                                                if key8 == "nodes":
                                                    for key9, value9 in value8.items():
                                                        for key10, value10 in value9.items():
                                                            if key10 == "extractionRule":
                                                                row = {
                                                                    "Measure": value7["name"],
                                                                    "Metric": value9["name"],
                                                                    "Metric_Weight": value9["weight"],
                                                                    "Metric_Description": value9["description"],
                                                                    "Extraction_Rule": value9["extractionRule"],
                                                                    "Evaluation_Rule": value9["evaluationRule"]
                                                                }
                                                                if func:
                                                                    if value10["source"] == "service-availability":
                                                                        url_start = value10["url_start"]
                                                                        if url_start != url_start_previous:
                                                                            api_file = execute_load_API(row["Extraction_Rule"],serviceId)
                                                                            url_start_previous = url_start
                                                                        model = {
                                                                            'dataset-metadata': load_dataset_metadata(metadata_file),
                                                                            'service-metadata' : load_dataset_metadata(service_metadata_file),
                                                                            'service-availability' : load_dataset_metadata(api_file),
                                                                            'quality-evaluation': qualityEvaluation_file,
                                                                            'interoperability-maturity-model': interoperability_file
                                                                        }
                                                                        row["Extraction_Rule_value"] = func(row["Extraction_Rule"],model,api_file,serviceId)   
                                                                    elif value10["source"] == "quality-evaluation":
                                                                        row["Extraction_Rule_value"] = func(row["Extraction_Rule"],model,qualityEvaluation_file,serviceId)                                              
                                                                    elif value10["source"] == "dataset-metadata":
                                                                        row["Extraction_Rule_value"] = func(row["Extraction_Rule"],model,metadata_file,serviceId)
                                                                    elif value10["source"] == "service-metadata":
                                                                        row["Extraction_Rule_value"] = func(row["Extraction_Rule"],model,service_metadata_file,serviceId)
                                                                    elif value10["source"] == "interoperability-maturity-model":
                                                                       row["Extraction_Rule_value"] = func(row["Extraction_Rule"],model,interoperability_file,serviceId)                                                                   
                                                            if key10 == "evaluationRule":
                                                                value = row["Extraction_Rule_value"]
                                                                evaluationRule = value9["evaluationRule"]
                                                                if "type" in evaluationRule:
                                                                    if value10["type"] == "presence":
                                                                        row["Score"] = evaluate(evaluationRule,value,'','')
                                                                    elif value10["type"] == "date" or value10["type"] == "range":
                                                                        min = value10["minimum"]
                                                                        max = value10["maximum"]
                                                                        row["Score"] = evaluate(evaluationRule,value, min,max)   
                                                                    elif value10["type"] == "comparison":
                                                                        operator = value10["operator"]
                                                                        referenceValue = value10["referenceValue"]
                                                                        row["Score"] = evaluate(evaluationRule, value,operator,referenceValue)                                                
                                                                    elif value10["type"] == "comparisonDependent":
                                                                        temp_df = pd.DataFrame(table_data_Metrics)
                                                                        row["Score"] = evaluate(evaluationRule,value, temp_df, value10["dependentOn"])
                                                                    #For the MatchMaintenanceExpected metric but not sure I can compare it to any 'maintenance date'...
                                                                    '''elif value10["type"] == "maintenance":
                                                                        temp_df = pd.DataFrame(table_data)
                                                                        row["Score"] = evaluate(evaluationRule,value, frequency_code, '')'''
                                                            
                                                                table_data_Metrics.append(row)
    metrics = pd.DataFrame(table_data_Metrics)
    VP = pd.DataFrame(table_data_VP)
    D = pd.DataFrame(table_data_Dimensions)
    E = pd.DataFrame(table_data_Elements)
    M = pd.DataFrame(table_data_Measures)
    M,E,D,VP = evaluate_categories(metrics,M,E,D,VP)
    '''Delete the temp file created to contain the API data'''
    try:
        os.remove(api_file)
        print(f"Service availability temp file from API has been deleted.")
    except OSError as error:
        print(error)

    return metrics, M,E,D,VP

def extract_rule(rule, model,metadata,serviceId):
    extractor = extractor_by_type[rule['type']]
    if extractor is None:
        raise f"Unknown rule extractor type {rule['type']}"
    return extractor(rule, model,metadata,serviceId)

# This function executes xpath extraction rules
def execute_xpath_rule(rule, model,file,serviceId=None):
    """Executes xpath extraction rule and returns the result value"""
    def extract_all_text(node_or_nodes, delimiter=' '):
        """extracts all non-whitespace text from an etree node or list of etree nodes"""
        def flatten(list_of_lists):
            return [item for sublist in list_of_lists for item in sublist]
        if isinstance(node_or_nodes, list):
            nodes = node_or_nodes
        else:
            nodes = [node_or_nodes]
        tmp = [
            [
                str(value) for value in filter(lambda str : str != '',
                map(lambda str : str.strip(), node.xpath(".//text()")))
            ]
            if isinstance(node, lxml.etree._Element)
            else [str(node) if not isinstance(node, float) else str(int(node))]
            for node in nodes
        ]
        return delimiter.join(flatten(tmp))

    source = model[rule['source']]
    xpath_rule = rule['rule']
    value_method = rule['value']
    result = source.xpath(xpath_rule, namespaces=ns)
    if value_method == 'text':
        result = extract_all_text(result)
    else:
        logging.warning('Unknown value extraction method (%s) in extractionRule', value_method)
    return result

def execute_formula_rule(rule,model,file,serviceId=None):
    """Executes formula extraction rule and returns the result value"""
    formula = rule['rule']
    rows = load_cvs(file)
    # Iterate over the rows to find the desired value
    for row in rows:
        if len(row) > 1 and row[1] == formula:
            if len(row) > 2:
                result = row[2]
                return result
    return 0 # Because if nothing is returned by the process, it means no error was found

extractor_by_type = {
    'xpath': execute_xpath_rule,
    'formula' : execute_formula_rule
}

if __name__ == "__main__":
    clear = lambda: os.system('cls')
    clear()

    #metadata_file = input("Please enter the path to Metadatafile :")
    metadata_file = 'MD_Bui_EX_1.xml'
    service_metadata_file = 'SMD_Bui_EX_1.xml'
    qualityEvaluation_file = 'C:/Users/CCOSSEC/Work Folders/Evaluator configuration/geoe3-quality-dashboard/geoe3-quality-dashboard/src/buildings_and_errors/results_NO_cc.csv'
    serviceId = input("Please enter the service ID (list of service Id : 39859,164572,157386,88383,157353) :")
    interoperability_file = 'C:/Users/CCOSSEC/Work Folders/Evaluator configuration/geoe3-quality-dashboard/geoe3-quality-dashboard/src/interoperability_maturityModel.csv'

    # Read the JSON file structuring the dashboard
    structure_file = read_rules_from_json("C:/Users/CCOSSEC/Work Folders/Evaluator configuration/geoe3-quality-dashboard/geoe3-quality-dashboard/Dashboard_structure.json")
    
    # Define model object
    model = {
        'dataset-metadata': load_dataset_metadata(metadata_file),
        'service-availability': 0,
        'service-metadata': load_dataset_metadata(service_metadata_file),
        'quality-evaluation': load_cvs(qualityEvaluation_file),
        'interoperability-maturity-model': load_cvs(interoperability_file)
    }

    extractionRule_table = extract_all_info(structure_file, metadata_file, service_metadata_file, serviceId, qualityEvaluation_file, interoperability_file, func = extract_rule)
    print(extractionRule_table)

    # save the DataFrame to an Excel file
    extractionRule_table.to_excel('my_data.xlsx', index=False)
