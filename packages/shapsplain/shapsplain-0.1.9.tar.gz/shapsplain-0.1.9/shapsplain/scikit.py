import numpy as np

from shapsplain.forest import ShapForest

def to_json(node_index, predicates, sktree):
    objective = sktree.tree_.value[node_index]

    if objective.shape[1] > 1:
        objective = objective / np.sum(objective)

    new_node = {
        'predicates': predicates,
        'objective': objective[0].tolist(),
        'population': sktree.tree_.weighted_n_node_samples[node_index]
    }

    threshold = sktree.tree_.threshold[node_index]

    if sktree.tree_.feature[node_index] >= 0:
        left_preds = [{
            'op': '<=',
            'field': str(sktree.tree_.feature[node_index]),
            'value': threshold,
        }]

        right_preds = [{
            'op': '>',
            'field': str(sktree.tree_.feature[node_index]),
            'value': threshold,
        }]

        left = sktree.tree_.children_left[node_index]
        right = sktree.tree_.children_right[node_index]

        left_child = to_json(left, left_preds, sktree)
        right_child = to_json(right, right_preds, sktree)

        new_node['children'] = [right_child, left_child]

    return new_node

def to_shap_forest(skensemble, fields):
    nodes = [to_json(0, [True], tree) for tree in skensemble.estimators_]
    trees = [{'root': node} for node in nodes]

    model = {'fields': fields, 'trees': trees}

    return ShapForest({'model': model, 'sample_size': 0})

def shap_importances(skensemble, fields, aggregate):
    sforest = to_shap_forest(skensemble, fields)
    return sforest.shap_importances(aggregate)
