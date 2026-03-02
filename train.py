import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from xgboost import XGBClassifier


def aggregate_table(rows):
    df = pd.DataFrame(rows)

    features = {}

    for col in df.columns:
        if np.issubdtype(df[col].dtype, np.number):
            features[f"{col}_mean"] = df[col].mean()
            features[f"{col}_sum"] = df[col].sum()
            features[f"{col}_max"] = df[col].max()
            features[f"{col}_min"] = df[col].min()
            features[f"{col}_std"] = df[col].std()

    return features


def build_features(sample):
    features = {}

    features.update(aggregate_table(sample["table_a_last20"]))
    features.update(aggregate_table(sample["table_b_last20"]))
    features.update(aggregate_table(sample["table_c_last20"]))

    features["number_recycled"] = sample["number_recycled"]
    features["kyc_match"] = sample["kyc_match"]

    return features


# Cargar dataset ya estructurado como lista de samples
data = joblib.load("training_samples.pkl")  
# cada elemento debe tener estructura igual al JSON + campo "fraude"

X_list = []
y_list = []

for sample in data:
    y_list.append(sample["fraude"])
    X_list.append(build_features(sample))

X = pd.DataFrame(X_list)
y = np.array(y_list)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    scale_pos_weight=(len(y_train[y_train == 0]) / len(y_train[y_train == 1])),
    eval_metric="logloss"
)

model.fit(X_train, y_train)

probs = model.predict_proba(X_test)[:, 1]
print("AUC:", roc_auc_score(y_test, probs))

joblib.dump((model, X.columns.tolist()), "fraud_model.pkl")
print("Modelo guardado")