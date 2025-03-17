import argparse
import os

def validate_config(input_files, default_file):
    """
    Validates input configuration files against a default configuration.

    Args:
        input_files (list): List of input configuration file paths.
        default_file (str): Path to the default configuration file.
    """

    if not os.path.exists(default_file):
        print(f"Error: Default configuration file '{default_file}' not found.")
        exit(1)

    with open(default_file, 'r') as f_default:
        expected_content = f_default.read()

    for input_file in input_files:
        if not os.path.exists(input_file):
            print(f"Warning: Input file '{input_file}' not found.")
            continue

        with open(input_file, 'r') as f_input:
            input_content = f_input.read()

        if input_content != expected_content:
            print(f"Error: Configuration mismatch in '{input_file}'.")
            print(f"Expected:\n{expected_content}")
            print(f"Actual:\n{input_content}")
            exit(1)

        print(f"Validation successful for '{input_file}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate configuration files.")
    parser.add_argument("--input_files", required=True, help="Comma-separated list of input configuration files.")
    parser.add_argument("--default_file", required=True, help="Path to the default configuration file.")

    args = parser.parse_args()

    input_files_list = args.input_files.split(",")
    validate_config(input_files_list, args.default_file)