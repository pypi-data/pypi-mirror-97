from .interface import ImageTestInterface
from unittest import TestCase


class CIFAR10_Test(TestCase,ImageTestInterface):

    dataset_name = 'CIFAR10'

    @classmethod
    def setUpClass(cls):
        import random
        from torchvision import transforms as T
        dataset = cls.dataset()
        cls._error_locs = list( set( [ random.randint(0,len(dataset)) for _ in range( random.randint(12,25) ) ] ) )
        cls._t = T.Compose([ 
                T.ToTensor(),
                # T.Resize( (32,32) )
         ])
    
    @classmethod
    def _get_loss(cls):
        from torch import nn
        return nn.CrossEntropyLoss()

    def _get_model(self):
        from torch.nn import functional as F
        from torch import nn
        class Net(nn.Module):
            def __init__(self):
                super(self.__class__, self).__init__()
                self.conv1 = nn.Conv2d(3, 6, 5)
                self.conv2 = nn.Conv2d(6, 16, 5)
                self.fc1   = nn.Linear(16*5*5, 120)
                self.fc2   = nn.Linear(120, 84)
                self.fc3   = nn.Linear(84, 10)

            def forward(self, x):
                out = F.relu(self.conv1(x))
                out = F.max_pool2d(out, 2)
                out = F.relu(self.conv2(out))
                out = F.max_pool2d(out, 2)
                out = out.view(out.size(0), -1)
                out = F.relu(self.fc1(out))
                out = F.relu(self.fc2(out))
                out = self.fc3(out)
                return out
        return Net()

    def test_outlier_detection(self):
        from torch.utils.data import DataLoader
        import torch
        from tqdm import tqdm
        dataset = self.dataset()
        mw = self._init_outlier_detection()
        data_set = DataLoader( dataset,batch_size=16,shuffle=False )
        model = self.model()
        optim = self.optimizer()
        loss = self.loss()
        for idx,(x,y) in enumerate(tqdm(data_set,total=int(len(dataset)))):
            if idx in self._error_locs:
                x += torch.randn( x.size() )
                y += torch.ones( y.size() ).long()
                y = y % 10
            optim.zero_grad()
            y_hat = model(x)
            mw( y_hat,y,loss ).backward()
            optim.step()
        self.assertTrue(
            len(list(mw.montitors.values())[0].oods ) > 0,
            'No Out Of Distribution Samples weere found'
        )
        self.assertGreaterEqual(
            round((len(set(list(mw.montitors.values())[0].oods  ).intersection( self._error_locs ))/len(self._error_locs) ) * 100),
            12.5,
            'Did not find enough Out Of Distribution samples'
        )
        self.assertLessEqual(
            round((len(set(list(mw.montitors.values())[0].oods  ).intersection( self._error_locs ))/len(self._error_locs) ) * 100),
            25,
            f'Catching too many Out Of Distribution samples, logged {round((len(set(list(mw.montitors.values())[0].oods  ).intersection( self._error_locs ))/len(self._error_locs) ) * 100)}'
        )


    

    

