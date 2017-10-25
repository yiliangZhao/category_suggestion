from google.cloud import storage
import pandas as pd
import cPickle

client = storage.Client()
bucket = client.get_bucket("category_models")
blob = bucket.get_blob("models/")
# df = pd.read_csv("gs://category_models/models/cat_mapping.csv")
print len(df)
