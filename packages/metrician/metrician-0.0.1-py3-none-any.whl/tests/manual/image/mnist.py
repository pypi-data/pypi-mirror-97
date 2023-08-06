from .interface import ImageTestInterface
from unittest import TestCase


class MNIST_Test(TestCase,ImageTestInterface):
    @classmethod
    def setUpClass(cls):
        import random
        from torchvision import transforms as T
        dataset = cls.dataset()
        cls._error_locs = list( set( [ random.randint(0,len(dataset)) for _ in range(25) ] ) )
        cls._t = T.Compose([ 
                T.ToTensor(),
                T.Resize( (28,28) )
         ])

    def _get_model(self):
        from torch.nn import functional as F
        from torch import nn
        class Net(nn.Module):
            def __init__(self):
                super(Net, self).__init__()
                self.conv1 = nn.Conv2d(1, 32, 3, 1)
                self.conv2 = nn.Conv2d(32, 64, 3, 1)
                self.dropout1 = nn.Dropout(0.25)
                self.dropout2 = nn.Dropout(0.5)
                self.fc1 = nn.Linear(9216, 128)
                self.fc2 = nn.Linear(128, 10)

            def forward(self, x):
                x = self.conv1(x)
                x = F.relu(x)
                x = self.conv2(x)
                x = F.relu(x)
                x = F.max_pool2d(x, 2)
                x = self.dropout1(x)
                x = torch.flatten(x, 1)
                x = self.fc1(x)
                x = F.relu(x)
                x = self.dropout2(x)
                x = self.fc2(x)
                output = F.log_softmax(x, dim=1)
                return output
        return Net()

    def test_outlier_detection(self):
        from torch.utils.data import DataLoader
        from tqdm import tqdm
        dataset = self.dataset()
        mw = self._init_outlier_detection()
        data_set = DataLoader( dataset,batch_size=4 )
        model = self.model()
        optim = self.optimizer()
        loss = self.loss()
        for idx,(x,y) in enumerate(tqdm(data_set,total=len(dataset))):
            
            if idx in self._error_locs:x *= torch.randn( x.size() )
            optim.zero_grad()
            y_hat = model(x,y)
            mw( y_hat,y,loss ).backward()
            optim.step()



    

    

