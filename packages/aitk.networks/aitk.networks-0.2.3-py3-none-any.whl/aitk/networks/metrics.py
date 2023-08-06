# -*- coding: utf-8 -*-
# ******************************************************
# aitk.networks: Keras model wrapper with visualizations
#
# Copyright (c) 2021 Douglas S. Blank
#
# https://github.com/ArtificialIntelligenceToolkit/aitk.networks
#
# ******************************************************

import tensorflow.keras.backend as K

def acc(targets, outputs):
    return K.mean(K.all(K.less_equal(K.abs(targets - outputs), self._tolerance), axis=-1), axis=-1)

 
