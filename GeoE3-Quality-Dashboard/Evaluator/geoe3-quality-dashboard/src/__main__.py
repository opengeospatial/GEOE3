import os
from loader import load_dataset_metadata
from loader import load_cvs
from extract import read_rules_from_json
from extract import extract_all_info
from extract import extract_rule
from datetime import datetime

def main():
    clear = lambda: os.system('cls')
    clear()

    # INPUT :
    # Location of files :
    metadata_file = input("Please enter the path to Metadata file (eg. 'MD_Bui_EX_1.xml'):")
    service_metadata_file = input("Please enter the path to Service Metadata file (eg.'SMD_Bui_EX_1.xml'):")
    qualityEvaluation_file = input("Please enter the path to Quality Evaluation Software file (eg. 'buildings_and_errors/results_NO_cc.csv'): ")
    interoperability_file = input("Please enter the path to Metadatafile (eg. 'interoperability_maturityModel.csv'): ") 
    # Service ID (interoperability_maturityModel.csv to check what dataset has which serviceId)
    serviceId = input("Please enter the service ID (list of service Id : 39859,164572,157386,88383,157353) :")

    ''' 
    For testing :
    metadata_file = 'MD_Bui_EX_1.xml'
    service_metadata_file = 'SMD_Bui_EX_1.xml'
    interoperability_file = 'interoperability_maturityModel.csv'
    qualityEvaluation_file = 'buildings_and_errors/results_NO_cc.csv'
    serviceId = '164572'
    '''

    # Read rules from JSON file that describes the structure of the dashboard and its rules.
    structure_file = read_rules_from_json("Dashboard_structure.json")

    # Define model object
    model = {
    'dataset-metadata': load_dataset_metadata(metadata_file),
    'service-availability': 0,
    'service-metadata': load_dataset_metadata(service_metadata_file),
    'quality-evaluation': load_cvs(qualityEvaluation_file),
    'interoperability_map': load_cvs(interoperability_file)
    }
    # Extract rules from Structure file (JSON) and executes them. Result is a Dataframe table
    scores_table, M, E, D, VP = extract_all_info(structure_file, metadata_file, service_metadata_file, serviceId, qualityEvaluation_file,interoperability_file, func = extract_rule)
    
    # Save the DataFrames to csv files in one folder
    folder_name = serviceId + '_' + metadata_file.replace('.xml', '') + '_' + datetime.now().strftime('%Y%m%d_%H%M%S')
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    name_excel_file = metadata_file.replace('.xml', '')
    scores_table.to_csv(os.path.join(folder_name, 'Metrics'+'.csv'), index=False)
    VP.to_csv(os.path.join(folder_name, 'VP' + '.csv'), index=False)
    D.to_csv(os.path.join(folder_name, 'Dimensions' + '.csv'), index=False)
    E.to_csv(os.path.join(folder_name, 'Elements' + '.csv'), index=False)
    M.to_csv(os.path.join(folder_name, 'Measures' + '.csv'), index=False)
    print('Results have been saved in a folder named : ', folder_name)






if __name__ == '__main__':
    main()