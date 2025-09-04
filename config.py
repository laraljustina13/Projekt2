import os
from dotenv import load_dotenv

load_dotenv()

# MinIO konfiguracija
MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'localhost:9000')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'admin')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'password')
MINIO_BUCKET_NAME = os.getenv('MINIO_BUCKET_NAME', 'tcga-data')

# MongoDB konfiguracija
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://admin:password@localhost:27017')
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'tcga_database')
MONGO_COLLECTION_NAME = os.getenv('MONGO_COLLECTION_NAME', 'patients')

# cGAS-STING genski put
TARGET_GENES = [
    'C6orf150', 'CCL5', 'CXCL10', 'TMEM173', 'CXCL9', 
    'CXCL11', 'NFKB1', 'IKBKE', 'IRF3', 'TREX1', 
    'ATM', 'IL6', 'CXCL8'
]

# TCGA cohort URLs
TCGA_COHORT_URLS = {
    'coad': 'https://xenabrowser.net/datapages/?dataset=TCGA.COAD.sampleMap%2FHiSeqV2_PANCAN&host=https%3A%2F%2Ftcga.xenahubs.net&removeHub=http%3A%2F%2F127.0.0.1%3A7222',
    'brca': 'https://xenabrowser.net/datapages/?dataset=TCGA.BRCA.sampleMap%2FHiSeqV2_PANCAN&host=https%3A%2F%2Ftcga.xenahubs.net&removeHub=http%3A%2F%2F127.0.0.1%3A7222',
    'luad': 'https://xenabrowser.net/datapages/?dataset=TCGA.LUAD.sampleMap%2FHiSeqV2_PANCAN&host=https%3A%2F%2Ftcga.xenahubs.net&removeHub=http%3A%2F%2F127.0.0.1%3A7222'
}