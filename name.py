import os
import pandas as pd


# Step 1: Get the list of file names in the given path
def get_file_names(directory_path):
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    return [os.path.splitext(f)[0] for f in files]

# Step 2: Read "KPJ" sheet from Excel file into a pandas DataFrame
def read_excel_to_dataframe(excel_file_path):
    df = pd.read_excel(excel_file_path, sheet_name='KPJ')
    return df

# Step 3: Remove "-2" suffix from file names
def remove_suffix(file_names):
    return [name[:-2] if name.endswith('_2') else name for name in file_names]

# Step 4: Filter DataFrame based on conditions
def filter_dataframe(df, file_names):
    filtered_list = []
    for file_name in file_names:
        if file_name in df['ClaimNo'].values:
            filtered_list.append(file_name)
    return filtered_list

# Step 5: Rename PDF files with "_KPJ" suffix
def rename_pdf_files(directory_path, filtered_list):
    for file_name in filtered_list:
        old_path = os.path.join(directory_path, file_name + ".pdf")
        new_path = os.path.join(directory_path, file_name + "_KPJ.pdf")
        os.rename(old_path, new_path)


# Example usage
if __name__ == "__main__":
    # Provide the file path
    directory_path = os.environ.get("BILL_DIR", "C:/Users/CP1/Downloads/Bill/Bill")
    excel_file_path = os.environ.get("CLAIM_XLSX", "C:/Users/CP1/Downloads/claim_v1.xlsx")

    # Step 1: Get the list of file names
    file_names = get_file_names(directory_path)

    # Step 2: Read Excel file into DataFrame
    df = read_excel_to_dataframe(excel_file_path)

    # Step 3: Remove "-2" suffix from file names
    file_names = remove_suffix(file_names)

    # Step 4: Filter DataFrame based on conditions
    filtered_list = filter_dataframe(df, file_names)

    # Print the result
    print("Filtered List:", filtered_list)

    # Step 5: Rename PDF files with "_KPJ" suffix
    rename_pdf_files(directory_path, filtered_list)

    # Print the result
    print("PDF files renamed successfully.")
