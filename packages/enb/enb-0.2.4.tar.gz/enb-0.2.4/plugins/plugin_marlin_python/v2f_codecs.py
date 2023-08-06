#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""enb-compatible full-python prototype of the V2F codes for the paper:

 Manuel Martínez Torres, Miguel Hernández-Cabronero, Ian Blanes and Joan Serra-Sagristà,
  “High-throughput variable-to-fixed entropy codec using selective, stochastic code forests,” 
  IEEE Access, vol. 8, no. 1, pp. 81283-81297, 2020. DOI: 10.1109/ACCESS.2020.2991314.
"""
__author__ = "Miguel Hernández Cabronero <miguel.hernandez@uab.cat>"
__date__ = "04/07/2019"

import os
import sys
import numpy as np
import pickle

from .sources import Source
from .v2f import MarlinForestMarkov as _MarlinForestMarkov

from enb.config import get_options

options = get_options()

import enb.icompression
import enb.bitstream

sys.setrecursionlimit(2 ** 16)


class MarlinMarkovCodec(enb.icompression.LosslessCodec):
    """Markov-optimized Marlin forest codec.
    Unless a source is specified and not None, Source.from_data is used for each image being compressed
    """

    def __init__(self, bytes_per_sample, K=8, O=4, S=0, source=None):
        """
        :param bytes_per_sample: number of bytes per sample taken from the data to be compressed
        :param K: trees have size (number of included nodes) 2**K
        :param O: 2**O trees are created (number of process states)
        :param S: shift parameter (useful for very high-entropy sources, e.g., >= 90% of the maximum possible entropy)
        :param source: If None, Source.from_data is used for each image being compressed
          based on the number of bytes per sample. If not None, it is not checked that it can code
          all values in the dynamic range given by bytes per sample.
        """
        assert bytes_per_sample in [1, 2], f"Byte depth {bytes_per_sample} not supported"
        super().__init__(param_dict=dict(K=K, O=O, S=S,
                                         bytes_per_sample=bytes_per_sample,
                                         source=source))
        # compress saves the codec, and the default decompress deletes it from the dict
        self.codec_by_compressed_path = dict()

    def get_source(self, array):
        """Get the source to be used for compression.

        :param array: numpy array used to build a source unless self.param_dict["source"] is not None
        """
        if self.param_dict["source"] is not None:
            source = self.param_dict["source"]
        else:
            old_min = Source.min_symbol_probability
            Source.min_symbol_probability = 0
            source = Source.from_data(array=array)
            Source.min_symbol_probability = old_min
        return source

    def get_pickled_codec_path(self, original_path):
        """Path for a pre-computed codec (from the v2f module) given
        the original path.
        """
        pickle_dir = os.path.join(options.persistence_dir, "v2f_codec_cache", self.label)
        os.makedirs(pickle_dir, exist_ok=True)
        return os.path.join(pickle_dir,
                            "pickled_codec"
                            + os.path.abspath(original_path).replace(os.sep, "_")
                            + ".pickle")

    def unpicke_codec(self, original_path):
        """Load an existing codec stored in the persistence dir or None if not found
        or corrupted.
        """
        pickled_codec_path = self.get_pickled_codec_path(original_path=original_path)

        if not os.path.exists(pickled_codec_path):
            return None

        with open(pickled_codec_path, "rb") as pickled_file:
            print(f"[watch] loading from {pickled_codec_path}...")
            try:
                return pickle.loads(pickled_file.read())
            except EOFError as ex:
                print(f"[watch] Error loading pickled_file={pickled_file}; ex={ex}")
                return None

    def pickle_codec(self, original_path):
        """Dump a pickle of the codec """

    def compress(self, original_path: str, compressed_path: str, original_file_info=None):
        if self.param_dict["bytes_per_sample"] == 1:
            array = np.fromfile(original_path, dtype=np.uint8)
        elif self.param_dict["bytes_per_sample"] == 2:
            array = np.fromfile(original_path, dtype=np.uint16)
        else:
            assert False, f"Invalid bytes_per_sample={bytes_per_sample}"

        source = self.get_source(array=array)
        codec = self.unpicke_codec(original_path=original_path)
        if codec is None:
            codec = _MarlinForestMarkov(K=self.param_dict["K"], O=self.param_dict["O"],
                                        S=self.param_dict["S"], source=source,
                                        symbol_p_threshold=0)
            with open(self.get_pickled_codec_path(original_path), "wb") as pickled_file:
                pickled_file.write(pickle.dumps(codec))

        self.codec_by_compressed_path[compressed_path] = codec

        print(f"[watch] codec={codec}")
        print(f"[watch] codec.source={codec.source}")
        print(f"[watch] {self.__class__.__name__}-enb: coding array.size={array.size}")

        codec_dict = codec.code(array.flatten())

        print(f"[watch] {self.__class__.__name__}-enb: outputting to file={compressed_path}")

        with enb.bitstream.OutputBitStream(compressed_path) as obs:
            for node in codec_dict["coded_data_nodes"]:
                print(f"[watch] node.word={node.word}")
                exit()

    def decompress(self, compressed_path, reconstructed_path, original_file_info=None):
        codec = self.codec_by_compressed_path[compressed_path]
        print(f"[watch] codec={codec}")
        raise NotImplementedError


if __name__ == '__main__':
    print("Non executable module")
