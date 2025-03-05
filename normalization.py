import pandas as pd
from itertools import combinations

df = pd.read_csv('employee_data.csv')

# Generate list of functional dependencies
def find_functional_dependencies(df):
    functional_dependencies = []
    attributes = df.columns.tolist()
    
    # Generate all possible combinations of attributes
    for r in range(1, len(attributes)):
        for determinant in combinations(attributes, r):
            determinant = set(determinant)
            remaining_attributes = set(attributes) - determinant
            
            # Check if determinant determines remaining attributes
            grouped = df.groupby(list(determinant))
            if all(len(group) == 1 for _, group in grouped):
                for attr in remaining_attributes:
                    functional_dependencies.append((determinant, attr))
    
    return functional_dependencies

print(find_functional_dependencies(df))