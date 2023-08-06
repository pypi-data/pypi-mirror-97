import random

import shapsplain.importers
np = shapsplain.importers.import_numpy()
sk_ens = shapsplain.importers.import_sklearn_ensembles()
sk_clust = shapsplain.importers.import_sklearn_cluster()

# We don't want the full range of integers here because there are
# cases where numpy freaks out with random seeds bigger than 2 ** 32.
# This value should be sufficiently large to seed a generator
# randomly, espeically given all the other randomness here.
LARGE_INT = 32768

# We don't want to cluster over and over again if we have a whole
# bunch of classes with like 128 points each.  If we have a ton of
# classes here we'll just do plain old random sampling on the class
# level.
FANCY_SAMPLE_CLASS_LIMIT = 16

def set_sizes(total, fractions):
    start = 0

    for f in fractions:
        end = start + f
        yield int(round(end * total)) - int(round(start * total))
        start = end

def split_on_idxs(X, selected):
    selected_set = set(selected)
    unselected = []

    for i in range(X.shape[0]):
        if i not in selected_set:
            unselected.append(i)

    return X[selected,:], X[unselected,:]

def select_random(X, rng, npoints):
    if X.shape[0] <= npoints:
        return X, np.array([]).reshape((0, X.shape[1]))
    else:
        selected = sorted(rng.sample(list(range(X.shape[0])), npoints))
        return split_on_idxs(X, selected)

def select_anomalies(X, rng, npoints):
    if X.shape[0] <= npoints:
        return X, np.array([]).reshape((0, X.shape[1]))
    else:
        s = rng.randint(0, LARGE_INT)
        iforest = sk_ens.IsolationForest(n_estimators=32, random_state=s).fit(X)
        scores = iforest.score_samples(X)
        selected = np.argsort(scores, kind='mergesort')[:npoints].tolist()

        return split_on_idxs(X, sorted(selected))

def select_by_cluster(X, rng, npoints, n_clust):
    if n_clust < 2:
        return select_random(X, rng, npoints)
    else:
        s = rng.randint(0, LARGE_INT)
        Xc = sk_clust.KMeans(n_clusters=n_clust, random_state=s).fit_transform(X)
        X_sorted = np.argsort(Xc, axis=0, kind='mergesort')

        selected = set()

        for idx in X_sorted.flatten():
            # Note:  I hate break statements
            if len(selected) < npoints:
                selected.add(idx)

        return split_on_idxs(X, sorted(selected))

def select_points(X, rng, npoints, max_n_clust):
    if X.shape[0] < npoints:
        return X, np.array([]).reshape((0, X.shape[1]))
    else:
        sizes = list(set_sizes(npoints, [0.1, 0.3, 0.6]))
        n_clust = min(max_n_clust, int(round(X.shape[0]) / 8.0))

        anomalies, rem = select_anomalies(X, rng, sizes[0])
        randsamp, rem = select_random(rem, rng, sizes[1])
        clust, rem = select_by_cluster(rem, rng, sizes[2], n_clust)

        return np.concatenate([anomalies, randsamp, clust], axis=0), rem

def representatives(X, y, npoints, balanced, seed):
    class_list = np.argmax(y, 1).reshape(-1, 1)
    class_set = set(class_list.flatten().tolist())
    rng = random.Random(seed)

    if y.shape[1] > 1:
        Xy = np.concatenate([X, class_list], axis=1)
    else:
        Xy = np.concatenate([X, y], axis=1)

    if X.shape[0] <= npoints:
        return Xy
    elif y.shape[1] > 1:
        if balanced:
            class_arr = Xy
            for_classes = npoints
            all_selected = []
        else:
            overall = int(round(0.5 * npoints))
            selected, class_arr = select_points(Xy, rng, overall, 16)
            for_classes = npoints - overall
            all_selected = [selected]

        all_remaining = []
        fractions = [1.0 / len(class_set) for _ in class_set]

        for c, size in zip(sorted(class_set), set_sizes(for_classes, fractions)):
            class_points = class_arr[class_arr[:,-1] == c,:]

            if len(class_set) > FANCY_SAMPLE_CLASS_LIMIT:
                class_selected, rem = select_random(class_points, rng, size)
            else:
                class_selected, rem = select_points(class_points, rng, size, 4)

            all_selected.append(class_selected)
            all_remaining.append(rem)

        reps = np.concatenate(all_selected, axis=0)

        if reps.shape[0] < npoints:
            nmore = npoints - reps.shape[0]
            unselected = np.concatenate(all_remaining, axis=0)
            more_pts, _ = select_random(unselected, rng, nmore)

            reps = np.concatenate([reps, more_pts], axis=0)

    else:
        reps, _ = select_points(Xy, rng, npoints, 16)

    return reps
