import tensorflow as tf
import numpy as np

model = tf.keras.Sequential([
    tf.keras.layers.Dense(100,activation="leaky_relu",input_shape=(500,)),
    tf.keras.layers.Dense(100,activation="linear")
])

model.compile(optimizer='adam',loss=tf.keras.losses.CosineSimilarity(axis=1),metrics=['accuracy'])

x = np.random.uniform(-1,1,(500,))
y= np.random.uniform(-1,1,(100,))
print(np.array(x).shape)
prediction = model.predict(np.array([x]))
model.fit(np.array([x]),np.array([y]),epochs=10,verbose=1)