'''Scoring method :
- Scores are calculated from 0 to 5, 5 being the best.
- 0 is reserved for an absence of value.
- 5 means that the condition is fully met.

    For dates :
    - A period is checked
    - if the extracted date is within the range : 5/5
    - if the extracted date is less than 1 month outside the range : 4/5
    - if the extracted date is less than 1 year outside the range : 3/5
    - if the extracted date is less than 5 years outside the range : 2/5
    - if the extracted date is more than 2 years outside the range : 1/5

    For ranges and comparisons:
    - if the extracted value is within the range : 5/5
    - if the extracted value is less than 5% outside the range : 4/5
    - if the extracted value is less than 10% outside the range : 3/5
    - if the extracted value is less than 20% outside the range : 2/5
    - if the extracted value is more than 20% outside the range : 1/5

    For aggregation of metric, measures, elements, dimensions, viewpoints :
    - Score is calculated by weigted average of the scores of the categories that are one level down.

'''

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Evaluate presence of a value : 0 if not / 5 if yes
def evaluate_presence(rule, value, min,max):
    if value:
        return 5  # score of 5 out of 5 for a non-empty value
    else:
        return 0  # score of 0 out of 5 for an empty value

# Evaluate that the date is between two requested dates of a value : 1 if not / 5 if yes
def evaluate_date(rule, value, minimum, maximum):
    extracted_date = datetime.strptime(value, '%Y-%m-%d').date()
    min_date = datetime.strptime(minimum, '%Y-%m-%d').date()
    max_date = datetime.strptime(maximum, '%Y-%m-%d').date()
    time_diff = abs(extracted_date - min_date)
    if time_diff < timedelta(days=30):
        return 4  # score of 4 out of 5 for a date within 1 month of the range
    elif time_diff < timedelta(days=365):
        return 3  # score of 3 out of 5 for a date within 1 year of the range
    elif time_diff < timedelta(days=1825):
        return 2  # score of 2 out of 5 for a date within 5 years of the range
    if min_date <= extracted_date <= max_date:
        return 5  # score of 5 out of 5 for a valid date
    return 1  # score of 1 out of 5 for an invalid date

# Evaluate that the extracted value is in a range : 1 if not / 5 if yes
def evaluate_range(rule, value, minimum, maximum):
    value = float(value)
    minimum = float(minimum)
    maximum = float(maximum)
    range_size = maximum - minimum
    if isinstance(value, (int, float)):
        if minimum <= value <= maximum:
            return 5  # score of 5 out of 5 for a value within the range
        diff = abs(value - ((minimum + maximum) / 2))
        percentage_diff = diff / range_size
        if percentage_diff <= 0.05:
            return 4  # score of 4 out of 5 for a value within 5% of the range
        elif percentage_diff <= 0.1:
            return 3  # score of 3 out of 5 for a value within 10% of the range
        elif percentage_diff <= 0.2:
            return 2  # score of 2 out of 5 for a value within 20% of the range
    return 1  # score of 1 out of 5 for a value outside the range or not numeric


# Evaluate that the extracted value is in a range : 1 if not / 5 if yes
def evaluate_comparison(rule, value, operator, reference_value):
    if operator == "is":
        value = str(value)
        if value == reference_value:
            return 5  # score of 5 out of 5 for a value equal to the reference value
    else:
        value = float(value)
        reference_value = float(reference_value)
        diff = abs(value - reference_value)
        percent_diff = diff / reference_value * 100
        if operator == ">":
            if value > reference_value:
                return 5  # score of 5 out of 5 for a value greater than the reference value
            elif percent_diff <= 5:
                return 4  # score of 4 out of 5 for a value within 5% of the reference value
            elif percent_diff <= 10:
                return 3  # score of 3 out of 5 for a value within 10% of the reference value
            elif percent_diff <= 20:
                return 2  # score of 2 out of 5 for a value within 20% of the reference value
        elif operator == ">=":
            if value >= reference_value:
                return 5  # score of 5 out of 5 for a value greater than or equal to the reference value
            elif percent_diff <= 5:
                return 4  # score of 4 out of 5 for a value within 5% of the reference value
            elif percent_diff <= 10:
                return 3  # score of 3 out of 5 for a value within 10% of the reference value
            elif percent_diff <= 20:
                return 2  # score of 2 out of 5 for a value within 20% of the reference value
        elif operator == "<":
            if value < reference_value:
                return 5  # score of 5 out of 5 for a value less than the reference value
            elif percent_diff <= 5:
                return 4  # score of 4 out of 5 for a value within 5% of the reference value
            elif percent_diff <= 10:
                return 3  # score of 3 out of 5 for a value within 10% of the reference value
            elif percent_diff <= 20:
                return 2  # score of 2 out of 5 for a value within 20% of the reference value
        elif operator == "<=":
            if value <= reference_value:
                return 5  # score of 5 out of 5 for a value less than or equal to the reference value
            elif percent_diff <= 5:
                return 4  # score of 4 out of 5 for a value within 5% of the reference value
            elif percent_diff <= 10:
                return 3  # score of 3 out of 5 for a value within 10% of the reference value
            elif percent_diff <= 20:
                return 2  # score of 2 out of 5 for a value within 20% of the reference value
        elif operator == "==":
            if value == reference_value:
                return 5  # score of 5 out of 5 for a value equal to the reference value
        return 1  # score of 1 out of 5 for any other case

def evaluate_comparisonDependent(rule, value, df, index):
    value = float(value)
    refvalue_column = 'Extraction_Rule_value'
    dependent_on = df.loc[df['Metric'] == index , refvalue_column].iloc[0]
    multiplier = float(rule["multiplier"])
    operator_func = rule["operator"]
    result = evaluate_comparison(rule,value, operator_func, float(dependent_on)*multiplier)
    return result

def evaluate_maintenance(rule, maintenance_date, frequency_code, tt):
    if frequency_code in ['asNeeded', 'irregular', 'notPlanned', 'unknown']:
        return 5  # return None if declared frequency is not a fixed interval

    maintenance_date = datetime.fromisoformat(maintenance_date)
    current_date = datetime.now()
    time_diff = current_date - maintenance_date

    if frequency_code == 'continual':
        if time_diff < timedelta(days=1): return 5
        elif time_diff < timedelta(days=1.5): return 4
        elif time_diff < timedelta(days=2): return 3
        elif time_diff < timedelta(days=3): return 2
    elif frequency_code == 'daily':
        if time_diff <= timedelta(days=1): return 5
        elif time_diff <= timedelta(days=2): return 4
        elif time_diff <= timedelta(days=3): return 3
        elif time_diff <= timedelta(days=7): return 2
    elif frequency_code == 'weekly':
        if time_diff <= timedelta(days=7): return 5
        elif time_diff <= timedelta(days=10): return 4
        elif time_diff <= timedelta(days=14): return 3
        elif time_diff <= timedelta(days=21): return 2
    elif frequency_code == 'fortnightly':
        if time_diff <= timedelta(days=14): return 5
        elif time_diff <= timedelta(days=21): return 4
        elif time_diff <= timedelta(days=28): return 3
        elif time_diff <= timedelta(days=35): return 2
    elif frequency_code == 'monthly':
        if time_diff <= timedelta(days=31): return 5
        elif time_diff <= timedelta(days=62): return 4
        elif time_diff <= timedelta(days=93): return 3
        elif time_diff <= timedelta(days=124): return 2
    elif frequency_code == 'quarterly':
        if time_diff <= timedelta(days=93): return 5
        elif time_diff <= timedelta(days=124): return 4
        elif time_diff <= timedelta(days=155): return 3
        elif time_diff <= timedelta(days=186): return 2
    elif frequency_code == 'biannualy':
        if time_diff <= timedelta(days=182): return 5
        elif time_diff <= timedelta(days=242): return 4
        elif time_diff <= timedelta(days=302): return 3
        elif time_diff <= timedelta(days=365): return 2
    elif frequency_code == 'annualy':
        if time_diff <= timedelta(days=365): return 5
        elif time_diff <= timedelta(days=548): return 4
        elif time_diff <= timedelta(days=731): return 3
        elif time_diff <= timedelta(days=914): return 2
    else: return 0

    # Check if last_maintenance_date is not empty
    if last_maintenance_date:
        # Convert the date string to a datetime object
        last_maintenance_date = datetime.fromisoformat(last_maintenance_date[0].attrib["valueDateTime"])
        
        # Check if the last maintenance date is within the past 24 hours
        if last_maintenance_date >= datetime.now() - timedelta(days=1):
            # The rule is satisfied
            return 5
        else:
            # The rule is not satisfied
            return 1
    else:
        return 0


def evaluate(rule,value,min,max):
    if value is None or value == '':
        return 0 # the value is missing, assign the minimum score
    else :
        evaluator = evaluator_by_type[rule['type']]
        if evaluator is None:
            raise f"Unknown rule evaluator type {rule['type']}"
        return evaluator(rule,value,min,max)



evaluator_by_type = {
    'date': evaluate_date,
    'presence' : evaluate_presence,
    'comparison': evaluate_comparison,
    'comparisonDependent': evaluate_comparisonDependent,
    'range': evaluate_range,
    'maintenance': evaluate_maintenance
}

# Score each category of quality element
def evaluate_categories(metrics,M,E,D,VP):

    # calculate measure scores
    measure_score = metrics.groupby(['Measure']) \
                    .apply(lambda x: sum(x['Score'] * x['Metric_Weight']) / sum(x['Metric_Weight'])) \
                    .reset_index(name='Measure_Score')

    # join measure scores back to original dataframe
    M = pd.merge(M, measure_score, on=['Measure'])

    # calculate element scores
    element_scores = M.groupby(['Element']) \
                    .apply(lambda x: sum(x['Measure_Score'] * x['Measure_Weight']) / sum(x['Measure_Weight'])) \
                    .reset_index(name='Element_Score')
    E = pd.merge(E, element_scores, on=['Element'])

    # calculate dimension scores
    dimension_scores = E.groupby(['Dimension']) \
                        .apply(lambda x: sum(x['Element_Score'] * x['Element_Weight']) / sum(x['Element_Weight'])) \
                        .reset_index(name='Dimension_Score')
    D = pd.merge(D, dimension_scores, on=['Dimension'])
    # calculate viewpoint scores
    viewpoint_scores = D.groupby(['Viewpoint']) \
                        .apply(lambda x: sum(x['Dimension_Score'] * x['Dimension_Weight']) / sum(x['Dimension_Weight'])) \
                        .reset_index(name='Viewpoint_Score')
    VP = pd.merge(VP, viewpoint_scores, on=['Viewpoint'])

    return M,E,D,VP