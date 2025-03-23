import csv
import json
import os


FILE_PATH = "/home/guru/Desktop/whiskitphysics/code/data/whisker_param_average_rat/"


def read_csv_string(file_path):
    data = list()

    with open(file_path, "r") as file:
        csvreader = csv.reader(file)

        # To skip the header (if you have one)
        # next(csvreader)

        # Process each row
        for row in csvreader:  # Each row is a list of values
            data.append(row)
    return data


def read_csv_int(file_path):
    data = read_csv_string(file_path)
    for index in range(len(data)):
        data[index] = [int(item) for item in data[index]]

    return data


def read_csv_float(file_path):
    data = read_csv_string(file_path)
    for index in range(len(data)):
        data[index] = [float(item) for item in data[index]]

    return data


def data_reader():
    whisker_names = read_csv_string(FILE_PATH + "param_name.csv")
    whisker_geom = read_csv_float(FILE_PATH + "param_s_a.csv")
    whisker_angles = read_csv_float(FILE_PATH + "param_angles.csv")
    whisker_pos = read_csv_int(FILE_PATH + "param_side_row_col.csv")
    # print(whisker_angles)
    return [whisker_names, whisker_geom, whisker_angles, whisker_pos]


def read_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


if __name__ == "__main__":
    # whisker_names, whisker_geom, whisker_angles, whisker_pos = data_reader()
    # print(whisker_angles[10])
    # if os.path.exists("Python/utils/ratWhiskingArray.json"):
    #     print("File exists")
    point_cloud = read_json("Python/utils/ratWhiskingArray.json")
    whisker_points = {"right": [[] for _ in range(30)], "left": [[] for _ in range(30)]}
    # print(len(point_cloud["ratWhiskingArray"]))
    # print(len(point_cloud["ratWhiskingArray"][10]))
    # print(len(point_cloud["ratWhiskingArray"][10][0]))
    # print(len(point_cloud["ratWhiskingArray"][10][0][10]))
    # print(len(point_cloud["ratWhiskingArray"][10][0][10][0]))
    # print(type(point_cloud["ratWhiskingArray"][10][0][10][0][10]))
    right_rest = point_cloud["ratWhiskingArray"][0][0]
    left_rest = point_cloud["ratWhiskingArray"][0][1]
    for i in range(len(right_rest)):
        rx = right_rest[i][0]
        ry = right_rest[i][1]
        rz = right_rest[i][2]
        lx = left_rest[i][0]
        ly = left_rest[i][1]
        lz = left_rest[i][2]
        for j in range(len(rx)):
            r_point = [rx[j], ry[j], rz[j]]
            whisker_points["right"][j].append(r_point)
            l_point = [lx[j], ly[j], lz[j]]
            whisker_points["left"][j].append(l_point)
    print(len(whisker_points["right"]))
