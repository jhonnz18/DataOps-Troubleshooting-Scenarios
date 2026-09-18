import polars as pl
import numpy as np
import time
import os

def generate_massive_raw_data(output_path: str, n_rows: int = 1_000_000) -> None:
    """Genera un dataset masivo simulado con 1 millón de registros e imperfecciones."""
    print(f"[*] Generando dataset masivo de {n_rows:,} filas (esto puede tomar unos segundos)...")
    
    np.random.seed(42)
    
    # Generación eficiente con Numpy
    transaction_ids = np.arange(1, n_rows + 1)
    # Simulamos nombres con espacios extra y variantes
    names_pool = ["  jhonnier zambrano ", "MARIA PEREZ", "carlos gomez", None, "ana rojas", "  pedro perez "]
    agent_names = np.random.choice(names_pool, size=n_rows, p=[0.2, 0.2, 0.2, 0.1, 0.15, 0.15])
    
    status_pool = ["completed", "PENDING_", "failed!", "COMPLETED", "pending", "FAILED"]
    statuses = np.random.choice(status_pool, size=n_rows)
    
    handle_times = np.random.randint(-20, 900, size=n_rows) # Incluye tiempos negativos anómalos

    df = pl.DataFrame({
        "transaction_id": transaction_ids,
        "agent_name": agent_names,
        "status": statuses,
        "handle_time_sec": handle_times
    })
    
    # Inyectamos algunos nulos intencionales en transaction_id
    df = df.with_columns(
        pl.when(pl.col("transaction_id") % 50000 == 0)
        .then(None)
        .otherwise(pl.col("transaction_id"))
        .alias("transaction_id")
    )
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.write_csv(output_path)
    print(f"[+] Dataset masivo generado con éxito en: {output_path}")

def clean_massive_operational_dataset(input_csv_path: str, output_csv_path: str) -> None:
    if not os.path.exists(input_csv_path):
        generate_massive_raw_data(input_csv_path, n_rows=1_000_000)
        
    print(f"[*] Leyendo archivo masivo de entrada: {input_csv_path}")
    start_time = time.time()
    
    # Lectura optimizada por lotes con Polars (multihilo)
    df = pl.read_csv(input_csv_path)
    print(f"[*] Registros totales cargados en memoria: {df.height:,}")
    
    # Pipeline de transformación vectorizada de alto rendimiento
    df_clean = df.with_columns([
        pl.col("agent_name").str.strip_chars().str.to_titlecase(),
        pl.col("status").str.to_uppercase().str.replace(r"[^A-Z_]", ""),
        pl.when(pl.col("handle_time_sec") < 0)
          .then(0)
          .otherwise(pl.col("handle_time_sec"))
          .alias("handle_time_sec")
    ]).filter(
        pl.col("transaction_id").is_not_null() & 
        pl.col("agent_name").is_not_null()
    )
    
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    df_clean.write_csv(output_csv_path)
    
    elapsed_time = time.time() - start_time
    print(f"[+] ¡Saneamiento masivo completado!")
    print(f"    - Filas limpias resultantes: {df_clean.height:,}")
    print(f"    - Tiempo total de procesamiento: {elapsed_time:.4f} segundos")

if __name__ == "__main__":
    clean_massive_operational_dataset("data/raw_operations.csv", "data/clean_operations.csv")