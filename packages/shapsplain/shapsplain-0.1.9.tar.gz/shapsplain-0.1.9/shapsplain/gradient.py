import random

import shapsplain.importers
tf = shapsplain.importers.import_tensorflow()
np = shapsplain.importers.import_numpy()

from shapsplain.utils import to_numpy, shap_labels

class GradientExplainer(object):
    def __init__(self, model, data, fields, batch_size=512):
        assert len(fields) == data.shape[1]

        self._model = model
        self._data = data
        self._fields = fields
        self._batch_size = batch_size

        if len(model.output.shape) > 1:
            self._nclasses = model.output.shape[1]
        else:
            self._nclasses = 1

        data_predictions = self._model(data).numpy()
        # The "classes" of the input data are the top two predicted classes
        # for each point.  This is only used for computing the importance
        self._data_classes = np.argsort(data_predictions, axis=1)[:,:2]
        self._priors = np.mean(data_predictions, axis=0)

        self._index_map = {self._fields[k]['index']: k for k in self._fields}
        self._gradients = [None for i in range(self._nclasses)]

        # Space for sample data
        self._samples_input = np.zeros(self._data.shape, dtype=np.float32)
        self._samples_delta = np.zeros(self._data.shape, dtype=np.float32)

    def get_gradient_fn(self, i):
        if self._gradients[i] is None:
            @tf.function
            def grad_graph(X):
                phase = tf.keras.backend.learning_phase()
                tf.keras.backend.set_learning_phase(0)

                with tf.GradientTape(watch_accessed_variables=False) as tape:
                    tape.watch(X)
                    out = self._model(X)

                    if self._nclasses > 1:
                        out = out[:,i]

                X_grad = tape.gradient(out, X)
                tf.keras.backend.set_learning_phase(phase)

                return X_grad

            self._gradients[i] = grad_graph

        return self._gradients[i]

    def run(self, out, X):
        shape = list(self._model.input.shape)
        shape[0] = -1
        inputs = tf.constant(X.reshape(shape), dtype=self._model.input.dtype)

        return out(inputs)

    def point_shap(self, point, cls, rng):
        nsamples = self._data.shape[0]

        for dind in range(nsamples):
            rv = rng.random()
            self._samples_input[dind] = rv * point + (1 - rv) * self._data[dind]
            self._samples_delta[dind] = point - self._data[dind]

        grads = []

        for start in range(0, nsamples, self._batch_size):
            end = min(start + self._batch_size, nsamples)
            batch = self._samples_input[start:end,:]
            grads.append(self.run(self.get_gradient_fn(cls), batch))

        grad = np.concatenate(grads, axis=0)
        smps = grad * self._samples_delta
        return smps.mean(axis=0), smps.var(axis=0) / np.sqrt(smps.shape[0])

    def shap_values(self, X, seed):
        outputs = []

        for i in range(self._nclasses):
            phis = np.zeros(X.shape)
            phi_vars = np.zeros(X.shape)
            rng = random.Random(seed)

            for j in range(X.shape[0]):
                phi, phi_var = self.point_shap(X[j,:], i, rng)
                phis[j] = phi
                phi_vars[j] = phi_var

            outputs.append((phis, phi_vars))

        return outputs

    def compute_shap(self, X, seed=42):
        output_phis = []

        predictions = self._model(X).numpy()
        outputs = self.shap_values(X, seed)

        for i, output in enumerate(outputs):
            phi, phi_var = output
            nout = np.zeros((phi.shape[0], phi.shape[1] + 1), dtype=np.float32)

            # Use variance to correct for prediction error
            error_i = predictions[:,i] - np.sum(phi, axis=1) - self._priors[i]
            norm_var = phi_var / np.sum(phi_var, axis=1).reshape(-1, 1)
            new_phi = phi + (error_i.reshape(-1, 1) * norm_var)

            nout[:,:phi.shape[1]] = new_phi
            nout[:,phi.shape[1]] = self._priors[i]

            output_phis.append(nout)

        return output_phis

    def shap_importances(self, seed=42):
        phi_idx = 0
        dshape = self._data.shape
        dclasses = self._data_classes.shape[1]

        phis = np.zeros((dshape[0] * dclasses, dshape[1]), dtype=np.float32)

        for i in range(self._data.shape[0]):
            rng = random.Random(seed + i)

            for j in range(dclasses):
                aclass = self._data_classes[i, j]
                phi, _ = self.point_shap(self._data[i,:], aclass, rng)

                phis[phi_idx,:] = np.abs(phi)
                phi_idx += 1

        sum_phi = phis.sum(axis=0)
        shap_vals = np.array((sum_phi / np.sum(sum_phi)).tolist() + [0.0])

        return shap_labels(shap_vals, self._index_map, False)[1:]

    def predict(self, instance, explanation=False):
        X = np.expand_dims(to_numpy(self._fields, instance), axis=0)

        if explanation:
            shap_values = [arr[0] for arr in self.compute_shap(X)]
            return [shap_labels(v, self._index_map, False) for v in shap_values]
        else:
            return self._model(X)
