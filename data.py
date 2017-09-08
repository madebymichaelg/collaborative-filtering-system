import csv
import re
from math import sqrt
from operator import mul
import pandas as pd
from pprint import pprint
from time import time

class Data:
    def __init__(self):
        start_time = time()
        self.ratings = []
        self.users = {}
        self.scores = {}
        self.movies = {}
        self.cos_sim_arr = []
        self.pearsons_sim_arr = []
        self.collect()
        # self.fill_cos_sim_arr()
        # self.fill_pearsons_sim_arr()
        # self.fill_user_sim_arr()
        end_time = time()
        print "init time: ", end_time-start_time

    def collect(self):
        for row in csv.reader(open("100k.dat"), delimiter=" "): 
            match = re.findall("(\d+),", row[0])
            user = int(match[0])
            movie = int(match[1])
            score = int(match[2])

            if user in self.users:
                self.users[user].add_rating(movie, score)
            else: 
                self.users[user] = User(user, movie, score)

            if movie in self.movies:
                self.movies[movie].add_rating(user, score)
            else: 
                self.movies[movie] = Movie(movie, user, score)

            if score in self.scores:
                self.scores[score] += 1
            else: 
                self.scores[score] = 1

            self.ratings.append(Rating(user,movie,score))

    def fill_user_sim_arr(self):
        for u_0 in self.users.keys():
            for u_1 in self.users.keys():
                if u_0 == u_1: continue
                cos = self.calc_cos_sim(self.users[u_0], self.users[u_1])
                pearsons = self.calc_pearsons_sim(self.users[u_0], self.users[u_1])
                self.users[u_0].append_sim_arr(u_1, cos, pearsons)


    def mean_item_rating_metric(self, user_id, item_id, neighborhood=None):
        ratings = self.movies[item_id].user_ratings
        if neighborhood:
            scores = [ratings[r] for r in ratings.keys() if r in neighborhood]
        else:
            scores = [ratings[r] for r in ratings.keys() if r != user_id]

        if len(scores) < 1: return -1
        return float(sum(scores)) / len(scores)

    def calc_all_mean_item_rating(self):
        start_time = time()
        data = []
        num_ratings = 0
        for r in self.ratings:
            mean_item_rating = self.mean_item_rating_metric(r.user, r.movie)
            if mean_item_rating < 0: continue
            num_ratings += 1
            data.append({
                "user_id": r.user,
                "item_id": r.movie,
                "actual_rating": r.score,
                "predicted_rating": mean_item_rating,
                "RMSE": self.rmse(mean_item_rating, r.score)
                })
        end_time = time()
        pd.DataFrame.from_dict(data).set_index(["user_id"]).to_csv("mean_item_rating.csv" , encoding='utf-8')
        fin = {
            "RMSE": self.total_rmse(data),
            "Coverage": self.coverage(num_ratings), 
            "Time": end_time-start_time,
        }   
        return fin


    def predictions_with_cos(self, n_size=None, min_sim=None):
        if n_size == None and min_sim == None: 
            assert False

        start_time = time()
        data = []
        num_ratings = 0
        for r in self.ratings:
            other_ratings = self.movies[r.movie].user_ratings
            if n_size != None and len(other_ratings) < n_size:
                neighborhood = other_ratings.keys()
            else:
                neighborhood = self.users[r.user].get_cos_neighborhood(n_size=n_size, min_sim=min_sim)
            
            if not neighborhood: continue

            mean_item_rating = self.mean_item_rating_metric(r.user, r.movie, neighborhood)
            if mean_item_rating < 0: continue
            num_ratings += 1
            data.append({
                "user_id": r.user,
                "item_id": r.movie,
                "actual_rating": r.score,
                "predicted_rating": mean_item_rating,
                "RMSE": self.rmse(mean_item_rating, r.score)
                })

        if not data: 
            return None

        if n_size:
            file_name = "Cos_n_size_" + str(n_size) + ".csv"
        else:
            file_name = "Cos_min_sim_" + str(min_sim).replace('.','p') + ".csv"
        pd.DataFrame.from_dict(data).set_index(["user_id"]).to_csv(file_name , encoding='utf-8')
        end_time = time()
        fin = {
            "RMSE": self.total_rmse(data),
            "Coverage": self.coverage(num_ratings), 
            "Time": end_time-start_time
        }   
        if n_size:
            fin["Neighborhood Size"] = n_size
        elif min_sim:
            fin["Minimum Similarity"] = min_sim
        return fin

    def calc_cos_sim(self, a, b):
        movies = self.intersection(a.user_ratings.keys(), b.user_ratings.keys())
        numerator = 0
        for m in movies: 
            numerator += a.user_ratings[m] * b.user_ratings[m]
        return numerator / (a.dot_product_of_self() * b.dot_product_of_self())

    def fill_cos_sim_arr(self):
        for u_0 in self.users:
            self.cos_sim_arr.append([])
            for u_1 in self.users:
                self.cos_sim_arr[u_0-1].append(self.calc_cos_sim(self.users[u_0], self.users[u_1]))

    def get_cos_sim(self, a, b):
        return self.cos_sim_arr[a.user_id-1][b.user_id-1]


    def predictions_with_pearsons(self, n_size=None, min_sim=None):
        if n_size == None and min_sim == None: 
            assert False

        start_time = time()
        data = []
        num_ratings = 0
        for r in self.ratings:
            other_ratings = self.movies[r.movie].user_ratings
            if len(other_ratings) < n_size:
                neighborhood = other_ratings.keys()
            else:
                neighborhood = self.users[r.user].get_pearsons_neighborhood(n_size=n_size, min_sim=min_sim)
            
            if not neighborhood: continue

            mean_item_rating = self.mean_item_rating_metric(r.user, r.movie, neighborhood)
            if mean_item_rating < 0: continue
            num_ratings += 1
            data.append({
                "user_id": r.user,
                "item_id": r.movie,
                "actual_rating": r.score,
                "predicted_rating": mean_item_rating,
                "RMSE": self.rmse(mean_item_rating, r.score)
                })
        
        if not data: 
            return None
        if n_size:
            file_name = "Pearsons_n_size_" + str(n_size) + ".csv"
        else:
            file_name = "Pearsons_min_sim_" + str(min_sim).replace('.','p') + ".csv"
        pd.DataFrame.from_dict(data).set_index(["user_id"]).to_csv(file_name , encoding='utf-8')
        end_time = time()
        fin = {
            "RMSE": self.total_rmse(data),
            "Coverage": self.coverage(num_ratings), 
            "Time": end_time-start_time,
        }
        if n_size:
            fin["Neighborhood Size"] = n_size
        elif min_sim:
            fin["Minimum Similarity"] = min_sim
        return fin

    def calc_pearsons_sim(self, a, b):
        movies = self.intersection(a.user_ratings.keys(), b.user_ratings.keys())
        if len(movies) < 2:
            return None
        a_mean = a.mean()
        b_mean = b.mean()
        numerator = d_0 = d_1 = 0
        for m in movies: 
            n_0 = a.user_ratings[m] - a_mean
            n_1 = b.user_ratings[m] - b_mean
            numerator += n_0 * n_1
            d_0 += (a.user_ratings[m] - a_mean)**2
            d_1 += (b.user_ratings[m] - b_mean)**2
        if d_0 == 0 or d_1 == 0:
            return None
        return numerator/(sqrt(d_0) * sqrt(d_1))

    def fill_pearsons_sim_arr(self):
        for u_0 in self.users:
            self.pearsons_sim_arr.append([])
            for u_1 in self.users:
                self.pearsons_sim_arr[u_0-1].append(self.calc_pearsons_sim(self.users[u_0], self.users[u_1]))

    def get_pearsons_sim(self, a, b):
        return self.pearsons_sim_arr[a.user_id-1][b.user_id-1]


    def calc_resnick_prediction(self, user, movie, n_size, min_sim, n_type=None):
        if n_type == None:
            assert False

        numerator = denominator = 0
        user_mean = user.mean()
        if n_type == "cos":
            neighborhood = user.get_cos_neighborhood(n_size=n_size, min_sim=min_sim)
        elif n_type == "pearsons":
            neighborhood = user.get_pearsons_neighborhood(n_size=n_size, min_sim=min_sim)
        else: assert False

        for other_user in neighborhood:
            if other_user not in self.movies[movie.movie_id].user_ratings.keys():
                continue
            if n_type == "cos":
                similarity = self.get_cos_sim(user, self.users[other_user])
                similarity = self.translate(similarity, 0, 1, -1, 1)
            elif n_type == "pearsons":
                similarity = self.get_pearsons_sim(user, self.users[other_user])
            
            numerator += (self.movies[movie.movie_id]\
                .user_ratings[other_user] - user_mean) \
                * similarity
            denominator += abs(similarity)
        if denominator == 0:
            return None
        return user_mean + (numerator/denominator)

    def predictions_with_resnick(self, n_size=None, min_sim=None, n_type=None):
        if n_size == None and min_sim == None or n_type == None: 
            assert False

        start_time = time()
        data = []
        num_ratings = 0
        for r in self.ratings:
            prediction = self.calc_resnick_prediction(self.users[r.user], \
                self.movies[r.movie],\
                n_size,\
                min_sim, \
                n_type
            )
            if prediction == None: continue
            num_ratings += 1
            data.append({
                "user_id": r.user,
                "item_id": r.movie,
                "actual_rating": r.score,
                "predicted_rating": prediction,
                "RMSE": self.rmse(prediction, r.score)
            })

        if not data: 
            return None

        if n_size:
            file_name = "Resnick" + n_type + "_n_size_" + str(n_size) + ".csv"
        else:
            file_name = "Resnick" + n_type + "_n_size_" + str(min_sim).replace('.','p') + ".csv"
        pd.DataFrame.from_dict(data).set_index(["user_id"]).to_csv(file_name , encoding='utf-8')
        end_time = time()
        fin = {
            "RMSE": self.total_rmse(data),
            "Coverage": self.coverage(num_ratings), 
            "Time": end_time-start_time,
        }
        if n_size:
            fin["Neighborhood Size"] = n_size
        elif min_sim:
            fin["Minimum Similarity"] = min_sim
        return fin


    def translate(self, value, before_min, before_max, after_min, after_max):
        leftSpan = before_max - before_min
        rightSpan = after_max - after_min

        valueScaled = float(value - before_min) / float(leftSpan)

        return after_min + (valueScaled * rightSpan)

    def intersection(self, a, b):
        return list(set(a) & set(b))

    def dot(self, a, b):
        return sum(map(mul, a, b))
    
    def coverage(self, n):
        return n / float(len(self.ratings))

    def total_rmse(self, data):
        total_error = 0
        for d in data:
            total_error += (d["predicted_rating"] - d["actual_rating"])**2
        total_error = (total_error)/len(data)
        return sqrt(total_error)

    def rmse(self, predicted, actual):
        return abs(predicted-actual)


class Rating():
    """Simple class to hold ratings data"""

    def __init__(self, user, movie, score):
        self.user = user
        self.movie = movie
        self.score = score

    def __str__(self):
        return "\nUser: " + str(self.user) + \
            "\nMovie: " + str(self.movie) + \
            "\nScore: " + str(self.score)

class User():
    """Simple user class"""

    def __init__(self, user_id, movie, score):
        self.user_ratings = {}
        self.ratings = []
        self.cos_sim_arr = []
        self.pearsons_sim_arr = []
        self.arrs_are_sorted = False
        self.avg_score = 0
        self.max_score = -1
        self.min_score = 6
        self.user_id = user_id
        self.user_ratings[movie] = score
        self.ratings.append(score)
        self.dot_total = 0
        self.dot_total = score**2
        if score < self.min_score: self.min_score = score
        if score > self.max_score: self.max_score = score

    def add_rating(self, movie, score):
        self.dot_total += score**2
        self.user_ratings[movie] = score
        self.ratings.append(score)

    def append_sim_arr(self, user, cos, pearsons):
        self.cos_sim_arr.append({
                        'user': user,
                        'sim': cos
                        })
        self.pearsons_sim_arr.append({
                        'user': user,
                        'sim': pearsons
                        })

    def get_cos_neighborhood(self, n_size, min_sim):
        if not self.arrs_are_sorted:
            self.cos_sim_arr.sort(key=lambda x:x['sim'])
            self.pearsons_sim_arr.sort(key=lambda x:x['sim'])
            self.arrs_are_sorted = True

        if n_size:
            return [x['user'] for x in self.cos_sim_arr][n_size*-1:]
        else:
            return [x['user'] for x in self.cos_sim_arr if x['sim'] >= min_sim]

    def get_pearsons_neighborhood(self, n_size, min_sim):
        if not self.arrs_are_sorted:
            self.cos_sim_arr.sort(key=lambda x:x['sim'])
            self.pearsons_sim_arr.sort(key=lambda x:x['sim'])
            self.arrs_are_sorted = True

        if n_size:
            return [x['user'] for x in self.pearsons_sim_arr][n_size*-1:]
        else:
            return [x['user'] for x in self.pearsons_sim_arr if x['sim'] >= min_sim]

    def total_user_ratings(self):
        return len(self.user_ratings)

    def dot_product_of_self(self):
        return sqrt(self.dot_total)

    def mean(self):
        total_score = sum([self.user_ratings[r] for r in self.user_ratings.keys()])
        return float(total_score) / self.total_user_ratings()

    def median(self):
        return sorted([self.user_ratings[r] for r in self.user_ratings.keys()])[self.user_ratings.count/2]

    def mode(self):
        scores = [self.user_ratings[r] for r in self.user_ratings.keys()]
        return max(scores, key = scores.count)

    def std_dev(self):
        count = len(self.user_ratings)
        if count < 2:
            return -1
        mean = self.mean()
        square_devs = sum([(self.user_ratings[r]-mean)**2 for r in self.user_ratings.keys()])
        var = square_devs/float(count)
        return var**.5


class Movie():
    """Simple movie class"""

    def __init__(self, movie_id, user, score):
        self.user_ratings = {}
        self.avg_score = 0
        self.max_score = -1
        self.min_score = 6
        self.movie_id = movie_id
        self.user_ratings[user] = score
        if score < self.min_score: self.min_score = score
        if score > self.max_score: self.max_score = score

    def add_rating(self, user, score):
        self.user_ratings[user] = score

    def total_user_ratings(self):
        return len(self.user_ratings)

    def mean(self):
        total_score = sum([rating.score for rating in self.user_ratings])
        return float(total_score) / self.total_user_ratings()

    def median(self):
        return sorted([self.user_ratings[r] for r in self.user_ratings.keys()])[self.user_ratings.count/2]

    def mode(self):
        scores = [self.user_ratings[r] for r in self.user_ratings.keys()]
        return max(scores, key = scores.count)

    def std_dev(self):
        count = len(self.user_ratings)
        mean = self.mean()
        square_devs = sum([(self.user_ratings[r]-mean)**2 for r in self.user_ratings.keys()])
        var = square_devs/float(count)
        return var**.5

