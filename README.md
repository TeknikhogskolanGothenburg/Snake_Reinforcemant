# Snake Game, Controlled by either a human or AI player

This project is the classic snake game, and it can be controlled either by a human or an AI.

The AI part is using a feedforward neural network to train its game play.

Here are some links to the theoretical aspects of the AI.

### PyTorch Module
The game is using the PyTorch library, and its Module base class.
Read more about it here:

https://pytorch.org/docs/stable/generated/torch.nn.Module.html

### Activation Function
We are using the ReLU activator function to transform the summed weighted input.
This article describes ReLU.

https://machinelearningmastery.com/rectified-linear-activation-function-for-deep-learning-neural-networks/

### Optimizer
As our optimizer we are using ADAM

Here is an article about why we use optimizers
https://www.geeksforgeeks.org/optimization-techniques-for-gradient-descent/

There is also a nice video describing them here
https://www.youtube.com/watch?v=mdKjMPmcWjY

To get an understanding of what the ADAM optimizer does, you can go here
https://www.geeksforgeeks.org/intuition-of-adam-optimizer/#:~:text=Adam%20optimizer%20involves%20a%20combination,minima%20in%20a%20faster%20pace.

### Loss Function
We use MSELoss, to measure the loss at each learning step. Read more about it here
https://pythonguides.com/pytorch-mseloss/

### Learning Rate
Read this article to get an understanding the impact the learning rate has on Nural Networks
https://machinelearningmastery.com/understand-the-dynamics-of-learning-rate-on-deep-learning-neural-networks/

### Backpropagation
To understand the role of backpropagation you can look at this Wikipedia article
https://en.wikipedia.org/wiki/Backpropagation
