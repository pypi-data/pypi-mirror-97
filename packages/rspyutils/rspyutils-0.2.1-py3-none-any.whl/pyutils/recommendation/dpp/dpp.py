# !/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created on MAY 21, 2018
@author: zlh
"""
import numpy as np
import math
# from process import database


def dpp(kernel_matrix, max_length, epsilon=1E-10):
    """
    fast implementation of the greedy algorithm
    :param kernel_matrix: 2-d array
    :param max_length: positive int
    :param epsilon: small positive scalar
    :return: list
    """
    item_size = kernel_matrix.shape[0]
    cis = np.zeros((max_length, item_size))
    di2s = np.copy(np.diag(kernel_matrix))
    selected_items = list()
    selected_item = np.argmax(di2s)
    selected_items.append(selected_item)
    while len(selected_items) < max_length:
        k = len(selected_items) - 1
        ci_optimal = cis[:k, selected_item]
        di_optimal = math.sqrt(di2s[selected_item])
        elements = kernel_matrix[selected_item, :]
        eis = (elements - np.dot(ci_optimal, cis[:k, :])) / di_optimal
        cis[k, :] = eis
        di2s -= np.square(eis)
        selected_item = np.argmax(di2s)
        # print(di2s[selected_item])
        if di2s[selected_item] < epsilon:
            break
        selected_items.append(selected_item)
    return selected_items


def gen_recall_score(item_size: int, punish=50):
    # punish 越大多样性效果越好
    scores = np.exp(-np.arange(0, item_size) / punish)  # recall score
    # scores = np.exp(-np.ones(item_size))  # recall score
    return scores


def gen_recall_similarities(items: np.array, cid_embedding: dict):
    size = 0
    feature_vectors = []
    vector_len = 0
    for i in items:
        v = cid_embedding.get(i, None)
        if v is not None:
            if vector_len == 0:
                vector_len = len(v)
            feature_vectors.append(v)
            size += 1
    if 0 == size:
        return np.array([]), 0
    # print("vector_len",vector_len)
    feature_vectors = np.array(feature_vectors).reshape((-1, vector_len))
    # print("feature_vectors shape",feature_vectors.shape)
    feature_vectors /= np.linalg.norm(feature_vectors, axis=1, keepdims=True)
    # print(feature_vectors)
    similarities = np.dot(feature_vectors, feature_vectors.T)
    # print("similarities", similarities)
    # print("similarities", similarities.shape)
    # similarities=np.array(feature_vectors).reshape((vector_len,-1))
    # print("similarities.shape",similarities.shape)
    # print(similarities)
    return similarities, size


def gen_kernel_matrix(items: np.array, embedding: dict):
    similarities, size = gen_recall_similarities(items, embedding)
    if 0 == size:
        return np.array([])
    scores = gen_recall_score(size)
    return scores.reshape((size, 1)) * similarities * scores.reshape((1, size))


if __name__ == '__main__':
    # collect = database.FeaturesMysql("../config/dev/samh/config.yaml", "samh")
    # out = collect.fetch_item_features()
    # t = gen_kernel_matrix(np.array([106611, 106612, 7119]), out)
    # print(t)
    print(dpp(t, 2))
