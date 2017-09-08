from data import Data
from pprint import pprint
import json

d = Data()
print len(d.users), "users"
print len(d.users), "movies"
pprint(d.scores)

# d = Data()
# fin = {}
# fin['Cosin'] = {"minimum_similarity": [], "neighborhood_size": []}

# i = 0.0
# for _ in range(7):
# 	hold = d.predictions_with_cos(min_sim=i)
# 	fin['Cosin']['minimum_similarity'].append(hold)
# 	i += 0.15
# 	print i
# print "1/8"

# i = 50
# for _ in range(5):
# 	hold = d.predictions_with_cos(n_size=i)
# 	fin['Cosin']['neighborhood_size'].append(hold)
# 	i += 50
# 	print i
# print "2/8"

# fin['Pearsons'] = {"minimum_similarity": [], "neighborhood_size": []}
# i = 0.0
# for _ in range(7):
# 	hold = d.predictions_with_pearsons(min_sim=i)
# 	fin['Pearsons']['minimum_similarity'].append(hold)
# 	i += 0.15
# 	print i
# print "3/8"

# i = 50
# for _ in range(5):
# 	hold = d.predictions_with_pearsons(n_size=i)
# 	fin['Pearsons']['neighborhood_size'].append(hold)
# 	i += 50
# 	print i
# print "4/8"

# fin['Resnick_Cos'] = {"minimum_similarity": [], "neighborhood_size": []}
# i = 0.0
# for _ in range(7):
# 	hold = d.predictions_with_resnick(min_sim=i, n_type='cos')
# 	fin['Resnick_Cos']['minimum_similarity'].append(hold)
# 	i += 0.15
# 	print i
# print "5/8"

# i = 50
# for _ in range(5):
# 	hold = d.predictions_with_resnick(n_size=i, n_type='cos')
# 	fin['Resnick_Cos']['neighborhood_size'].append(hold)
# 	i += 50
# 	print i
# print "6/8"

# fin['Resnick_Pear'] = {"minimum_similarity": [], "neighborhood_size": []}
# i = 0.0
# for _ in range(7):
# 	hold = d.predictions_with_resnick(min_sim=i, n_type='pearsons')
# 	fin['Resnick_Pear']['minimum_similarity'].append(hold)
# 	i += 0.15
# 	print i
# print "7/8"

# i = 50
# for _ in range(5):
# 	hold = d.predictions_with_resnick(n_size=i, n_type='pearsons')
# 	fin['Resnick_Pear']['neighborhood_size'].append(hold)
# 	i += 50
# 	print i
# print "8/8"

# with open('data.json', 'w') as outfile:
#     json.dump(fin, outfile, indent=4)