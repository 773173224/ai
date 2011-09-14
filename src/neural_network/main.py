from network import NeuralNetwork
from pprint import pprint
data = [
    {
        'output': [1, 0, 0],
        'input': (
            1,1,1,1,1,
            1,0,0,0,1,
            1,0,0,0,1,
            1,0,0,0,1,
            1,0,0,0,1,
            1,0,0,0,1,
            1,1,1,1,1
        )
    },
    {
        'output': [0, 1, 0],
        'input': (
            0,0,0,0,1,
            0,0,0,0,1,
            0,0,0,0,1,
            0,0,0,0,1,
            0,0,0,0,1,
            0,0,0,0,1,
            0,0,0,0,1
        )
    },
    {
        'output': [0, 0, 1],
        'input': (
            0,1,1,1,1,
            0,0,0,0,1,
            0,0,0,1,0,
            0,0,1,0,0,
            0,1,0,0,0,
            1,0,0,0,0,
            1,1,1,1,1
        )
    },        
]

def format(l):
    return ['%.2f' % i for i in l]

if __name__ == "__main__":
    network = NeuralNetwork((5*7, 14, 3), learning_rate=0.1, momentum=0.8)
    network.teach(data, 10000)
    
    for item in data:
        print format(network.calculate(item['input'])), format(item['output'])

