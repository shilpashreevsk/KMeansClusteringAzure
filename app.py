import matplotlib
matplotlib.use('Agg')
import sys
from flask import Flask,render_template,request
import time   #query time-
import cStringIO
import pymysql
from azure.storage.blob import PublicAccess
from flask import Flask
from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings
from flask import render_template
from flask import request
import glob
import os
import datetime
import hashlib
import pickle as cPickle
import csv
import pylab
from sklearn.cluster import KMeans
from numpy import vstack,array
from scipy.cluster.vq import *
from werkzeug.utils import secure_filename

hostname = 'shilpashreedb.mysql.database.azure.com'
username = 'shilpahshree@shilpashreedb'
password = 'shOne12#'
database = 'clouddb'

#myConnection = pymysql.connect( host=hostname, user=username, passwd=password, db=database, cursorclass=pymysql.cursors.DictCursor, local_infile=True)
myConnection = pymysql.connect( host=hostname, user=username, passwd=password, db=database, cursorclass=pymysql.cursors.DictCursor, local_infile=True)
print 'DB connected'

#blob
block_csv = BlockBlobService(account_name='resourcegroupnumberon311', account_key='MmC2fx5DZMWoaTP2lZFY2ja4CkfYxlvuklMLbekBpcSJKalvY8VO0wwQvSlfr4wduEhluVeV3v+pxuAbE+1cBA==')
print ('Blob connected')


application = Flask(__name__)
app=application

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_ROOT = os.path.dirname(APP_ROOT)
print APP_ROOT

@app.route('/')
def main():
	return render_template("index.html")

@app.route("/upload", methods = ['POST'])
def csv_upload():
	user_act=request.form['shilpa']
	username_be=request.form['username']
	password_be=request.form['password']
	query="select * from students where Username='"+username_be+"' and Password='"+password_be+"'"
	print (query)
	with myConnection.cursor() as cursor:
		cursor.execute(query)
		row_count = cursor.rowcount
		if row_count==0:
			return "Invalid Credentials"
		else:	
			print (user_act)
			if user_act=="1":
				return render_template("Upload.html")
			elif user_act=="2":
				return render_template("Kmeansmain.html")
			elif user_act=="3":
				return render_template("filehandle.html")
	cursor.close()
	return "failure"


@app.route("/uploadCsv", methods = ['POST'])
def csv_uploadCsv():
	global file_name
	f=request.files['upload_files']
	file_name=f.filename	
	print (file_name)
	titlename=request.form['file']
	global newfile
	newfile=os.path.abspath(file_name)
	print "new file down"
	print newfile
	block_csv.create_blob_from_path('shilpashreesvp',file_name,newfile,content_settings=ContentSettings(content_type='text/csv'))
	return "done"

mylist=[]
#coloumn_names = ["Postal","House","Sector","City","State","Lat","Long","Bracket","Occupancy","District"]
coloumn_names = ["Course #","Section #","Instructor","Room #"]

myfile = open("/home/shilpashree/cdassign/classes.csv","r")
csv_reader = csv.DictReader(myfile, fieldnames=coloumn_names)
next(csv_reader)

@app.route('/kmeans', methods=['GET', 'POST'])
def kmeans():

        attribute1 = request.form['attribute1']
        attribute2 = request.form['attribute2']
        clusters = request.form['clusters']
        K_clusters = int(clusters)
        mylist = getdata(attribute1,attribute2)
        data = []
        cdist=[]
        data = array(mylist)
        #cent, pts = kmeans2(data,K_clusters)
	kmeans= KMeans(K_clusters)
	kmeans.fit(data)

	cent = kmeans.cluster_centers_
    	pts = kmeans.labels_
	print (pts)
        disCluster = []
        for i in range(len(cent)):
		x1 = cent[i][0]
		y1 = cent[i][1]
            	x1 = float("{0:.3f}".format(x1))
            	y1 = float("{0:.3f}".format(y1))
	
	for j in range(i+1,len(cent)):
                dc = {}
                x2 = cent[j][0]
                y2 = cent[j][1]
                x2 = float("{0:.3f}".format(x2))
                y2 = float("{0:.3f}".format(y2))
                dist = np.sqrt((x1-x2)*2 + (y1-y2)*2)
                cdist.append(dist)
                dc['dist'] = "Distance between cluster " + str(i) + " and cluster " + str(j) + " is: " + str(dist)
                disCluster.append(dc)
                print (disCluster)
                print ("Distance between cluster " + str(i) + " and cluster " + str(j) + " is: " + str(dist))
                #colors = ([(clr)[i] for i in pts])
	clr = ([1, 1, 0.0], [0.2, 1, 0.2], [1, 0.2, 0.2], [0.3, 0.3, 1],[0.0, 1.0, 1.0], [0.6, 0.6, 0.1], [1.0, 0.5, 0.0], [1.0, 0.0, 1.0], [0.6, 0.2, 0.2], [0.1, 0.6, 0.6], [0.0, 0.0, 0.0], [0.8, 1.0, 1.0], [0.70, 0.50, 0.50], [0.5, 0.5, 0.5], [0.77, 0.70, 0.00])
	colors = ([(clr)[i] for i in pts])
	print colors
	print pts
	clr_dict = {"yellow":0,"green":0,"red":0,"blue":0,"cyan":0,"deepolive":0,"orange":0,"magenta":0,"ruby":0,"deepteal":0,"black":0,"palecyan":0,"dirtyviolet":0,"gray":0,"olive":0}
	pdict=[]
	for x in colors:
    		if str(x) == "[1, 1, 0.0]":
        		clr_dict["yellow"] += 1
    		if str(x) == "[0.2, 1, 0.2]":
        		clr_dict["green"] += 1
    		if str(x) == "[1, 0.2, 0.2]":
        		clr_dict["red"] += 1
    		if str(x) == "[0.3, 0.3, 1]":
        		clr_dict["blue"] += 1
    		if str(x) == "[0.0, 1.0, 1.0]":
        		clr_dict["cyan"] += 1
    		if str(x) == "[0.6, 0.6, 0.1]":
        		clr_dict["deepolive"] += 1
    		if str(x) == "[1.0, 0.5, 0.0]":
        		clr_dict["orange"] += 1
    		if str(x) == "[1.0, 0.0, 1.0]":
        		clr_dict["magenta"] += 1
    		if str(x) == "[0.6, 0.2, 0.2]":
        		clr_dict["ruby"] += 1
    		if str(x) == "[0.1, 0.6, 0.6]":
        		clr_dict["deepteal"] += 1
    		if str(x) == "[0.0, 0.0, 0.0]":
        		clr_dict["black"] += 1
    		if str(x) == "[0.8, 1.0, 1.0]":
        		clr_dict["palecyan"] += 1
	    	if str(x) == "[0.70, 0.50, 0.50]":
        		clr_dict["dirtyviolet"] += 1
	    	if str(x) == "[0.5, 0.5, 0.5]":
        		clr_dict["gray"] += 1
	    	if str(x) == "[0.77, 0.70, 0.00]":
        		clr_dict["olive"] += 1

        f_write='Cluster,Count\r\n'
        cnt=0
        print (clr_dict)
        for i in clr_dict:
            if clr_dict[i] == 0:
                continue
            string = str(cnt) + " : " + str(clr_dict[i])
            pdict.append(string)
            print ("No of points in cluster with " + str(i) + " is: " + str(clr_dict[i]))
            f_write+= str(cnt)+','+str(clr_dict[i])+'\r\n'
            cnt += 1
        with open("static/d3chart.csv",'wb') as nfile:
            nfile.write(f_write.encode("utf-8"))
        pylab.scatter(data[:,0],data[:,1], c=colors)
        pylab.scatter(cent[:,0],cent[:,1], marker='o', s = 400, linewidths=3, c='none')
        pylab.scatter(cent[:,0],cent[:,1], marker='x', s = 400, linewidths=3)

        pylab.savefig("static/kmeans7.png")

        return render_template('Kmeansmain.html',cdist=cdist,pdict=pdict, disCluster = disCluster)	

def getdata(attr1,attr2):
	c = 0
	for row in csv_reader:
		c += 1
        	if c == 5000:
            		break
        	pair = []
        	if row[attr1] == "":
            		row[attr1] = 0
        	if row[attr2] == "":
            		row[attr2] = 0
		row_1=row[attr1]
		print (row_1)
        	x = float(row[attr1])
        	y = float(row[attr2])
        	pair.append(x)
        	pair.append(y)
        	mylist.append(pair)
    	return mylist


@app.route('/show', methods=['GET', 'POST'])
def show():
  return render_template('show.html')

@app.route('/Bargraph', methods=['GET', 'POST'])
def bargraph():
  return render_template('d3barchart.html')

@app.route('/Piegraph', methods=['GET', 'POST'])
def Piegraph():
  return render_template('d3piechart.html')

@app.route("/load_db", methods = ['POST'])
def load_db():#For uploading the file
	#global file_name'
	UPLOAD_FOLDER="/home/shilpashree/cdassign/"
	csv_file = request.files['file_upload']	
	file_name=csv_file.filename
	#session['file_name']=file_name
	print "file recieved"
	#filename = secure_filename(csv_file.filename)
	#csv_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	drop_query="drop table IF EXISTS "+ file_name[:-4]
	with myConnection.cursor() as cursor:
		cursor.execute(drop_query)
		myConnection.commit()
	print "dropped"
	column_name="("
	abs_filename=UPLOAD_FOLDER+file_name
	with open(abs_filename, 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			line=row
			break
	for i in line:
		column_name+=i+" VARCHAR(50),"
	query="Create table if not exists " + file_name[:-4]+column_name+" sr_no INT NOT NULL AUTO_INCREMENT, PRIMARY KEY(sr_no));"
	print query
	starttime = time.time()
	with myConnection.cursor() as cursor:
		cursor.execute(query)
		myConnection.commit()
	cursor.close()
	print "successfully created"
	#insert_str = r"LOAD DATA LOCAL INFILE + abs_filename + INTO TABLE + file_name[:-4]+  FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 lines"
   	#newline="\\\n"
	#new_char=newline[1:3]
	#print new_char
	insert_str="""LOAD DATA LOCAL INFILE '"""+abs_filename+ """' INTO TABLE """+ file_name[:-4] +""" FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;"""
	print (insert_str)
	with myConnection.cursor() as cursor:
		cursor.execute(insert_str)
		myConnection.commit()
	endtime = time.time()
	count_str="SELECT count(*) FROM "+ file_name[:-4]
	with myConnection.cursor() as cursor:
		cursor.execute(count_str)
		result=cursor.fetchall()
	print "successfully loaded"
	totalsqltime = endtime - starttime 
	return render_template("index.html")


if __name__ == "__main__":
	app.run(debug=True,host='0.0.0.0')

