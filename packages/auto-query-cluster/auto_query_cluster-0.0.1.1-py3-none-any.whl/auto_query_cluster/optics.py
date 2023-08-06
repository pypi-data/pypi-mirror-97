import sys
import logging
import argparse
from typing import List
from sklearn import cluster, metrics
from .query_cluster import EvaluationScore, QueryClusterModel, EstimatorElem
from .query_cluster import Sentence2Vector, QueryClusterCoach


class QueryClusterCoachOPTICS(QueryClusterCoach):
    def __init__(self, sent2vec: Sentence2Vector, model: QueryClusterModel, model_file: str = "",
                 max_exp_count: int = 8):
        """ query cluster """
        super().__init__(sent2vec, model, model_file, max_exp_count)

    def create_estimators(self, max_exp_count: int = 8):
        """
        创建多实验的聚类算子
        :param max_exp_count:
        :return:
        """
        self.estimators = {
            i: EstimatorElem(
                estimator=cluster.OPTICS(min_samples=2 + i, max_eps=0.2),
                class_num=1) for i in range(max_exp_count)
        }

    def search_best_model(self, scores: List[EvaluationScore]):
        """
        选择最优模型
        :return:
        """
        best_value = -10000
        best_score = EvaluationScore()
        for score in scores:
            if score.calinski_harabasz > best_value:
                best_score = score.copy()
                best_value = score.calinski_harabasz
            else:
                break

        self.model.set_model_score(best_score.copy())

    def evaluate_cluster(self, matrix, estimator_elem: EstimatorElem):
        """
        根据当前的estimator计算评估值
        :param matrix:
        :param estimator_elem:
        :return:
        """
        try:
            silhouette_score = metrics.silhouette_score(X=matrix, labels=estimator_elem.estimator.labels_)
        except:
            silhouette_score = -1.0

        try:
            calinski_harabasz_score = metrics.calinski_harabasz_score(X=matrix, labels=estimator_elem.estimator.labels_)
        except:
            calinski_harabasz_score = -1.0

        return EvaluationScore(
            class_num=estimator_elem.class_num,
            labels=estimator_elem.estimator.labels_,
            sse=0.0,
            silhouette=silhouette_score,
            calinski_harabasz=calinski_harabasz_score
        )


def main():
    log_format_string = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format_string, stream=sys.stderr)
    parser = argparse.ArgumentParser()
    parser.add_argument("queries_file", type=str, help="Query file", default="queries.txt")
    parser.add_argument("model_file", type=str, help="Model file", default="model.pkl")
    # 实验次数(实验次数影响聚类结果的每个cluster中最小样本数量)
    parser.add_argument("--max_exp_count", type=int, help="最大实验次数", default=8, required=False)
    args = parser.parse_args()

    with open(args.queries_file, "r") as fp:
        queries = [line.strip("\r\n") for line in fp.readlines()]

    QueryClusterCoachOPTICS(
        sent2vec=Sentence2Vector(),
        model=QueryClusterModel(),
        model_file="",
        max_exp_count=args.max_exp_count
    ).train(queries=queries, saved_model=args.model_file)


if __name__ == '__main__':
    main()