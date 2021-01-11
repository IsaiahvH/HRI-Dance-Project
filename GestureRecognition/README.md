# Gesture Recognition

We trained our own classifier that can recognise the different gestures. Each of the gestures stands for a dance move that the Nao can do.

1. The required steps are described [here in section 1](https://github.com/tringn/2D-Keypoints-based-Pose-Classifier).
2. We could use the same neural network (NN) architecture as used in the previously mentioned source. It has:
  - 4 dense layers
  - 4 drop-out layers
3. The NN should have 7 output nodes, namely 6 for the poses, and 1 for the default, 'No pose'.
