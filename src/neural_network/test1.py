from network import NeuralNetwork

weights = [
    [
        [1, -1, 0],
        [-1, 1, 0]
    ],
    [
        [1, 1, 0]
    ]
]

data = [
    {
        'input': [0.0, 0.0],
        'output': [0.0]
    },
    {
        'input': [1.0, 0.0],
        'output': [1.0]
    },
    {
        'input': [0.0, 1.0],
        'output': [1.0]
    },
    {
        'input': [1.0, 1.0],
        'output': [0.0]
    },        
]

def format(l):
    return ['%.2f' % i for i in l]

if __name__ == "__main__":
    network = NeuralNetwork((2, 2, 1))#, weights=weights)
    network.teach(data, 1000)
    print network.weights
    for item in data:
        print format(network.calculate(item['input'])), format(item['output'])        