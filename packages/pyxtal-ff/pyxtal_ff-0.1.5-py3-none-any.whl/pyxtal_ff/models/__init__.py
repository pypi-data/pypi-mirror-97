#!/usr/bin/env  python
# encoding: utf-8
import os
import json
import numpy as np
from monty.serialization import MontyEncoder, loadfn
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.ticker as mticker
#plt.style.use("bmh")
plt.style.use("ggplot")

class NeuralNetwork():
    """ Atom-centered Neural Network model. The inputs are atom-centered 
    descriptors: BehlerParrinello or Bispectrum. The forward propagation of 
    the Neural Network predicts energy per atom, and the derivative of the 
    forward propagation predicts force. 
    A machine learning interatomic potential can developed by optimizing the 
    weights of the Neural Network for a given system.
    
    Parameters
    ----------
    elements: list
         A list of atomic species in the crystal system.
    hiddenlayers: list or dict
        [3, 3] contains 2 layers with 3 nodes each. Each atomic species in the 
        crystal system is assigned with its own neural network architecture.
    activation: str
        The activation function for the neural network model.
        Options: tanh, sigmoid, and linear.
    random_seed: int
        Random seed for generating random initial random weights.
    batch_size: int
        The size of the data points for each iteration.
    force_coefficient: float
        This parameter is used in the penalty function to scale the force
        contribution relative to the energy.
    alpha: int
        L2 penalty (regularization term) parameter.
    softmax_beta:
        The parameters for Softmax Energy Penalty function.
    unit: str
        The unit of energy ('eV' or 'Ha').
    restart: str
        continuing Neural Network training from where it was left off.
    path: str
        The path of the directory where everything is saved.
    """
    def __init__(self, elements, hiddenlayers, activation, random_seed, 
                 batch_size, atoms_per_batch, force_coefficient, alpha, 
                 softmax_beta, unit, logging, restart, path):
        
        if restart is not None and os.path.exists(restart):
            self.import_nn_parameters(restart)
            if force_coefficient is not None:
                self.force_coefficient = force_coefficient
            if alpha is not None:
                self.alpha = alpha
            self.batch_size = batch_size
            self.softmax_beta = softmax_beta
            
        else:
            self.elements = sorted(elements)
            
            # Format hiddenlayers by adding the last output layer.
            self._hiddenlayers = hiddenlayers
            if isinstance(hiddenlayers, list):
                hl = {}
                for element in self.elements:
                    hl[element] = hiddenlayers + [1]
                self.hiddenlayers = hl
            elif isinstance(hiddenlayers, dict):
                for key, value in hiddenlayers.items():
                    hiddenlayers[key] = value + [1]
                self.hiddenlayers = hl
            else:
                msg = f"Don't recognize {type(hiddenlayers)}. " +\
                      f"Please refer to documentations!"
                raise TypeError(msg)

            # Set-up activation
            self.activation = {}
            activation_modes = ['tanh', 'sigmoid', 'linear']
            
            if isinstance(activation, str):
                for e in self.elements:
                    self.activation[e] = [activation] * \
                                         len(self.hiddenlayers[e])
            elif isinstance(activation, list):
                for element in self.elements:
                    self.activation[element] = activation
            else:
                # Users construct their own activation
                self.activation = activation
            
            # Check if each of the activation functions is implemented.
            for e in self.elements:
                for act in self.activation[e]:
                    if act not in activation_modes:
                        msg = f"{act} is not implemented. " +\
                              f"Please choose from {activation_modes}."
                        raise NotImplementedError(msg)
                assert len(self.activation[e]) == len(self.hiddenlayers[e]),\
                "The length of the activation function is inconsistent "+\
                "with the length of the hidden layers."
                        
            # weights and scalings parameters
            self.weights = None
            self.scalings = None
            self.seed = random_seed
            
            self.batch_size = batch_size
            self.atoms_per_batch = atoms_per_batch

            # Regularization coefficients
            self.alpha = alpha
            self.softmax_beta = softmax_beta
            self.force_coefficient = force_coefficient
            
            unit_options = ['eV', 'Ha']
            if unit not in unit_options:
                msg = f"{unit} is not implemented. " +\
                      f"Please choose from {unit_options}."
                raise NotImplementedError(msg)
            self.unit = unit
            
        self.logger = logging
        self.restart = restart
        self.path = path
        

    def train(self, TrainDescriptors, TrainFeatures, optimizer, runner, use_force=None):
        """ Training of Neural Network. """
        no_of_descriptors = len(TrainDescriptors[0]['x'][0])
        no_of_structures = len(TrainDescriptors)
        if use_force is None:
            # create the default value
            if 'dxdr' in TrainDescriptors[0]:
                self.use_force = True
            else:
                self.use_force = False
        else:
            if (use_force) and ('dxdr' not in TrainDescriptors[0]):
                #raise ValueError("use_force cannot be True if dxdr is not present")
                self.use_force = False
            else:
                self.use_force = use_force
        
        # Generate descriptor range.
        self.drange = self.get_descriptors_range(TrainDescriptors)
        self.plot_hist(TrainDescriptors, figname=self.path+"histogram.png", figsize=(12, 24))
        
        # Generate random weights if None.
        if self.weights == None:
            self.weights = self.get_random_weights(self.hiddenlayers, 
                                                   no_of_descriptors,
                                                   self.seed)
            del(self.hiddenlayers)
        
        for e in self.elements:
            print("\nNN layers for element {:s}".format(e))
            no_of_weights = 0
            for i in range(1, len(self.weights[e])+1):
                l1, l2 = self.weights[e][i].shape
                no_of_weights += l1*l2
                print("Layer #{:1d}: {:4d}, {:4d}".format(i, l1, l2))
            print("Total number of parameters: {:d}".format(no_of_weights))
        
        # Normalize Descriptors
        TrainDescriptors = self.normalized(TrainDescriptors, 
                                           self.drange, self.unit)

        # Parse Energy & Forces
        energy = []
        force = []
        for i in range(no_of_structures):
            energy.append(TrainFeatures[i]['energy'])
            force.append(np.asarray(TrainFeatures[i]['force']))
        TrainFeatures = {'energy': np.asarray(energy), 'force': force}

        self.softmax = self._SOFTMAX(energy, TrainDescriptors['x'], beta=self.softmax_beta)
        
        # Generate scalings based on min-max Energy.
        if self.scalings == None:
            min_E = min(energy)        # Perhaps these 2 should be user-
            max_E = max(energy)        # defined scalings
            self.scalings = self.get_scalings(self.activation, [min_E, max_E],
                                              self.drange.keys())
        
        # NN training with NumPy, CuPy, or PyTorch
        self.get_runner(runner)
        self.model.train(TrainDescriptors, TrainFeatures, optimizer)

        # Generate graph for loss
        plt.plot(self.model.losses)
        plt.xlabel('Epoch')
        plt.ylabel('MSE Loss')
        plt.tight_layout()
        plt.savefig(self.path+"Loss.png")
        plt.close()
        
        # After NN training is done. Update scalings, drange, weights
        self.update_nn_parameters()
        
        # Export the scalings, drange, weights, etc. to -parameters.json
        self.export_nn_parameters()


    def evaluate(self, TestDescriptors, TestFeatures, figname):
        """ Evaluating the train or test data set. """
            
        print("======================== Evaluating ==========================")
        self.get_runner('numpy')

        TestDescriptors = self.normalized(TestDescriptors, 
                                          self.drange, self.unit)

        Energy, Force = [], []
        for i in range(TestDescriptors['no_of_structures']):
            Energy.append(TestFeatures[i]['energy'])
            if 'dxdr' in TestDescriptors:
                Force.append(np.array(TestFeatures[i]['force']))

        TestFeatures = {'energy': Energy,
                        'force': Force}

        energy, _energy, force, _force = self.model.evaluate(TestDescriptors, 
                                                             TestFeatures) 
        self.dump_evaluate(_energy, energy, filename=figname[:-4]+'Energy.txt')
        self.dump_evaluate(_force, force, filename=figname[:-4]+'Force.txt')

        # Calculate the mean absolute error and r2
        E_mae = mean_absolute_error(energy, _energy)
        E_mse = mean_squared_error(energy, _energy)
        E_r2 = r2_score(energy, _energy)
        print("Energy R2  : {:8.6f}".format(E_r2))
        print("Energy MAE : {:8.6f}".format(E_mae))
        print("Energy MSE : {:8.6f}".format(E_mse))
        energy_str = 'Energy: r2({:.4f}), MAE({:.4f} {}/atom)'. \
                     format(E_r2, E_mae, self.unit)

        plt.title(energy_str)
        plt.scatter(energy, _energy, label='Energy', s=5)
        plt.legend(loc=2)
        plt.xlabel('True ({}/atom)'.format(self.unit))
        plt.ylabel('Prediction ({}/atom)'.format(self.unit))
        plt.tight_layout()
        plt.savefig(self.path+'Energy_'+figname)
        plt.close()
        print("\nExport the figure to: {:s}".format(self.path+'Energy_'+figname))

        if len(force) > 0: 
            F_mae = mean_absolute_error(force, _force)
            F_mse = mean_squared_error(force, _force)
            F_r2 = r2_score(force, _force)
            print("Force R2   : {:8.6f}".format(F_r2))
            print("Force MAE  : {:8.6f}".format(F_mae))
            print("Force MSE  : {:8.6f}".format(F_mse))
            length = 'A'
            if self.unit == 'Ha':
                length == 'Bohr'
            force_str = 'Force: r2({:.4f}), MAE({:.3f} {}/{})'. \
                        format(F_r2, F_mae, self.unit, length)
            plt.title(force_str)
            plt.scatter(force, _force, s=5, label='Force')
            plt.legend(loc=2)
            plt.xlabel('True ({}/{})'.format(self.unit, length))
            plt.ylabel('Prediction ({}/{})'.format(self.unit, length))
            plt.tight_layout()
            plt.savefig(self.path+'Force_'+figname)
            plt.close()
            print("\nExport the figure to: {:s}".format(self.path+'Force_'+figname))
        else:
            F_mae, F_mse, F_r2 = None, None, None
        print("=================== Evaluation is Completed ==================")
        print("\n")
        
        return (E_mae, E_mse, E_r2, F_mae, F_mse, F_r2)

    def export_nn_parameters(self, filename=None):
        """ Save the Neural Network parameters in a json file. """
        paras = ['elements', '_hiddenlayers', 'activation', 'weights', 
                 'scalings', 'drange', 'force_coefficient', 'alpha', 
                 'softmax_beta', 'unit', 'path', 'atoms_per_batch']
        
        self.filename = self.path

        if filename:
            self.filename += filename
        else:
            if isinstance(self._hiddenlayers, list):
                _hl = "-".join(str(x) for x in self._hiddenlayers)
                self.filename += _hl + '-parameters.json'
            else:
                count = 0
                for i in range(len(self.elements)):
                    self.filename += "-".join(str(x) \
                        for x in self._hiddenlayers[self.elements[i]])
                    if count < len(self.elements)-1:
                        self.filename += "_"
                self.filename += '-parameters.json'
                    
        dicts = {}
        for para in paras:
            dicts[para] = eval('self.'+para)
        with open(self.filename, 'w') as f:
            json.dump(dicts, f, indent=2, cls=MontyEncoder)

        print("\nExport the NN parameters to: {:s}".format(self.filename))
            
            
    def import_nn_parameters(self, file=None, weight_only=False):
        """ Load the Neural Network parameters from the json file. """
        nn_dict = loadfn(file)
        
        for key in nn_dict.keys():
            if key == 'weights':
                weights = {}
                for i, (k1, v1) in enumerate(nn_dict[key].items()):
                    weights[k1] = {}
                    for k2, v2 in v1.items():
                        weights[k1][int(k2)] = v2
                setattr(self, key, weights)
            elif key in ['drange', 'scalings']:
                setattr(self, key, nn_dict[key])
            elif not weight_only:
                setattr(self, key, nn_dict[key])
                
    
    def get_runner(self, runner):
        self.runner = runner
        if runner == 'numpy':
            from pyxtal_ff.models.neuralnetwork import NN
        elif runner == 'numpy2':
            from pyxtal_ff.models.neuralnetwork2 import NN
        elif runner == 'pytorch':
            from pyxtal_ff.models.gneuralnetwork import NN
        elif runner == 'pytorch2':
            from pyxtal_ff.models.gneuralnetwork2 import NN
        elif runner == 'pytorch3':
            from pyxtal_ff.models.gneuralnetwork3 import NN
        elif runner == 'cupy':
            from pyxtal_ff.models.cneuralnetwork import NN
        else:
            raise NotImplementedError
        self.model = NN(self)
            
    def update_nn_parameters(self):
        """ Update Neural Network parameters after training. """
        if self.runner in ['pytorch', 'pytorch2', 'pytorch3']:
            weights = {}
            for e in self.elements:
                weights[e] = {}
                for i in range(len(self.model.weights[e])):
                    weights[e][i+1] = \
                            (self.model.weights[e][i+1].cpu()).numpy()
            self.weights = weights
            
        elif self.runner == 'cupy':
            weights = {}
            for e in self.elements:
                weights[e] = {}
                for i in range(len(self.model.weights[e])):
                    weights[e][i+1] = self.model.weights[e][i+1].get()
            self.weights = weights
            
        else:
            self.weights = self.model.weights

            
    def get_random_weights(self, hiddenlayers, no_of_descriptor, seed):
        """ Generating random initial weights for the neural network.

        Parameters
        ----------
        hiddenlayers: list
            The hiddenlayers nodes of the neural network.
        no_of_adescriptor: int
            The length of a descriptor.
        seed: int
            The seed for Numpy random generator.

        Returns
        -------
        dict
            Randomly-generated weights.
        """
        _WEIGHTS = {}
        nnArchitecture = {}
        r = np.random.RandomState(seed=seed)
        
        elements = hiddenlayers.keys()
        for element in sorted(elements):
            _WEIGHTS[element] = {}
            nnArchitecture[element] = [no_of_descriptor] + \
                                        hiddenlayers[element]
            n = len(nnArchitecture[element])
            
            for layer in range(n-1):
                epsilon = np.sqrt(6. / (nnArchitecture[element][layer] +
                                        nnArchitecture[element][layer+1]))
                norm_epsilon = 2. * epsilon
                _WEIGHTS[element][layer+1] = r.random_sample(
                                        (nnArchitecture[element][layer]+1,
                                        nnArchitecture[element][layer+1])) * \
                                        norm_epsilon - epsilon
                #print(layer+1, _WEIGHTS[element][layer+1].shape)
                                        
        return _WEIGHTS
    
    
    def get_descriptors_range(self, descriptors):
        """ Calculate the range (min and max values) of the descriptors 
        corresponding to all of the crystal structures.
        
        Parameters
        ----------
        descriptors: dict of dicts
            Atom-centered descriptors.
            
        Returns
        -------
        dict
            The range of the descriptors for each element species.
        """
        _DRANGE = {}
        no_of_structures = len(descriptors)
        for i in range(no_of_structures):
            for j, descriptor in enumerate(descriptors[i]['x']):
                element = descriptors[i]['elements'][j]
                if element not in _DRANGE.keys():
                    _DRANGE[element] = np.asarray([np.asarray([__, __]) \
                                      for __ in descriptor])
                else:
                    assert len(_DRANGE[element]) == len(descriptor)
                    for j, des in enumerate(descriptor):
                        if des < _DRANGE[element][j][0]:
                            _DRANGE[element][j][0] = des
                        elif des > _DRANGE[element][j][1]:
                            _DRANGE[element][j][1] = des
        
        return _DRANGE
    
    
    def get_scalings(self, activation, energy, elements):
        """ To scale the range of activation to the range of actual energy.

        Parameters
        ----------
        activation: str
            The activation function for the neural network model.
        energies: list
            The min and max value of the energies.
        elements: list
            A list of atomic species in the crystal system.

        Returns
        -------
        dict
            The scalings parameters, i.e. slope and intercept.
        """
        # Max and min of true energies.
        min_E = energy[0] 
        max_E = energy[1] 

        _SCALINGS = {}

        for element in elements:
            _SCALINGS[element] = {}
            _activation = activation[element]
            if _activation[-1] == 'tanh':
                _SCALINGS[element]['intercept'] = (max_E + min_E) / 2.
                _SCALINGS[element]['slope'] = (max_E - min_E) / 2.
            elif _activation[-1] == 'sigmoid':
                _SCALINGS[element]['intercept'] = min_E
                _SCALINGS[element]['slope'] = (max_E - min_E)
            elif _activation[-1] == 'linear':
                _SCALINGS[element]['intercept'] = 0.
                _SCALINGS[element]['slope'] = 1.
            elif _activation[-1] == 'relu':
                _SCALINGS[element]['intercept'] = -(max_E * min_E) / \
                                                   (max_E - min_E)
                _SCALINGS[element]['slope'] = max_E / (max_E - min_E)

        return _SCALINGS
    
    
    def normalized(self, descriptors, drange, unit, norm=[0., 1.]):
        """ Normalizing the descriptors to the range of [0., 1.] based on the
        min and max value of the descriptors in the crystal structures. 
        
        Parameters
        ----------
        descriptors: dict
            The atom-centered descriptors.
        drange:
            The range of the descriptors for each element species.
        unit: str
            The unit of energy ('eV' or 'Ha').
            
        Returns
        -------
        dict
            The normalized descriptors.
        
        """
        d = {}
        d['no_of_structures'] = len(descriptors)
        d['no_of_descriptors'] = len(descriptors[0]['x'][0])
        
        d['x'] = {}
        if 'dxdr' in descriptors[0]:
            d['dxdr'] = {}
        
        # Normalize each structure.
        for i in range(d['no_of_structures']):
            d['x'][i] = {}
            if 'dxdr' in descriptors[0]:
                d['dxdr'][i] = {}
            
            no_of_center_atom = {}
            count = {}
            
            for element in self.elements:
                no_of_center_atom[element] = 0
                no_of_neighbors = 0
                count[element] = 0
                
            for e in descriptors[i]['elements']:
                no_of_center_atom[e] += 1
                no_of_neighbors += 1
                
            for element in self.elements:
                i_size = no_of_center_atom[element]
                j_size = no_of_neighbors
                d['x'][i][element] = np.zeros((i_size, d['no_of_descriptors']))
                if 'dxdr' in descriptors[0]:
                    d['dxdr'][i][element] = np.zeros((i_size, j_size, 
                                                    d['no_of_descriptors'], 3))
            
            for m in range(len(descriptors[i]['x'])):
                _des = descriptors[i]['x'][m]
                element = descriptors[i]['elements'][m]
                _drange = drange[element]
                scale = (norm[1] - norm[0]) / (_drange[:, 1] - _drange[:, 0])
                des = norm[0] + scale * (_des - _drange[:, 0])
                d['x'][i][element][count[element]] = des
                
                if 'dxdr' in descriptors[i].keys():
                    for n in range(len(descriptors[i]['dxdr'][m])):
                        for p in range(3):
                            index = count[element]
                            _desp = descriptors[i]['dxdr'][m, n, :, p]
                            if unit == 'eV':
                                desp = scale * _desp
                            elif unit == 'Ha':
                                desp = 0.529177 * scale * _desp # to 1/Bohr
                            d['dxdr'][i][element][index, n, :, p] = desp
                count[element] += 1
        
        return d


    def _SOFTMAX(self, energy, x, beta=-1):
        """ Assign the weight to each sample based on the softmax function. """
        # Ensure that the sum of smax is equal to number of samples
        smax = np.ones(len(energy))

        if beta is not None:
            smax = np.zeros(len(energy))
            no_of_atoms = []
            for i in range(len(x)):
                natoms = 0
                for key in x[i].keys():
                    natoms += len(x[i][key])
                no_of_atoms.append(natoms)

            epa = np.asarray(energy) / np.asarray(no_of_atoms)

            smax += np.exp(beta*epa) / sum(np.exp(beta*epa))
            smax *= len(energy)
        return smax


    def check_gradients(self, descriptors, features, optimizer):
        """ Run the check gradients (dEdW, dFdW, and dLdW). """

        self.train(descriptors, features, optimizer)
        self.check_dEdW()
        if self.model.dxdr is not None:
            self.check_dFdW()
        self.check_dLdW()
        

    def check_dLdW(self):
        """ Checking the derivative of Loss function w.r.t. the weights. """
        from scipy.optimize import approx_fprime
        print('\n======================== Checking dLdW =======================')
        parameters = self.model.vector.copy()
        def fun(parameters):
            return self.model.get_loss(parameters, lossprime=False, 
                                       suppress=True)[0]
        grad = approx_fprime(parameters, fun, 1e-5)

        #print('\ngradients of loss function from scipy optimizer:')
        #print(grad)
 
        L, dLdW = self.model.get_loss(parameters, lossprime=True, 
                                      suppress=True)
        #print('\ngradients of loss function derived from NN code:')
        #print(dLdW)
        diff = np.linalg.norm(grad - dLdW)
        print('diff in dLdW ({:d}): {:.2E}'.format(len(dLdW), diff))
        print('======================== Checking is done ====================')
        
        
    def check_dEdW(self, epsilon=1e-8):
        """ Experimental functions to compare the energy gradients 
        from both analytic and numerical solutions for one structure."""
        from copy import deepcopy
        
        print("\n")
        print('======================== Checking dEdW =======================')
        x = self.model.x[0]
        E, _, dEdW, _ = self.model.calculate_nnResults(x, None, 
                                                       self.model.ravel.count)
        grads_E = []
        for e in self.elements:
            for l in range(len(self.weights[e])):
                for i in range(self.weights[e][l+1].shape[0]):
                    for j in range(self.weights[e][l+1].shape[1]):
                        weights_plus = deepcopy(self.weights)
                        weights_plus[e][l+1][i,j] += epsilon
                        energy_plus, _ = self.model.calculate_energy_forces(x, 
                                                             None, weights_plus)
                        grad_E = (energy_plus - E)/epsilon
                        grads_E.append(grad_E)
        diff = np.linalg.norm(np.array(grads_E) - dEdW)
        print('diff in dEdW ({:d}): {:.2E}'.format(len(dEdW), diff))
        print('======================= Checking is done =====================')
        

    def check_dFdW(self, epsilon=1e-8):
        """ Experimental functions to compare the energy gradients 
        from both analytic and numerical solutions for one structure."""
        from copy import deepcopy
        
        print("\n")
        print('======================== Checking dFdW =======================')
        x = self.model.x[0]
        dxdr = self.model.dxdr[0]
        E, F, dEdW, dFdW = self.model.calculate_nnResults(x, dxdr, self.model.ravel.count)
        grads_F = []
        dFdW = dFdW.transpose(2, 0, 1).ravel()
        for e in self.elements:
            for l in range(len(self.weights[e])):
                for i in range(self.weights[e][l+1].shape[0]):
                    for j in range(self.weights[e][l+1].shape[1]):
                        weights_plus = deepcopy(self.weights)
                        weights_plus[e][l+1][i,j] += epsilon
                        _, force_plus = self.model.calculate_energy_forces(x, 
                                                             dxdr, weights_plus)
                        grad_F = (force_plus - F)/epsilon
                        grads_F.append(grad_F.ravel())

        diff = np.linalg.norm(np.array(grads_F).ravel() - dFdW)
        print('diff in dFdW ({:d}): {:.2E}'.format(len(dFdW), diff))
        print('======================= Checking is done =====================')
        

    def plot_hist(self, descriptors, figname=None, figsize=(12, 16)):
        """ Plot the histogram of descriptors. """
        flatten_array = {}
        for e in self.elements: 
            flatten_array[e] = []
            
        no_of_descriptors = descriptors[0]['x'].shape[1]
        for i in range(len(descriptors)):
            x = descriptors[i]['x']
            symbols = descriptors[i]['elements']
            for e in self.elements:
                ids = []
                for id in range(len(symbols)):
                    if e == symbols[id]:
                        ids.append(id)
                if flatten_array[e] == []:
                    flatten_array[e] = x[ids, :]
                else:
                    flatten_array[e] = np.vstack( (flatten_array[e], x[ids, :]) )

        # Plotting
        fig = plt.figure(figsize=figsize)
        fig.suptitle('The distribution of descriptors after normalization', 
                     fontsize=22)
        gs = GridSpec(no_of_descriptors, len(self.elements))
        for ie, e in enumerate(self.elements):
            if self.drange is not None:
                print('\nDescriptors range for {:s} from the training set {:d}'. format(e, len(self.drange[e])))
                max_x = self.drange[e][:,1]
                min_x = self.drange[e][:,0]
            else:
                print('\nDescriptors range for {:s} from the provided data {:d}'. format(e, len(flatten_array[e])))
                max_x = np.max(flatten_array[e], axis=0)
                min_x = np.min(flatten_array[e], axis=0)

            flatten_array[e] -= min_x
            flatten_array[e] /= (max_x - min_x)

            for ix in range(len(max_x)):
               print('{:12.6f} {:12.6f}'.format(min_x[ix], max_x[ix]))
               tmp = flatten_array[e][:,ix]
               ids = np.where((tmp<-1e-2) | (tmp>1))[0]
               if len(ids) > 0:
                   print('Warning: {:d} numbers are outside the range after normalization'.format(len(ids)))
                   print('-------', ids, tmp[ids], '---------')

            for ix in range(no_of_descriptors-1,-1,-1):
                label = "{:s}{:d}: {:8.4f} {:8.4f}".format(e, ix, min_x[ix], max_x[ix])
                if ix == no_of_descriptors-1:
                    ax0 = fig.add_subplot(gs[ix,ie])
                    ax0.hist(flatten_array[e][:,ix], bins=100, label=label)
                    ax0.legend(loc=1)
                    ax0.yaxis.set_major_formatter(mticker.NullFormatter())
                    ax0.set_xlim([0,1])
                else:
                    ax = fig.add_subplot(gs[ix,ie], sharex=ax0)
                    ax.hist(flatten_array[e][:,ix], bins=100, label=label)
                    ax.legend(loc=1)
                    ax.yaxis.set_major_formatter(mticker.NullFormatter())
                    plt.setp(ax.get_xticklabels(), visible=False)
        plt.subplots_adjust(hspace=.0)
        #plt.tight_layout()
        plt.savefig(figname)
        plt.close()


    def dump_evaluate(self, predicted, true, filename):
        """ Dump the evaluate results to text files. """
        
        absolute_diff = np.abs(np.subtract(predicted, true))
        combine = np.vstack((predicted, true, absolute_diff)).T
        
        np.savetxt(self.path+filename, combine, header='Predicted True Diff', fmt='%.7e')



class LossFunction:
    """ This class grabs the value(s) of a given loss function passed from 
    the model to a local optimization algorithm.

    Parameters
    ----------
    model: object
        The class representing the model.
    """
    def __init__(self, model):
        self.model = model
    
    
    def loss(self, parameters, lossprime=False):
        """ This method takes parameters (array) given by a local optimization 
        algorithm and feeds the parameters to the model (i.e. NeuralNetwork) 
        for loss function calculation.

        Parameters
        ----------
        parameters: list
            A list of parameters to be optimized.
        lossprime: bool
            If True, calculate the derivative of the loss function.
        
        Returns
        -------
        float
            If lossprime is true, this lossfunction returns both the loss and
            its derivative. Otherwise, this function returns 
        """
        fun, jac = self.model.get_loss(parameters, lossprime=lossprime)
        
        if lossprime:
            return fun, jac
        else:
            return fun


class Regressor:
    """ This class contains local optimization methods.

    Parameters
    ----------
    method: str
        Type of minimization scheme, e.g.: 'BFGS'.
    derivative: bool
        If False, the local optimization algorithm will calculate the Jacobian.
    user_kwargs: dict
        The arguments of the optimization function are passed by the dict 
        keywords.
    """
    def __init__(self, method, derivative, user_kwargs):
        kwargs = {'method': method,
                  'tol': 1e-10,
                  'jac': derivative,
                  'args': (derivative,)
                  }

        if method in ['CG', 'BFGS']:
            from scipy.optimize import minimize as optimizer
            _kwargs = {'options': {'gtol': 1e-8,
                                   'maxiter': 2000,
                                   'disp': False,
                                  }
                      }

        elif method in ['L-BFGS-B']:
            from scipy.optimize import minimize as optimizer
            _kwargs = {'options': {'gtol': 1e-8,
                                   'maxiter': 100,
                                   'disp': False,
                                  }
                      }

        elif method in ['SGD', ]:
            from pyxtal_ff.models.optimize import SGD as optimizer
            _kwargs = {'options': {'maxiter': 2000},
                       'lr_init': 0.001,
                       'lr_method': 'constant',
                       'power_t': 0.5,
                       'momentum': 0.9,
                       'nesterovs_momentum': True,
                      }
        
        elif method in ['ADAM']:
             from pyxtal_ff.models.optimize import ADAM as optimizer
             _kwargs = {'options': {'maxiter': 50000}, 
                        'lr_init': 0.001,
                        'beta1': 0.9,
                        'beta2': 0.999,
                        'epsilon': 10E-8,
                        't': 0,
                       }
             
        else:
            msg = f"The {method} is not implemented yet."
            raise NotImplementedError(msg)
            
        kwargs.update(_kwargs)
        
        if user_kwargs is not None:
            kwargs.update(user_kwargs)

        self.optimizer = optimizer
        self.kwargs = kwargs


    def regress(self, model):
        """ Run the optimization scheme here.

        Parameters
        ----------
        model: object
            Class representing the regression model.

        Returns
        -------
        List
            List of the optimized parameters and loss value.
        """
        print(f"Optimizer: {self.kwargs['method']}")
        print(f"Jacobian: {self.kwargs['jac']}\n")
        print(f"MaxIter: {self.kwargs['options']['maxiter']}\n")
        
        parameters0 = model.vector.copy()
        f = LossFunction(model)
        regression = self.optimizer(f.loss, parameters0, **self.kwargs)

        return [regression.x, regression.fun]
