# Shapsplain

A wrapper library for SHAP-value based explanations, suitable for
several sorts of BigML models.  For an explanation of Shapely-value
based model explanation, there are academic papers on both
[tree-based](https://arxiv.org/abs/1802.03888) and
[gradient-based](https://arxiv.org/abs/1703.01365) algorithms.

SHAP-valued explanations are additive, in the sense that you start out
with some "expected value" for a prediction (usually based on the
prior distribution of the training data), and then each feature
contributes some amount to "push" the prediction in one direction or
another.  As such, SHAP importance values can be positive or negative.

## Tree-based Model Explanations

To construct a Shapely-value predictor for a BigML model, one can use
the `ShapForest` class:

```
from shapsplain.forest import ShapForest

forest = ShapForest(model)
```

where `model` is a dictionary containing the JSON model downloaded
from BigML.  To make a prediction with the model, one can use the
`predict` method:

```
forest.predict({'petal length': 4.2, 'sepal length': 0.2})
```

If this is an anomaly detector, for example, this will output a list
with a single value:

```
[0.8785773]
```

To get an explanation with the prediction, pass the optional argument
`explanation=True`.


```
forest.predict({'petal length': 4.2, 'sepal length': 0.2}, explanation=True)
```

The value returned from this call is a list, with one element per
class for classification models, or a single element for regression
models and anomaly detectors.  In the inner lists, The first value is
the prediction.  Subsequent values are the importance factors for each
feature in the model, ordered by absolute importance value.

```
[
    [
        0.8785772973680668,
        ["000003", 0.10580323276121423],
        ["000004", 0.12349988309753568],
        ["000001", 0.1452021495824386],
        ["000000", 0.034717729468588754],
        ["000002", 0.029713614812585054]
    ]
]
```

Subtracting all of these importances from the prediction will give a
"baseline" score for the model on its training data.  You can see from
the importances above that the two provided values for the model are
far less important than the missing values for "petal width", "sepal
width", and "species", as there were no missing values in training.

In general, these importance values may be positive or negative,
depending on their overall impact on the prediction.  For example,
let's generate an explanation for an "Iris" model prediction for one of
the "Iris-setosa" instances.

```
forest = ShapForest(iris_classifier)
pt = {"petal length": 5.1, "petal width": 3.5, "sepal length": 1.4, "sepal width": 0.2}
forest.predict(pt, explanation=True)
```

Here, of course, the outermost list will have three elements, one for
each class.  Also, we see that in this case all features happen to
contribute positively to the positively predicted class, but this is
not true in general.

```
[
    [
        1.0,
        ['000002', 0.31709336248906567],
        ['000003', 0.29068868841929324],
        ['000000', 0.06062257935410617],
        ['000001', 0.0025287030708683912]
    ],
    [
        0.0,
        ['000002', -0.16150644430157587],
        ['000003', -0.15387190455071248],
        ['000000', -0.02328311608231396],
        ['000001', 0.004928131601268985]],
    [
        0.0,
        ['000002', -0.15558691818748985],
        ['000003', -0.13681678386858068],
        ['000000', -0.03733946327179222],
        ['000001', -0.0074568346721373725]
    ]
]
```

If one wishes to have a direction-agnostic notion of importance for
the predicted class, the absolute value of the returned values may be
normalized and still retain a useful semantics.
