# -*- coding: utf-8 -*-
"""Task 2.ipynb

Automatically generated by Colab.

Original file is located at
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

class HotelBookingModel:
    def __init__(self):
        self.model = RandomForestClassifier(random_state=42)
        self.feature_encoders = {}
        self.target_encoder = LabelEncoder()

    def _preprocess_features(self, X: pd.DataFrame) -> pd.DataFrame:
        """Encode kolom kategorikal menggunakan LabelEncoder."""
        categorical_cols = ["type_of_meal_plan", "room_type_reserved", "market_segment_type"]
        X_processed = X.copy()
        for col in categorical_cols:
            if col not in self.feature_encoders:
                le = LabelEncoder()
                X_processed[col] = le.fit_transform(X_processed[col])
                self.feature_encoders[col] = le
            else:
                X_processed[col] = self.feature_encoders[col].transform(X_processed[col])
        return X_processed

    def _preprocess_target(self, y: pd.Series) -> pd.Series:
        """Encode target (booking_status)."""
        return self.target_encoder.fit_transform(y)

    def train(self, X_train: pd.DataFrame, y_train: pd.Series) -> None:
        """Train model dengan data yang sudah diproses."""
        X_processed = self._preprocess_features(X_train)
        y_processed = self._preprocess_target(y_train)
        self.model.fit(X_processed, y_processed)

    def save(self, path: str) -> None:
        """Simpan model dan encoder ke file."""
        with open(path, "wb") as f:
            pickle.dump({
                "model": self.model,
                "feature_encoders": self.feature_encoders,
                "target_encoder": self.target_encoder
            }, f)

    @classmethod
    def load(cls, path: str) -> "HotelBookingModel":
        """Muat model dan encoder dari file."""
        with open(path, "rb") as f:
            data = pickle.load(f)
        loaded_model = cls()
        loaded_model.model = data["model"]
        loaded_model.feature_encoders = data["feature_encoders"]
        loaded_model.target_encoder = data["target_encoder"]
        return loaded_model

if __name__ == "__main__":
    df = pd.read_csv("/content/Dataset_B_hotel.csv")
    df = df.drop(columns=["Booking_ID", "arrival_year", "arrival_date"])
    df.dropna(inplace=True)

    X = df.drop(columns=["booking_status"])
    y = df["booking_status"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = HotelBookingModel()
    model.train(X_train, y_train)
    model.save("hotel_booking_model.pkl")