import requests
import json
import iso8601
import datetime
import math
import random
import time
import sys

flights = {}
people = []

# Get destination
destination = input('Enter destination: ')
print ("*************************")

# Get people
c = 1
while (c):
	print('PERSON ' + str(c))
	person_name  =  input('Name: ')
	person_origin  =  input('Origin: ')
	people.append((person_name,person_origin))

	c += 1
	print('----------')
	prompt  =  input('Finished? ')
	print('\n')
	if prompt == 'y':
		c = 0

# TEST INPUT PARAM
l = [1,4,7,3]
out_date = '2016-02-10'
ret_date = '2016-02-20'

url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key = " + "your_API_key"
h = {"content-type": "application/json"}
response_list = []

for i in range(len(people)):
	d = { 
	"request": {
		"passengers": {
		"adultCount": 1
		},
		"slice": [
		{
			"origin": people[i][1],
			"destination": destination,
			"date": out_date
		},
		{
			"origin": destination,
			"destination": people[i][1],
			"date": ret_date
		}
		],
		"solutions": "9"
	}
	}

	response = requests.post(url, data = json.dumps(d), headers = h)
	print(response.status_code)
	if response.status_code != 200:
		print('ERROR: flights not found')
		sys.exit()

	data = response.json()

	for j in range(9):
		x = data['trips']['tripOption'][j]

		out_origin = x['slice'][0]['segment'][0]['leg'][0]['origin']
		out_dest = x['slice'][0]['segment'][-1]['leg'][-1]['destination']
		out_depT = iso8601.parse_date(x['slice'][0]['segment'][0]['leg'][0]['departureTime']).strftime("%H:%M")
		out_arrT = iso8601.parse_date(x['slice'][0]['segment'][-1]['leg'][-1]['arrivalTime']).strftime("%H:%M")
		out_price = round(float(x['saleTotal'][3:])/2)

		ret_origin = x['slice'][1]['segment'][0]['leg'][0]['origin']
		ret_dest = x['slice'][1]['segment'][-1]['leg'][-1]['destination']
		ret_depT = iso8601.parse_date(x['slice'][1]['segment'][0]['leg'][0]['departureTime']).strftime("%H:%M")
		ret_arrT = iso8601.parse_date(x['slice'][1]['segment'][-1]['leg'][-1]['arrivalTime']).strftime("%H:%M")
		ret_price = round(float(x['saleTotal'][3:])/2)

		flights.setdefault((out_origin,out_dest),[])
		flights[(out_origin,out_dest)].append((out_depT,out_arrT,int(out_price)))

		flights.setdefault((ret_origin,ret_dest),[])
		flights[(ret_origin,ret_dest)].append((ret_depT,ret_arrT,int(ret_price)))

def getminutes(t):
	x = time.strptime(t,'%H:%M')
	return x[3] * 60 + x[4]

def printschedule(r):
	for d in range(len(r) / 2):
		name = people[d][0]
		origin = people[d][1]
		out = flights[(origin,destination)][r[2 * d]]
		ret = flights[(destination,origin)][r[2 * d + 1]]
		print('%20s   %.10s	%5s-%5s %3s | %5s-%5s %3s' % (name, origin, out[0], out[1], out[2], ret[0], ret[1], ret[2]))

def schedulecost(s):
	totalprice = 0
	latestarrival = 0
	earliestdep = 24 * 60

	for d in range(len(s) / 2):
		origin = people[d][1]
		outbound = flights[(origin,destination)][s[2 * d]]
		returnf = flights[(destination,origin)][s[2 * d + 1]]

		totalprice += outbound[2]
		totalprice += returnf[2]

		if latestarrival < getminutes(outbound[1]): latestarrival = getminutes(outbound[1])
		if earliestdep > getminutes(returnf[0]): earliestdep = getminutes(returnf[0])

	totalwait = 0
	for d in range(len(s) / 2):
		origin = people[d][1]
		outbound = flights[(origin,destination)][s[2 * d]]
		returnf = flights[(destination,origin)][s[2 * d + 1]]
		
		totalwait += latestarrival - getminutes(outbound[1])
		totalwait += getminutes(returnf[0]) - earliestdep

	return totalprice + totalwait

def geneticoptimization(domain, costf, popsize = 50, step = 1, mutprob = 0.2, elite = 0.4, maxiter = 30):
	def mutate(vec):
		i = random.randint(0,len(domain) - 1)
		if vec[i] > domain[i][0] or vec[i] == domain[i][1]:
			return vec[0:i] + [vec[i] - step] + vec[i + 1:] 
		elif vec[i] < domain[i][1] or vec[i] == domain[i][0]:
			return vec[0:i] + [vec[i] + step] + vec[i + 1:]

	def crossover(r1, r2):
		i = random.randint(1, len(domain) - 2)
		return r1[0:i] + r2[i:]

	pop = []
	for i in range(popsize):
		vec = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
		pop.append(vec)

	topelite = int(elite * popsize)

	# Main loop 
	for i in range(maxiter):
		scores = [(costf(v), v) for v in pop]
		scores.sort()
		ranked = [v for (s, v) in scores]

		pop = ranked[0:topelite]

		while len(pop)<popsize:
			if random.random() < mutprob:
				# Mutation
				c = random.randint(0, topelite)
				pop.append(mutate(ranked[c]))
			else:
				# Crossover
				c1 = random.randint(0, topelite)
				c2 = random.randint(0, topelite)
				pop.append(crossover(ranked[c1], ranked[c2]))

	return scores[0][1]


dom = [(0,8)] * (len(people) * 2)

# Give geneticoptimization() extra SHAKE! :D
def geneticshake(domain, fitness):
	best_shake = [0] * (len(people) * 2)
	for i in range(10):
		x = geneticoptimization(domain, fitness)
		if schedulecost(x) < schedulecost(best_shake):
			best_shake = x
		print('Schedule: ' + str(x))
		print('Cost:	 ' + str(schedulecost(x)) + '\n')
	return best_shake
