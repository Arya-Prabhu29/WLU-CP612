import pandas as pd
from functional_dependencies import *

df = pd.read_csv('employee_data.csv')

# Step 2: Check Normalization (1NF, 2NF, 3NF)
# NEEDS TO UPDATED TO POP functional_dependencies array is 2nf or 3f rules are broken
# More rules can be added
def check_normalization(df, functional_dependencies):
    # Check 1NF: Ensure atomicity of values
    is_1nf = all(df[col].apply(lambda x: isinstance(x, (int, float, str))).all() for col in df.columns)
    
    # Check 2NF: No partial dependencies
    is_2nf = True
    primary_key = {'StudentID'}  # Replace with your primary key
    for determinant, dependent in functional_dependencies:
        if not primary_key.issubset(determinant):
            is_2nf = False
            break
    
    # Check 3NF: No transitive dependencies
    is_3nf = True
    for determinant, dependent in functional_dependencies:
        if dependent in primary_key:
            continue
        if not primary_key.issubset(determinant):
            is_3nf = False
            break
    
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