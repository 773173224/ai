from network import NeuralNetwork
import matplotlib.pyplot as plt

if __name__ == "__main__":
    network = NeuralNetwork((4, 3, 4))

    x = []
    y = []
    xd = []
    yd = []
    for i in range(-50, 50):
        val = i / 10.

        xd.append(val)
        yd.append(network.activate_derivative(network.activate(val)))
    plt.plot(xd, yd, 'b-')
    plt.show()
