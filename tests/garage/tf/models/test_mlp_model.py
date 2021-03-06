import pickle

from nose2.tools.params import params
import numpy as np
import tensorflow as tf

from garage.tf.models import MLPModel
from tests.fixtures import TfGraphTestCase


class TestMLPModel(TfGraphTestCase):
    def setUp(self):
        super().setUp()
        self.input_var = tf.placeholder(tf.float32, shape=(None, 5))
        self.obs = np.ones((1, 5))

    @params((1, (0, )), (1, (1, )), (1, (2, )), (2, (3, )), (2, (1, 1)),
            (3, (2, 2)))
    def test_output_values(self, output_dim, hidden_sizes):
        model = MLPModel(
            output_dim=output_dim,
            hidden_sizes=hidden_sizes,
            hidden_nonlinearity=None,
            hidden_w_init=tf.ones_initializer(),
            output_w_init=tf.ones_initializer())
        outputs = model.build(self.input_var)
        output = self.sess.run(outputs, feed_dict={self.input_var: self.obs})

        expected_output = np.full([1, output_dim], 5 * np.prod(hidden_sizes))

        assert np.array_equal(output, expected_output)

    @params((1, (0, )), (1, (1, )), (1, (2, )), (2, (3, )), (2, (1, 1)),
            (3, (2, 2)))
    def test_is_pickleable(self, output_dim, hidden_sizes):
        model = MLPModel(
            output_dim=output_dim,
            hidden_sizes=hidden_sizes,
            hidden_nonlinearity=None,
            hidden_w_init=tf.ones_initializer(),
            output_w_init=tf.ones_initializer())
        model_pickled = pickle.loads(pickle.dumps(model))
        with tf.Session(graph=tf.Graph()) as sess:
            input_var = tf.placeholder(tf.float32, shape=(None, 5))
            outputs = model_pickled.build(input_var)
            output = sess.run(outputs, feed_dict={input_var: self.obs})

            expected_output = np.full([1, output_dim],
                                      5 * np.prod(hidden_sizes))

            assert np.array_equal(output, expected_output)
