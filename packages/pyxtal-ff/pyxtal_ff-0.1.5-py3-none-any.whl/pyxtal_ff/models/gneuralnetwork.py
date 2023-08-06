import gc
import time
import torch
import numpy as np
from collections import OrderedDict
from pyxtal_ff.models import Regressor


class NN():
    def __init__(self, model):
        keys = ['elements', 'activation', 'weights', 'scalings', 'batch_size',
                'force_coefficient', 'alpha', 'softmax', 'logger', 'runner', 
                'restart', 'use_force']
        
        for key in keys:
            values = getattr(model, key)
            setattr(self, key, values)


    def preprocess(self, descriptors, features):
        """ Split the input descriptors and energy & force. """

        self.no_of_descriptors = descriptors['no_of_descriptors']
        self.no_of_structures = descriptors['no_of_structures']
        
        self.x = descriptors['x']
        if self.use_force:
            self.dxdr = descriptors['dxdr']
        else:
            self.dxdr = [None]*len(self.x)
        
        # Flush memory
        gc.collect()
        
        # Descriptors in Torch mode.
        for i in range(self.no_of_structures):
            for element in self.elements:
                self.x[i][element] = torch.FloatTensor(
                                    self.x[i][element]).cuda()
                if self.use_force:
                    self.dxdr[i][element] = torch.FloatTensor(
                                    self.dxdr[i][element]).cuda()
        
        self.energy = torch.FloatTensor(features['energy'])
        self.force = []
        for i in range(len(features['force'])):
            self.force.append(torch.from_numpy(features['force'][i]).float())

        # Flush memory
        gc.collect()
    
    
    def train(self, descriptors, features, optimizer):

        # Preprocess descriptors and features
        self.preprocess(descriptors, features)

        # Initiate batch...
        self.epoch = []
        self.losses= []           
        if self.batch_size == None:
            self.batch_size = self.no_of_structures
        modulus = self.no_of_structures % self.batch_size
        self.multiplier = int((self.no_of_structures - modulus) / 
                              self.batch_size)
        self.iterator = self.multiplier
        
        print("\n")
        print("========================== Training ==========================")
        print(f"Restart: {self.restart}")
        print(f"Runner: {self.runner}")
        print(f"Batch: {self.batch_size}")
        print(f"Force_coefficient: {self.force_coefficient}")
        
        # Run Neural Network training
        t0 = time.time()
        self.regressor = Regressor(optimizer['method'], 
                                   optimizer['derivative'],
                                   optimizer['parameters'])
        self.vector, self.loss = self.regressor.regress(model=self)
        t1 = time.time()
        
        print("The training time: {:.2f} s".format(t1-t0))
        print("==================== Training is Completed ===================")
        
        
    def get_loss(self, parameters, lossprime, suppress=False):
        self.vector = parameters
        
        # Minibatch method setup
        if self.iterator < (self.multiplier-1):
            self.iterator += 1
        else:
            self.batches = self.minibatch(self.no_of_structures, 
                                          self.batch_size)
            self.iterator = 0
        
        # Get the Loss and dLossdW
        loss, dLossdW = self.calculate_loss(self.batches[self.iterator],
                                            lossprime)
        
        self.losses.append(loss)

        if not suppress:
            print("Epoch: {:4d}, Loss: {:16.8f}".format(len(self.losses), loss))
            if self.logger:
                self.logger.info("Epoch: {:4d}, Loss: {:16.8f}".format(
                                                           len(self.losses), loss))

        return loss, dLossdW
    
    
    def calculate_loss(self, batch, lossprime):
        """Calculate the error function and its derivative with respect to the
        parameters (weights and scalings).
        
        This error function is consistent with:
        Behler, J. Int. J. Quantum Chem. 2015, 115, 1032– 1050."""
        no_of_samples = len(batch)
        energyloss = 0.
        forceloss = 0.
        dEnergydWeights = torch.zeros((self.ravel.count,))
        dForcedWeights = torch.zeros((self.ravel.count,))
        dLossdW = None
        
        for i in batch:
            if self.force_coefficient:
                fc = self.force_coefficient
            else:
                fc = 1. / (len(self.force[i]) * 3)
            
            # Determine number of atoms in i-th crystal structure
            no_of_atoms = 0
            for key in self.x[i].keys():
                no_of_atoms += len(self.x[i][key])
                
            nnEnergy, nnForce, dEdW, dFdW = self.calculate_nnResults(
                                            self.x[i],
                                            self.dxdr[i],
                                            self.ravel.count)
            
            true_energy = self.energy[i]
            energyloss += self.softmax[i] * ((nnEnergy - true_energy) / no_of_atoms) ** 2

            if self.dxdr[i] is not None:
                true_force = self.force[i]
                forceloss += self.softmax[i] * torch.sum((nnForce - true_force) ** 2.) \
                            * fc / 3. / no_of_atoms

            if lossprime:
                # dEdW
                dEnergydWeights += self.softmax[i] * (nnEnergy - true_energy) \
                                     * dEdW / (no_of_atoms ** 2)
                                     
                # dFdW
                if self.dxdr[i] is not None:
                    temp = torch.zeros(self.ravel.count)
                    for p in range(no_of_atoms):
                        for q in range(3):
                            temp += (nnForce[p][q] - true_force[p][q]) *\
                                        dFdW[(p, q)]
                    dForcedWeights += self.softmax[i] * temp * fc / 3. / no_of_atoms

        # Add regularization
        W0 = self.clean_bias(self.weights)
        flat_weights = self.ravel.to_vector(self.weights, gpu=True)
        regTerm = self.alpha * torch.sum(flat_weights**2)
        
        loss = (energyloss + forceloss + regTerm) / (2 * no_of_samples)
        if lossprime:
            dRegdWeights = self.alpha*flat_weights
            dLossdW = (dEnergydWeights + dForcedWeights + dRegdWeights) / \
                                 (no_of_samples)

        gc.collect()
        
        return loss, (dLossdW.numpy()).astype(np.float64)
    
    
    def calculate_energy_forces(self, x, dxdr=None, w=None):
        """
        A routine to compute energy and forces only.
        Used for the purpose of evalution.
        See detailed math in documentation

        Args:
        -----------
        x: 2D array
            input descriptors
        dxdr: 4d array (optional)
            the primes of inputs
        w: dict of 2D arrays
            weights 

        Returns:
        --------
        energy: float, 
            the predicted energy
        forces: 2D array [N_atom, 3] (if dxdr is provided)
            the predicted forces
        """

        # load the default parameters
        elements = self.elements
        scalings = self.scalings

        # load the weights
        if w is None:
            w = self.weights

        no_of_atoms = 0
        for e in elements:
            no_of_atoms += len(x[e])
            
        energy = 0.

        forces = torch.cuda.FloatTensor(no_of_atoms, 3).fill_(0)
        o, ohat, aprime, aprime2, dodx, dohatdx = self.forward(x, w)
        
        for e in elements:
            _slope, _intercept = scalings[e]['slope'], scalings[e]['intercept']
            energy += torch.sum(_slope * o[e][len(o[e])-1] + _intercept)
            if dxdr is not None:
                dEdx = torch.sum(dodx[e][len(dodx[e])-1], axis=1)
                forces += - _slope * torch.einsum('ik, ijkl->jl', dEdx, dxdr[e]) 
                
        return energy.cpu(), forces.cpu()

    def calculate_forces(self, _dxdr, _dodx, _slope):
        """
        A routine to compute forces only.
        """
        dEdx = torch.sum(_dodx[len(_dodx)-1], axis=1)
        _forces = - _slope * torch.einsum('ik, ijkl->jl', dEdx, _dxdr) 
 
        return _forces
        
    def calculate_nnResults(self, x, dxdr=None, ravel_count=None):
        """
        A routine to compute energy and forces only.
        Used for the purpose of evalution.
        See detailed math in documentation

        Args:
        -----------
        x: 2D array
            input descriptors
        dxdr: 4d array (optional)
            the primes of inputs
        ravel_count: int
            The total number of weights

        Returns:
        --------
        energy: float, 
            the predicted energy
        forces: 2D array [N_atom, 3] (if dxdr is provided)
            the predicted forces
        dEdW: 1D array (#_of_weights)
            the derivative of energy W.R.T weights
        dFdw: 4D array (N_atom, 3, #_of_weights)
            the derivative of force W.R.T weights
        """

        # load the default parameters
        elements = self.elements
        scalings = self.scalings
        w = self.weights
        W = self.remove_bias(w)

        no_of_atoms = 0
        for e in elements:
            no_of_atoms += len(x[e])
            
        energy = 0.
        wcount = 0
        forces = torch.cuda.FloatTensor(no_of_atoms, 3).fill_(0)
        
        dnnEnergydWeights = torch.cuda.FloatTensor(ravel_count).fill_(0)
        dnnForcedWeights = torch.cuda.FloatTensor(no_of_atoms, 3 , ravel_count).fill_(0)

        o, ohat, aprime, aprime2, dodx, dohatdx = self.forward(x, w)
        dEdW, dFdW = self.backprop(o, ohat, aprime, aprime2, dodx, dohatdx, W, dxdr)
        
        for e in elements:
            _slope, _intercept = scalings[e]['slope'], scalings[e]['intercept']
            energy += torch.sum(_slope * o[e][len(o[e])-1] + _intercept)
            if dxdr is not None:
                #dEdx = torch.sum(dodx[e][len(dodx[e])-1], axis=1)
                #forces += - _slope * torch.einsum('ik, ijkl->jl', dEdx, dxdr[e]) 
                forces += self.calculate_forces(dxdr[e], dodx[e], _slope)
                
            for i in range(1, len(W[e])+1):
                
                # dE/dW
                dEdW[e][i] *= _slope
                Etemp = dEdW[e][i].flatten()
                _size = len(Etemp)
                dnnEnergydWeights[wcount:(wcount+_size)] += Etemp

                # dF/dW
                if dxdr is not None:
                    dFdW[e][i] *= - _slope
                    s1, s2, s3, s4 = dFdW[e][i].size()
                    Ftemp = dFdW[e][i].reshape((s1, s2, _size))
                    dnnForcedWeights[:, :, wcount:(wcount+_size)] += Ftemp
                
                wcount += _size
                        
        return energy.cpu(), forces.cpu(), \
               dnnEnergydWeights.cpu(), dnnForcedWeights.cpu()
               
    
    def forward(self, x, w=None):
        """
        A routine to perform foward NN calculation.
        See detailed math in documentation

        Parameters:
        -----------
        x: 2D array
            inputs descriptors
        w: dict of 2D arrays
            weights including bias as a dictionary of 2D arrays

        Returns:
        --------
        o: dict of 2D arrays
            the output of each layer 
        ohat: dict of 2D arrays
            the concatenated neuron values 
        dodx: dict of 2D arrays 
            the derivative of o 
        dohatdx: dict of 2D arrays
            the derivative of ohat 
        aprime: dict of 2D arrays
            the derivative of activation functions with respect to output 
        aprime2: dict of 2D arrays
            the 2nd derivative of activation functions with respect to output 
        """

        # load the default parameters
        elements = self.elements
        activation = self.activation

        # load the weights
        if w is None:
            w = self.weights
        W = self.remove_bias(w)

        # initialize the properties
        o, ohat, dodx, dohatdx = {}, {}, {}, {} # starts from 0
        aprime, aprime2 = {}, {}                # starts from 1
        
        # Feedforward neural network
        for e in elements:
            _x = x[e]
            _W = W[e]
            _w = w[e]
            _activation = activation[e]

            o[e], ohat[e] = {}, {}
            aprime[e], aprime2[e] = {}, {}
            dodx[e], dohatdx[e] = {}, {}
            
            o[e][0] = _x
            
            dohatdx[e][0] = torch.cuda.FloatTensor(_x.shape[0], _x.shape[1]+1, _x.shape[1]).fill_(0)
            dodx[e][0] = torch.cuda.FloatTensor(_x.shape[0], _x.shape[1], _x.shape[1]).fill_(0)
            
            #for i in range(_x.shape[1]):
            #    dodx[e][0][:, i, i] = 1
            #    dohatdx[e][0][:, i, i] = 1

            shp = _x.shape[1]
            dodx[e][0][:, np.arange(shp), np.arange(shp)] = 1
            dohatdx[e][0][:, np.arange(shp), np.arange(shp)] = 1

            ones = torch.cuda.FloatTensor(len(_x), 1).fill_(1)
            ohat[e][0] = torch.cat((_x, ones), 1)
            
            aprime[e][0] = None
            aprime2[e][0] = None
            N_layer = len(_W)
            for i in range(N_layer):
                term = torch.mm(ohat[e][i], _w[i+1])
                o[e][i+1] = ACTIVATION(term, _activation[i], 0)
                aprime[e][i+1] = ACTIVATION(o[e][i+1], _activation[i], 1)

                if i == 0:
                    dodx[e][i+1] = torch.einsum('ij,jk->ijk', 
                                                aprime[e][i+1], _W[i+1].T)
                else:
                    term = torch.einsum('ij,jk->ijk', aprime[e][i+1], _W[i+1].T)
                    dodx[e][i+1] = torch.einsum('ijk,ikl->ijl', term, dodx[e][i])

                N_x = len(o[e][i+1]) # number of neurons
                ones = torch.cuda.FloatTensor(N_x, 1).fill_(1)
                ohat[e][i+1] = torch.cat((o[e][i+1], ones), 1)
                
                #used for only force training
                aprime2[e][i+1] = ACTIVATION(o[e][i+1], _activation[i], 2)
                if i < N_layer-1:
                    dohatdx[e][i+1] = torch.cuda.FloatTensor(_x.shape[0], o[e][i+1].shape[1]+1, _x.shape[1]).fill_(0)
                    dohatdx[e][i+1][:,:-1,:] = dodx[e][i+1]

        return o, ohat, aprime, aprime2, dodx, dohatdx
    
 
    def backprop(self, o, ohat, aprime, aprime2, dodx, dohatdx, 
                 w=None, dxdr=None):
        """
        A routine to perform backward NN calculation.
        See detailed math in documentation

        Parameters:
        -----------
            o: dict, 
                the output of each layer as a dict of 2D arrays
            ohat: dict, 
                the concatenated neuron values as a dict of 2D arrays
            dodx: dict, 
                the derivative of o as a dict of 2D arrays
            dohatdx: dict, 
                the derivative of ohat as a dict of 2D arrays
            aprime: dict, 
                the derivative of activation functions with respect to output 
            aprime2: dict, 
                the 2nd derivative of activation functions with respect to output 
            w: dict, 
                weights as a dictionary of 2D arrays
            dxdr: array, 
                decriptor primes as 4D array [N_atom, N_atom, N_x, 3]

        Returns:
        --------
            dEdW: dict, 
                the derivative of total energy WRT weights as a dict of 2D arrays
            dFdW: dict, 
                the derivative of forces WRT weights as a dict of 4D arrays
        """

        # load the default parameters
        elements = self.elements

        # load the weights
        if w is None:
            w = self.weights

        # initialize the properties
        delta, delta_prime, dEdW, d2EdxdW, dFdW = {}, {}, {}, {}, {}

        # backprop
        for e in elements:
            _w = w[e]

            if dxdr is None:
                _dxdr = None
            else:
                _dxdr = dxdr[e]

            N = len(w[e])
            delta[e], delta_prime[e] = {}, {}
            dEdW[e], d2EdxdW[e], dFdW[e] = {}, {}, {}

            for i in range(N, 0, -1):
                term = torch.einsum('jk,ikl->ijl', _w[i].T, dodx[e][i-1])
                if i == N:
                    delta[e][i] = aprime[e][i]
                    if _dxdr is not None:
                        delta_prime[e][i] = torch.einsum('ij,ijk->ijk', 
                                                         aprime2[e][i], term)
                else:
                    delta[e][i] = torch.mm(delta[e][i+1], _w[i+1].T) * aprime[e][i] 
                    if _dxdr is not None:
                        term0 = torch.einsum('ijk,jl->ilk', 
                                          delta_prime[e][i+1], _w[i+1].T)
                        term1 = torch.einsum('ijk,ij->ijk', term0, aprime[e][i])
                        term2 = torch.mm(delta[e][i+1], _w[i+1].T) * aprime2[e][i]
                        term3 = torch.einsum('ij,ijk->ijk', term2, term)
                        delta_prime[e][i] = term1 + term3

                dEdW[e][i] = torch.einsum('ij,ik->kj', delta[e][i], ohat[e][i-1])

                if _dxdr is not None:
                    term1 = torch.einsum('ij,ikl->ikjl', 
                                      delta[e][i], dohatdx[e][i-1])
                    term2 = torch.einsum('ijk,il->iljk', 
                                      delta_prime[e][i], ohat[e][i-1])
                    d2EdxdW[e][i] = term1 + term2
                    dFdW[e][i] = torch.einsum('ijkl,imln->mnjk', 
                                 d2EdxdW[e][i], _dxdr,)
                    
        return dEdW, dFdW


    def remove_bias(self, weights):
        """Remove the bias term from weights.
        
        Parameters
        ----------
        weights: dict
            Weights of the neural network model.
        
        Returns
        -------
        dict
            The original weights without bias.
        """
        _WEIGHTS = {}
        
        for key in weights.keys():
            _WEIGHTS[key] = {}
            for i in range(len(weights[key])):
                    _WEIGHTS[key][i+1] = weights[key][i+1][:-1]
                    
        return _WEIGHTS
    
    
    def clean_bias(self, weights):
        """Reset the bias term to 0 from weights.
        
        Parameters
        ----------
        weights: dict
            Weights of the neural network model.
        
        Returns
        -------
        dict
            The Weights with bias as 0 rows.
        """
        _WEIGHTS = {}
        
        for key in weights.keys():
            _WEIGHTS[key] = {}
            for i in range(len(weights[key])):
                    tmp = weights[key][i+1][:-1]
                    zeros = torch.cuda.FloatTensor(1, tmp.shape[1]).fill_(0)
                    _WEIGHTS[key][i+1] = torch.cat((tmp, zeros))
                    
        return _WEIGHTS
 
    
    def minibatch(self, no_of_structures, batch_size):
        """Set up minibatch for * Gradient Descent optimization.
        
        Parameters
        ----------
        no_of_structures: int
            The number of samples.
        batch_size: int
            The number of batch per training.
        """
        samples = no_of_structures
        array = np.arange(samples)
        np.random.shuffle(array)
        
        mod = samples % batch_size
        multiplier = int((samples - mod) / batch_size)
        size = int(multiplier * batch_size)
        
        return array[:size].reshape((multiplier, batch_size))


    @property
    def vector(self):
        """Access to get or set the model parameters (weights, scaling for 
        each network) as a single vector, useful in particular for regression.
        
        Parameters
        ----------
        vector : list
            Parameters of the regression model in the form of a list.
        """
        if self.weights is None:
            return None
        if not hasattr(self, 'ravel'):
            self.ravel = Raveler(self.weights)
            
        return self.ravel.to_vector(self.weights)


    @vector.setter
    def vector(self, vector):
        if not hasattr(self, 'ravel'):
            self.ravel = Raveler(self.weights)
        weights = self.ravel.to_dicts(vector)
        self.weights = weights


################################ AUX functions ################################


class Raveler:
    """(CP) Class to ravel and unravel variable values into a single vector.

    This is used for feeding into the optimizer. Feed in a list of dictionaries
    to initialize the shape of the transformation. Note no data is saved in the
    class; each time it is used it is passed either the dictionaries or vector.
    The dictionaries for initialization should be two levels deep.

    weights, scalings are the variables to ravel and unravel
    """
    def __init__(self, weights,):
        self.count = 0
        self.weightskeys = []
        for key1 in sorted(weights.keys()):  # element
            for key2 in sorted(weights[key1].keys()):  # layer
                value = weights[key1][key2]
                self.weightskeys.append({'key1': key1,
                                         'key2': key2,
                                         'shape': np.array(value).shape,
                                         'size': np.array(value).size})
                self.count += np.array(weights[key1][key2]).size

        self.vector = np.zeros(self.count)
        

    def to_vector(self, weights, gpu=False):
        """Puts the weights and scalings embedded dictionaries into a single
        vector and returns it. The dictionaries need to have the identical
        structure to those it was initialized with."""
        if gpu:
            vector = torch.zeros(self.count)
            count = 0
            for k in self.weightskeys:
                lweights = weights[k['key1']][k['key2']].flatten()
                vector[count:(count+lweights.numel())] = lweights
                count += lweights.numel()
        else:
            vector = np.zeros(self.count)
            count = 0
            for k in self.weightskeys:
                lweights = np.array(weights[k['key1']][k['key2']]).ravel()
                vector[count:(count + lweights.size)] = lweights
                count += lweights.size
        
        return vector
    

    def to_dicts(self, vector):
        """Puts the vector back into weights and scalings dictionaries of the
        form initialized. vector must have same length as the output of
        unravel."""
        count = 0
        weights = OrderedDict()

        for k in self.weightskeys:
            if k['key1'] not in weights.keys():
                weights[k['key1']] = OrderedDict()
            matrix = vector[count:count + k['size']]
            matrix = matrix.flatten()
            matrix = matrix.reshape(k['shape'])
            weights[k['key1']][k['key2']] = torch.from_numpy(matrix).float().cuda()
            count += k['size']
        
        return weights
    
    
def ACTIVATION(x, method, order=0):
    """
    The activation functions used in Neural Network training.

    Parameters:
    -----------

    x: float array
        the output of array from each NN layer
    method: string (`tanh`, `sigmoid`, `linear`)
        activation functions 
    order: int (0, 1, 2)
        0: NN results; 1: 1st derivative; 2: 2nd derivative 


    return:
        function or derivative values
    """

    def tanh(x, order=0):
        if order == 0:
            return torch.tanh(x)
        elif order == 1:
            return 1. - x*x
        elif order == 2:
            return -2*x*(1-x*x)  #needs to check
    
    def sigmoid(x, order=0):
        if order == 0:
            return 1/(1+torch.exp(-x))
        elif order == 1:
            return x*(1-x)
        elif order == 2:
            return (1-2*x)*x*(1-x)
    
    def linear(x, order=0):
        if order == 0:
            return x
        elif order == 1:
            return torch.cuda.FloatTensor(np.shape(x)).fill_(1)
        elif order == 2:
            return torch.cuda.FloatTensor(np.shape(x)).fill_(0)
    
    if method in ['tanh', 'sigmoid', 'linear']:
        if method == 'tanh':
            value = tanh(x, order)
        elif method == 'sigmoid':
            value = sigmoid(x, order)
        elif method == 'linear':
            value = linear(x, order)
            
    else:
        value = None
        raise ValueError
        
    return value
