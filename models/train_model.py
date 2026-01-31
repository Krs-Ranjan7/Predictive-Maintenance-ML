
# train_model.py
# Trains Logistic Regression and Random Forest on data/sample.csv and saves models to models/
import pandas as pd
import os, json
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

ROOT = os.path.dirname(os.path.dirname(__file__)) if os.path.basename(__file__) == "train_model.py" else "."
DATA_PATH = os.path.join(ROOT, "data", "sample.csv")
models_dir = os.path.join(ROOT, "models")
os.makedirs(models_dir, exist_ok=True)

df = pd.read_csv(DATA_PATH)
# simple preprocessing
df = df.dropna(subset=['Temperature','Vibration','Pressure','Failure'])
df['EquipmentCode'] = df['EquipmentID'].astype('category').cat.codes
X = df[['UsageHours','Temperature','Vibration','Pressure','EquipmentCode']]
y = df['Failure'].astype(int)

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.25, random_state=42, stratify=y)
lr = LogisticRegression(max_iter=1000)
rf = RandomForestClassifier(n_estimators=200, random_state=42)

lr.fit(X_train, y_train)
rf.fit(X_train, y_train)

pred_lr = lr.predict(X_test)
pred_rf = rf.predict(X_test)

report_lr = classification_report(y_test, pred_lr, output_dict=True)
report_rf = classification_report(y_test, pred_rf, output_dict=True)

# save models and metadata
joblib.dump(lr, os.path.join(models_dir, "lr_model.pkl"))
joblib.dump(rf, os.path.join(models_dir, "rf_model.pkl"))

meta = {
    "equipment_mapping": dict(zip(df['EquipmentID'].astype('category').cat.categories, range(len(df['EquipmentID'].astype('category').cat.categories)))),
    "report_lr": report_lr,
    "report_rf": report_rf
}
with open(os.path.join(models_dir, "meta.json"), "w") as f:
    json.dump(meta, f, indent=2)
print("Training completed. Models saved to models/ (lr_model.pkl, rf_model.pkl).")
print("LR report (summary):")
print({k: v for k,v in report_lr.items() if k in ['0','1','accuracy']})
print("RF report (summary):")
print({k: v for k,v in report_rf.items() if k in ['0','1','accuracy']})
