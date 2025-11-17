# VoiceLock.py — Local Voice Authentication for Firefly
import numpy as np
from cryptography.fernet import Fernet
import torch
from torchaudio import load
from torch.nn import CosineSimilarity

class VoiceLock:
    def __init__(self, passphrase="newfoundland-fog-2025"):
        self.key = Fernet.generate_key(passphrase.encode())
        self.cipher = Fernet(self.key)
        self.similarity = CosineSimilarity(dim=1)
        self.voiceprint = self.load_voiceprint()
        self.threshold = 0.6  # Adjust for sensitivity

    def load_voiceprint(self):
        try:
            with open('voiceprint.npy', 'rb') as f:
                encrypted = f.read()
            return np.load(io.BytesIO(self.cipher.decrypt(encrypted)))
        except FileNotFoundError:
            return None

    def save_voiceprint(self, embedding):
        encrypted = self.cipher.encrypt(io.BytesIO(embedding).read())
        with open('voiceprint.npy', 'wb') as f:
            f.write(encrypted)

    def enroll(self):
        print("Say 'Woof, cousin' 3 times...")
        embeddings = []
        for i in range(3):
            audio = self.record_audio()
            embedding = self.extract_embedding(audio)
            embeddings.append(embedding)
        average = np.mean(embeddings, axis=0)
        self.save_voiceprint(average)
        print("Voiceprint saved.")

    def verify(self, prompt="Woof, cousin"):
        if self.voiceprint is None:
            print("No voiceprint. Enroll first.")
            return False
        print(prompt)
        audio = self.record_audio()
        embedding = self.extract_embedding(audio)
        score = self.similarity(torch.tensor([embedding]), torch.tensor([self.voiceprint]))
        return score > self.threshold

    # Placeholder for record_audio and extract_embedding (use Whisper or ECAPA)
    def record_audio(self):
        # Use pyaudio or torchaudio for mic input
        pass

    def extract_embedding(self, audio):
        # Use pre-trained ECAPA-TDNN or ResNet for embedding
        pass
