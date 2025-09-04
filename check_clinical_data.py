import pandas as pd

def check_clinical_structure():
    """Provjeri strukturu kliničkih podataka"""
    try:
        clinical_df = pd.read_csv('data/TCGA_clinical_survival_data.tsv', sep='\t', nrows=5)
        
        print("🔍 Struktura kliničkih podataka:")
        print(f"Shape: {clinical_df.shape}")
        print(f"Columns: {clinical_df.columns.tolist()}")
        print(f"Index: {clinical_df.index.tolist()}")
        print("\nPrvih 5 redova:")
        print(clinical_df.head())
        
        # Provjeri ima li traženih stupaca
        target_cols = ['bcr_patient_barcode', 'DSS', 'OS', 'clinical_stage']
        available_cols = [col for col in target_cols if col in clinical_df.columns]
        print(f"\n✅ Dostupni traženi stupci: {available_cols}")
        
        # Provjeri jesu li pacijenti u stupcima
        if 'bcr_patient_barcode' not in clinical_df.columns:
            print("🤔 Pacijenti su vjerojatno u stupcima - treba transponirati!")
            print(f"Primjer stupaca: {clinical_df.columns.tolist()[:5]}")
            
    except Exception as e:
        print(f"❌ Greška: {e}")

if __name__ == "__main__":
    check_clinical_structure()