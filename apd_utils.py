# adulterated product detection utility functions
import pandas as pd
import numpy as np
from scipy.stats import shapiro
import random 

# generate referenced dataset
def generate_ref_data(
        num_sample:int = 50,
        num_analyte:int = 200,
        mean_low:int = 20,
        mean_high:int = 1000,
        std_factor_low:float = 0.1,
        std_factor_high:float = 0.5,
        seed:int = None    
    ):
    """Generate a referenced dataset in pandas dataframe. 
    Args:
        num_sample[int]: Number of samples to be generated.
        num_analyte[int]: Number of analytes to be generated.
        mean_low[int]: Lower bound of mean analyte concentration.
        mean_high[int]: Upper bound of mean analyte concentration.
        std_factor_low[float]: Floating value (0-1) to determine lower bound of standard deviation.  
        std_factor_high[float]: Floating value (0-1) to determine upper bound of standard deviation. 
        seed[int or None]: random seed
    Return:
        numpy 2d array
    """
    # check std_factor_ input
    if std_factor_low < 0 or std_factor_low > 1:
        raise ValueError("std_factor_low must be between 0 and 1")
    if std_factor_high < 0 or std_factor_high > 1:
        raise ValueError("std_factor_high must be between 0 and 1")
    
    # set random seed
    np.random.seed(seed)

    # start a dataset
    dataset = np.zeros((num_sample, num_analyte))

    i = 0
    while i < num_analyte:
        # Define the mean and standard deviation for each variable
        mean = np.random.uniform(low=mean_low, high=mean_high)
        std_dev = np.random.uniform(low=mean*std_factor_low, high=mean*std_factor_high)

        # Generate random values from a normal distribution
        values = np.random.normal(mean, std_dev, num_sample)
        
        # ensure values are all greater than zero and fit normal distribution
        stat, p = shapiro(values)
        if min(values) > 0 and p > 0.1:
            dataset[:, i] = values
            i += 1
    
    return np.round(dataset)


# create a random sample
def generate_random_sample(
        data,
        adulterated: bool = False,
        num_analyte: int = 30,
        analyte_select_method: str = "random",
        conc_percentile = (0, 5),
        seed = None
    ):
    """Generate a random sample based on referenced data.
    Args:
        data[numpy array]: Your input referenced dataset. 
        adulterated[bool]: Determine whether to generate an adulterated(True) or non-adulterated(False) sample.
        num_analyte[int]: Number of analytes for adulteratoins.
        analyte_select_method[str]:
            "random": Select analytes randomly 
            "high": Select analytes with greater variations (std dev) for adulterations.
            "low": Select analytes with less varaitions (std dev) for adulterations.
        conc_percentile: A set of two percentile values between 0 and 100 inclusive to determine the range of
            analyte concentrations to be altered.
            e.g., (0, 5) will make the analyte concentration falls within the interval of 0th and 5th percentiles
            from the referenced data.  
        seed = None
    Return:
        when adulterated = False, return a numpy array with shape of (1, n) where n = number of analytes in input data
        when adulterated = True, return a numpy array as described above, and a list of indices of selected variables/analytes. 
    """
    # check input arguments
    if analyte_select_method not in ["random", "high", "low"]:
        raise ValueError("'analyte_select_method' must be either 'random' or 'high' or 'low'.")
    if type(conc_percentile) != tuple and type(conc_percentile) != list or len(conc_percentile) != 2:
        raise ValueError("'conc_percentile' must be a tuple or list with size of 2.")
    if conc_percentile[0] >= conc_percentile[1]:
        raise ValueError("First value must be less than second value in 'conc_percentile'.")
    if conc_percentile[0] < 0 or conc_percentile[0] > 100 or conc_percentile[1] < 0 or conc_percentile[1] > 100:
        raise ValueError("Value in 'conc_percentile' out of range (0-100).")
    
    # set random seed
    random.seed(seed)

    # create a sample which variables were randomly chosen from the data
    sample = np.zeros((1,data.shape[1]))

    for i in range(data.shape[1]):
        # use random.uniform to slightly random change the value
        sample[0, i] = random.choice(data[:,i]) * random.uniform(0.95, 1.05)

    # ouput random ref sample
    if adulterated == False:
        return np.round(sample)

    # ouput random adulterated sample
    else:
        # check num_analyte input
        if num_analyte > data.shape[1]:
            raise ValueError("'num_analyte' must be less than the number of analytes in your referenced dataset.")
        
        # calculate std for each analyte
        analyte_std = np.std(data, axis=0)
        
        # select analytes with greater variations
        if analyte_select_method == "high":
            des_std_index = np.argsort(analyte_std)[::-1]
            selected_analyte_index = des_std_index[0:num_analyte]
        # select analytes with less variations
        elif analyte_select_method == "low":
            asc_std_index = np.argsort(analyte_std)
            selected_analyte_index = asc_std_index[0:num_analyte]
        # randomly select analytes
        elif analyte_select_method == "random":
            selected_analyte_index = random.sample(range(0, data.shape[1]), num_analyte)

        # get percentile values of selected analytes
        selected_data = data[:, selected_analyte_index]
        perc_range = np.percentile(selected_data, conc_percentile, axis=0)
        alt_values = np.random.uniform(low=perc_range[0,:], high=perc_range[1,:])

        # alter values in the sample
        sample[0, selected_analyte_index] = alt_values


        return np.round(sample), list(selected_analyte_index)
        