import scipy.io
import json
import numpy as np


# Function to convert numpy arrays to JSON-serializable lists
def convert_to_serializable(obj):
    if isinstance(obj, np.ndarray):
        return [convert_to_serializable(item) for item in obj]
    elif isinstance(obj, np.void):
        return {key: convert_to_serializable(obj[key]) for key in obj.dtype.names}
    elif isinstance(obj, dict):
        return {key: convert_to_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    else:
        return obj


if __name__ == "__main__":
    # Load .mat files
    file1_path = "ratWhiskingArrayByDeg.mat"
    file2_path = "ratWhiskingOrientationsByDeg.mat"

    data1 = scipy.io.loadmat(file1_path)
    data2 = scipy.io.loadmat(file2_path)

    # Extract main data structures
    rat_whisking_array = data1["ratWhiskingArray"]
    rat_whisking_orientations = data2["ratWhiskingOrientations"][0, 0]  # Unwrap struct

    # Extract right and left orientations
    right_data = rat_whisking_orientations["right"][0, 0]
    left_data = rat_whisking_orientations["left"][0, 0]

    # Extract theta, phi, zeta for both sides
    right_json = {
        "theta": right_data["theta"],
        "phi": right_data["phi"],
        "zeta": right_data["zeta"],
    }

    left_json = {
        "theta": left_data["theta"],
        "phi": left_data["phi"],
        "zeta": left_data["zeta"],
    }

    # Create structured JSON object
    # whisking_data_json = {
    #     "ratWhiskingArray": rat_whisking_array,
    #     "ratWhiskingOrientations": {"right": right_json, "left": left_json},
    # }

    # Convert to JSON-serializable format
    # whisking_data_json_serializable = convert_to_serializable(whisking_data_json)

    # Save JSON file
    with open("ratWhiskingArray.json", "w") as json_file:
        whisking_arr = convert_to_serializable({"ratWhiskingArray": rat_whisking_array})
        json.dump(whisking_arr, json_file)
    with open("ratWhiskingOrientations.json", "w") as json_file:
        whisking_orientations = convert_to_serializable(
            {"ratWhiskingOrientations": {"right": right_json, "left": left_json}}
        )
        json.dump(whisking_orientations, json_file)

    print(f"JSON files saved")
