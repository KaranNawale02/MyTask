# import argparse
# import os

# def validate_config(input_files, default_file):
#     """
#     Validates input configuration files against a default configuration.

#     Args:
#         input_files (list): List of input configuration file paths.
#         default_file (str): Path to the default configuration file.
#     """

#     if not os.path.exists(default_file):
#         print(f"Error: Default configuration file '{default_file}' not found.")
#         exit(1)

#     with open(default_file, 'r') as f_default:
#         expected_content = f_default.read()

#     for input_file in input_files:
#         if not os.path.exists(input_file):
#             print(f"Warning: Input file '{input_file}' not found.")
#             continue

#         with open(input_file, 'r') as f_input:
#             input_content = f_input.read()

#         if input_content != expected_content:
#             print(f"Error: Configuration mismatch in '{input_file}'.")
#             print(f"Expected:\n{expected_content}")
#             print(f"Actual:\n{input_content}")
#             exit(1)

#         print(f"Validation successful for '{input_file}'.")

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Validate configuration files.")
#     parser.add_argument("--input_files", required=True, help="Comma-separated list of input configuration files.")
#     parser.add_argument("--default_file", required=True, help="Path to the default configuration file.")

#     args = parser.parse_args()

#     input_files_list = args.input_files.split(",")
#     validate_config(input_files_list, args.default_file)


import configparser
import argparse

def read_cfg_to_dict(file_path):
    config = configparser.ConfigParser()
    config.optionxform = str  # Preserve case sensitivity
    try:
        with open(file_path) as f:
            config.read_file(f)
    except Exception as e:
        raise ValueError(f"Error reading file {file_path}: {e}")

    return {section: dict(config.items(section)) for section in config.sections()}

def validate_config(actual_cfg, expected_cfg, file_path):
    mismatches = []
    flag = 0

    #  Compare expected vs actual values
    for section, expected_params in expected_cfg.items():
        if section in actual_cfg:
            for key, expected_value in expected_params.items():
                actual_value = actual_cfg[section].get(key)

                # Case 1: SHOULD_NOT_BE_PRESENT — key should not exist
                if expected_value == "SHOULD_NOT_BE_PRESENT":
                    if actual_value is not None:
                        mismatches.append(
                            f"Error: '{key}' should not be present in section [{section}] in {file_path}"
                        )
                        flag = 1

                # Case 2: Expected value is present but wrong
                else:
                    if actual_value is None:
                        mismatches.append(
                            f"Error: '{key}' is missing in section [{section}] in {file_path}"
                        )
                        flag = 1
                    elif actual_value != expected_value:
                        mismatches.append(
                            f"'{key}' in section [{section}] is '{actual_value}', expected '{expected_value}'"
                        )
                        flag = 1
        else:
            # Case 3: Missing section entirely (if keys are not marked as SHOULD_NOT_BE_PRESENT)
            if not all(value == "SHOULD_NOT_BE_PRESENT" for value in expected_params.values()):
                mismatches.append(
                    f"Error: Section [{section}] is missing in {file_path}"
                )
                flag = 1

    return mismatches, flag

def main():
    parser = argparse.ArgumentParser(description="Compare multiple .cfg files with a single expected .cfg file")
    parser.add_argument('--input_files', type=str, required=True,
                        help="Comma-separated list of input .cfg files to validate")
    parser.add_argument('--default_file', type=str, required=True,
                        help="Path to the expected .cfg file")

    args = parser.parse_args()

    input_files = args.input_files.split(",")
    expected_file = args.default_file

    # Read expected config
    expected_config = read_cfg_to_dict(expected_file)

    overall_flag = 0
    for file in input_files:
        actual_config = read_cfg_to_dict(file)

        mismatch_list, flag = validate_config(actual_config, expected_config, file)

        if mismatch_list:
            print(f"\n Mismatches in '{file}':")
            print("\n".join(mismatch_list))
        else:
            print(f" All parameters in '{file}' match the expected configuration.")

        overall_flag = max(overall_flag, flag)

    print("\n Overall Execution flag:", overall_flag)
    return overall_flag

if __name__ == "__main__":
    exit(main())
