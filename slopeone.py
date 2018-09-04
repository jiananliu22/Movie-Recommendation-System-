# coding = utf-8

# Slopeone
import random

import math
from operator import itemgetter


class SlopeOne():
    # 初始化相关参数
    def __init__(self):
        # 为其推荐10部电影
        #self.n_sim_user = 20
        self.n_rec_movie = 10

        # 将数据集划分为训练集和测试集
        self.trainSet = {}
        #self.testSet = {}

        # 用户相似度矩阵
        self.user_sim_matrix = {}
        self.movie_count = 0

        self.frequencies = {}
        self.deviations = {}

        #print('Similar user number = %d' % self.n_sim_user)
        print('Recommneded movie number = %d' % self.n_rec_movie)


    # 读文件得到“用户-电影”数据
    def get_dataset(self, filename, pivot=0.75):
        trainSet_len = 0
        testSet_len = 0
        for line in self.load_file(filename):
            user, movie, rating, timestamp = line.split(',')
            #if random.random() < pivot:
            self.trainSet.setdefault(user, {})
            self.trainSet[user][movie] = rating
            trainSet_len += 1
            #else:
            #    self.testSet.setdefault(user, {})
            #    self.testSet[user][movie] = rating
            #    testSet_len += 1
        print('Split trainingSet and testSet success!')
        print('TrainSet = %s' % trainSet_len)
        print('TestSet = %s' % testSet_len)


    # 读文件，返回文件的每一行
    def load_file(self, filename):
        with open(filename, 'r') as f:
            for i, line in enumerate(f):
                if i == 0:  # 去掉文件第一行的title
                    continue
                yield line.strip('\r\n')
        print('Load %s success!' % filename)



    # compute the DEV of 2 movies
    def computeDeviations(self):
    # 获取每位用户的评分数据
        for user, movies in self.trainSet.items():
            # 对于该用户的每个评分项（歌手、分数）
            for (movie, rating) in movies.items():
                self.frequencies.setdefault(movie, {})
                self.deviations.setdefault(movie, {})
                # 再次遍历该用户的每个评分项
                for (movie2, rating2) in movies.items():
                    if movie != movie2:
                        # 将评分的差异保存到变量中
                        self.frequencies[movie].setdefault(movie2, 0)
                        self.deviations[movie].setdefault(movie2, 0.0)
                        self.frequencies[movie][movie2] += 1
                        self.deviations[movie][movie2] += float(rating) - float(rating2)

        for (movie, movies2) in self.deviations.items():
            for movie2 in movies2:
                movies2[movie2] /= self.frequencies[movie][movie2]

        print('Calculate movie deviation success!')        



    def slopeOneRecommendations(self, user):
        recommendations = {}
        frequencies = {}
        watched_movies = self.trainSet[user]
        N = self.n_rec_movie
        # 遍历目标用户的评分项（电影、分数）
        for ((movie, rating)) in watched_movies.items():
            # 对目标用户未评价的电影进行计算
            for (diffmovie, diffRatings) in self.deviations.items():
                if diffmovie not in watched_movies and movie in self.deviations[diffmovie]:
                    freq = self.frequencies[diffmovie][movie]
                    recommendations.setdefault(diffmovie, 0.0)
                    frequencies.setdefault(diffmovie, 0)
                    # 分子
                    recommendations[diffmovie] += (diffRatings[movie] + float(rating)) * freq
                    # 分母
                    frequencies[diffmovie] += freq

        #recommendations = [(k, v / frequencies[k]) for (k, v) in recommendations.items()]
        for k in recommendations:
            recommendations[k] = recommendations[k] / frequencies[k]
        # 排序并返回
        #recommendations.sort(key=lambda artistTuple: artistTuple[1], reverse=True)
        return sorted(recommendations.items(), key=itemgetter(1), reverse=True)[0:N]
        #return recommendations


if __name__ == '__main__':
    rating_file = 'D:\\tamu\\ecen765\\project\\ml-latest-small\\ml-latest-small\\new.csv'
    slopeoneRec = SlopeOne()
    slopeoneRec.get_dataset(rating_file)
    slopeoneRec.computeDeviations()
    #print("original user_movie set:")
    #print(slopeoneRec.trainSet)
    user = str(672)
    rec_movies = slopeoneRec.slopeOneRecommendations(user)
    print("user " + user + " :recommendation movies list based on SlopeOne")
    print(rec_movies)
