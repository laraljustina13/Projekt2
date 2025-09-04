import pandas as pd
import os
import io
from utils.minio_client import get_minio_client, ensure_bucket_exists
from utils.data_processor import process_all_cohorts, enrich_with_clinical_data
from utils.mongo_client import insert_patients_data
from config import TCGA_COHORT_URLS, MINIO_BUCKET_NAME

def upload_local_files_to_minio():
    """Uploada lokalne TSV datoteke u MinIO"""
    print("=== UPLOAD LOKALNIH PODATAKA U MinIO ===")
    
    client = get_minio_client()
    ensure_bucket_exists(client, MINIO_BUCKET_NAME)
    
    cohorts = ['coad', 'brca', 'luad']
    
    for cohort in cohorts:
        file_path = f'downloaded_data/{cohort}_gene_expression.tsv'
        
        print(f"🔍 Provjeravam: {file_path}")
        
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"✅ Datoteka postoji: {file_size} bytes")
            
            try:
                with open(file_path, 'rb') as file_data:
                    file_content = file_data.read()
                
                print(f"📦 Uploadam {cohort} ({len(file_content)} bytes)...")
                
                data_stream = io.BytesIO(file_content)
                object_name = f"{cohort}/gene_expression.tsv"
                
                client.put_object(
                    MINIO_BUCKET_NAME,
                    object_name,
                    data_stream,
                    len(file_content),
                    content_type='text/tab-separated-values'
                )
                
                print(f"✅ {cohort} uspješno uploadan u MinIO")
                
            except Exception as e:
                print(f"❌ Greška pri uploadu {cohort}: {e}")
                return False
        else:
            print(f"❌ Datoteka ne postoji: {file_path}")
            return False
    
    return True

def process_and_store_data():
    """Procesira podatke i pohranjuje ih u MongoDB"""
    print("\n=== PROCESIRANJE I POHRANA PODATAKA U MongoDB ===")
    
    # Procesiraj sve kohorte
    cohorts = list(TCGA_COHORT_URLS.keys())
    processed_data = process_all_cohorts(cohorts)
    
    if processed_data.empty:
        print("❌ Nema podataka za procesiranje.")
        return
    
    # Obogati podatke kliničkim podacima (ako datoteka postoji)
    try:
        clinical_path = 'data/TCGA_clinical_survival_data.tsv'
        if os.path.exists(clinical_path):
            processed_data = enrich_with_clinical_data(processed_data, clinical_path)
        else:
            print("ℹ️  Klinički podaci nisu pronađeni, nastavljam bez njih")
    except Exception as e:
        print(f"❌ Greška pri obogaćivanju kliničkim podacima: {e}")
    
    # Pretvori DataFrame u listu rječnika za MongoDB
    patients_data = processed_data.to_dict('records')
    
    # Pohrani podatke u MongoDB
    success = insert_patients_data(patients_data)
    
    if success:
        print(f"✅ Podaci uspješno pohranjeni u MongoDB ({len(patients_data)} pacijenata)")
    else:
        print("❌ Greška pri pohrani podataka u MongoDB")

def main():
    """Glavna funkcija koja pokreće cijeli pipeline"""
    print("Pokrećem TCGA data pipeline...")
    
    # 1. Uploadaj lokalne datoteke u MinIO
    upload_success = upload_local_files_to_minio()
    
    if not upload_success:
        print("❌ Upload nije uspio, prekidam pipeline")
        return
    
    # 2. Procesiraj i pohrani podatke u MongoDB
    process_and_store_data()
    
    print("\n=== PIPELINE ZAVRŠEN ===")

if __name__ == "__main__":
    main()