import pandas as pd
import glob
import os

# Define the path to your CSV files
csv_files = glob.glob("ddg_*averaged.csv")

# Loop through each file and process
for file in csv_files:
    # Extract the protein name from the filename
    base_name = os.path.basename(file)
    protein_name = base_name.split("_")[1]  # Extract the part after 'ddg_' and before '_averaged.csv'

    # Read the CSV file
    df = pd.read_csv(file)
    
    # Select the desired columns
    selected_columns = df[['ligand1', 'ligand2', 'exp_ddG', 'avg_ddG','std_ddG','MAE']]
    
    # Create the new filename
    output_file = os.path.join(
        "./", 
        f"ddG_{protein_name}_GAFF2.csv"
    )
    
    # Save the processed file
    selected_columns.to_csv(output_file, index=False)

