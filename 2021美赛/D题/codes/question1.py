import csv
import os
import networkx as nx
import matplotlib.pyplot as plt


# Make new folder to save images
folder = "pics"
if not os.path.exists(folder):
    os.mkdir(folder)

# Reading file Influence_data.csv
f = open("../datas/influence_data.csv",mode="r",encoding="utf-8")
csv_reader = csv.reader(f)
# Loading all rows in a list
rows = [i for i in csv_reader]
# Headers of the csv file
headers = rows[0]
# the list contain influencer_name
influencer_name = [row[1] for row in rows[1:]]
# the list contain follower_name
follower_name = [row[5] for row in rows[1:]]
# Make dict to save all musicians
musicians_dict = {}

for musician in influencer_name:
    if musician not in musicians_dict:
        musicians_dict[musician] = 1
    else:
        musicians_dict[musician] += 1
for musician in follower_name:
    if musician not in musicians_dict:
        musicians_dict[musician] = 1
    else:
        musicians_dict[musician] += 1
# Need to count followers and influencers
influencers_dict = {}
followers_dict = {}
for key,value in musicians_dict.items():
    influencers_dict[key] = 0
    followers_dict[key] = 0

for musician in influencer_name:
    if musician not in influencers_dict:
        influencers_dict[musician] = 1
    else:
        influencers_dict[musician] += 1
for musician in follower_name:
    if musician not in followers_dict:
        followers_dict[musician] = 1
    else:
        followers_dict[musician] += 1

influencers = list(influencers_dict.values())
followers = list(followers_dict.values())

# print all musicians of this file
print(musicians_dict)
print(len(musicians_dict))

musicians = list(musicians_dict.keys())
# make several list to save statistics datas
diameters = []
assortativitys = []

# count the scores of every musician
scores = []
news = []
for musician in musicians:
    # Using directed edge connect them
    score = 1
    new = 1
    G = nx.MultiDiGraph()
    for i in range(len(influencer_name)):
        if musician == influencer_name[i]:
            G.add_edge(musician, follower_name[i])
            score += 0.1
        if musician == follower_name[i]:
            G.add_edge(influencer_name[i], musician)
            new += 0.1
    scores.append(score)
    news.append(new)
    # nx.draw(G)
    diameter = nx.average_shortest_path_length(G)
    diameters.append(diameter)
    assortativity = nx.degree_assortativity_coefficient(G)
    assortativitys.append(assortativity)
    # save pitcure in windows can't use this character
    name = musician.replace('\\',"_").replace("/","_").replace(":","_").replace("*","_").replace("?","_").replace('"',"_").replace("<","_").replace(">","_").replace("|","_")
    # plt.savefig(folder + '/' + '{}.png'.format(name))
    # plt.show()

f = open("question1_result.csv",mode='w+',encoding="utf-8-sig",newline="")
csv_write = csv.writer(f)
for i in range(len(musicians)):
    csv_write.writerow([musicians[i],diameters[i],assortativitys[i],influencers[i],followers[i],scores[i],news[i]])
f.close()