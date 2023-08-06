from enum import Enum
class DatasetType(Enum):
    audio       = 'audio'
    image       = 'image'
    text        = 'text'
    tabular     = 'distribution'

IMAGE_DATASETS = '''CelebA
CIFAR10
CIFAR100
Cityscapes
COCO
DatasetFolder
EMNIST
FakeData
Fashion-MNIST
Flickr
HMDB51
ImageFolder
ImageNet
Kinetics-400
KMNIST
LSUN
MNIST
Omniglot
PhotoTour
Places365
QMNIST
SBD
SBU
STL10
SVHN
UCF101
USPS
VOC'''.split('\n')
AUDIO_DATASETS = '''CMUARCTIC
COMMONVOICE
GTZAN
LIBRISPEECH
LIBRITTS
LJSPEECH
SPEECHCOMMANDS
TEDLIUM
VCTK
VCTK_092
YESNO'''.split('\n')
TEXT_DATASETS = '''WikiText-2
WikiText103
PennTreebank
SST
IMDb
TextClassificationDataset
AG_NEWS
SogouNews
DBpedia
YelpReviewPolarity
YelpReviewFull
YahooAnswers
AmazonReviewPolarity
AmazonReviewFull
TREC
SNLI
MultiNLI
Multi30k
IWSLT
WMT14
UDPOS
CoNLL2000Chunking
BABI20
EnWik9'''.split('\n')
DATASET_INPUT_TYPES = {

}

DATASET_INPUT_TYPES.update( {ds:DatasetType.audio for ds in AUDIO_DATASETS } )
DATASET_INPUT_TYPES.update( {ds:DatasetType.image for ds in IMAGE_DATASETS } )
DATASET_INPUT_TYPES.update( {ds:DatasetType.text for ds in TEXT_DATASETS } )
