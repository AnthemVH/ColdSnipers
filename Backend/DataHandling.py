from gensim.models import Word2Vec
import numpy as np
import database as db

temp_sentences = ["pad hey how are you im good and you eos","pad pad whats your name my name is loyd eos","what colour is the sky the sky is blue eos"]
Training_sentences = ["hey how are you ,im good and you eos","whats your name ,my name is loyd eos","what colour is the sky ,the sky is blue eos"]
temp_sentences = []
with open("../Frontend/word2vec_training.txt",'r') as file:
    for files in file:
        temp_sentences.append((files.strip()).lower())
Training_sentences = []
with open("../Frontend/data.txt",'r') as file:
    for files in file:
        Training_sentences.append((files.strip()).lower())
print(temp_sentences)
sentences = []
for index in range(len(temp_sentences)):
    tokenized_sentence = temp_sentences[index].split()
    sentences.append(tokenized_sentence)

word2vec_model = Word2Vec(sentences=sentences,vector_size=100,workers=4,window=5,min_count=1)


def word_to_vector(word):
    try:
        vector = word2vec_model.wv(word)
    except:
        vector = np.zeros(100)
    return vector

def vector_to_word(vector):
    word = word2vec_model.wv.similar_by_vector(vector,topn=1)[0][0]
    return word

def Training_Data(window_size):
    x_training = []
    y_training = []
    split_training = []
    for index in range(len(Training_sentences)):
        split_sentence = Training_sentences[index].split(":")
        x = split_sentence[0].split()
        y= split_sentence[1].split()
        if len(x) < window_size:
            while len(x) < window_size:
                x.insert(0,"pad")
            x_training.append(x.copy())
            y_training.append(y[0])
            for output_index in range(1,len(y)):
                x.pop(0)
                x.append(y[output_index-1])
                if output_index < len(y):
                    x_training.append(x.copy())
                    y_training.append(y[output_index])
            
        elif len(x) > window_size:
            start = x[:5].copy()
            x_training.append(start)
            y_training.append(x[window_size])
            for input_index in range(window_size,len(x)):
                start.pop(0)
                start.append(x[input_index])
                if input_index +1 < len(x):
                    x_training.append(start)
                    y_training.append(x[input_index+1])  
            for output_index in range(0,len(y)):
                start.pop(0)
                start.append(y[output_index])
                if output_index < len(y):
                    x_training.append(start.copy())
                    y_training.append(y[output_index]) 
        else:
            x_training.append(x.copy())
            y_training.append(y[0])
            for output_index in range(1,len(y)):
                x.pop(0)
                x.append(y[output_index-1])
                if output_index < len(y):
                    x_training.append(x.copy())
                    y_training.append(y[output_index])

    return x_training,y_training


def training_to_vector(Input,outputs):
    x_vector_training = []
    y_vector_training = []
    for index in range(len(Input)):
        vector = []
        for input_index in range(len(Input[index])):
            try:
                vector.append(word2vec_model.wv[Input[index][input_index]])
            except:
                vector.append(np.zeros(100))
        
        x_vector_training.append(np.array(vector).flatten())
        y_vector_training.append(word2vec_model.wv[outputs[index]])
    return x_vector_training,y_vector_training



def prompt_to_vec(prompt):
    prompt_vector = []
    if len(prompt) < 5:
        while len(prompt) < 5:
            prompt.insert(0,"pad")
    for index in range(len(prompt)):
        prompt_vector.append(word2vec_model.wv[prompt[index]])
    return np.array(prompt_vector).flatten()

def slide_prompt(prompt,newword):
    newprompt = prompt.copy()
    newprompt.pop(0)
    newprompt.append(newword)
    return newprompt

def Fromat_respone(response):
    New_response_list = response.split()
    New_response_list[0] = New_response_list[0].capitalize() #Make first letter capital
    New_response = ""
    for index in range(len(New_response_list)):
        word = New_response_list[index]
        if (word[0] == '<') and (word[-1] == '>') and (word != "<EventList>"):
            information = db.Retrieve_Module(word)
            New_response += " " + information
        elif word == "<EventList>":
            information = db.RetrieveEvents()
            New_response += " " + information
        elif word == "eos":
            New_response += ""
        else:
            New_response += " " + word
    return (New_response)


    