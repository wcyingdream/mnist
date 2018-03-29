import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import numpy as np

mnist_data = input_data.read_data_sets("MNIST_data/", one_hot=True)

# x for 28 * 28 images data
x = tf.placeholder(tf.float32, shape= [None, 784])
# y for probability of each digit(0-9). Such as [0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
y = tf.placeholder(tf.float32, shape = [None, 10])

# define modle
weight = tf.Variable(tf.zeros([784, 10]))
bias = tf.Variable(tf.zeros([10]))
y_predic = tf.nn.softmax(tf.matmul(x, weight) + bias)

# the loss function
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=y_predic))

# minimize the loss in each training
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

# initialize
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

# training
for i in range(1000):
	batch_xs, batch_ys = mnist_data.train.next_batch(100) # get 100 random training data
	sess.run(train_step, feed_dict={x: batch_xs, y:batch_ys}) # optimize the loss with data

# evaluate accuracy with test data
correct_prediction = tf.equal(tf.argmax(y_predic, 1), tf.argmax(y, 1))
get_accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
accuracy = sess.run(get_accuracy, feed_dict={x: mnist_data.test.images, y: mnist_data.test.labels})

np.set_printoptions(threshold=np.inf) # output all data without ellopsis
np.set_printoptions(formatter={'float_kind':'{:f}'.format})
print("Model: output = input * weight + bias\nweight = {0}\nbias = {1}".format(sess.run(weight), sess.run(bias)))
print("Accuracy: {0}".format(accuracy))

print("{0}\n\n{1}\n\n{2}".format(batch_xs[0], batch_ys[0], sess.run(tf.matmul(batch_xs, weight) + bias)[0]))
sess.close()