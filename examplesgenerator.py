import random
import joblib
from datetime import datetime, timedelta

NUM_SAMPLES = 2000  # puedes subirlo


def random_date():
    base = datetime.now()
    delta = timedelta(days=random.randint(0, 365))
    return (base - delta).timestamp()


def generate_table_location():
    rows = []
    for _ in range(20):
        rows.append({
            "latitude": random.uniform(-90, 90),
            "longitude": random.uniform(-180, 180)
        })
    return rows


def generate_table_device_swap(fraud=False):
    rows = []
    for _ in range(20):
        if fraud and random.random() < 0.4:
            # más swaps recientes si es fraude
            ts = datetime.now().timestamp()
        else:
            ts = random_date()

        rows.append({
            "last_device_swap_date": ts
        })
    return rows


def generate_table_sim_swap(fraud=False):
    rows = []
    for _ in range(20):
        if fraud and random.random() < 0.3:
            ts = datetime.now().timestamp()
        else:
            ts = random_date()

        rows.append({
            "last_sim_swap_date": ts
        })
    return rows


def generate_sample():
    # Generamos fraude con 20% probabilidad
    fraude = 1 if random.random() < 0.2 else 0

    sample = {
        "table_a_last20": generate_table_device_swap(fraude),
        "table_b_last20": generate_table_location(),
        "table_c_last20": generate_table_sim_swap(fraude),
        "number_recycled": 1 if fraude and random.random() < 0.3 else 0,
        "kyc_match": 0 if fraude and random.random() < 0.4 else 1,
        "fraude": fraude
    }

    return sample


def main():
    dataset = []

    for _ in range(NUM_SAMPLES):
        dataset.append(generate_sample())

    joblib.dump(dataset, "training_samples.pkl")
    print("training_samples.pkl generado correctamente")
    print(f"Total samples: {len(dataset)}")


if __name__ == "__main__":
    main()