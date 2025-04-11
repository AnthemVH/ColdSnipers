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

model.fit(np.array(X),np.array(Y),epochs=1,verbose=1)

def respond(prompt):
    print("Prompted")
    working_prompt = prompt.split()
    prompt_vec = DH.prompt_to_vec(working_prompt.copy())
    word = ""
    response = ""
    index = 0
    while word != "eos" and index <20:
        prediction = model.predict(np.array([prompt_vec]))
        index += 1
        word = DH.vector_to_word(np.array(prediction).flatten())
        working_prompt = DH.slide_prompt(working_prompt.copy(),word)
        response += " " + word
        prompt_vec = DH.prompt_to_vec(working_prompt.copy())
    return response

def Answer_prompt(prompt):
    response = respond(prompt)
    new_response = DH.Fromat_respone(response=response)
    return new_response

print(Answer_prompt("when is my exam starting"))