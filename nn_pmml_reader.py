# ==============================================================================
# Original code has been taken from Vaclav's Titanium library
# https://github.com/vaclavcadek/titanium/blob/master/titanium/__init__.py
# Modifications by yogeshhk (Yogesh H. Kulkarni)
# - Made a class just for reading
# - Made dictionary of activation functions
# - Added Main for modular testing/printing
# - etc
# ==============================================================================


try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

SUPPORTED_NS = {
    '4.2': 'http://www.dmg.org/PMML-4_2',
    '4.2.1': 'http://www.dmg.org/PMML-4_2',
    '4.3': 'http://www.dmg.org/PMML-4_3'
}


class PMMLversionNotSupportedException(Exception):
    pass

import numpy as np

class NN_PMML_Reader:
    def __init__(self):
        self._functions = []
        self._num_layers = 0
        self._version = ''
        self._source_data = {}
        self._learning_rate = 0.1
        self._num_epochs = 10000
        self._regularization_strength = 0.1
        self._hidden_layer_size = 10

    def read_pmml(self,filename):
        self.filename = filename
        tree = ET.parse(self.filename)
        pmml = tree.getroot()
        self._version = pmml.attrib.get('version', None)
        ns = SUPPORTED_NS.get(self._version, None)
        if None in [self._version, ns]:
            msg = 'Unsupported self._version of PMML.\nSupported self._versions are: {}'.format(SUPPORTED_NS.keys())
            raise PMMLversionNotSupportedException(msg)

        mbt = pmml.find('{}:MiningBuildTask'.format(self._version), SUPPORTED_NS)
        ext = mbt.find('{}:Extension'.format(self._version), SUPPORTED_NS)
        dm = ext.find('{}:DataMining'.format(self._version), SUPPORTED_NS)
        mt = dm.find('{}:MiningTask'.format(self._version), SUPPORTED_NS)
        mds = mt.findall('{}:MiningData'.format(self._version), SUPPORTED_NS)
        for md in mds:
            name = md.attrib['name']
            filename = md.attrib['filename']
            self._source_data[name] = filename

        nn = pmml.find('{}:NeuralNetwork'.format(self._version), SUPPORTED_NS)
        self._learning_rate = float(nn.attrib['learning_rate'])
        self._num_epochs = int(nn.attrib['num_epochs'])
        self._regularization_strength = float(nn.attrib['regularization_strength'])
        self._hidden_layer_size = int(nn.attrib['hidden_layer_size'])


        layers = nn.findall('{}:NeuralLayer'.format(self._version), SUPPORTED_NS)
        functions = [l.attrib['function'] for l in layers]
        self._functions = functions
        self._num_layers = len(layers)

    def print(self):
        print("Data Sources: {}".format(self._source_data))
        print("Learning rate: {}".format(self._learning_rate))
        print("Num Epochs: {}".format(self._num_epochs))
        print("Regularization Strength: {}".format(self._regularization_strength))

        print("Num Layers: {}".format(self._num_layers))
        print("Functions: {}".format(self._functions))



if __name__ == "__main__":
    pmml = NN_PMML_Reader()
    pmml.read_pmml('data/iris_for_tf.pmml') # generated by keras2pmml
    pmml.print()


