import numpy as np
import math


class GaussMixCluster:
    def __init__(self, k, n, avg_vectors, cov_matrix):
        # k是混合成分数量,n是数据维度
        # 初始化alpha i,u i,sigma i
        # avg_vector:初始n维均值向量；cov_matrix:初始n*n协方差矩阵
        # para_1,2,3:参数
        self.k = k
        self.n = n
        self.para_1 = [1 / k for i in range(k)]
        self.para_2 = avg_vectors
        self.para_3 = [cov_matrix for i in range(k)]
        return

    def _iter_once(self, records):
        # 一次迭代
        # 先算出 y ji(数据j属于混合成分i的后验概率)
        records_num = len(records)  # 数据条数
        y_ji = [[0] * self.k for i in range(records_num)]
        for j in range(records_num):
            # 根据贝叶斯公式
            for i in range(self.k):
                y_ji[j][i] = self.para_1[i] * GaussMixCluster._gauss_result(self.para_2[i], self.para_3[i],
                                                                           records[j]) / sum(
                    [self.para_1[t] * GaussMixCluster._gauss_result(self.para_2[t], self.para_3[t], records[j]) for t in
                     range(self.k)])
        # 再对alpha i,u i,sigjma i分别进行更新

        for i in range(self.k):
            a = sum([x[i] for x in y_ji])  # 后验概率和
            b = np.array([0.0] * self.n)  # 加权概率和
            for j in range(records_num):
                b += y_ji[j][i] * np.array(records[j])
            b = list(b.tolist())  # 转成python list类型

            self.para_1[i] = a / records_num
            self.para_2[i] = [b[t] / a for t in range(len(b))]

            c = [[0.0] * self.n for t in range(self.n)]  # n*n 0矩阵
            for j in range(records_num):
                d = np.array(records[j]) - np.array(self.para_2[i])
                m1 = np.matrix(d)
                # print(m1)
                m2 = np.transpose(m1)  # 转置矩阵
                c += y_ji[j][i] * (np.dot(m2, m1))
            c /= a
            self.para_3[i] = c
        print(self.para_1)
        # 计算似然函数LLD
        LLD = 0
        for j in range(records_num):
            inner = 0
            for i in range(self.k):
                inner += self.para_1[i] * GaussMixCluster._gauss_result(self.para_2[i], self.para_3[i], records[j])
            LLD += np.log(inner)
        return LLD

    def iter_all(self, rs, upper=100, limit=0.0000001):
        # 达到最大迭代次数/LLD变化小于阈值
        a = 0
        for i in range(upper):
            b = self._iter_once(rs)
            if limit >= b - a >= -limit:
                break
            a = b
        return

    def split(self, records):
        # 簇划分
        # 先算出 y ji(数据j属于混合成分i的后验概率)
        records_num = len(records)  # 数据条数
        y_ji = [[0.0] * self.k for i in range(records_num)]
        for j in range(records_num):
            # 根据贝叶斯公式
            for i in range(self.k):
                y_ji[j][i] = self.para_1[i] * GaussMixCluster._gauss_result(self.para_2[i], self.para_3[i],
                                                                           records[j]) / sum(
                    [self.para_1[t] * GaussMixCluster._gauss_result(self.para_2[t], self.para_3[t], records[j]) for t in
                     range(self.k)])

        # 对每个数据确定簇标记(对应簇的下标)
        max_possibility_index = [0] * records_num
        for i in range(records_num):
            max_possibility_index[i] = y_ji[i].index(max(y_ji[i]))
        # 将下标相同的数据归类
        s = []
        for i in range(records_num):
            has_same = False
            for t in s:
                if max_possibility_index[t[0]] == max_possibility_index[i]:
                    # 簇号相同，归为同一类
                    t.append(i)
                    has_same = True
                    break
            if not has_same:
                s.append([i])
        return s

    @staticmethod
    def _gauss_result(u, v, x):
        dimension = len(x)
        a = [x[i] - u[i] for i in range(len(x))]
        m1 = np.mat(a)
        # print(m1)
        m2 = np.matrix(v).I  # 逆矩阵
        # print(m2)
        m3 = np.transpose(m1)  # 转置矩阵
        # print(m3)
        matrix_part_mult = np.dot(np.dot(m1, m2), m3).max()  # 矩阵乘积
        # print( matrix_part_mult)
        h = np.linalg.det(np.array(v))  # 行列式
        if h < 0:
            h = -h
        return np.exp(-0.5 * matrix_part_mult) / (pow(2 * math.pi, dimension / 2) * math.sqrt(h))


if __name__ == '__main__':
    avg = [[0.403, 0.237], [0.714, 0.346], [0.532, 0.472]]
    cov = [[0.1, 0.0], [0.0, 0.1]]
    k = 3
    n = 2
    records = [[0.697, 0.460], [0.774, 0.376], [0.634, 0.264], [0.608, 0.318], [0.556, 0.215], [0.403, 0.237],
               [0.481, 0.149], [0.437, 0.211], [0.666, 0.091], [0.243, 0.267], [0.245, 0.057], [0.343, 0.099],
               [0.639, 0.161], [0.657, 0.198], [0.360, 0.370], [0.593, 0.042], [0.719, 0.103], [0.359, 0.188],
               [0.339, 0.241], [0.282, 0.257], [0.748, 0.232], [0.714, 0.346], [0.483, 0.312], [0.478, 0.437],
               [0.525, 0.369], [0.751, 0.489], [0.532, 0.472], [0.473, 0.376], [0.725, 0.445], [0.446, 0.459]]
    g = GaussMixCluster(k, n, avg, cov)
    g.iter_all(records)
    print(g.split(records))
