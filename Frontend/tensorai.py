import tensorflow as tf
import numpy as np
import DataHandling as DH

model = tf.keras.Sequential([
    tf.keras.layers.Dense(300,activation="leaky_relu",input_shape=(500,)),
    tf.keras.layers.Dense(100,activation="linear")
])

model.compile(optimizer='adam',loss=tf.keras.losses.CosineSimilarity(axis=1),metrics=['accuracy'])

x,y = DH.Training_Data(5)

X,Y = DH.training_to_vector(x,y)

model.fit(np.array(X),np.array(Y),epochs=2000,verbose=1)

def respond(prompt):
    prompt_bigger_window = False
    if len(prompt.split()) > 5:
        working_prompt = prompt.split()[:5]
        prompt_bigger_window = True
    else:
        working_prompt = prompt.split()
    prompt_vec = DH.prompt_to_vec(working_prompt.copy())
    response = ""
    word = ""
    index = 0
    while word != "eos" and index < 20:
        prediction = model.predict(np.array([prompt_vec]))
        word = DH.vector_to_word(prediction.flatten())
        working_prompt = DH.slide_prompt(working_prompt, word)
        prompt_vec = DH.prompt_to_vec(working_prompt)
        if prompt_bigger_window == True:
            if (prompt.split()[-1] == word) or (index == ((len(prompt.split()))-5)):
                prompt_bigger_window = False
        else:
            response += " " + word
        index += 1
    print(response)
    return response.strip()

def Answer_prompt(prompt):
    return DH.Fromat_respone(response=respond(prompt))

print(Answer_prompt("when is the mapc1112 exam"))