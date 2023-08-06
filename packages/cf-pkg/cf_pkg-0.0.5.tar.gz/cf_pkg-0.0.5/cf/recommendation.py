from random import *

from cf.clustering import *
from cf.user_based_cf import user_correlation_calculation


class Recommender:
    def __init__(self, user_skill_matrix, user_task_matrix):
        # 初始化需要 用户技能矩阵 用户历史数据
        K = 3
        N = len(user_skill_matrix[0])  # 技能种类数量
        A = []
        C = []
        # 随机初始化A,C
        C = Recommender._random_cov(len(user_skill_matrix[0]))
        for i in range(K):
            A.append(user_skill_matrix[randint(0, len(user_skill_matrix) - 1)])
        g = GaussMixCluster(K, N, A, C)
        g.iter_all(user_skill_matrix)
        s = g.split(user_skill_matrix)
        # 得到用户的聚类

        self.user_split = s
        self.history_data = user_task_matrix

        return

    def recommend(self, user_id, upper=5):
        # upper:推荐任务数量上限
        # 找到用户所属的聚类
        # 协同过滤
        # 推荐
        belonging = []  # user_id
        for t in self.user_split:
            if user_id in t:
                belonging = t
                break
        rs = []
        for t in belonging:
            rs.append(self.history_data[t])

        m = user_correlation_calculation(rs)[belonging.index(user_id)]
        index = m.index(max(m))
        i_userid = belonging[index]
        u_record = self.history_data[i_userid]  # 相似度最高用户的历史数据

        # 选取次数最高的任务
        recommend_candidate = [(i, u_record[i]) for i in range(len(u_record))]
        recommend_candidate.sort(key=lambda x: x[1], reverse=True)  # 按照任务次数从高到低进行排序
        recommends = []
        for i in range(upper):
            if recommend_candidate[i][1] > 0:
                recommends.append(recommend_candidate[i][0])
            else:
                break

        return recommends

    @staticmethod
    def _random_cov(dimension):
        # 随机协方差矩阵
        s = []
        for i in range(dimension):
            s.append([random() for j in range(dimension)])
        return s


if __name__ == '__main__':
    skills = [[0.2, 0.3, 0.3], [0.2, 0.2, 0.4], [0.5, 0.6, 0.7], [0.4, 0.5, 0.3],[0.1, 0.3, 0.4],[0.3, 0.5, 0.2],[0.2, 0.4, 0.6],[0.7, 0.5, 0.3],[0.2, 0.3, 0.5],[0.4, 0.3, 0.2]]
    tasks = [[2, 3, 1, 3, 4, 6], [1, 1, 1, 2, 2, 2], [2, 10, 9, 0, 1, 4], [2, 3, 6, 2, 1, 1], [0, 0, 1, 1, 1, 1],
             [7, 6, 5, 4, 3, 2], [1, 5, 2, 3, 4, 2], [4, 3, 2, 10, 1, 3], [3, 2, 2, 3, 3, 5], [4, 2, 4, 6, 7, 3]]
    r = Recommender(skills, tasks)
    print(r.recommend(7, 3))
