import pandas as pd
from itertools import combinations

df = pd.read_csv('employee.csv')

# WE NEED TO ADD A CHECK TO DETERMINE MAKE SURE WE DONT MAKE COMBINATIONS WITH PRIMARY KEYS
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

normalization2_violations = []
normalization3_violations = []

# Step 2: Check Normalization (1NF, 2NF, 3NF)
# NEEDS TO UPDATED TO POP functional_dependencies array is 2nf or 3f rules are broken
# More rules can be added
# ONLY CHECKS FOR PRIMARY KEY StudentID
def check_normalization(df, functional_dependencies):
    # Check 1NF: Ensure atomicity of values
    is_1nf = all(df[col].apply(lambda x: isinstance(x, (int, float, str))).all() for col in df.columns)
    
    # Check 2NF: No partial dependencies
    is_2nf = True
    # NEEDS TO BE UPDATED FOR EVERY TABLE
    primary_key = {'EmployeeID'}  # Replace with your primary key
    for determinant, dependent in functional_dependencies:
        if not primary_key.issubset(determinant):
            is_2nf = False
            normalization2_violations.append((determinant, dependent)) 
            # break
    
    # Check 3NF: No transitive dependencies
    is_3nf = True
    for determinant, dependent in functional_dependencies:
        if dependent in primary_key:
            continue
        # If 3NF is violated
        if not primary_key.issubset(determinant):
            is_3nf = False
            print(f"{determinant} -> {dependent}")
            normalization3_violations.append((determinant, dependent)) 
            # break
    
    return is_1nf, is_2nf, is_3nf

# Main execution
if __name__ == "__main__":
    # Find functional dependencies
    fds = find_functional_dependencies(df)
    
    # print("Functional Dependencies:")
    # for fd in fds:
    #     print(f"{fd[0]} -> {fd[1]}")
    
    # Check normalization
    is_1nf, is_2nf, is_3nf = check_normalization(df, fds)
    print("\nNormalization Analysis:")
    print(f"1NF: {'Yes' if is_1nf else 'No'}")
    print(f"2NF: {'Yes' if is_2nf else 'No'}")
    print(f"3NF: {'Yes' if is_3nf else 'No'}")
    
    # Print out violators
    # print(len(normalization2_violations))
    # print(len(normalization3_violations))