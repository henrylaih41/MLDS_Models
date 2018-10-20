import tensorflow as tf
import numpy as np
import math
from keras.utils import np_utils
import matplotlib.pyplot as plt
import sys


##load_data
mnist = tf.keras.datasets.mnist
(x_train, y_train),(x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0
num_data=x_train.shape[0]
x_train=x_train.reshape(-1,784)
x_test=x_test.reshape(-1,784)
y_train=np_utils.to_categorical(y_train, 10)
y_test=np_utils.to_categorical(y_test, 10)

X = tf.placeholder(shape=[None,784], dtype=tf.float32, name="X")
Y = tf.placeholder(shape=[None,10], dtype=tf.float32, name="Y")

##first model
W1_1 = tf.Variable(tf.truncated_normal([784, 300], stddev=0.1))  
B1_1 = tf.Variable(tf.truncated_normal([300], stddev=0.1))
W1_2 = tf.Variable(tf.truncated_normal([300, 200], stddev=0.1))  
B1_2 = tf.Variable(tf.truncated_normal([200], stddev=0.1))
W1_3 = tf.Variable(tf.truncated_normal([200, 200], stddev=0.1))  
B1_3 = tf.Variable(tf.truncated_normal([200], stddev=0.1))
W1_4 = tf.Variable(tf.truncated_normal([200, 200], stddev=0.1))  
B1_4 = tf.Variable(tf.truncated_normal([200], stddev=0.1))
W1_5 = tf.Variable(tf.truncated_normal([200, 200], stddev=0.1))  
B1_5 = tf.Variable(tf.truncated_normal([200], stddev=0.1))
W1_6 = tf.Variable(tf.truncated_normal([200, 100], stddev=0.1))  
B1_6 = tf.Variable(tf.truncated_normal([100], stddev=0.1))
W1_7 = tf.Variable(tf.truncated_normal([100, 50], stddev=0.1))  
B1_7 = tf.Variable(tf.truncated_normal([50], stddev=0.1))
W1_8 = tf.Variable(tf.truncated_normal([50, 10], stddev=0.1))  
B1_8 = tf.Variable(tf.truncated_normal([10], stddev=0.1))

total_par=[W1_1,B1_1,W1_2,B1_2,W1_3,B1_3,W1_4,B1_4,W1_5,B1_5,W1_6,B1_6,W1_7,B1_7,W1_8,B1_8]


O1_1 = tf.nn.relu(tf.matmul(X, W1_1) + B1_1)
O1_2 = tf.nn.relu(tf.matmul(O1_1, W1_2) + B1_2)
O1_3 = tf.nn.relu(tf.matmul(O1_2, W1_3) + B1_3)
O1_4 = tf.nn.relu(tf.matmul(O1_3, W1_4) + B1_4)
O1_5 = tf.nn.relu(tf.matmul(O1_4, W1_5) + B1_5)
O1_6 = tf.nn.relu(tf.matmul(O1_5, W1_6) + B1_6)
O1_7 = tf.nn.relu(tf.matmul(O1_6, W1_7) + B1_7)
pred_1 = tf.nn.softmax(tf.matmul(O1_7, W1_8) + B1_8)
loss_1 = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits = pred_1, labels = Y)) 
correct_prediction = tf.equal(tf.argmax(pred_1, 1), tf.argmax(Y, 1))
acc_num = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))




with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    par1=np.load("32.npy")
    par2=np.load("4096.npy")
    train_loss_arr = []
    train_acc_arr = []
    val_loss_arr = []
    val_acc_arr = []
    a=-1.0
    for i in range(300):
        weight=(1-a)*par1+a*par2
        for i,weights in enumerate(weight):
            assign=total_par[i].assign(weights)
            sess.run(assign)
        tra_l, tra_a = sess.run([loss_1,acc_num],{X: x_train, Y: y_train})
        train_loss_arr.append(tra_l)
        train_acc_arr.append(tra_a)
        val_l, val_a = sess.run([loss_1,acc_num],{X: x_test, Y: y_test})
        val_loss_arr.append(val_l)
        val_acc_arr.append(val_a)
        a+=0.01
        print(a)
    axis=np.arange(-1,2,0.01)
    plt.plot(axis,val_acc_arr,'b:')
    plt.plot(axis,train_acc_arr,'b')
    plt.plot(axis,val_loss_arr,'r:')
    plt.plot(axis,train_loss_arr,'r')
    plt.legend(['test_acc', 'train_acc','test_loss','train_loss'], loc='upper right')
    plt.show()
