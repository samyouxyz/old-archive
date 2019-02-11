from sklearn import preprocessing, svm
from training_set import *
import numpy as np

D = np.array(training_set['data'])
T = np.array(training_set['target'])

scaler = preprocessing.StandardScaler().fit(D)
D = scaler.transform(D)

def train():
	print('Initialize training...')
	clf = svm.SVC(gamma = 0.01, C = 1000)
	clf.fit(D,T)
	print('Done training! \n')
	return clf

def predict_hbond(classifier):
	aa_hp = {'A': 1.8, 'C': 2.5, 'E': -3.5, 'D': -3.5, 'G': -0.4, 'F': 2.8, 'I': 4.5, 'H': -3.2, 'K': -3.9, 'M': 1.9, 'L': 3.8, 'N': -3.5, 'Q': -3.5, 'P': -1.6, 'S': -0.8, 'R': -4.5, 'T': -0.7, 'W': -0.9, 'V': 4.2, 'Y': -1.3}

	aa_pka = {'A': 7, 'C': 8, 'E': 4, 'D': 4, 'G': 7, 'F': 7, 'I': 7, 'H': 6, 'K': 11, 'M': 7, 'L': 7, 'N': 7, 'Q': 7, 'P': 7, 'S': 7, 'R': 12, 'T': 7, 'W': 7, 'V': 7, 'Y': 10}

	aa_weight = {'A': 89, 'C': 121, 'E': 147, 'D': 133, 'G': 75, 'F': 165, 'I': 131, 'H': 155, 'K': 146, 'M': 149, 'L': 131, 'N': 132, 'Q': 146, 'P': 115, 'S': 105, 'R': 174, 'T': 119, 'W': 204, 'V': 117, 'Y': 181}

	protein_seq = input('\nInput protein sequence: ')
	
	w = 11
	window = []
	target_res = 5  
	for _ in range(len(protein_seq) - w + 1):
		window.append(protein_seq[target_res - 5:target_res + 6])
		target_res += 1

	p = []
	for a in window:
		v = []
		for b in a:
			pka = aa_pka[b]
			hp = aa_hp[b]
			weight = aa_weight[b]
			v.append(pka)
			v.append(hp)
			v.append(weight)
		p.append(v)

	p = scaler.transform(p)

	result = classifier.predict(p)

	str_result = ''
	for r in result:
		str_result += r

	output = f'''
	---------------------------------------------------------------
	Prediction result
	{protein_seq}
	xxxxx{str_result}xxxxx
	---------------------------------------------------------------
	'''
	print(output)

def main():
	classifier = train()
	while True:
		predict_hbond(classifier)

if __name__ == '__main__':
	main()