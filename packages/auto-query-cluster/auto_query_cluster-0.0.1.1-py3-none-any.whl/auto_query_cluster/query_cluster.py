# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2020 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
接口

Authors: fubo
Date:    2021/01/07 11:23:42
"""

import logging
import os
import pickle
from abc import ABCMeta, abstractmethod
from copy import deepcopy
from typing import List, Any
from pydantic import BaseModel

import numpy
from sklearn import preprocessing, metrics, cluster
from nlp_nn.app.sent_similarity.infer import SentSimilarity


class EstimatorElem(BaseModel):
    # 聚类estimator
    estimator: Any

    # class数量
    class_num: int = -1


class EvaluationScore(BaseModel):
    # class数量
    class_num: int = -1

    # label详情
    labels: Any = None

    # SSE
    sse: float = -0.1

    # silhouette index
    silhouette: float = -0.1

    # calinski harabasz index
    calinski_harabasz: float = -0.1


class QueryClusterModelData(BaseModel):
    # 聚类模型的原始query
    queries: List[str]

    # 聚类模型数据
    matrix: Any

    # 模型效果
    score: EvaluationScore = EvaluationScore()


class Sentence2Vector(object):
    def __init__(self):
        try:
            self.sv = SentSimilarity("/".join(os.path.abspath(__file__).split("/")[:-1]) + "/" + "sent2vec.models")
        except Exception as exp:
            raise ValueError("Failed to load sentence to vector model %s" % exp)

    def encoding(self, queries: List[str]):
        """
        query转化为向量
        :param queries:
        :return:
        """
        return preprocessing.normalize(X=self.sv.sent_encode_batch(queries=queries).detach().numpy())


class QueryClusterModel(object):
    def __init__(self):
        self.__model = QueryClusterModelData(queries=[], matrix=None)

    def load_model(self, model_file: str):
        """
        加载模型文件
        :param model_file:
        :return:
        """
        if model_file == "":
            return

        logging.info("Load model file %s" % model_file)
        try:
            with open(model_file, "rb") as fp:
                data = pickle.load(fp)
                self.__model.matrix = data["matrix"]
                self.__model.queries = deepcopy(data["queries"])
                self.__model.score = EvaluationScore.parse_obj(data["score"])
        except Exception as exp:
            raise ValueError("Failed to load best model file %s" % exp)

    def save_model(self, model_file: str):
        """
        保存模型
        :param model_file:
        :return:
        """
        try:
            with open(model_file, "wb") as fp:
                fp.write(pickle.dumps(self.__model.dict()))
        except Exception as exp:
            raise ValueError("Failed to save model to %s %s" % (model_file, exp))

    def get_model_obj(self):
        """
        获取模型详情
        :return:
        """
        return self.__model.copy()

    def set_model_obj(self, model: QueryClusterModelData):
        """
        获取模型详情
        :return:
        """
        self.__model = model.copy()

    def set_model_queries(self, queries: List[str]):
        """
        为模型设置queries
        :param queries:
        :return:
        """
        self.__model.queries = deepcopy(queries)

    def set_model_matrix(self, matrix):
        """
        为模型设置queries
        :param queries:
        :return:
        """
        self.__model.matrix = matrix

    def set_model_score(self, score: EvaluationScore):
        """
        为模型设置score
        :param score:
        :return:
        """
        self.__model.score = score.copy()


class QueryClusterPredictor(object):
    def __init__(self, sent2vec: Sentence2Vector, model: QueryClusterModel, model_file: str):
        self.__model_file = model_file
        self.__sent2vec = sent2vec
        self.__model = model

        # 初始化best模型
        self.__model.load_model(model_file=model_file)
        self.best_model = self.__model.get_model_obj()

    def inference(self, query: str) -> int:
        """
        计算query的类别
        :param query:
        :return:
        """
        logging.info("Inference query label")
        if self.best_model.matrix is None:
            logging.error("No model loaded train/load first")
            raise ValueError("No model loaded train/load first")

        if query in self.best_model.queries:
            logging.info("Query in model %s" % query)
            return self.best_model.score.labels[self.best_model.queries.index(query)]

        vector = self.__sent2vec.encoding(queries=[query])
        scores = numpy.matmul(self.best_model.matrix, numpy.transpose(vector))
        top_k_index = scores[:, 0].argsort()[::-1][0:self.best_model.score.class_num + 1]
        labels = self.best_model.score.labels[top_k_index].tolist()
        dict_data = {}
        for label in labels:
            if label not in dict_data:
                dict_data[label] = 0
            dict_data[label] = dict_data[label] + 1
        max_count = 0
        max_label = -1
        for label in dict_data:
            if dict_data[label] >= max_count:
                max_count = dict_data[label]
                max_label = label
        return max_label

    def get_train_samples(self):
        """
        获取训练集的query数据和label
        :return:
        """
        if self.best_model.matrix is None:
            logging.error("No model loaded train/load first")
            raise ValueError("No model loaded train/load first")

        output = []
        for index, query in enumerate(self.best_model.queries):
            output.append("%d\t%s" % (self.best_model.score.labels[index], query))
        return output


class QueryClusterCoach(metaclass=ABCMeta):
    def __init__(self, sent2vec: Sentence2Vector, model: QueryClusterModel, model_file: str, max_exp_count: int = 8):
        """ query cluster """
        self.sv = sent2vec

        # 加载模型文件或者初始化模型
        logging.info("Initialize or load cluster model %s" % model_file)
        self.model = model
        self.model.load_model(model_file=model_file)

        logging.info("Create cluster estimators count=%d" % max_exp_count)
        self.estimators = {}
        self.create_estimators(max_exp_count=max_exp_count)

    @abstractmethod
    def create_estimators(self, max_exp_count: int = 8):
        """
        创建多实验的聚类算子
        :param max_exp_count:
        :return:
        """
        self.estimators = {
            i: EstimatorElem(estimator=cluster.KMeans(n_clusters=i + 2), class_num=i + 2) for i in range(max_exp_count)
        }

    @abstractmethod
    def search_best_model(self, scores: List[EvaluationScore]):
        """
        选择最优模型
        :return:
        """
        best_value = -10000
        best_score = EvaluationScore()
        for score in scores:
            if score.silhouette > best_value:
                best_score = score.copy()
                best_value = score.silhouette

        self.model.set_model_score(best_score.copy())

    @abstractmethod
    def evaluate_cluster(self, matrix, estimator_elem: EstimatorElem):
        """
        根据当前的estimator计算评估值
        :param matrix:
        :param estimator:
        :return:
        """
        return EvaluationScore(
            class_num=estimator_elem.estimator.labels_.max() + 1,
            labels=estimator_elem.estimator.labels_,
            sse=estimator_elem.estimator.inertia_,
            silhouette=metrics.silhouette_score(
                X=matrix, labels=estimator_elem.estimator.labels_
            ),
            calinski_harabasz=metrics.calinski_harabasz_score(
                X=matrix, labels=estimator_elem.estimator.labels_
            )
        )

    def train(self, queries: List[str], saved_model: str):
        """
        使用样本训练聚类模型
        :param queries: query数据
        :param saved_model: 保存的模型文件
        :return:
        """
        logging.info("Run query embedding")
        matrix = self.sv.encoding(queries=queries)
        self.model.set_model_queries(queries=queries)
        self.model.set_model_matrix(matrix=matrix)

        scores = []
        logging.info("Start to train cluster model")
        for exp_id in self.estimators:
            n_class = self.estimators[exp_id].class_num
            self.estimators[exp_id].estimator.fit(matrix)
            scores.append(self.evaluate_cluster(matrix=matrix, estimator_elem=self.estimators[exp_id]))
            logging.info(
                "Run exp=%d class_num=%d sse=%f silhouette_score=%f calinski_harabasz_score=%f" % (
                    exp_id, n_class, scores[-1].sse, scores[-1].silhouette, scores[-1].calinski_harabasz
                )
            )
        self.search_best_model(scores=scores)
        self.model.save_model(model_file=saved_model)

        logging.info("Training Terminated model saved %s" % saved_model)
