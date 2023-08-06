import numpy as np

from numba import jit

from shapsplain.node import Leaf

@jit(nopython=True)
def path_sum(value, phi, udepth, feature_idxs, zero_fracs, one_fracs, pweights):
    udp1 = udepth + 1

    for i in range(1, udp1):
        one_frac = one_fracs[i]
        zero_frac = zero_fracs[i]

        next_one = pweights[udepth]
        total = 0

        for j in range(udepth - 1, -1, -1):
            udmj = udepth - j

            if one_frac != 0.:
                tmp = next_one * udp1 / ((j + 1.) * one_frac)
                total += tmp
                next_one = pweights[j] - tmp * zero_frac * (udmj / udp1)
            elif zero_frac != 0.:
                total += (pweights[j] / zero_frac) / (udmj / udp1)

        path_fidx = feature_idxs[i]
        frac_diff = one_frac - zero_frac
        phi[path_fidx,:] += total * frac_diff * value

@jit(nopython=True)
def path_extend(fi, d, zero_frac, one_frac, fis, zero_fracs, one_fracs, pwts):
    fis[d] = fi
    zero_fracs[d] = zero_frac
    one_fracs[d] = one_frac

    udp1 = d + 1.

    if d == 0:
        pwts[d] = 1.
    else:
        pwts[d] = 0.

    for i in range(d - 1, -1, -1):
        pw_i = pwts[i]
        pwts[i + 1] += one_frac * pw_i * (i + 1.) / udp1
        pwts[i] = zero_frac * pw_i * (d - i) / udp1

@jit(nopython=True)
def maybe_unwind(udepth, split_index, feature_idxs, zero_fracs, one_fracs, pwts):
        path_index = 0

        while path_index <= udepth:
            if feature_idxs[path_index] == split_index:
                break

            path_index += 1

        if path_index != udepth + 1:
            zero_frac = zero_fracs[path_index]
            one_frac = one_fracs[path_index]

            next_one = pwts[udepth]
            udp1 = udepth + 1

            for i in range(udepth - 1, -1, -1):
                udmi = udepth - i
                tmp_pwi = pwts[i]

                if one_frac != 0.:
                    pwts[i] = next_one * udp1 / ((i + 1.) * one_frac)
                    next_one = tmp_pwi - pwts[i] * zero_frac * udmi / udp1
                else:
                    pwts[i] = (tmp_pwi * udp1) / (zero_frac * udmi)

            for i in range(path_index, udepth):
                feature_idxs[i] = feature_idxs[i + 1]
                zero_fracs[i] = zero_fracs[i + 1]
                one_fracs[i] = one_fracs[i + 1]

            return udepth - 1, zero_frac, one_frac
        else:
            return udepth, 1., 1.

class Path(object):
    def __init__(self, path, unique_or_max_depth):
        if path is None:
            max_depth = unique_or_max_depth + 2
            s = (max_depth * (max_depth + 1)) // 2

            self._feature_idxs = np.zeros(s, dtype=np.int32)
            self._zero_fracs = np.zeros(s, dtype=np.float64)
            self._one_fracs = np.zeros(s, dtype=np.float64)
            self._pweights = np.zeros(s, dtype=np.float64)
        else:
            udp1 = unique_or_max_depth + 1

            self._feature_idxs = path._feature_idxs[udp1:]
            self._feature_idxs[:udp1] = path._feature_idxs[:udp1]
            self._zero_fracs = path._zero_fracs[udp1:]
            self._zero_fracs[:udp1] = path._zero_fracs[:udp1]
            self._one_fracs = path._one_fracs[udp1:]
            self._one_fracs[:udp1] = path._one_fracs[:udp1]
            self._pweights = path._pweights[udp1:]
            self._pweights[:udp1] = path._pweights[:udp1]

    def unwound_path_sum(self, node_value, phi, unique_depth):
        path_sum(node_value,
                 phi,
                 unique_depth,
                 self._feature_idxs,
                 self._zero_fracs,
                 self._one_fracs,
                 self._pweights)

def tree_shap(
        x,
        phi,
        current_node,
        unique_depth,
        parent_path,
        zero_fraction,
        one_fraction,
        feature_index):

    # extend the unique path
    path = Path(parent_path, unique_depth)
    path_extend(feature_index,
                unique_depth,
                zero_fraction,
                one_fraction,
                path._feature_idxs,
                path._zero_fracs,
                path._one_fracs,
                path._pweights)

    if current_node._is_leaf:
        node_value = np.array(current_node._objective)
        path.unwound_path_sum(node_value, phi, unique_depth)
    else:
        split_index = current_node._split_index

        if type(x) == int:
            n = current_node
            if n._left._expectation[x] > n._right._expectation[x]:
                next_index = 0
            else:
                next_index = 1
        else:
            next_index = current_node.next_index(x)

        if current_node._deterministic and next_index is not None:
            node_value = np.array(current_node._expectation)
            path.unwound_path_sum(node_value, phi, unique_depth)
        else:

            # Missing or out-of-sample value; create a phantom leaf
            # node and treat both branches the same
            if next_index is None:
                phantom_node = Leaf(current_node._objective, 0)
            else:
                phantom_node = None

            if next_index == 0 or next_index is None:
                hot_node = current_node._left
                cold_node = current_node._right
            elif next_index == 1:
                hot_node = current_node._right
                cold_node = current_node._left
            else:
                raise ValueError('Next index is %s?' % str(next_index))

            current_weight = current_node._weight

            if current_weight > 0:
                hot_fraction = hot_node._weight / current_weight
                cold_fraction = cold_node._weight / current_weight
            else:
                hot_fraction = cold_fraction = 0.0

            next_depth, in_zf, in_of = maybe_unwind(unique_depth,
                                                    split_index,
                                                    path._feature_idxs,
                                                    path._zero_fracs,
                                                    path._one_fracs,
                                                    path._pweights)

            si = split_index
            nd = next_depth + 1

            cold_zf = cold_fraction * in_zf
            cold_of = 0
            hot_zf = hot_fraction * in_zf
            hot_of = in_of

            if phantom_node is not None:
                tree_shap(x, phi, phantom_node, nd, path, 0, in_of, si)
                hot_of = 0

            if hot_zf > 0 or hot_of > 0:
                tree_shap(x, phi, hot_node, nd, path, hot_zf, hot_of, si)

            if cold_zf > 0 or cold_of > 0:
                tree_shap(x, phi, cold_node, nd, path, cold_zf, cold_of, si)
