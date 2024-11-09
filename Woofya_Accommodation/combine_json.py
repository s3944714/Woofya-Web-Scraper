import os
import json

def combine_json_files(input_directory, output_file):
    combined_data = []

    # Iterate through all files in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith('.json'):
            file_path = os.path.join(input_directory, filename)
            with open(file_path, 'r') as file:
                try:
                    data = json.load(file)
                    combined_data.extend(data)  # Add the data to the combined list
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from {file_path}: {e}")

    # Write the combined data to the output file
    with open(output_file, 'w') as outfile:
        json.dump(combined_data, outfile, indent=4)

    print(f"Combined JSON data has been written to {output_file}")

if __name__ == "__main__":
    input_directory = 'Scrapers/Raw_Data'  # Path to the directory containing the JSON files
    output_file = 'combined_data.json'  # Name of the output file

    combine_json_files(input_directory, output_file)
