from flask import Flask, flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import pymongo
import pandas as pd
import json

ALLOWED_EXTENSIONS = {'csv'}
UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = '53780654128405102508'

# DONE
def inject_es(df, data):
    # text-index = table
    es = Elasticsearch(
        ['http://odfe-node1:9200'],
        http_auth=("admin", "admin"),
        use_ssl=True,
        verify_certs=False,
        ssl_show_warn=True,
        timeout=60,
    )
    print()
    es.cluster.health(wait_for_status='green', request_timeout=1)
    #for single_data in data['data']
    #   res = es.index(index="test-index", body=single_data)
    #res = es.bulk(index="test-index", body=df.to_json(orient="records"), refresh=True)
    es.indices.delete(index='test-index', ignore=[400, 404])
    es.indices.create(index='test-index')
    documents = df.to_dict(orient='records')
    bulk(es, documents, index='test-index', doc_type='foo', raise_on_error=True)

# DONE
def inject_mongo(df, data):
    # temp_db = database / datas = table
    conn = pymongo.MongoClient("mongodb://mongo:27017/", username='root', password='mongodb')
    #conn = MongoClient(MongoClient(host=['mongo:27017'], document_class=dict, tz_aware=False, connect=True), u'temp_db')
    mydb = conn["temp_database"]
    collection = mydb["temp_collection"]
    for key in data['data']:
        rec_id1 = collection.insert_one(key)
    print("Data inserted in Mongo") 

    
def check_performance(filepath):
    df = pd.read_csv(filepath, delimiter=';')
    df['index'] = range(1, len(df) + 1)
    data = df.to_json(orient="table", indent=4)
    data = json.loads(data)
    # Injection des données
    inject_es(df, data)
    inject_mongo(df, data)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/",  methods=['GET'])
def hello():
    return render_template("home.html")

@app.route("/upload", methods=['POST'])
def upload():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        check_performance(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "Allez voir sur Kibana ;)"
    
    return 'Failed'

app.run(host="0.0.0.0", port="5000")