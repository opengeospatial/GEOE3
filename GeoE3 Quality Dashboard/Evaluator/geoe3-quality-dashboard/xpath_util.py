"""This is a test utility script that can be used to manually perform trials"""

from datetime import datetime

from src.extract import extract_rule
from src.evaluate import evaluate_results
from src.loader import load_dataset_metadata

# Documentation: https://docs.python.org/3/library/xml.etree.elementtree.html#xpath-support
# https://inspire.ec.europa.eu/reports/ImplementingRules/metadata/MD_IR_and_ISO_20081219.pdf


# Produced for each service list row
test_model = {
  'dataset-metadata': load_dataset_metadata('example-metadata/Dataset MD Bui-ES-5.xml'),
  'service-metadata': None,
  'quality-evaluation': None,
  'availability-data': None
}

# This is the metric/dimension/etc from the configuration
test_rule = {
  'extractionRule': {
    'source': "dataset-metadata",
    'type': "xpath",
    'rule': "gmd:identificationInfo[1]/*/gmd:citation/*/gmd:date[./*/gmd:dateType/*/text()='publication']/*/gmd:date",
    'value': "text"
  },
  'evaluationCriteria': {
    'type': 'date-not-older-than',
    'duration': 'P6M'
  }
}

# This context defines values from the current contaxt that rule evaluation criteria might
# be evaluated against
test_context = {
  'now': datetime.now()
}

## The process
#
# input: model + config + context
#  * model   = data derived from the dataset list
#  * config  = quality dashboard configuration file
#  * context = surrounding runtime context (e.g. current time)
#
# function: Extract         _ Evaluate
#                  \        /|        \
#                  _\|     /          _\|
# data:              result              value


result = extract_rule(test_rule['extractionRule'], test_model)
print(f"value extracted via extraction rule: {result}")

value = evaluate_results(test_rule['evaluationCriteria'], result, test_context)
print(f"evaluated value: {value}")