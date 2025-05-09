import numpy as np
import DataHandling as DH

# Random initialization with better variance scaling (Xavier for tanh, He for ReLU)
weights_one = np.random.randn(500, 100) * np.sqrt(2 / 500)
bias_one = np.zeros((1, 100))

weights_two = np.random.randn(100, 100) * np.sqrt(2 / 100)
bias_two = np.zeros((1, 100))

def save_model(path="model_weights.npz"):
    np.savez(path,
             weights_one=weights_one,
             bias_one=bias_one,
             weights_two=weights_two,
             bias_two=bias_two)
    print(f"Model saved to {path}")

def load_model(path="model_weights.npz"):
    global weights_one, bias_one, weights_two, bias_two
    data = np.load(path)
    weights_one = data["weights_one"]
    bias_one = data["bias_one"]
    weights_two = data["weights_two"]
    bias_two = data["bias_two"]
    print(f"Model loaded from {path}")

load_model()
def leaky_relu(x):
    return np.where(x > 0, x, 0.001 * x)

def derivative_leaky_relu(x):
    return np.where(x > 0, 1, 0.001)

def cosine_similarity_loss(predictions, targets):
    predictions = predictions / (np.linalg.norm(predictions, axis=1, keepdims=True) + 1e-8)
    targets = targets / (np.linalg.norm(targets, axis=1, keepdims=True) + 1e-8)
    cosine = np.sum(predictions * targets, axis=1)
    loss = 1 - cosine
    return np.mean(loss)

def cosine_similarity_error(prediction, target):
    dot = np.sum(prediction * target, axis=1, keepdims=True)
    norm_output = np.linalg.norm(prediction, axis=1, keepdims=True)
    norm_target = np.linalg.norm(target, axis=1, keepdims=True)
    scaling = 1 / (norm_output * norm_target + 1e-8)
    projected = (dot / (norm_output ** 2 + 1e-8)) * prediction
    error = -scaling * (target - projected)
    return error

def cosine_accuracy(predictions, targets, threshold=0.95):
    predictions = predictions / (np.linalg.norm(predictions, axis=1, keepdims=True) + 1e-8)
    targets = targets / (np.linalg.norm(targets, axis=1, keepdims=True) + 1e-8)
    cosine_similarities = np.sum(predictions * targets, axis=1)
    correct = np.sum(cosine_similarities >= threshold)
    accuracy = correct / len(predictions)
    return accuracy

def predict(x):
    hidden = leaky_relu(np.dot(x, weights_one) + bias_one)
    output = np.dot(hidden, weights_two) + bias_two
    return output

def train(inputs, targets, epochs, lr):
    global weights_one, weights_two, bias_one, bias_two
    for epoch in range(epochs):
        total_outputs = []
        for i in range(len(inputs)):
            x = inputs[i].reshape(1, -1)
            y = targets[i].reshape(1, -1)

            hidden = leaky_relu(np.dot(x, weights_one) + bias_one)
            output = np.dot(hidden, weights_two) + bias_two
            total_outputs.append(output)

            error = cosine_similarity_error(output, y)
            grad_w2 = np.dot(hidden.T, error)
            grad_b2 = error

            delta = np.dot(error, weights_two.T) * derivative_leaky_relu(hidden)
            grad_w1 = np.dot(x.T, delta)
            grad_b1 = delta

            weights_two -= lr * grad_w2
            bias_two -= lr * grad_b2

            weights_one -= lr * grad_w1
            bias_one -= lr * grad_b1

        total_outputs = np.vstack(total_outputs)
        targets_batch = np.vstack(targets)
        loss = cosine_similarity_loss(total_outputs, targets_batch)
        accuracy = cosine_accuracy(total_outputs,targets_batch)
        print(f"Epoch {epoch + 1}/{epochs} - Loss: {loss:.6f} - Accuracy: {accuracy:.4f}")

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
        prediction = predict(np.array([prompt_vec]))
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

def Answer_prompt_Loyd(prompt):
    return DH.Fromat_respone(response=respond(prompt))



x, y = DH.Training_Data(5)
X, Y = DH.training_to_vector(x, y)
##train(X, Y, epochs=1000, lr=0.01)
save_model()

print("\nResponse:", Answer_prompt_Loyd("when is my exam starting"))