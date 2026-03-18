import joblib
import numpy as np

# load model
model = joblib.load("../model/fraud_model.pkl")

def detect_transaction(transaction):
    """
    transaction: list [V1, V2, ..., Amount]
    """
    transaction = np.array(transaction).reshape(1, -1)

    result = model.predict(transaction)

    if result[0] == -1:
        return True  # fraud
    return False


# test
if __name__ == "__main__":
    test_tx = np.random.rand(30)  # fake transaction

    if detect_transaction(test_tx):
        print("🚨 Fraud detected")
    else:
        print("✅ Normal transaction")