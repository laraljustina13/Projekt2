import pandas as pd
import io
from config import TARGET_GENES
from utils.minio_client import download_from_minio

# sinonimi za tražene gene
ALIASES = {
    "C6orf150": ["C6orf150", "MB21D1", "CGAS", "C6ORF150"],
    "TMEM173":  ["TMEM173", "STING"],
    "IL8":      ["IL8", "CXCL8"],
    # ostali bez sinonima:
    "CCL5": ["CCL5"], "CXCL10": ["CXCL10"], "CXCL9": ["CXCL9"], "CXCL11": ["CXCL11"],
    "NFKB1": ["NFKB1"], "IKBKE": ["IKBKE"], "IRF3": ["IRF3"], "TREX1": ["TREX1"], "ATM": ["ATM"], "IL6": ["IL6"]
}

def _resolve_rows(df_index):
    """vrati mapu canonical->row_name koji postoji u df.index"""
    found = {}
    up = {x.upper() for x in df_index}
    for canon in TARGET_GENES:
        for alias in ALIASES.get(canon, [canon]):
            if alias.upper() in up:
                # pronađi točno ime kako postoji u indexu (case-sensitive match)
                row_name = next(r for r in df_index if r.upper() == alias.upper())
                found[canon] = row_name
                break
    return found

def process_gene_expression_data(tsv_data, cohort_name):
    try:
        df = pd.read_csv(io.BytesIO(tsv_data), sep="\t", index_col=0)

        print(f"📈 Originalni podaci: {df.shape}")
        if df.shape[0] < 50 or df.shape[1] < 50:
            print("⚠️ Dimenzije izgledaju krivo — je li uploadan pravi TSV a ne HTML/greška?")
            return pd.DataFrame()

        mapping = _resolve_rows(df.index)
        available = list(mapping.keys())
        print(f"🔬 Dostupni (canonical) geni: {available}")

        if not available:
            # pokaži prvih par redova za dijagnostiku
            print("⚠️ Nema ciljanih gena; prvih 10 redaka indeksa:", df.index.tolist()[:10])
            return pd.DataFrame()

        sub = df.loc[list(mapping.values())].copy()
        # preimenuj retke na canonical imena
        sub.index = list(mapping.keys())

        # transponiraj -> redovi = sampleovi, stupci = canonical geni
        X = sub.T
        X.reset_index(inplace=True)
        X.rename(columns={"index": "sample_barcode"}, inplace=True)

        # iz sample barcoda izvuci patient_id = prvih 12 znakova
        X["patient_id"] = X["sample_barcode"].str.slice(0, 12)
        X["cancer_cohort"] = cohort_name

        # agregiraj ako pacijent ima više uzoraka (median)
        gene_cols = list(mapping.keys())
        agg = X.groupby(["patient_id", "cancer_cohort"], as_index=False)[gene_cols].median(numeric_only=True)

        print(f"✅ Procesirano pacijenata: {len(agg)}")
        return agg

    except Exception as e:
        print(f"❌ Greška pri obradi podataka: {str(e)}")
        return pd.DataFrame()

def process_cohort(cohort_name):
    tsv_data = download_from_minio(cohort_name)
    if tsv_data is None:
        print(f"✗ Nema podataka za kohortu {cohort_name} u MinIO-u")
        return pd.DataFrame()
    return process_gene_expression_data(tsv_data, cohort_name)

def process_all_cohorts(cohorts):
    all_data = pd.DataFrame()
    for cohort_name in cohorts:
        print(f"\n--- Procesiram kohortu: {cohort_name} ---")
        df_cohort = process_cohort(cohort_name)
        if not df_cohort.empty:
            all_data = pd.concat([all_data, df_cohort], ignore_index=True)
            print(f"✓ {cohort_name} uspješno procesirana")
        else:
            print(f"✗ Nema podataka za {cohort_name}")
    return all_data
