'''
图转化工具
'''
from tensorflow.core.protobuf import meta_graph_pb2
from bmlx.utils import io_utils
import sys
import os


def convert(xdl, tf):
    meta_graph = meta_graph_pb2.MetaGraphDef()
    meta_graph.ParseFromString(io_utils.read_file_string(xdl))
    io_utils.write_string_file(tf, meta_graph.graph_def.SerializeToString())