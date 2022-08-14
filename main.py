# This Python code is part of Master Project entitled "Data Pre-processing for Machine Learning System"
'''
Brief explanation : The given set of data can be initially preprocessed, by the method of interpolation,
such as linear, cubic, nearest and so on. Given data here is IMU sensor data. Here interpolation is done
for latitude and longitude with respect to time.
'''
from geographiclib.geodesic import Geodesic
from haversine import haversine
from scipy.interpolate import interp1d

import xlsxwriter
import csv
import numpy as np
import pylab


def main():
    '''Read the given csv and populate python variables to hold time_stamp, latitude, longitude values'''
    data = []
    time_stamp = []  # Variable to hold time values after removing the empty cells in between
    latitude = []  # Variable to hold the latitude values
    longitude = []  # Variable to hold the longitude values
    samples_of_time = []  # Variable to hold the number of empty cells in the given csv

    with open(r"input_files\\data_interpolation.csv", 'r') as infile:
        reader = csv.reader(infile, delimiter=',')
        next(reader)
        for row in reader:
            data.append(row)

    tmp_time_stamp = []
    tmp_lat = []
    tmp_long = []

    for val in data:
        tmp_time_stamp.append(val[0])
        tmp_lat.append(val[1])
        tmp_long.append(val[2])

    for sample in tmp_time_stamp:
        if sample:
            time_stamp.append(sample)

    for sample in tmp_lat:
        if sample:
            latitude.append(sample)

    for sample in tmp_long:
        if sample:
            longitude.append(sample)

    no_of_empty_values = 0

    for sample in tmp_time_stamp:
        if sample:
            if no_of_empty_values > 0:
                samples_of_time.append(no_of_empty_values)
                no_of_empty_values = 0
        else:
            no_of_empty_values = no_of_empty_values + 1
    print(samples_of_time)

    distance = calc_dist_values(latitude, longitude)
    bearing = calc_bearing_values(latitude, longitude)
    '''output data  = not interpolated values of latitude, longitude for which distance is calculated '''
    output_data = [time_stamp, latitude, longitude, distance, bearing]
    header_list = ["Time stamp", "Latitude", "Longitude", "Distance", "Bearing"]
    write_data_to_output_file(output_data, header_list, "dist_bearing_output")

    '''The below block of code is used to interpolate the given time values, latitude
    and longitude values'''
    sampled_time_stamp = get_sampled_time_stamp(time_stamp, samples_of_time)
    interpolated_lat = get_interpolated_val(sampled_time_stamp, time_stamp, latitude)
    interpolated_long = get_interpolated_val(sampled_time_stamp, time_stamp, longitude)
    interpolated_data = [sampled_time_stamp, interpolated_lat, interpolated_long]
    header_list = ["Time stamp", "Latitude", "Longitude"]
    write_data_to_output_file(interpolated_data, header_list, "interpolated_data")

    '''Display the longitude values against time'''
    plot_and_display(sampled_time_stamp, interpolated_long, time_stamp, longitude)

    new_interpolated_distance = calc_dist_values(interpolated_lat, interpolated_long)
    new_interpolated_bearing = calc_bearing_values(interpolated_lat, interpolated_long)
    new_data = [sampled_time_stamp, interpolated_lat, interpolated_long, new_interpolated_distance, new_interpolated_bearing]
    header_list = ["Time stamp", "Latitude", "Longitude", "Distance", "Bearing"]
    write_data_to_output_file(new_data, header_list, "interpolated_values")

# End of main function.

''' 
    calc_dist_values(latitude,longitude) brief exp: Calculates distance values for  given list of latitude and longitude lists. 
    input parameter : latitude - List of latitude values
    input parameter : longitude - List of longitude values
    return value    : List containing distance values for the given list of latitude and longitudes.   
'''


def calc_dist_values(latitude, longitude):
    if len(longitude) != len(latitude):
        print("ERROR: The given number of latitude values are not same as longitude values, please check the data")
        return

    dist = [float(0)]
    for i in range(len(latitude) - 1):
        long_1 = float(longitude[i])
        lat_1 = float(latitude[i])

        long_2 = float(longitude[i + 1])
        lat_2 = float(latitude[i + 1])

        hav_dist = haversine((lat_1, long_1), (lat_2, long_2), unit='km')
        dist.append(float(hav_dist))
    print("Calculated distance values for given latitude and longitude values")
    return dist


''' calc_bearing_values(latitude,longitude) brief exp: Calculates bearing values for  given list of latitude and longitude lists.
    input parameter : latitude - List of latitude values
    input parameter : longitude - List of longitude values
    return value    : List containing bearing angle values for the given list of latitude and longitudes.
'''


def calc_bearing_values(latitude, longitude):
    if len(longitude) != len(latitude):
        print("ERROR: The given number of latitude values are not same as longitude values, please check the data")
        return
    bearing = [float(0)]
    for i in range(len(latitude) - 1):
        long_1 = float(longitude[i])
        lat_1 = float(latitude[i])

        long_2 = float(longitude[i + 1])
        lat_2 = float(latitude[i + 1])

        bearing_val = get_bearing(lat_1, lat_2, long_1, long_2)
        bearing.append(float(bearing_val))
    print("Calculated bearing values for given latitude and longitude values")
    return bearing


''' get_bearing(lat_1, lat_2, long_1, long_2) brief exp: Calculates bearing values for  given set of co-ordinates.'''


def get_bearing(lat_1, lat_2, long_1, long_2):

    bearing = Geodesic.WGS84.Inverse(lat_1, long_1, lat_2, long_2)['azi1']
    return bearing


''' write_data_to_output_file(data, header list, output_file_name)
    brief exp: Writes given data to xlsx file with the
    name given in output_file_name'''


def write_data_to_output_file(data, header_list, output_file_name):
    if not data:
        print("ERROR: given data is empty, not able to write to csv")
        return
    # Here write the data to csv file with name of the file as output_file_name

    file_name = output_file_name + '.xlsx'
    out_wb = xlsxwriter.Workbook(file_name)
    out_ws = out_wb.add_worksheet()

    for i in range(len(header_list)):
        out_ws.write(0, i, header_list[i])
        for index in range(len(data[i])):
            out_ws.write(index + 1, i, data[i][index])
    out_wb.close()
    print("Output data is successfully writen to :", file_name, "file")
    return


''' get_sampled_time_stamp(time_stamp, sample_sizes)
    brief exp: Creates the new list with time values
    sampled according to give sample_sizes list'''


def get_sampled_time_stamp(time_stamp, sample_sizes):

    sample_time_stamp = []
    for i in range(len(time_stamp) - 1):
        sample = np.linspace(int(time_stamp[i]), int(time_stamp[i + 1]), int(sample_sizes[i]))
        sample_list = sample.tolist()
        sample_time_stamp.extend(sample_list)
        sample_list.clear()

    return sample_time_stamp


''' get_interpolated_val(new_x_val, x_val, y_val)
    brief exp: Calculates y values for given new_x_val
    using interp1d function calculated from x_val, y_val'''


def get_interpolated_val(new_x_val, x_val, y_val):

    x_val_arr = np.array(x_val)
    x_val_float = x_val_arr.astype(float)
    y_val_arr = np.array(y_val)
    y_val_float = y_val_arr.astype(float)


    y_f = interp1d(x_val_float, y_val_float, kind="cubic")
    return y_f(new_x_val)


def plot_and_display(x_val, y_val, x_ref, y_ref):


    x_val_arr = np.array(x_ref)
    x_val_int = x_val_arr.astype(int)
    y_val_arr = np.array(y_ref)
    y_val_float = y_val_arr.astype(float)


    pylab.plot(x_val_int, y_val_float, 'o', label='data points')
    pylab.plot(x_val, y_val, label='quadratic')
    pylab.legend()
    pylab.xlabel("Time")
    pylab.ylabel("Longitude")
    pylab.title("Quadratic interpolation of longitude values")
    pylab.show()
    return


if __name__ == main():
    main()
