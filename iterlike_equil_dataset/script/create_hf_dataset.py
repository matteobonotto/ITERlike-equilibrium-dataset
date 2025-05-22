from scipy import io
import numpy as np
import json
import matplotlib.pyplot as plt 
import json
from datasets import Dataset


if __name__ == '__main__':

    data = io.loadmat("../ITER_like_equilibrium_dataset.mat")

    mag_measures = data['DB_meas_Bpickup_test_ConvNet']
    flux = data['DB_psi_pixel_test_ConvNet']
    rhx = data['DB_res_RHS_pixel_test_ConvNet']
    jpla = data['DB_Jpla_pixel_test_ConvNet']
    coils_current = data['DB_coils_curr_test_ConvNet']
    separatrix = data['DB_separatrix_200_test_ConvNet']
    is_diverted = data['XP_YN'].reshape(-1,1)
    f_prpofile = data['DB_f_test_ConvNet']
    p_profile = data['DB_p_test_ConvNet']

    ### full dataset
    data_dict = {
        'mag_measures' : mag_measures,
        'flux' : flux,
        'rhs' : rhx,
        'coils_current' : coils_current,
        'separatrix' : separatrix,
        'is_diverted' : is_diverted,
        'p_profile' : p_profile,   
    }

    for k,v in data_dict.items():
        if "__" not in k:
            print(f"{k}: shape: {v.shape}")

    ds = Dataset.from_dict(data_dict)
    ds = ds.with_format("numpy")

    ds.push_to_hub("matteobonotto/iterlike_equil")

    ### subsample 
    data_dict = {
        'mag_measures' : mag_measures,
        'flux' : flux,
        'rhs' : rhx,
        'coils_current' : coils_current,
        'separatrix' : separatrix,
        'is_diverted' : is_diverted,
        'p_profile' : p_profile,   
    }

    isel = 8192
    data_dict = {k:v[:isel, ...] for k,v in data_dict.items()}

    for k,v in data_dict.items():
        if "__" not in k:
            print(f"{k}: shape: {v.shape}")


    ds = Dataset.from_dict(data_dict)
    ds = ds.with_format("numpy")
    ds.push_to_hub("matteobonotto/iterlike_equil_sample")














