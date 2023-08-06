import numpy as np

class SGD:
    def __init__(self, lossfunction, parameters0, **kwargs):
        self.method = kwargs['method']
        self.max_iter = kwargs['options']['maxiter']
        self.tol = kwargs['tol']
        self.lr_init = kwargs['lr_init']
        self.lr_method = kwargs['lr_method']
        self.power_t = kwargs['power_t']
        self.momentum = kwargs['momentum']
        self.nestrerovs_momentum = kwargs['nesterovs_momentum']

        self.parameters = parameters0
        self.l_loss = [0., 0.]

        self.velocities = np.zeros_like(parameters0)
        
        for i in range(self.max_iter):
            loss, dloss = lossfunction(self.parameters, True)
            self.l_loss[1] = loss
            self.update_lr(i)
            self.parameters += self.update_parameters(dloss)
            
            if abs(self.l_loss[1] - self.l_loss[0]) < self.tol:
                print("Tolerance is reached")
                break
            else:
                self.l_loss[0] = loss
        
        self.params = self.parameters
        self.loss = self.l_loss[1]

    def update_lr(self, i):
        if self.lr_method == 'invscaling':
            self.lr_rate = (float(self.lr_init) / (i+1) ** self.power_t)
        elif self.lr_method == 'constant':
            self.lr_rate = (float(self.lr_init))

    def update_parameters(self, dloss):
        updates = (self.momentum * self.velocities) - (self.lr_rate * dloss)
        self.velocities = updates

        if self.nestrerovs_momentum:
            updates = (self.momentum * self.velocities) - (self.lr_rate * dloss)
        
        return updates

    @property
    def x(self,):
        return self.params

    @property
    def fun(self,):
        return self.loss

class ADAM:
    def __init__(self, lossfunction, parameters0, **kwargs):
                  
        self.parameters = parameters0
        self.max_epoch = kwargs['options']['maxiter']
        self.learning_rate_init = kwargs['lr_init']
        self.decay_rate1 = kwargs['beta1']
        self.decay_rate2 = kwargs['beta2']
        self.epsilon = kwargs['epsilon']
        self.t = kwargs['t']
        
        self.tol = kwargs['tol']                      # loss cutoff tolerance
        self.l_loss = [0., 0.]               # monitor tolerance between current and previous loss

        # initialize first and second moments of the gradient
        self.ms = np.zeros(self.parameters.shape)
        self.vs = np.zeros(self.parameters.shape)
       
        for i in range(self.max_epoch):     
             
            loss, gradloss = lossfunction(self.parameters, True)
            self.l_loss[1] = loss
           
            self.t += 1
                    
            # update the first and secont moments
            self.ms = self.decay_rate1 * self.ms + (1 - self.decay_rate1) * gradloss
            self.vs = self.decay_rate2 * self.vs + (1 - self.decay_rate2) * (gradloss ** 2) 
            
            # update the learning rate
            self.learning_rate = (self.learning_rate_init * np.sqrt(1 - self.decay_rate2 ** self.t) / (1 - self.decay_rate1 ** self.t))

            # update the params
            self.parameters -= self.learning_rate * self.ms / (np.sqrt(self.vs) + self.epsilon) 
             
            # check if tolerance is reached
            if abs(self.l_loss[1] - self.l_loss[0]) < self.tol:
                print("Tolerance is reached")
                break
            else:
                self.l_loss[0] = loss

        self.params = self.parameters
        self.loss = self.l_loss[1]

    @property
    def x(self,):
            return self.params
    @property
    def fun(self,):
            return self.loss


        
