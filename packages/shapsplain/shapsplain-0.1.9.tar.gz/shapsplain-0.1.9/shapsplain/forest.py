import shapsplain.importers
np = shapsplain.importers.import_numpy()

from shapsplain.shap import tree_shap, Path
from shapsplain.node import create_node
from shapsplain.utils import make_fields, shap_labels, to_numpy

DEPTH_FACTOR = 0.5772156649

def add_values_for_node(node, value_map):
    if 'children' in node:
        assert len(node['children']) == 2
        add_values_for_node(node['children'][0], value_map)
        add_values_for_node(node['children'][1], value_map)

    if 'predicates' in node:
        for predicate in node['predicates']:
            if predicate is not True:
                op, fid, value = [predicate[k] for k in ['op', 'field', 'value']]

                if fid not in value_map:
                    value_map[fid] = set()

                if 'in' in op:
                    value_map[fid].update([v for v in value])

    return value_map

def find_mean_depth(model):
    real_mean_depth = model['model'].get('mean_depth', np.float64('inf'))
    sample_size = model['sample_size']

    log_samples = np.log(sample_size - 1)
    size_correction = np.float64(sample_size - 1) / sample_size
    default_depth = 2 * (DEPTH_FACTOR + log_samples - size_correction)

    return min(real_mean_depth, default_depth)

def compute_expectations(node, depth):
    if node._is_leaf:
        node._expectation = node._objective
        return 0
    else:
        left_depth = compute_expectations(node._left, depth + 1)
        right_depth = compute_expectations(node._right, depth + 1)

        if node._left._weight == 0 and node._right._weight == 0:
            w_ex = [n._expectation * 0.5 for n in [node._left, node._right]]
            w_sum = 1
        else:
            w_ex = [n._expectation * n._weight for n in [node._left, node._right]]
            w_sum = node._left._weight + node._right._weight

        node._expectation = np.sum(w_ex, axis=0) / w_sum

        if node._left._deterministic and node._right._deterministic:
            if node._left._weight == node._right._weight == 1:
                if np.all(node._left._expectation == node._right._expectation):
                    node._deterministic = True

        return max(left_depth, right_depth) + 1

class ShapForest(object):
    def __init__(self, adict):
        if 'model' in adict:
            model = adict
        elif 'object' in adict and 'model' in adict['object']:
            model = adict['object']
        else:
            raise ValueError('Model format not recognized with keys %s',
                             str(sorted(adict.keys())))

        roots = [t['root'] for t in model['model']['trees']]

        value_map = {}
        [add_values_for_node(r, value_map) for r in roots]

        self._fields = make_fields(model, value_map)
        self._index_map = {self._fields[k]['index']: k for k in self._fields}

        if 'objective' in roots[0]:
            self._anomaly_model = False
            dnorm = 1
        else:
            self._anomaly_model = True
            dnorm = find_mean_depth(model)

        trees = [create_node(r, None, self._fields, 1, dnorm) for r in roots]

        self._trees = trees
        self._max_depth = np.max([compute_expectations(t, 0) for t in trees])
        self._n_outputs = len(self._trees[0]._expectation)
        self._start_path = Path(None, self._max_depth)

    def shap_for_tree(self, tree, X, phi):
        phi[-1,:] += tree._expectation
        tree_shap(X, phi, tree, 0, self._start_path, 1, 1, -1)

    def compute_shap(self, instance):
        X = to_numpy(self._fields, instance)
        phi = np.zeros(((len(self._fields)) + 1, self._n_outputs))

        for tree in self._trees:
            self.shap_for_tree(tree, X, phi)

        phi /= len(self._trees)

        return [phi[:, i] for i in range(self._n_outputs)]

    def label_shap(self, shap_value):
        return shap_labels(shap_value, self._index_map, self._anomaly_model)

    def shap_importances(self, aggregate):
        phis = np.zeros((self._n_outputs, len(self._fields)))

        for i in range(self._n_outputs):
            cp = np.array([np.abs(vals[:-1]) for vals in self.compute_shap(i)])
            phis[i,:] = cp.sum(axis=0) / np.sum(cp)

        if aggregate:
            shaps = phis.sum(axis=0) / np.sum(phis)
            return self.label_shap(shaps.tolist() + [0.0])[1:]
        else:
            shaps = [phis[i,:] for i in range(self._n_outputs)]
            return [self.label_shap(sv.tolist() + [0.0])[1:] for sv in shaps]

    def node_predict(self, node, X):
        if node._is_leaf:
            return node._objective
        else:
            next_index = node.next_index(X)

            if next_index is None:
                return node._objective
            elif next_index == 0:
                return self.node_predict(node._left, X)
            elif next_index == 1:
                return self.node_predict(node._right, X)
            else:
                raise ValueError()

    def predict(self, instance, explanation=False):
        if explanation:
            shap_values = self.compute_shap(instance)
            return [self.label_shap(sv) for sv in shap_values]
        else:
            X = to_numpy(self._fields, instance)
            preds = np.array([self.node_predict(t, X) for t in self._trees])

            if self._anomaly_model:
                return np.power(2, -(np.sum(preds, axis=0) / len(self._trees)))
            else:
                return np.sum(preds, axis=0) / len(self._trees)
