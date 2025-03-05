import pandas as pd
from itertools import combinations
from pathlib import Path


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
        # Check if the determinant is a proper subset of the primary key
        if determinant.issubset(primary_key) and determinant != primary_key:
            # If the dependent is a non-prime attribute, it violates 2NF
            if dependent not in primary_key:
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

# Generates all possible dependencies


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


def check_normalization(df, functional_dependencies, primary_key):
    # Check 1NF: Ensure atomicity of values
    is_1nf = check_is_1nf(df)

    # Check 2NF: No partial dependencies
    is_2nf = check_is_2nf(functional_dependencies, primary_key)

    # Check 3NF: No transitive dependencies
    is_3nf = check_is_3nf(functional_dependencies, primary_key)

    return is_1nf, is_2nf, is_3nf


# Main execution
if __name__ == "__main__":

    # Specify the folder path
    folder_path = Path('data')

    # Get a list of all files in the folder
    files = [f for f in folder_path.iterdir() if f.is_file()]

    print(files)

    for file in files:
        print("Analysis for ", file.name)
        df = pd.read_csv(file)  # Use the full path to the file

        # Determine the primary key based on the file path
        if file.name == 'benefits_package.csv':
            primary_key = {'EmployeeID'}
        elif file.name == 'contract_job.csv':
            primary_key = {'ContractID', 'EmployeeID'}
        elif file.name == 'department.csv':
            primary_key = {'DepartmentID'}
        elif file.name == 'employee.csv':
            primary_key = {'EmployeeID'}
        elif file.name == 'employee_contacts.csv':
            primary_key = {'EmployeeID'}
        elif file.name == 'interns.csv':
            primary_key = {'CollegeID', 'InternName'}
        elif file.name == 'project.csv':
            primary_key = {'ProjectID'}
        elif file.name == 'salary.csv':
            primary_key = {'EmployeeID', 'PayrollDate'}
        else:
            primary_key = set()  # Default to an empty set if no match

        # Find functional dependencies
        fds = find_functional_dependencies(df)

        print("Functional Dependencies:")
        print("All possible functional dependencies: ", len(fds))

        # Check normalization
        is_1nf, is_2nf, is_3nf = check_normalization(df, fds, primary_key)
        print("\nNormalization Analysis:")
        print(f"1NF: {'Yes' if is_1nf else 'No'}")
        print(f"2NF: {'Yes' if is_2nf else 'No'}")
        print(f"3NF: {'Yes' if is_3nf else 'No'}")
        print("***************************")
