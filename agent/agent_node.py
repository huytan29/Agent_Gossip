import socket
import threading
import random
import joblib
import numpy as np
import json
from datetime import datetime

HOST = "0.0.0.0"

logs = []
attack_nodes = set()

metrics = {
    "push": 0,
    "pull": 0
}

LOG_FILE = "logs.txt"
METRIC_FILE = "metrics.json"

model = joblib.load("../model/fraud_model.pkl")
scaler = joblib.load("../model/scaler.pkl")


def write_log(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    log = f"[{timestamp}] {message}"

    logs.append(log)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log + "\n")


def save_metrics():
    with open(METRIC_FILE, "w") as f:
        json.dump(metrics, f, indent=2)


class AgentNode:
    def __init__(self, node_id, port):
        self.id = node_id
        self.port = port
        self.informed = False
        self.running = False

        self.start_server()

    def start_server(self):
        if self.running:
            return

        self.running = True
        thread = threading.Thread(target=self.server, daemon=True)
        thread.start()

    def server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            s.bind((HOST, self.port))
        except:
            print(f"⚠️ Port {self.port} busy")
            return

        s.listen()

        while True:
            conn, addr = s.accept()
            data = conn.recv(1024).decode()

            if data == "REQUEST":
                conn.send("EVENT".encode() if self.informed else "NONE".encode())

            elif "ATTACK" in data:
                self.informed = True
                attack_nodes.add(self.id)
                write_log(f"🔥 ATTACK at Node {self.id}")

            elif "EVENT" in data:
                if not self.informed:
                    write_log(f"📩 Node {self.id} received EVENT")
                self.informed = True

            conn.close()

    def detect(self):
        tx = np.random.rand(30)
        tx = scaler.transform(tx.reshape(1, -1))
        return model.predict(tx)[0] == -1

    def push(self, nodes):
        targets = random.sample(nodes, min(2, len(nodes)))

        for t in targets:
            self.send_event(t.port)
            write_log(f"[PUSH] {self.id} → {t.id}")
            metrics["push"] += 1

        save_metrics()

    def pull(self, nodes):
        target = random.choice(nodes)

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("127.0.0.1", target.port))
            s.send("REQUEST".encode())

            data = s.recv(1024).decode()

            if data == "EVENT":
                self.informed = True
                write_log(f"[PULL] {self.id} ← {target.id}")
                metrics["pull"] += 1

            s.close()
        except:
            pass

        save_metrics()

    def send_event(self, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("127.0.0.1", port))
            s.send("EVENT".encode())
            s.close()
        except:
            pass