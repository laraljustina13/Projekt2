from minio import Minio
from minio.error import S3Error
import io
import requests
from config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET_NAME

def get_minio_client():
    client = Minio(
        MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False
    )
    return client

def ensure_bucket_exists(client, bucket_name):
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

def upload_tsv_to_minio(url, cohort_name):
    # Implementacija uploada
    pass

def download_from_minio(cohort_name):
    """Preuzima TSV datoteku iz MinIO bucketa"""
    try:
        print(f"🔍 Pokušavam preuzeti {cohort_name} iz MinIO...")
        
        client = get_minio_client()
        object_name = f"{cohort_name}/gene_expression.tsv"
        
        print(f"🔍 Tražim objekt: {object_name} u bucketu: {MINIO_BUCKET_NAME}")
        
        # Prvo provjeri postoji li objekt
        try:
            client.stat_object(MINIO_BUCKET_NAME, object_name)
            print(f"✅ Objekt {object_name} postoji u MinIO")
        except Exception as e:
            print(f"❌ Objekt {object_name} ne postoji: {e}")
            return None
        
        # Dohvati objekt iz MinIO-a
        response = client.get_object(MINIO_BUCKET_NAME, object_name)
        data = response.read()
        
        print(f"✅ {cohort_name} uspješno preuzet ({len(data)} bytes)")
        
        return data
        
    except Exception as e:
        print(f"❌ Greška pri preuzimanju {cohort_name}: {e}")
        return None
    finally:
        if 'response' in locals():
            response.close()
            response.release_conn()