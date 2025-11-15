import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import seaborn as sns
import matplotlib.pyplot as plt
import os

# --- Configuration ---
DATA_PATH = 'data/combined_nbaiot.csv' 
MODEL_DIR = 'models' 
MODEL_PATH = os.path.join(MODEL_DIR, 'intrusion_model.pkl')
PLOT_PATH = 'confusion_matrix.png'

# This is the new file we will create
MONITOR_SAMPLE_PATH = 'data/monitor_sample.csv' 
# --- End Configuration ---

def train_model():
    # --- 1. Load Data ---
    try:
        print(f"Loading preprocessed dataset from {DATA_PATH}...")
        data = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        print(f"❌ ERROR: Data file not found at {DATA_PATH}")
        return
    except Exception as e:
        print(f"❌ ERROR: Could not load data. Details: {e}")
        return

    # --- THIS IS THE FIX ---
    print("Sampling data to 200,000 rows...")
    data = data.sample(n=200000, random_state=42)
    
    # --- NEW LINE ---
    print(f"Saving shuffled sample to {MONITOR_SAMPLE_PATH} for the monitor script...")
    data.to_csv(MONITOR_SAMPLE_PATH, index=False)
    # --- END OF NEW LINE ---


    # --- 2. Setup Features (X) and Labels (y) ---
    print("Setting up features (X) and labels (y)...")
    
    label_column = 'intrusion_label' 
    
    if label_column not in data.columns:
        print(f"❌ ERROR: '{label_column}' column not found in your data.")
        return
        
    y = data[label_column]
    X = data.select_dtypes(include='number')
    
    if label_column in X.columns:
        X = X.drop(label_column, axis=1)
        
    print(f"Training with {len(X.columns)} numeric features.")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # --- 3. Train Model ---
    print("Training RandomForestClassifier...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    clf.fit(X_train, y_train)
    print("✅ Model training complete.")

    # --- 4. Evaluate Model & Print Reports ---
    print("Evaluating model...")
    y_pred = clf.predict(X_test)

    print("\n" + "="*30)
    print("--- Classification Report ---")
    print("="*30)
    print(classification_report(y_test, y_pred))

    print("\n" + "="*30)
    print("--- Confusion Matrix ---")
    print("="*30)
    cm = confusion_matrix(y_test, y_pred)
    print(cm)

    print(f"\nSaving confusion matrix plot to '{PLOT_PATH}'...")
    try:
        plt.figure(figsize=(10, 7))
        class_names = [str(c) for c in clf.classes_] 
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                    xticklabels=class_names, yticklabels=class_names)
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.title('Confusion Matrix')
        plt.savefig(PLOT_PATH)
        print(f"✅ Plot saved to {PLOT_PATH}")
    except Exception as e:
        print(f"⚠️ Warning: Could not save plot. Details: {e}")

    # --- 5. Save Model to the Correct Directory ---
    print(f"\nSaving model to {MODEL_PATH}...")
    os.makedirs(MODEL_DIR, exist_ok=True) 
    joblib.dump(clf, MODEL_PATH)
    print(f"✅ Model saved successfully!")

if __name__ == "__main__":
    train_model()