import json
import pandas as pd

data = json.load(open('data_out.json'))

for a in data.keys():
	for b in data[a]:
		if b == "minimum_similarity":
			index = "Minimum Similarity"
		else: 
			index = "Neighborhood Size"
		df = pd.DataFrame.from_dict(data[a][b]).set_index(index).to_csv(str(a) + "_" + str(b) + ".csv" , encoding='utf-8')
