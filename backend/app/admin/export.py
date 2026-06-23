import csv
import os

EXPORT_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', 'generated_exports')


def get_order_history_for_customer(customer_id):
    """Legacy mock version — kept for reference, tasks.py now queries real data directly."""
    return []


def write_csv_file(rows, filename):
    os.makedirs(EXPORT_FOLDER, exist_ok=True)
    filepath = os.path.join(EXPORT_FOLDER, filename)

    if not rows:
        with open(filepath, 'w') as f:
            f.write("No data available\n")
        return filepath

    fieldnames = rows[0].keys()
    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return filepath
