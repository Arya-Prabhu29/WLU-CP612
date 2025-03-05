import pandas as pd
from itertools import combinations

df = pd.read_csv('employee.csv')


def check_is_1nf(df):
    """
    Check if the given functional dependencies satisfy 1NF.

    Args:
        df (dataframe): the current data frame being analyzed

    Returns:
        bool: True if the table is in 1NF, False otherwise.
    """
    return all(df[col].apply(lambda x: isinstance(x, (int, float, str))).all() for col in df.columns)


def check_is_2nf(functional_dependencies, primary_key):
    """
    Check if the given functional dependencies satisfy 2NF.

    Args:
        functional_dependencies (list of tuples): List of (determinant, dependent) pairs.
        primary_key (set): The primary key of the table.

    Returns:
        bool: True if the table is in 2NF, False otherwise.
    """
    for determinant, dependent in functional_dependencies:
        # Check if the determinant is a subset of the primary key
        if not primary_key.issubset(determinant):
            return False  # Partial dependency found, not in 2NF
    return True  # No partial dependencies, table is in 2NF


def check_is_3nf(functional_dependencies, primary_key):
    """
    Check if the given functional dependencies satisfy 3NF.

    Args:
        functional_dependencies (list of tuples): List of (determinant, dependent) pairs.
        primary_key (set): The primary key of the table.

    Returns:
        bool: True if the table is in 3NF, False otherwise.
    """
    for determinant, dependent in functional_dependencies:
        # Skip if the dependent is part of the primary key
        if dependent in primary_key:
            continue
        # Check if the determinant is a superset of the primary key
        if not primary_key.issubset(determinant):
            return False  # Transitive dependency found, not in 3NF
    return True  # No transitive dependencies, table is in 3NF

# Generates all possible depedencies

# HINT: 
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
            # Convert tuple to set for easier operations
            determinant = set(determinant)
            # Attributes not in determinant
            remaining_attributes = set(attributes) - determinant

            # Group DataFrame by determinant attributes
            grouped = df.groupby(list(determinant))

            # Check if determinant uniquely determines remaining attributes
            if all(len(group) == 1 for _, group in grouped):
                for attr in remaining_attributes:
                    functional_dependencies.append((determinant, attr))

    return functional_dependencies

# Step 2: Check Normalization (1NF, 2NF, 3NF)
# 1. NEEDS TO UPDATED TO POP functional_dependencies array is 2nf or 3f rules are broken
# 2. ONLY CHECKS FOR PRIMARY KEY StudentID
# 3. Needs to check for forgein keys


def check_normalization(df, functional_dependencies):
    # Check 1NF: Ensure atomicity of values
    is_1nf = check_is_1nf(df)

    # Check 2NF: No partial dependencies
    is_2nf = True
    # NEEDS TO BE UPDATED FOR EVERY TABLE
    primary_key = {'EmployeeID'}  # Replace with your primary key
    is_2nf = check_is_2nf(functional_dependencies, primary_key)
    # break

    # Check 3NF: No transitive dependencies
    is_3nf = True
    is_3nf = check_is_3nf(functional_dependencies, primary_key)

    return is_1nf, is_2nf, is_3nf


# Main execution
if __name__ == "__main__":
    # Find functional dependencies
    fds = find_functional_dependencies(df)

    print("Functional Dependencies:")
    print("All possible functional dependencies: ", len(fds))
    # for fd in fds[100:120]:
    #     print(f"{fd[0]} -> {fd[1]}")

    # Check normalization
    is_1nf, is_2nf, is_3nf = check_normalization(df, fds)
    print("\nNormalization Analysis:")
    print(f"1NF: {'Yes' if is_1nf else 'No'}")
    print(f"2NF: {'Yes' if is_2nf else 'No'}")
    print(f"3NF: {'Yes' if is_3nf else 'No'}")
