import os
import csv
import re

RAW_DIR = "data/raw"
OUTPUT_FILE = "sql/generated_schema.sql"


def clean_col(name: str) -> str:
    name = name.strip()
    name = re.sub(r"\s+", "_", name)
    name = re.sub(r"[^a-zA-Z0-9_]", "", name)
    return name.lower()


def infer_type(values):
    """
    Very simple heuristic:
    - int → INTEGER
    - float → REAL
    - datetime → TIMESTAMP (basic detection)
    - else TEXT
    """

    is_int = True
    is_float = True
    is_date = True

    for v in values:
        v = v.strip()

        if v == "":
            continue

        # int check
        if not re.fullmatch(r"-?\d+", v):
            is_int = False

        # float check
        if not re.fullmatch(r"-?\d+(\.\d+)?", v):
            is_float = False

        # naive date check
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}.*", v):
            is_date = False

    if is_int:
        return "INTEGER"
    if is_float:
        return "REAL"
    if is_date:
        return "TIMESTAMP"

    return "TEXT"


def process_csv(file_path):
    table_name = os.path.basename(file_path).replace(".csv", "")

    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        columns = reader.fieldnames
        data_sample = {col: [] for col in columns}

        # sample first 50 rows for inference
        for i, row in enumerate(reader):
            if i > 50:
                break
            for col in columns:
                data_sample[col].append(row[col])

    col_defs = []

    for col in columns:
        clean = clean_col(col)
        col_type = infer_type(data_sample[col])
        col_defs.append(f'"{clean}" {col_type}')

    sql = f'CREATE TABLE IF NOT EXISTS "{table_name}" (\n    ' + ",\n    ".join(col_defs) + "\n);\n"

    return sql


def main():
    os.makedirs("sql", exist_ok=True)

    output = []

    for file in os.listdir(RAW_DIR):
        if file.endswith(".csv"):
            path = os.path.join(RAW_DIR, file)
            print(f"Processing {file}")
            output.append(process_csv(path))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(output))

    print(f"\nSchema written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()