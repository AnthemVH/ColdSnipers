import tensorflow as tf
import numpy as np
import DataHandling as DH

model = tf.keras.Sequential([
    tf.keras.layers.Dense(100,activation="leaky_relu",input_shape=(500,)),
    tf.keras.layers.Dense(100,activation="linear")
])

model.compile(optimizer='adam',loss=tf.keras.losses.CosineSimilarity(axis=1),metrics=['accuracy'])

x,y = DH.Training_Data(5)
X,Y = DH.training_to_vector(x,y)

model.fit(np.array(X),np.array(Y),epochs=1000,verbose=1)