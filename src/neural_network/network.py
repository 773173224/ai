import random
import math
from copy import copy

class NeuralNetwork(object):
    """
    With sigmoid activation function
    """
    t = 1
    
    def __init__(self, neurals_counts, learning_rate=0.2, momentum=0, verbosity=True, weights=None):
        self.weights = []
        self.learning_rate = learning_rate
        self.neurals_counts = neurals_counts
        self.node_values = []
        self.momentum = momentum
        self.prev_weight_correction = []
        self._layers_count = len(neurals_counts)-1
        
        self._init_weights(neurals_counts, weights)

    def format(self, l):
        return ['%.2f' % i for i in l]
    
    def log(self, *args):
        if self.verbosity:
            print args
    
    def activate(self, value):
        return 1.0 / (1.0 + math.exp(-self.t*value)) 
    
    def activate_derivative(self, value):
        return self.t * value * (1.0 - value)
    
    def _init_weights(self, neurals_counts, weights=None):
        """
        init waights and threshold (w1, ..., wn, w0)
        """
        if not weights:
            for i in range(len(neurals_counts))[1:]:
                weights = []
                weights_count = neurals_counts[i-1]+1
                
                for _ in range(neurals_counts[i]):
                    weights.append([random.random()-0.5 for i in range(weights_count)])
                
                self.weights.append(weights)
        else:
            self.weights = weights
            
        for i in range(len(neurals_counts))[1:]:
            weights_count = neurals_counts[i-1]+1
            prew_weights_corrections = []
            
            for _ in range(neurals_counts[i]):
                prew_weights_corrections.append([0]*weights_count)
            
            self.prev_weight_correction.append(prew_weights_corrections)
            
    def calculate(self, input):
        self.node_values = []
        self.input = copy(input) 
        
        for layer in self.weights:
            values = []

            for weights in layer:
                s = ''
                value = 0
                for i, _ in enumerate(input):
                    value += weights[i] * input[i]
                    s += '+%.2f*%.2f' % (weights[i], input[i])
                s += '+%.2f' % weights[-1]
                value += weights[-1]
                s += '=%.2f' % value
                result = self.activate(value)
                s += '=%.2f' % result
                #print s
                values.append(result)
                
            self.node_values.append(copy(values))
            
            input = values
        
        return input
    
    def backpropagate(self, output, desired_output):
        error_gradient = [0]*self._layers_count
        
        #calculate error gradient
        
        #calculate for output(last) layer
        layer = -1
        errors = []
        
        for node in range(len(self.weights[layer])):
            error = desired_output[node] - output[node]
            errors.append(self.activate_derivative(output[node]) * error)        
        
        error_gradient[-1] = errors
        
        #calculate for hidden layers
        for layer in range(self._layers_count-1)[::-1]:
            errors = []
            next_layer = layer + 1
            
            for node, _ in enumerate(self.weights[layer]):
                sum = 0
                
                for next_node in range(len(self.weights[next_layer])):
                    gradient = error_gradient[next_layer][next_node]
                    weight = self.weights[next_layer][next_node][node]
                    sum += gradient * weight
                
                value = self.node_values[layer][node]
                errors.append(self.activate_derivative(value) * sum)
            
            error_gradient[layer] = errors
        
        #update weights
        for layer in range(self._layers_count):
            for node, _ in enumerate(self.weights[layer]):
                er_gr = error_gradient[layer][node]
                #update w0
                self.weights[layer][node][-1] += self.learning_rate * er_gr
                
                if layer == 0:
                    input = self.input
                else:
                    input = self.node_values[layer-1]
                    
                #update other weights
                for i, _ in enumerate(self.weights[layer][node][:-1]):
                    weight_correction = self.learning_rate * er_gr * input[i]
                    prev_correction = self.prev_weight_correction[layer][node][i]
                    self.weights[layer][node][i] += weight_correction + prev_correction * self.momentum
                    self.prev_weight_correction[layer][node][i] = weight_correction
        
    def teach(self, data, max_retries=1000):
        for i in range(max_retries):
            if i % 1000 == 0:
                print i, 'of', max_retries
            
            #random.shuffle(data)
            
            errors = []
            for item in data:
                #print '=================================='

                desired_output = item['output']

                output = self.calculate(item['input'])

                errors.append(self.least_mean_square(output, desired_output))
                
                self.backpropagate(output, desired_output)
                
            if i % 1000 == 0:
                print self.root_mean_squared_error(errors)
    
    def test(self, data):
        for item in data:
            print self.format(self.calculate(item['input'])), self.format(item['output'])   
            
    def root_mean_squared_error(self, errors):
        sum = 0
        for error in errors:
            sum += error ** 2
            
        return math.sqrt(sum/len(errors))
                
    def least_mean_square(self, output, desired_output):
        err = 0
        
        for i in range(len(output)):
            err += (desired_output[i] - output[i]) ** 2 
            
        return err/2