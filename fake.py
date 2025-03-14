# Deepseek provided code to
import pandas as pd
from faker import Faker
import random

# Initialize Faker
fake = Faker()

# Function to generate synthetic data for the Department table


def generate_department_data(num_rows=100):
    data = {
        # Primary Key
        'DepartmentID': [fake.unique.random_number(digits=3) for _ in range(num_rows)],
        'DepartmentName': [fake.unique.company() for _ in range(num_rows)],
        'NumberOfEmployees': [fake.random_number(digits=3) for _ in range(num_rows)]
    }
    return pd.DataFrame(data)

# Function to generate synthetic data for the Project table


def generate_project_data(num_rows=100, department_ids=None):
    if department_ids is None:
        raise ValueError(
            "Department IDs must be provided for foreign key reference.")

    data = {
        # Primary Key
        'ProjectID': [fake.unique.random_number(digits=5) for _ in range(num_rows)],
        # Foreign Key
        'DepartmentID': [random.choice(department_ids) for _ in range(num_rows)],
        'ProjectName': [fake.catch_phrase() for _ in range(num_rows)],
        'ProjectStatus': [random.choice(['Active', 'Inactive', 'Completed']) for _ in range(num_rows)],
        'Budget': [fake.random_number(digits=6) for _ in range(num_rows)],
        'Stakeholder': [fake.name() for _ in range(num_rows)]
    }
    return pd.DataFrame(data)

# Function to generate synthetic data for the Employee table


def generate_employee_data(num_rows=100, department_ids=None):
    if department_ids is None:
        raise ValueError(
            "Department IDs must be provided for foreign key reference.")

    data = {
        # Primary Key
        'EmployeeID': [fake.unique.random_number(digits=5) for _ in range(num_rows)],
        'Address': [fake.address() for _ in range(num_rows)],
        'EmpName': [fake.name() for _ in range(num_rows)],
        # Foreign Key
        'DepartmentID': [random.choice(department_ids) for _ in range(num_rows)],
        'Designation': [fake.job() for _ in range(num_rows)],
        'ContractType': [random.choice(['Full-Time', 'Part-Time', 'Contract']) for _ in range(num_rows)],
        'TechQualification': [fake.boolean() for _ in range(num_rows)],
        'NonTechQualification': [fake.boolean() for _ in range(num_rows)],
        # Self-referencing Foreign Key
        'ManagerID': [fake.random_number(digits=5) for _ in range(num_rows)]
    }
    return pd.DataFrame(data)

# Function to generate synthetic data for the EmployeeContacts table


def generate_employee_contacts_data(num_rows=100, employee_ids=None):
    if employee_ids is None:
        raise ValueError(
            "Employee IDs must be provided for foreign key reference.")

    data = {
        # Foreign Key
        'EmployeeID': [random.choice(employee_ids) for _ in range(num_rows)],
        'Contacts': [fake.phone_number() for _ in range(num_rows)]
    }
    return pd.DataFrame(data)

# Function to generate synthetic data for the BenefitsPackage table


def generate_benefits_package_data(num_rows=100, employee_ids=None):
    if employee_ids is None:
        raise ValueError(
            "Employee IDs must be provided for foreign key reference.")

    data = {
        # Foreign Key
        'EmployeeID': [random.choice(employee_ids) for _ in range(num_rows)],
        'Benefits': [random.choice(['Gym', 'Insurance', 'Both']) for _ in range(num_rows)]
    }
    return pd.DataFrame(data)

# Function to generate synthetic data for the Interns table


def generate_interns_data(num_rows=100):
    data = {
        # Primary Key
        'CollegeID': [fake.unique.random_number(digits=5) for _ in range(num_rows)],
        'InternName': [fake.name() for _ in range(num_rows)]
    }
    return pd.DataFrame(data)

# Function to generate synthetic data for the ContractJob table


def generate_contract_job_data(num_rows=100, employee_ids=None):
    if employee_ids is None:
        raise ValueError(
            "Employee IDs must be provided for foreign key reference.")

    data = {
        # Primary Key
        'ContractID': [fake.unique.random_number(digits=5) for _ in range(num_rows)],
        # Foreign Key
        'EmployeeID': [random.choice(employee_ids) for _ in range(num_rows)]
    }
    return pd.DataFrame(data)

# Function to generate synthetic data for the Salary table


def generate_salary_data(num_rows=100, employee_ids=None):
    if employee_ids is None:
        raise ValueError(
            "Employee IDs must be provided for foreign key reference.")

    data = {
        # Foreign Key
        'EmployeeID': [random.choice(employee_ids) for _ in range(num_rows)],
        'PayrollDate': [fake.date_this_year() for _ in range(num_rows)],
        'SalaryAmount': [fake.random_number(digits=5) for _ in range(num_rows)]
    }
    return pd.DataFrame(data)


# Generate datasets
department_df = generate_department_data()
project_df = generate_project_data(
    department_ids=department_df['DepartmentID'])
employee_df = generate_employee_data(
    department_ids=department_df['DepartmentID'])
employee_contacts_df = generate_employee_contacts_data(
    employee_ids=employee_df['EmployeeID'])
benefits_package_df = generate_benefits_package_data(
    employee_ids=employee_df['EmployeeID'])
interns_df = generate_interns_data()
contract_job_df = generate_contract_job_data(
    employee_ids=employee_df['EmployeeID'])
salary_df = generate_salary_data(employee_ids=employee_df['EmployeeID'])

# Save datasets to CSV files
department_df.to_csv('data/department.csv', index=False)
project_df.to_csv('data/project.csv', index=False)
employee_df.to_csv('data/employee.csv', index=False)
employee_contacts_df.to_csv('data/employee_contacts.csv', index=False)
benefits_package_df.to_csv('data/benefits_package.csv', index=False)
interns_df.to_csv('data/interns.csv', index=False)
contract_job_df.to_csv('data/contract_job.csv', index=False)
salary_df.to_csv('data/salary.csv', index=False)

print("Synthetic datasets generated and saved to CSV files.")
