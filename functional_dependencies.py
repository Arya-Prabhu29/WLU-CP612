import pandas as pd
from itertools import combinations



def find_functional_dependencies(df):
    """
    Identifies functional dependencies in a given DataFrame.
    
    A functional dependency exists if a set of attributes (the determinant)
    uniquely determines another attribute.

    Parameters:
    df (pd.DataFrame): The input DataFrame to analyze.

    Returns:
    list of tuples: A list of functional dependencies represented as tuples.
                    Each tuple consists of a determinant (set of attributes)
                    and a determined attribute.
    """
    functional_dependencies = []  # Stores discovered functional dependencies
    attributes = df.columns.tolist()  # Get list of column names
    
    # Generate all possible combinations of attributes (excluding empty and full set)
    for r in range(1, len(attributes)):
        for determinant in combinations(attributes, r):
            determinant = set(determinant)  # Convert tuple to set for easier operations
            remaining_attributes = set(attributes) - determinant  # Attributes not in determinant
            
            # Group DataFrame by determinant attributes
            grouped = df.groupby(list(determinant))
            
            # Check if determinant uniquely determines remaining attributes
            if all(len(group) == 1 for _, group in grouped):
                for attr in remaining_attributes:
                    functional_dependencies.append((determinant, attr))
    
    return functional_dependencies

# Testing
# func_dependencies = find_functional_dependencies(df)

# for dependency in func_dependencies:
#     print(dependency)