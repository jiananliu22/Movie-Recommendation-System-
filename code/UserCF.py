
import random

import math
from operator import itemgetter


class UserBasedCF():

    def __init__(self):

        self.n_sim_user = 20
        self.n_rec_movie = 10


        self.trainSet = {}
        self.testSet = {}

        self.user_sim_matrix = {}
        self.movie_count = 0

        print('Similar user number = %d' % self.n_sim_user)
        print('Recommneded movie number = %d' % self.n_rec_movie)



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



    def load_file(self, filename):
        with open(filename, 'r') as f:
            for i, line in enumerate(f):
                if i == 0:  
                    continue
                yield line.strip('\r\n')
        print('Load %s success!' % filename)


    def calc_user_sim(self):
       
        print('Building movie-user table ...')
        movie_user = {}
        for user, movies in self.trainSet.items():
            for movie in movies:
                if movie not in movie_user:
                    movie_user[movie] = set()
                movie_user[movie].add(user)
        print('Build movie-user table success!')
        print("movie_user:")
        #print(movie_user)

        self.movie_count = len(movie_user)
        print('Total movie number = %d' % self.movie_count)

        print('Build user co-rated movies matrix ...')
        for movie, users in movie_user.items():
            for u in users:
                for v in users:
                    if u == v:
                        continue
                    self.user_sim_matrix.setdefault(u, {})# setdefult function: if there are no u in the dictionary, add u in the dictionary, and the value is {}. else return the value of u in the dictionary. 
                    self.user_sim_matrix[u].setdefault(v, 0)
                    self.user_sim_matrix[u][v] += 1    
        print('Build user co-rated movies matrix success!')

        # 计算相似性
        print('Calculating user similarity matrix ...')
        for u, related_users in self.user_sim_matrix.items():
            for v, count in related_users.items():
                self.user_sim_matrix[u][v] =  count / math.sqrt(len(self.trainSet[u]) * len(self.trainSet[v])) #count belongs to how many movies u and v both watch
        
        
        print('Calculate user similarity matrix success!')



    def recommend(self, user):
        K = self.n_sim_user
        N = self.n_rec_movie
        rank = {}
        watched_movies = self.trainSet[user]

        # v=similar user, wuv=similar factor
        for v, wuv in sorted(self.user_sim_matrix[user].items(), key=itemgetter(1), reverse=True)[0:K]:
            for movie in self.trainSet[v]:
                rate = float(self.trainSet[v][movie])####
                if movie in watched_movies:
                    continue
                rank.setdefault(movie, 0)
                rank[movie] += wuv * rate###
        return sorted(rank.items(), key=itemgetter(1), reverse=True)[0:N]



if __name__ == '__main__':
    rating_file = 'D:\\tamu\\ecen765\\project\\ml-latest-small\\ml-latest-small\\new.csv'
    userCF = UserBasedCF()
    userCF.get_dataset(rating_file)
    userCF.calc_user_sim()
    #print("original user_movie set:")
    #print(userCF.trainSet)
    #print("user's similar_matrix:")
    #print(userCF.user_sim_matrix)


    for i, user in enumerate(userCF.user_sim_matrix):
        if int(user) == 1:
            rec_movies = userCF.recommend(user)
            print("user " + user + " :recommendation movies list based on UserCF")
            print(rec_movies)
            print()