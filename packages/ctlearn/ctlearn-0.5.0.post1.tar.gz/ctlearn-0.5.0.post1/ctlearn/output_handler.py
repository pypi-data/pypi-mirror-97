import logging
import numpy as np
import pandas as pd

def write_output(h5file, reader, indices, example_description, predictions, prediction_label='prediction'):
    data = {}
    tel_pointing = reader.tel_pointing
    energy_unit = 'TeV'
    for i, idx in enumerate(indices):
        for val, des in zip(reader[idx], example_description):
            if des['name'] == 'particletype':
                if i == 0:
                    data['mc_particle'] = []
                data['mc_particle'].append(val)
            elif des['name'] == 'energy':
                if i == 0:
                    data['mc_energy'] = []
                if des['unit'] == 'log(TeV)':
                    energy_unit = 'log(TeV)'
                    val[0] = np.power(10,val[0])
                data['mc_energy'].append(val[0])
            elif des['name'] == 'direction':
                if i == 0:
                    data['mc_altitude'], data['mc_azimuth'] = [],[]
                data['mc_altitude'].append(val[0] + tel_pointing[1])
                data['mc_azimuth'].append(val[1] + tel_pointing[0])
            elif des['name'] == 'impact':
                if i == 0:
                    data['mc_impact_x'], data['mc_impact_y'] = [],[]
                data['mc_impact_x'].append(val[0])
                data['mc_impact_y'].append(val[1])

        prediction = predictions[i]
        # Gamma/hadron classification
        if 'particletype' in prediction and 'particletype_probabilities' in prediction:
            if i == 0:
                data['reco_particle'], data['reco_gammaness'] = [],[]
            data['reco_particle'].append(prediction['particletype'])
            data['reco_gammaness'].append(prediction['particletype_probabilities'][1])
        # Energy regression
        if 'energy' in prediction:
            if i == 0:
                data['reco_energy'] = []
            if energy_unit == 'log(TeV)':
                prediction['energy'][0] = np.power(10,prediction['energy'][0])
            data['reco_energy'].append(prediction['energy'][0])
        # Arrival direction regression
        if 'direction' in prediction:
            if i == 0:
                data['reco_altitude'], data['reco_azimuth'] = [],[]
            data['reco_altitude'].append(prediction['direction'][0] + tel_pointing[1])
            data['reco_azimuth'].append(prediction['direction'][1] + tel_pointing[0])
        # Impact parameter regression
        if 'impact' in prediction:
            if i == 0:
                data['reco_impact_x'], data['reco_impact_y'] = [],[]
            data['reco_impact_x'].append(prediction['impact'][0])
            data['reco_impact_y'].append(prediction['impact'][1])
        # Shower maximum regression
        if 'showermaximum' in prediction:
            if i == 0:
                data['reco_x_max'] = []
            data['reco_x_max'].append(prediction['showermaximum'][0])

    if prediction_label in list(pd.HDFStore(h5file).keys()):
        pd.HDFStore(h5file).remove(prediction_label)
    pd.DataFrame(data=data).to_hdf(h5file, key=prediction_label, mode='a')
