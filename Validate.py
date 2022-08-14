'''
This Python code is part of Master Project entitled "Data Pre-processing for Machine Learning System (LSTM)"
************************************************************************************************************
Brief explanation : The given set of data can be initially preprocessed, by the method of interpolation,
such as linear, cubic, nearest and so on. Given data here is IMU sensor data. Here interpolation is done
between latitude and longitude with respect to time.
'''

def main():
    x1 = ['1638013709', '1638013710', '1638013711', '1638013712', '1638013713', '1638013714', '1638013715', '1638013716', '1638013717', '1638013718', '1638013719']
    y1 = ['8.714514309', '8.714514309', '8.714514309', '8.714514309', '8.714591338', '8.714598968', '8.714598968', '8.714598968', '8.714631335', '8.714640674', '8.714652864']
    x = ['1638013709', '1638013710', '1638013711', '1638013713',  '1638013715', '1638013717', '1638013718', '1638013719']
    y = ['8.714514309', '8.714514309', '8.714514309', '8.714591338',  '8.714598968', '8.714631335', '8.714640674', '8.714652864']
    import numpy as np
    x_val_arr = np.array(x)
    x_val_int = x_val_arr.astype(int)
    y_val_arr = np.array(y)
    y_val_float = y_val_arr.astype(float)
    x1_val_arr = np.array(x1)
    x1_val_int = x1_val_arr.astype(int)

    y1_val_arr = np.array(y1)
    y1_val_float = y1_val_arr.astype(float)
    from scipy.interpolate import interp1d
    import pylab

    f_quadratic = interp1d(x1_val_int, y1_val_float, kind='quadratic')
    f_linear = interp1d(x1_val_int, y1_val_float)
    f_cubic = interp1d(x1_val_int, y1_val_float, kind='cubic')
    f_previous = interp1d(x1_val_int,y1_val_float,kind='previous')
    x2 = np.linspace(1638013709, 1638013719, 1100)
    pylab.plot(x1_val_int, y1_val_float, 'o', label='data points')
    #pylab.plot(x1_val_int, y1_val_float, label='exact')
    #pylab.plot(x2, f_quadratic(x2), label='quadratic')
    #pylab.plot(x2, f_linear(x2), label='linear')
    #pylab.plot(x2, f_cubic(x2), label='cubic')
    pylab.plot(x2, f_previous(x2), label='previous')

    pylab.legend()
    pylab.xlabel("Time in seconds (S)")
    pylab.ylabel("Longitude in degree (°)")
    pylab.title(" Time vs Longitudnal Data Points")
    pylab.show()

def get_sampled_time_stamp(time_stamp):
    import numpy as np
    sample_time_stamp = []
    for i in range(len(time_stamp) - 1):
        sample = np.linspace(int(time_stamp[i]), int(time_stamp[i + 1]), 998)
        sample_list = sample.tolist()
        sample_time_stamp.extend(sample_list)
        sample_list.clear()
        sample_time_stamp.append(int(time_stamp[i + 1]))
    return sample_time_stamp


def get_interpolated_val(new_x_val, x_val, y_val):
    import numpy as np
    x_val_arr = np.array(x_val)
    x_val_int = x_val_arr.astype(int)
    y_val_arr = np.array(y_val)
    y_val_float = y_val_arr.astype(float)

    from scipy.interpolate import interp1d
    y_f = interp1d(x_val_int, y_val_float, kind="cubic")
    return y_f(new_x_val)

if __name__ == main():
    main()