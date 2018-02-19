# sqlite3 commands
# DROP TABLE reports
# CREATE TABLE reports(who TEXT, location TEXT, what BLOB)
# SELECT who, location, what FROM reports
# DELETE FROM reports
# INSERT INTO reports(who, location, what) VALUES(?,?,?)

from flask import Flask, render_template, request
import sqlite3

import paralleldots as pd
from paralleldots import set_api_key, get_api_key
from paralleldots import similarity, ner, taxonomy, sentiment, keywords, intent, emotion, multilang, abuse  

set_api_key("n9lcNSVHnvuOumX4cVtVNo9sPlONAt6vcK9qGsgxA0Y") 
get_api_key()

def keywords(raw):
	w = []
	a=[]
	w.append(pd.keywords(raw))
	del (w[0])['usage']
	my_list=[]
	for d in w[0]['keywords']:
		my_list.append(d['keyword'])
	
	tags = my_list
	return tags

def keywords_exist(text):
	w = []
	a=[]
	w.append(pd.keywords(text))
	del (w[0])['usage']

	if((w[0]['keywords']) == {'keywords': 'No Keywords.', 'confidence_score': '0'}):
		return False
	else:
		return True

def find_similar_reports(who, location, what, other_reports):
	reports = [] 
	for report in other_reports:
		if who==report[0]:
			print("SIMILARITY: {}".format(similarity(what,report[2])['normalized_score']))
			if location == report[1] or similarity(what,report[2])['normalized_score']>=4.55:
				reports.append(report)
	return reports

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    return render_template('main_form.html', invalid=False)

@app.route('/submit', methods=['GET', 'POST'])
def submit():

	who = request.form['who']
	location = request.form['location']
	what_raw = request.form['what']

	if what_raw == "" or not keywords_exist(what_raw):
		return render_template('main_form.html',invalid=True)

	con = sqlite3.connect('database.db')
	cur = con.cursor()

	cur.execute('''SELECT who, location, what FROM reports''')
	rows = cur.fetchall()
	similar_reports = find_similar_reports(who, location, what_raw, rows)

	similar_words = []
	for report in similar_reports:
		for words in keywords(report[2]):
			similar_words.append(words)

	cur.execute('''INSERT INTO reports(who, location, what) VALUES(?,?,?)''', (who, location, what_raw))

	con.commit()
	con.close()

	return render_template('results.html', similar_words=str(similar_words)[1:-1], num_of_similar=len(similar_reports))

if __name__ == "__main__":
    app.run()
	