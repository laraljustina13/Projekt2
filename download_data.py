# download_data.py
import io, gzip, urllib.parse, requests, pandas as pd
from pathlib import Path

XENA_HUB = "https://tcga.xenahubs.net"
DATASETS = {
    "coad": "TCGA.COAD.sampleMap/HiSeqV2_PANCAN",
    "brca": "TCGA.BRCA.sampleMap/HiSeqV2_PANCAN",
    "luad": "TCGA.LUAD.sampleMap/HiSeqV2_PANCAN",
}

OUT_DIR = Path("downloaded_data")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def download_one(abbr: str, dataset_id: str) -> Path:
    url = f"{XENA_HUB}/download/{urllib.parse.quote(dataset_id, safe='')}.gz"
    r = requests.get(url, stream=True, timeout=180, allow_redirects=True)
    r.raise_for_status()

    # dekompresija i čitanje u DataFrame (redovi = geni, stupci = sampleovi)
    with gzip.open(io.BytesIO(r.content), "rt") as gz:
        df = pd.read_table(gz, index_col=0)

    # sanity check – pravi dataset ima tisuće redaka i stotine+ stupaca
    if df.shape[0] < 50 or df.shape[1] < 50:
        raise RuntimeError(f"{abbr}: neočekivana dimenzija {df.shape} – vjerojatno krivi download.")

    out = OUT_DIR / f"{abbr}_gene_expression.tsv"
    df.to_csv(out, sep="\t")
    print(f"✅ {abbr}: spremio {out} (shape={df.shape})")
    return out

if __name__ == "__main__":
    for abbr, ds in DATASETS.items():
        download_one(abbr, ds)
    print("🎉 Download gotov.")
