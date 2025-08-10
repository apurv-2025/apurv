"""
Claims Anomaly Detection Models Module

This module contains the machine learning models for detecting anomalous health insurance claims.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import logging
from typing import Dict, List, Tuple, Any

logger = logging.getLogger(__name__)


class ClaimsAnomalyDetector:
    """Machine Learning model for detecting anomalous claims"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.isolation_forest = IsolationForest(
            contamination=0.05, 
            random_state=42, 
            n_estimators=100
        )
        self.random_forest = RandomForestClassifier(
            n_estimators=200, 
            random_state=42, 
            max_depth=10,
            class_weight='balanced'
        )
        self.feature_columns = []
        self.is_trained = False
    
    def prepare_features(self, df):
        """Feature engineering for claims data"""
        
        features_df = df.copy()
        
        # Date features
        features_df['submission_date'] = pd.to_datetime(features_df['submission_date'])
        features_df['day_of_week'] = features_df['submission_date'].dt.dayofweek
        features_df['month'] = features_df['submission_date'].dt.month
        features_df['is_weekend'] = (features_df['day_of_week'] >= 5).astype(int)
        
        # Provider features
        provider_stats = features_df.groupby('provider_id').agg({
            'billed_amount': ['mean', 'std', 'count'],
            'units_of_service': 'mean',
            'is_anomaly': 'mean'  # Historical anomaly rate for provider
        }).round(2)
        
        provider_stats.columns = ['provider_avg_bill', 'provider_std_bill', 'provider_claim_count',
                                'provider_avg_units', 'provider_anomaly_rate']
        
        features_df = features_df.merge(
            provider_stats, 
            left_on='provider_id', 
            right_index=True, 
            how='left'
        )
        
        # Amount-based features
        features_df['bill_to_avg_ratio'] = (
            features_df['billed_amount'] / features_df['provider_avg_bill']
        ).fillna(1)
        
        features_df['amount_per_unit'] = (
            features_df['billed_amount'] / features_df['units_of_service']
        )
        
        # Categorical encoding
        categorical_features = ['provider_specialty', 'patient_gender', 'cpt_code', 
                              'icd_code', 'place_of_service', 'prior_authorization']
        
        for feature in categorical_features:
            if feature not in self.label_encoders:
                self.label_encoders[feature] = LabelEncoder()
                features_df[f'{feature}_encoded'] = self.label_encoders[feature].fit_transform(
                    features_df[feature].astype(str)
                )
            else:
                # Handle unseen categories in test data
                features_df[f'{feature}_encoded'] = features_df[feature].apply(
                    lambda x: self.label_encoders[feature].transform([str(x)])[0] 
                    if str(x) in self.label_encoders[feature].classes_ else -1
                )
        
        # Select final feature columns
        feature_columns = [
            'patient_age', 'units_of_service', 'billed_amount', 'paid_amount',
            'day_of_week', 'month', 'is_weekend', 'provider_avg_bill', 
            'provider_std_bill', 'provider_claim_count', 'provider_avg_units',
            'provider_anomaly_rate', 'bill_to_avg_ratio', 'amount_per_unit'
        ]
        
        # Add encoded categorical features
        feature_columns.extend([f'{cat}_encoded' for cat in categorical_features])
        
        self.feature_columns = feature_columns
        
        return features_df[feature_columns].fillna(0)
    
    def train(self, df):
        """Train the anomaly detection models"""
        
        logger.info("Preparing features for training...")
        X = self.prepare_features(df)
        y = df['is_anomaly']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train Isolation Forest (unsupervised)
        logger.info("Training Isolation Forest...")
        self.isolation_forest.fit(X_train_scaled)
        
        # Train Random Forest (supervised)
        logger.info("Training Random Forest...")
        self.random_forest.fit(X_train_scaled, y_train)
        
        # Evaluate models
        self._evaluate_models(X_test_scaled, y_test)
        
        self.is_trained = True
        logger.info("Training completed successfully!")
        
        return {
            'X_test': X_test_scaled,
            'y_test': y_test,
            'feature_names': self.feature_columns
        }
    
    def _evaluate_models(self, X_test, y_test):
        """Evaluate model performance"""
        
        # Isolation Forest predictions
        iso_scores = self.isolation_forest.decision_function(X_test)
        iso_preds = self.isolation_forest.predict(X_test)
        iso_preds = np.where(iso_preds == -1, 1, 0)  # Convert to 0/1
        
        # Random Forest predictions
        rf_preds = self.random_forest.predict(X_test)
        rf_proba = self.random_forest.predict_proba(X_test)[:, 1]
        
        logger.info("=== Isolation Forest Results ===")
        logger.info(f"Classification Report:\n{classification_report(y_test, iso_preds)}")
        
        logger.info("=== Random Forest Results ===")
        logger.info(f"Classification Report:\n{classification_report(y_test, rf_preds)}")
        logger.info(f"AUC Score: {roc_auc_score(y_test, rf_proba):.3f}")
    
    def predict(self, df):
        """Make predictions on new claims"""
        
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        X = self.prepare_features(df)
        X_scaled = self.scaler.transform(X)
        
        # Get predictions from both models
        iso_scores = self.isolation_forest.decision_function(X_scaled)
        rf_proba = self.random_forest.predict_proba(X_scaled)[:, 1]
        
        # Combine scores (weighted average)
        # Handle division by zero in normalization
        iso_range = iso_scores.max() - iso_scores.min()
        if iso_range > 0:
            iso_normalized = (iso_scores - iso_scores.min()) / iso_range
        else:
            iso_normalized = np.zeros_like(iso_scores)
            
        combined_score = 0.3 * iso_normalized + 0.7 * rf_proba
        
        # Convert to 0-100 scale
        risk_scores = (combined_score * 100).round(1)
        
        # Classification thresholds
        classifications = np.where(
            risk_scores >= 80, 'High Risk',
            np.where(risk_scores >= 50, 'Suspicious', 'Normal')
        )
        
        # Feature importance (top drivers)
        feature_importance = self.random_forest.feature_importances_
        top_features_idx = np.argsort(feature_importance)[::-1][:5]
        
        results = []
        for i, (score, classification) in enumerate(zip(risk_scores, classifications)):
            top_drivers = [self.feature_columns[idx] for idx in top_features_idx]
            
            results.append({
                'claim_id': df.iloc[i]['claim_id'] if 'claim_id' in df.columns else f"claim_{i}",
                'risk_score': score,
                'classification': classification,
                'top_drivers': top_drivers
            })
        
        return results 