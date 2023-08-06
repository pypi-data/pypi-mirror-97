import numpy as np

def to_set(op, fid, values, indexes):
    assert op == 'in'
    all_values = indexes[fid]['values']

    return set([np.float64(all_values.index(v)) for v in values])

def values_set(predicate, indexes):
    op, fid, value = [predicate[k] for k in ['op', 'field', 'value']]
    return to_set(op, fid, value, indexes)

class TreeNode(object):
    def __init__(self, adict, fields, objective):
        self._is_leaf = False
        self._deterministic = False
        self._objective = objective
        self._weight = adict['population']

        first_pred = adict['children'][0]['predicates'][0]
        self._split_index = fields[first_pred['field']]['index']

    def set_missing(self, left, right):
        self._left_missing = False
        self._right_missing = False

        if left['predicates'][0]['op'].endswith('*'):
            self._left_missing = True
        elif right['predicates'][0]['op'].endswith('*'):
            self._right_missing = True

    def set_subtrees(self, left, right):
        self._left = left
        self._right = right

        return self

class Numeric(TreeNode):
    def __init__(self, adict, fields, objective):
        super(Numeric, self).__init__(adict, fields, objective)

        left, right = self.get_children(adict)
        self.set_missing(left, right)
        self._threshold = np.float64(left['predicates'][0]['value'])

    def get_children(self, adict):
        right, left = adict['children']

        assert left['predicates'][0]['op'].startswith('<=')
        assert right['predicates'][0]['op'].startswith('>')

        return left, right

    def next_index(self, X):
        value = X[self._split_index]
        diff = abs(value - self._threshold)

        if np.isnan(value):
            if self._left_missing:
                return 0
            elif self._right_missing:
                return 1
            else:
                return None
        elif value <= self._threshold:
            return 0
        else:
            return 1

class Missing(TreeNode):
    def __init__(self, adict, fields, objective):
        super(Missing, self).__init__(adict, fields, objective)

        left, right = self.get_children(adict)

        assert left['predicates'][0]['op'] == '='
        assert right['predicates'][0]['op'] == '!='

        for n in [left, right]:
            assert n['predicates'][0]['value'] is None

    def get_children(self, adict):
        c0, c1 = adict['children']

        if c0['predicates'][0]['op'] == '=':
            assert c1['predicates'][0]['op'] == '!='
            left = c0
            right = c1
        else:
            assert c1['predicates'][0]['op'] == '='
            left = c1
            right = c0

        return left, right

    def next_index(self, X):
        value = X[self._split_index]

        if np.isnan(value):
            return 0
        else:
            return 1

class SingleCategorical(TreeNode):
    def __init__(self, adict, fields, objective):
        super(SingleCategorical, self).__init__(adict, fields, objective)

        left, right = self.get_children(adict)
        self.set_missing(left, right)

        values = fields[left['predicates'][0]['field']]['values']
        self._threshold = float(values.index(left['predicates'][0]['value'][0]))

        assert self._threshold >= 0

    def get_children(self, adict):
        c0, c1 = adict['children']

        if len(c0['predicates'][0]['value']) > 1:
            assert len(c1['predicates'][0]['value']) == 1
            left = c1
            right = c0
        else:
            assert len(c0['predicates'][0]['value']) == 1
            left = c0
            right = c1

        return left, right

    def next_index(self, X):
        value = X[self._split_index]

        if np.isnan(value):
            if self._threshold is None or self._left_missing:
                return 0
            elif self._right_missing:
                return 1
            else:
                return None
        elif value == self._threshold:
            return 0
        else:
            return 1

class SetCategorical(TreeNode):
    def __init__(self, adict, fields, objective):
        super(SetCategorical, self).__init__(adict, fields, objective)
        left, right = self.get_children(adict)

        self._left_set = values_set(left['predicates'][0], fields)
        self._right_set = values_set(right['predicates'][0], fields)

    def get_children(self, adict):
        right, left = adict['children']
        return left, right

    def next_index(self, X):
        value = X[self._split_index]

        if value in self._left_set:
            return 0
        elif value in self._right_set:
            return 1
        else:
            return None

class PredicateNode(TreeNode):
    def __init__(self, op, fid, value, fields):
        self._is_leaf = False
        self._deterministic = False
        self._split_index = fields[fid]['index']

class EqualsPredicate(PredicateNode):
    def __init__(self, op, fid, value, fields):
        super(EqualsPredicate, self).__init__(op, fid, value, fields)
        all_values = fields[fid]['values']

        if op == 'in':
            assert all_values is not None
            assert len(value) == 1
            self._value = np.float64(all_values.index(value[0]))
        elif op == '=':
            assert all_values is None
            self._value = np.float64(value)
        else:
            raise ValueError('Illegal predicate: %s' % str((op, fid, value)))

    def next_index(self, X):
        if X[self._split_index] == self._value:
            return 0
        else:
            return 1

class InPredicate(PredicateNode):
    def __init__(self, op, fid, value, fields):
        super(InPredicate, self).__init__(op, fid, value, fields)
        self._value = to_set(op, fid, value, fields)

    def next_index(self, X):
        if X[self._split_index] in self._value:
            return 0
        else:
            return 1

class Leaf(object):
    def __init__(self, objective, weight):
        self._is_leaf = True
        self._deterministic = True
        self._objective = objective
        self._weight = weight

def get_node_type(adict, fields):
    left_pred = adict['children'][0]['predicates'][0]
    right_pred = adict['children'][1]['predicates'][0]

    assert left_pred['field'] == right_pred['field']

    fid = left_pred['field']

    if fields[fid]['values'] is None:
        assert left_pred['value'] == right_pred['value']
        op = left_pred['op']

        if op in ['=', '!='] and left_pred['value'] is None:
            return Missing
        elif op in ['<=', '<=*', '>', '>*']:
            assert right_pred['op'] in ['<=', '<=*', '>', '>*']
            return Numeric
        else:
            raise ValueError(str((left_pred, right_pred, fields[fid])))

    elif len(fields[fid]['values']) > 0:
        assert len(left_pred['value']) > 0
        assert len(right_pred['value']) > 0

        if len(left_pred['value']) == 1 or len(right_pred['value']) == 1:
            all_values = set(left_pred['value'] + right_pred['value'])
            if set(all_values) == set(fields[fid]['values']):
                return SingleCategorical
            else:
                return SetCategorical
        else:
            return SetCategorical
    else:
        raise ValueError((left_pred, right_pred))

def make_predicate_node(predicate, fields, objective, weight):
    op, fid, value = [predicate[k] for k in ['op', 'field', 'value']]

    if op == 'in' and len(value) > 1:
        node = InPredicate(op, fid, value, fields)
    elif op == '=' or op == 'in':
        node = EqualsPredicate(op, fid, value, fields)
    else:
        raise ValueError('Illegal predicate: %s' % str(predicate))

    node._objective = objective
    node._weight = weight

    return node

def multipredicate(adict, final_subtree, objective, fields):
    top = None
    prev_node = None
    leaf = Leaf(objective, 0)
    weight = adict['population']

    for predicate in adict['predicates'][1:]:
        node = make_predicate_node(predicate, fields, objective, weight)

        if top is None and prev_node is None:
            top = prev_node = node
        else:
            prev_node.set_subtrees(node, leaf)
            prev_node = node

    prev_node.set_subtrees(final_subtree, leaf)

    return top

def get_objective(adict, default):
    objective = adict.get('objective', default)
    return np.array(objective, dtype=np.float64).reshape(-1,)

def create_node(adict, parent, fields, depth, depth_norm):
    objective = get_objective(adict, depth / depth_norm)

    if not adict.get('children', None):
        root = Leaf(objective, adict['population'])
    else:
        ntype = get_node_type(adict, fields)
        root = ntype(adict, fields, objective)
        left, right = root.get_children(adict)

        left_subtree = create_node(left, root, fields, depth + 1, depth_norm)
        right_subtree = create_node(right, root, fields, depth + 1, depth_norm)

        root.set_subtrees(left_subtree, right_subtree)

    if len(adict['predicates']) > 1:
        if parent is None:
            preroot_objective = np.array(0, dtype=np.float64).reshape(-1,)
            return multipredicate(adict, root, preroot_objective, fields)
        else:
            return multipredicate(adict, root, parent._objective, fields)
    else:
        return root
