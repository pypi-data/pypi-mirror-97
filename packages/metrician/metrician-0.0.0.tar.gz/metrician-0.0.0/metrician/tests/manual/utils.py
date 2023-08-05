



def make_classifier():
    from tests.manual import constants
    from torch import nn
    return nn.Sequential(
        nn.Linear(constants.INPUT_SIZE, constants.INPUT_SIZE),
        nn.ReLU(),
        nn.Linear(constants.INPUT_SIZE, constants.N_CLASSES),
    )

def make_data():
    from tests.manual import constants
    import torch
    return torch.randn((8,constants.INPUT_SIZE)),torch.randn((8,constants.N_CLASSES))