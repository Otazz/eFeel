import numpy as np
import pandas as pd
import datetime
import json
import tweepy
import pickle
import requests
import random
import time
from watson_developer_cloud import ToneAnalyzerV3

REGIOES = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 
			'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
DATES = ['2017-10-29', '2017-10-30', '2017-10-31', '2017-10-28', '2017-10-27']

def read_file():
	ts = list()
	data = np.genfromtxt('IBM Standard Software Installer.csv', delimiter=';', dtype='S50')
	for lin in data:
		ts.append(Tweet(lin[1].decode('utf-8'),lin[2].decode('utf-8'), lin[0].decode('utf-8')))

	return ts

class Tweet(object):
	def __init__(self, text, city, date):
		self.text = text
		self.city = city
		self.date = date
		self.tone_analyzer = ToneAnalyzerV3(
			username='86e31ced-3096-403e-8532-71a8dd54f64d',
			password='acBlLtRg6Azr',
			version='2016-05-19')
		self.tone = self.get_tone()

	def get_tone(self):
		tone_id = ''
		maxi = 0
		mini = 99
		tones = self.tone_analyzer.tone(self.text)
		for tone in tones['document_tone']['tone_categories'][0]['tones']:
			if tone['score'] > maxi:
				tone_id = tone['tone_id']
				maxi = tone['score']
			if(tone['score'] < mini):
				mini = tone['score'] 

		if maxi - mini < 0.1:
			return 0

		else:
			if tone_id == 'joy':
				return 1
			return -1

def get_reach(marca):
	#data = np.genfromtxt('data.csv', delimiter=';', dtype='S20')
	#data = np.delete(data,[1,2,3,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22], axis=1)
	periods = list()
	regions = dict()
	for r in REGIOES:
		regions[r] = None
	data = pd.read_csv('EMPL_2015_2017.CSV', delimiter=';', encoding='ISO-8859-1')
	data = data.loc[data['MARCA'] == marca]
	rd = data[['DATA_EMPLACAMENTO', 'ESTADO']]
	add = data[['DATA_EMPLACAMENTO', 'ESTADO', 'QUANTIDADE']].groupby(['DATA_EMPLACAMENTO', 'ESTADO'])['QUANTIDADE'].transform('sum')
	rd['QUANTIDADE'] = add
	rd['DATA_EMPLACAMENTO'] = pd.to_datetime(rd['DATA_EMPLACAMENTO'], format="%Y%m%d")
	rd = rd.drop_duplicates(['DATA_EMPLACAMENTO', 'ESTADO', 'QUANTIDADE']).reset_index()
	del rd['index']

	return rd


#tf -> Timestamp, emotion
def get_values(rd, tf, period, start_date):
	regions = dict()
	rt = dict()
	c = dict()
	per = list()
	for r in REGIOES:
		regions[r] = list()
		c[r] = 0
	values = dict()
	aux = tf[0].date
	cont = dict()
	for t in tf:
		if t.date == aux:
			if t.city not in cont:
				cont[t.city] = [0, 1]
			cont[t.city][0] += t.tone
			cont[t.city][1] += 1
		else:
			for key in cont:
				if cont[key][1] != 0:
					cont[key][0] /= (cont[key][1])

			values[aux] = cont
			cont = dict()
			aux = t.date

	end_date = start_date + datetime.timedelta(days=period+1)
	while(any(rd['DATA_EMPLACAMENTO'] == start_date)):
		su = dict()
		for r in REGIOES:
			for key in values:
				if r not in su:
					su[r] = 0
				if key >= str(start_date) or key < str(end_date):
					if r in values[key]:
						su[r] += values[key][r][0]

				else:
					su[r] /= period
					break

		mask = (rd['DATA_EMPLACAMENTO'] >= start_date) & (rd['DATA_EMPLACAMENTO'] < end_date)
		for l in REGIOES:
			if l in rd.loc[mask]['ESTADO'].tolist():
				regions[l].append(rd.loc[rd['ESTADO'] == l, 'QUANTIDADE'].iloc[0])
			else:
				regions[l].append(0)

		for l in REGIOES:
			c[l] += sum(regions[l])/len(regions[l])

		start_date = end_date
		end_date = start_date + datetime.timedelta(days=period+1)

		per.append((su,c))
	ret = dict()
	for i in range(len(per)):
		ret[str(i)] = per[i] 
	return ret



def get_emotion(lt):
	tf = []
	for t in lt:
		tf.append([t.date, t.city, t.tone])

	return pd.DataFrame(tf, columns=['Date', 'Estado', 'Metric'])

def get_tweets(marca):
	tws = list()
	auth = tweepy.OAuthHandler('9ighE0dgNX3nxHuVDrga8VOme', '5tvaAYgnmfaG7dRRS542nZizhVPykEQHWaEFMFpBczonCsmYNt')

	api = tweepy.API(auth)

	query = marca
	max_tweets = 1000
	searched_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]

	for i in searched_tweets:
		if i.user.location != 'Brasil' and 'Brasil' in i.user.location:
			location = i.user.location
			for char in location:
				if char == ' ' or char == ',':
					char = '+'
			r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+location+'&key=')
			data = r.json()
			try:
				estado = data['results'][0]['address_components'][-2]['short_name']
				tw = Tweet(i.text, estado, i.created_at.date())
				tws.append(tw)
			except Exception:
				pass

	return tws

def get_geral(marca):
	ret = dict()
	rd = pd.read_pickle('p.pkl')
	for l in REGIOES:
		X = rd['DATA_EMPLACAMENTO'].astype(str).tolist()[13373:13873]
		Y = rd['QUANTIDADE'].tolist()[13373:13873]
		ret[l] = [X, Y]
	return ret

def get_val(periodo, start_date):
	regions = pd.read_pickle('p.pkl')
	#tw = read_file()
	#with open('l.pkl', 'wb') as f:
		#pickle.dump(tw, f)
	with open('l.pkl', 'rb') as f:
		tw = pickle.load(f)
	return get_values(regions, tw, periodo,  datetime.datetime.strptime(start_date, '%Y-%m-%d'))


if __name__ == "__main__":
	marca = 'FIAT'
	#regions = get_reach(marca)
	#regions.to_pickle('p.pkl')
	start = time.time()
	regions = pd.read_pickle('p.pkl')
	print(time.time() - start)
	start = time.time()
	#tw = get_tweets(marca.lower())
	#tw = read_file()
	print(time.time() - start)

	#tw = read_file()
	#with open('l.pkl', 'wb') as f:
		#pickle.dump(tw, f)
	with open('l.pkl', 'rb') as f:
		tw = pickle.load(f)
	start = time.time()
	print(get_values(regions, tw, 1, datetime.datetime.strptime('2017-10-27', '%Y-%m-%d')))
	print(time.time() - start)
	#tw = Tweet(txt, 'SP', datetime.datetime.strptime('2017-10-30', '%Y-%m-%d'))
	#print(tw.tone)
	#plt.figure();
	#regions['SP'].plot()
	#print(regions)
	with open('data.json', 'w') as f:
		json.dump(get_geral('FIAT'), f) 