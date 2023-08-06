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
                'restart', 'use_force', 'atoms_per_batch']
        
        for key in keys:
            values = getattr(model, key)
            setattr(self, key, values)


    def preprocess(self, descriptors, features):
        """ Split the input descriptors and energy & force. """
        self.softmax = torch.FloatTensor(self.softmax).cuda()
        self.no_of_descriptors = descriptors['no_of_descriptors']
        self.no_of_structures = descriptors['no_of_structures']
        
        _x = descriptors['x']
        if self.use_force:
            self.dxdr = descriptors['dxdr']
        else:
            self.dxdr = [None]*len(_x)
        
        # Flush memory
        gc.collect()
        
        # Features to Torch mode.
        self.energy = torch.FloatTensor(features['energy']).cuda()
        self.force = []
        for i in range(len(features['force'])):
            self.force.append(torch.FloatTensor(features['force'][i]).cuda())
                    
        # self.no_of_atoms is a dict of list of total atom per structure.
        # self.total_atoms is a dict of the total number of atom out of 
        # all structure.
        self.no_of_atoms = {}
        self.total_atoms_per_element = {}
        self.total_atoms_per_structure = torch.cuda.FloatTensor(self.no_of_structures).fill_(0)
        
        for ele in self.elements:
            self.total_atoms_per_element[ele] = 0
            self.no_of_atoms[ele] = np.zeros((self.no_of_structures,))
        for i in range(self.no_of_structures):
            for key in _x[i].keys():
                self.total_atoms_per_element[key] += len(_x[i][key])
                self.no_of_atoms[key][i] += len(_x[i][key])
                self.total_atoms_per_structure[i] = len(_x[i][key])
        self.total_atoms_per_structure2 = self.total_atoms_per_structure**2
        self.total_atoms = int(torch.sum(self.total_atoms_per_structure))

        # Descriptors in Torch mode.
        # self.x is one giant array of X for all atoms of all structures.
        self.x = {}
        xcount = {}
        for ele in self.elements:
            total = int(sum(self.no_of_atoms[ele]))
            self.x[ele] = torch.cuda.FloatTensor(total,
                          self.no_of_descriptors).fill_(0)
            xcount[ele] = 0
        
        for i in range(self.no_of_structures):
            for element in self.elements:
                atoms = int(self.no_of_atoms[element][i])
                _xc = xcount[element]
                self.x[ele][_xc:_xc+atoms, :] = torch.FloatTensor(_x[i][element]).cuda()
                xcount[element] += atoms
                if self.use_force:
                    self.dxdr[i][element] = torch.FloatTensor(self.dxdr[i][element]).cuda()

        # set up the initial configurations of ohat, dodx, and dohatdx.
        self.ohat = {}
        self.dodx0 = {}
        self.dohatdx = {}
        for e in self.elements:
            shp0 = self.no_of_descriptors
            _atoms = self.total_atoms_per_element[e]
            
            # ohat
            self.ohat[e] = {}
            self.ohat[e][0] = torch.cuda.FloatTensor(_atoms, shp0+1)
            self.ohat[e][0][:, -1] = 1.
            
            # dodx0
            self.dodx0[e] = torch.cuda.FloatTensor(_atoms, shp0, shp0).fill_(0)
            self.dodx0[e][:, np.arange(shp0), np.arange(shp0)] = 1.

            # dohatdx
            self.dohatdx[e] = {}
            self.dohatdx[e][0] = torch.cuda.FloatTensor(_atoms, shp0+1, shp0).fill_(0)
            self.dohatdx[e][0][:, np.arange(shp0), np.arange(shp0)] = 1.

            for i in range(len(self.weights[e])-1):
                shp = self.weights[e][i+1].shape[1]

                # ohat
                self.ohat[e][i+1] = torch.cuda.FloatTensor(_atoms, shp+1).fill_(0)
                self.ohat[e][i+1][:, -1] = 1.
                
                # dohatdx
                self.dohatdx[e][i+1] = torch.cuda.FloatTensor(_atoms, shp+1, shp0).fill_(0)

        # Set up scalings
        self._scalings = {}
        for ele in self.elements:
            self._scalings[e] = torch.cuda.FloatTensor(2)
            self._scalings[e][0] = self.scalings[e]['slope']
            self._scalings[e][1] = self.scalings[e]['intercept']
        
        if self.use_force:
            self.fc = torch.cuda.FloatTensor(1) + self.force_coefficient
            self.fc = self.fc[0]

        # Flush memory
        del(_x)
        gc.collect()
    
    
    def train(self, descriptors, features, optimizer):
        """ Training of Neural Network. """
        # Preprocess descriptors and features
        self.preprocess(descriptors, features)
        
        self.losses = []

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
        
        loss, dLossdW = self.calculate_loss(lossprime)
        
        self.losses.append(loss)

        if not suppress:
            print("Epoch: {:4d}, Loss: {:16.8f}".format(len(self.losses), loss))
            if self.logger:
                self.logger.info("Epoch: {:4d}, Loss: {:16.8f}".format(
                                                           len(self.losses), loss))

        return loss, dLossdW
    
    
    def calculate_loss(self, lossprime):
        """Calculate the error function and its derivative with respect to the
        parameters (weights and scalings).
        
        This error function is consistent with:
        Behler, J. Int. J. Quantum Chem. 2015, 115, 1032– 1050."""
        samples = self.no_of_structures
        if self.use_force:
            fc = self.fc
        energyloss = 0.
        forceloss = 0.
        dEnergydWeights = torch.cuda.FloatTensor(self.ravel.count).fill_(0)
        dForcedWeights = torch.cuda.FloatTensor(self.ravel.count).fill_(0)
        dLossdW = None
        
        w = self.weights
        W = self.remove_bias(w)

        # One-step forward propagation
        o, ohat, aprime, aprime2, dodx, dohatdx = self.forward(self.x, w, W)
        
        batches, tapb = self.get_batches()
        for i, batch in enumerate(batches):
            # To keep track of number of atoms/indices in the structures.
            count = {}
            for e in self.elements:
                count[e] = 0
            
            delta, d2dEdxdW = self.backprop(i, tapb, ohat, aprime, aprime2, dodx, dohatdx, W)
            
            for b in batch:
                atoms = 0
                for ele in self.elements:
                    atoms += int(self.no_of_atoms[ele][b])
                
                nnEnergy, nnForce, dEdW, dFdW = self.calculate_nnResults(i, tapb,
                                                count, b, o, dodx, delta, ohat,
                                                d2dEdxdW, atoms, 
                                                self.ravel.count)

                energyloss += self.softmax[b] * \
                                torch.mul((nnEnergy - self.energy[b]), (nnEnergy - self.energy[b])) / \
                                self.total_atoms_per_structure2[b]
                if self.use_force:
                    forceloss += self.softmax[b] * \
                                 torch.sum(torch.mul((nnForce - self.force[b]), (nnForce - self.force[b]))) * \
                                 fc / self.total_atoms_per_structure[b]

                if lossprime:
                    # dEdW
                    dEnergydWeights += self.softmax[b] * (nnEnergy - self.energy[b]) * dEdW / self.total_atoms_per_structure2[b]
                    if self.use_force:
                        # dFdW
                        temp = torch.einsum('ij,ijk->k', (nnForce - self.force[b]), dFdW)
                        dForcedWeights += self.softmax[b] * temp * fc / self.total_atoms_per_structure[b]

                for e in self.elements:
                    count[e] += int(self.no_of_atoms[e][b])

        # Regularization
        W0 = self.clean_bias(self.weights)
        flat_weights = self.ravel.to_vector(W0, True)
        regTerm = self.alpha * torch.sum(torch.mul(flat_weights, flat_weights))
        
        loss = (energyloss + forceloss/3. + regTerm).cpu() / (2. * samples)
        if lossprime:
            dRegdWeights = self.alpha*flat_weights
            dLossdW = (dEnergydWeights + dForcedWeights/3. + dRegdWeights).cpu() / (samples)

        gc.collect()

        return loss, (dLossdW.numpy()).astype(np.float64)
                
        
    def calculate_nnResults(self, i_batch, tapb, count, b, o, dodx, delta, ohat, d2EdxdW, 
                            no_of_atoms, ravel_count):        
        # make force0, dnnEnergydWeights0, and dnnForcedWeights0
        energy = 0.
        wcount = 0
        forces = torch.cuda.FloatTensor(no_of_atoms, 3).fill_(0)
        dnnEnergydWeights = torch.cuda.FloatTensor(ravel_count).fill_(0)
        dnnForcedWeights = torch.cuda.FloatTensor(no_of_atoms, 3 , ravel_count).fill_(0)

        dEdW, dFdW = {}, {}
        
        for h, e in enumerate(self.elements):
            init = 0
            for _ in range(i_batch):
                init += int(tapb[_][h])

            c = count[e]
            atoms = int(self.no_of_atoms[e][b])
            
            dEdW[e], dFdW[e] = {}, {}
            _slope = self._scalings[e][0]
            _intercept = self._scalings[e][1]
            
            energy += torch.sum(_slope * o[e][len(o[e])-1][init+c:init+c+atoms] + _intercept)

            if self.use_force:
                dEdx = torch.sum(dodx[e][len(dodx[e])-1][init+c:init+c+atoms], axis=1)
                forces += -_slope * torch.einsum('ik, ijkl->jl', dEdx, self.dxdr[b][e])
                
            for j in range(1, len(self.weights[e])+1):
                # dE/dW
                dEdW[e][j] = _slope * torch.einsum('ij,ik->kj', delta[e][j][c:c+atoms], ohat[e][j-1][init+c:init+c+atoms])
                Etemp = dEdW[e][j].flatten()
                _size = len(Etemp)
                dnnEnergydWeights[wcount:(wcount+_size)] += Etemp
                
                if self.use_force:
                    # dFdW
                    dFdW[e][j] = - _slope * torch.einsum('ijkl,imln->mnjk', d2EdxdW[e][j][c:c+atoms], self.dxdr[b][e])
                    s1, s2, s3, s4 = dFdW[e][j].size()
                    Ftemp = dFdW[e][j].reshape((s1, s2, _size))
                    dnnForcedWeights[:, :, wcount:(wcount+_size)] += Ftemp
                
                wcount += _size
                        
        return energy, forces, dnnEnergydWeights, dnnForcedWeights

    
    def forward(self, x, w, W):
        # Initialize the properties
        o, ohat, dodx, dohatdx = {}, {}, {}, {} # starts from 0
        aprime, aprime2 = {}, {}                # starts from 1
        
        # Feedforward neural network
        for e in self.elements:
            _x, _w, _W,  = x[e], w[e], W[e]
            _activation = self.activation[e]

            o[e], ohat[e] = {}, {}
            aprime[e], aprime2[e] = {}, {}
            dodx[e], dohatdx[e] = {}, {}
            
            o[e][0] = _x
            ohat[e][0] = self.ohat[e][0]
            ohat[e][0][:, :-1] = _x

            dodx[e][0] = self.dodx0[e]
            dohatdx[e][0] = self.dohatdx[e][0]
            
            aprime[e][0] = None
            aprime2[e][0] = None
            N_layer = len(_W)
            for i in range(N_layer):
                term = torch.mm(ohat[e][i], _w[i+1])
                o[e][i+1] = ACTIVATION(term, _activation[i], 0)
                aprime[e][i+1] = ACTIVATION(o[e][i+1], _activation[i], 1)

                if i == 0:
                    dodx[e][i+1] = torch.einsum('ij,jk->ijk', aprime[e][i+1], _W[i+1].T)
                else:
                    term = torch.einsum('ij,jk->ijk', aprime[e][i+1], _W[i+1].T)
                    dodx[e][i+1] = torch.einsum('ijk,ikl->ijl', term, dodx[e][i])

                # Only for force training
                if self.use_force:
                    aprime2[e][i+1] = ACTIVATION(o[e][i+1], _activation[i], 2)

                if i < N_layer-1:
                    N_x, shp = o[e][i+1].shape
                    ohat[e][i+1] = self.ohat[e][i+1]
                    ohat[e][i+1][:, :-1] = o[e][i+1]

                    dohatdx[e][i+1] = self.dohatdx[e][i+1]
                    dohatdx[e][i+1][:,:-1,:] = dodx[e][i+1]
                    
        return o, ohat, aprime, aprime2, dodx, dohatdx
    
    
    def backprop(self, i_batch, tapb, ohat, aprime, aprime2, dodx, dohatdx, W):
        # Initialize the properties
        delta, delta_prime, d2EdxdW = {}, {}, {}

        # backprop
        for h, e in enumerate(self.elements):
            delta[e], delta_prime[e] = {}, {}
            d2EdxdW[e] = {}
            
            init = 0
            for _ in range(i_batch):
                init += int(tapb[_][h])

            total = int(tapb[i_batch][h])

            N = len(W[e])
            for i in range(N, 0, -1):
                term = torch.einsum('jk,ikl->ijl', W[e][i].T, dodx[e][i-1][init:init+total, :])
                if i == N:
                    delta[e][i] = aprime[e][i][init:init+total, :]
                    if self.use_force:
                        delta_prime[e][i] = torch.einsum('ij,ijk->ijk', aprime2[e][i][init:init+total, :], term)
                else:
                    delta[e][i] = torch.mm(delta[e][i+1], W[e][i+1].T) * aprime[e][i][init:init+total, :]
                    if self.use_force:
                        term0 = torch.einsum('ijk,jl->ilk', delta_prime[e][i+1], W[e][i+1].T)
                        term1 = torch.einsum('ijk,ij->ijk', term0, aprime[e][i][init:init+total, :])
                        term2 = torch.mm(delta[e][i+1], W[e][i+1].T) * aprime2[e][i][init:init+total, :]
                        term3 = torch.einsum('ij,ijk->ijk', term2, term)
                        delta_prime[e][i] = term1 + term3
                
                if self.use_force:
                    term1 = torch.einsum('ij,ikl->ikjl', delta[e][i], dohatdx[e][i-1][init:init+total, :, :])
                    term2 = torch.einsum('ijk,il->iljk', delta_prime[e][i], ohat[e][i-1][init:init+total, :])
                    d2EdxdW[e][i] = term1 + term2

        return delta, d2EdxdW
    
    
    def get_batches(self):
        """ Partition a batch of structures into batches of structures. 
        atoms_per_batch determines the upper limit per batch. """
        atoms_per_batch = self.atoms_per_batch
        batches = []
        total_atoms_per_batch = []
        
        # Keep track on the number of atom in batch.
        atoms = {}
        for ele in self.elements:
            atoms[ele] = 0
            
        batch = []
        for b in range(self.no_of_structures):
            for ele in self.elements:
                if (atoms[ele]+self.no_of_atoms[ele][b]) < atoms_per_batch:
                    append_to_batch = True
                else:
                    append_to_batch = False

            if append_to_batch:
                for ele in self.elements:
                    atoms[ele] += self.no_of_atoms[ele][b]
                batch.append(b)
            else:
                # Store a batch of structures to batches
                tapb = []
                for ele in self.elements:
                    tapb.append(atoms[ele])
                    atoms[ele] = 0              # Reset atoms dictionary
                total_atoms_per_batch.append(tapb)
                batches.append(batch)

                batch = []      # Reset the batch counting.
                for ele in self.elements:
                    atoms[ele] += self.no_of_atoms[ele][b]
                batch.append(b)
                
        # Append the last batch
        tapb = []
        for ele in self.elements:
            tapb.append(atoms[ele])
        total_atoms_per_batch.append(tapb)  
        batches.append(batch)
        
        return batches, total_atoms_per_batch


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
            vector = torch.cuda.FloatTensor(self.count).fill_(0)
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
