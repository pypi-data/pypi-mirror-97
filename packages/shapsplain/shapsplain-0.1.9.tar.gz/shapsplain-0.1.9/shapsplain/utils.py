import shapsplain.importers
np = shapsplain.importers.import_numpy()

def make_fields(model, vmap):
    fields = {}

    for i, fid in enumerate(sorted(vmap.keys())):
        ftype = model['model']['fields'][fid]['optype']
        fname = model['model']['fields'][fid]['name']
        finfo = {'index': i, 'values': None, 'name': fname}

        if ftype == 'categorical':
            finfo['values'] = sorted(vmap[fid], key=lambda x: (x is not None, x))

        fields[fid] = finfo

    return fields

def shap_labels(shap_values, index_map, anomaly_model):
    sorted_idxs = np.argsort(-np.abs(shap_values[:-1]))
    last_value = shap_values[-1]

    if anomaly_model:
        output = [np.power(2, -float(np.sum(shap_values)))]
    else:
        output = [float(np.sum(shap_values))]

    for idx in sorted_idxs:
        if anomaly_model:
            next_value = last_value + shap_values[idx]
            pred_diff = np.power(2, -next_value) - np.power(2, -last_value)
            last_value = next_value
        else:
            pred_diff = shap_values[idx]

        output.append([index_map[idx], float(pred_diff)])

    return output

def to_numpy(fields, instance):
    if type(instance) == int:
        return instance
    else:
        X = np.empty((len(fields),), dtype=np.float64)
        X[:] = np.NaN

        for fid in fields:
            field = fields[fid]
            fname = field['name']
            index = field['index']
            value_list = field['values']

            value = instance.get(fname, instance.get(fid, None))

            if value_list is None and value is not None:
                X[index] = np.float64(value)
            elif value_list is not None:
                try:
                    X[index] = value_list.index(value)
                except ValueError:
                    X[index] = np.NaN

        return X
