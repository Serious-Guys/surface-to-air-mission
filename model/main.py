import tensorflow as tf
from tensorflow.keras.activations import relu
from tensorflow.keras.losses import mean_squared_error
from tensorflow.keras.metrics import MeanAbsoluteError
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, TensorBoard
import numpy as np


def get_model(input_shape):
	model = tf.keras.Sequential([tf.keras.layers.Dense(1, input_shape=input_shape)])
	return model


def get_data(N, M, total) -> tuple:
	x_train = np.random.randn(total, N*M)
	y_train = np.random.randn(total, 1)
	return x_train, y_train, x_train,y_train


def train(model, x_train, y_train, x_valid, y_valid, epochs=10, patience=3):
	adam = Adam()
	mae = MeanAbsoluteError()
	stop = EarlyStopping(monitor='val_loss', patience=patience)

	model.compile(optimizer=adam, 
		loss=mean_squared_error,
		metrics=[mae])

	history = model.fit(x_train, y_train, epochs=epochs,
	 callbacks=[stop], validation_data=(x_valid, y_valid))

	return history


if __name__ == '__main__':
	N, M = 3, 5
	data_count = 10
	x_train, y_train, x_valid, y_valid = get_data(N, M, data_count)
	model = get_model(input_shape=[N*M])
	history = train(model, x_train, y_train, x_valid, y_valid, epochs=10)
	i = 0
	x_sample = x_train[i].reshape(1,x_train[i].shape[0])
	y_pred = model.predict(x_sample)
	y_true = y_train[i]

	print(y_pred, y_true)