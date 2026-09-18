import polars as pl
import os

def generate_mock_raw_data(output_path: "data/raw_operations.csv") -> None:
    """Genera datos crudos simulados con anomalías para probar el saneamiento."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    data = {
        "transaction_id": [101, 102, None, 104, 105, 106],
        "agent_name": ["  jhonnier zambrano ", "MARIA PEREZ", "carlos gomez", None, "ana rojas", "  pedro perez "],
        "status": ["completed", "PENDING_", "failed!", "COMPLETED", "pending", "FAILED"],
        "handle_time_sec": [320, -15, 450, 210, -5, 510]
    }
    df = pl.DataFrame(data)
    df.write_csv(output_path)
    print(f"[*] Archivo de prueba crudo generado en: {output_path}")

def clean_operational_dataset(input_csv_path: str, output_csv_path: str) -> None:
    if not os.path.exists(input_csv_path):
        print(f"[!] No se encontró {input_csv_path}. Generando datos de prueba...")
        generate_mock_raw_data(input_csv_path)
        
    print(f"[*] Leyendo archivo: {input_csv_path}")
    df = pl.read_csv(input_csv_path)
    print(f"[*] Registros iniciales cargados: {df.height}")
    
    # 1. Limpieza de strings y estandarización con Regex vectorizado
    df = df.with_columns(
        pl.col("agent_name").str.strip_chars().str.to_titlecase(),
        pl.col("status").str.to_uppercase().str.replace(r"[^A-Z_]", "")
    )
    
    # 2. Corrección de anomalías numéricas (tiempos negativos a 0)
    df = df.with_columns(
        pl.when(pl.col("handle_time_sec") < 0)
        .then(0)
        .otherwise(pl.col("handle_time_sec"))
        .alias("handle_time_sec")
    )
    
    # 3. Filtrado de registros críticos nulos
    df_clean = df.filter(
        pl.col("transaction_id").is_not_null() & 
        pl.col("agent_name").is_not_null()
    )
    
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    df_clean.write_csv(output_csv_path)
    print(f"[+] Saneamiento exitoso. Exportado a: {output_csv_path} ({df_clean.height} filas limpias)")

if __name__ == "__main__":
    clean_operational_dataset("data/raw_operations.csv", "data/clean_operations.csv")