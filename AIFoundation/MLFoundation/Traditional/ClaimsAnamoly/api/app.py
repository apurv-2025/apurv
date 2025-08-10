#!/usr/bin/env python3
"""
Claims Anomaly Detection REST API

This module provides a REST API for the claims anomaly detection system.
"""

import sys
import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.inference import ClaimsInferenceEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global inference engine
inference_engine = None

def load_model():
    """Load the trained model"""
    global inference_engine
    try:
        model_path = "models/claims_anomaly_model.pkl"
        if os.path.exists(model_path):
            inference_engine = ClaimsInferenceEngine(model_path)
            logger.info(f"Model loaded from {model_path}")
            return True
        else:
            logger.error(f"Model file not found: {model_path}")
            return False
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'model_loaded': inference_engine is not None and inference_engine.model.is_trained
    })

@app.route('/api/v1/score', methods=['POST'])
def score_single_claim():
    """Score a single claim"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required fields
        required_fields = [
            'claim_id', 'submission_date', 'provider_id', 'provider_specialty',
            'patient_age', 'patient_gender', 'cpt_code', 'icd_code',
            'units_of_service', 'billed_amount', 'paid_amount',
            'place_of_service', 'prior_authorization'
        ]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {missing_fields}'
            }), 400
        
        # Add default values for optional fields
        data.setdefault('modifier', '')
        data.setdefault('is_anomaly', 0)
        
        # Score the claim
        if inference_engine is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        result = inference_engine.score_single_claim(data)
        
        # Add timestamp
        result['timestamp'] = datetime.now().isoformat()
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error scoring claim: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/score/batch', methods=['POST'])
def score_batch_claims():
    """Score multiple claims"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data or 'claims' not in data:
            return jsonify({'error': 'No claims array provided'}), 400
        
        claims = data['claims']
        
        if not isinstance(claims, list):
            return jsonify({'error': 'Claims must be an array'}), 400
        
        if len(claims) == 0:
            return jsonify({'error': 'Claims array is empty'}), 400
        
        if len(claims) > 1000:
            return jsonify({'error': 'Maximum 1000 claims per batch'}), 400
        
        # Validate each claim
        required_fields = [
            'claim_id', 'submission_date', 'provider_id', 'provider_specialty',
            'patient_age', 'patient_gender', 'cpt_code', 'icd_code',
            'units_of_service', 'billed_amount', 'paid_amount',
            'place_of_service', 'prior_authorization'
        ]
        
        for i, claim in enumerate(claims):
            missing_fields = [field for field in required_fields if field not in claim]
            if missing_fields:
                return jsonify({
                    'error': f'Claim {i}: Missing required fields: {missing_fields}'
                }), 400
            
            # Add default values
            claim.setdefault('modifier', '')
            claim.setdefault('is_anomaly', 0)
        
        # Score the claims
        if inference_engine is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        import pandas as pd
        claims_df = pd.DataFrame(claims)
        results = inference_engine.score_claims_batch(claims_df)
        
        # Convert to list of dictionaries
        results_list = results.to_dict('records')
        
        return jsonify({
            'results': results_list,
            'count': len(results_list),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error scoring batch claims: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/model/info', methods=['GET'])
def get_model_info():
    """Get model information"""
    try:
        if inference_engine is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        info = inference_engine.get_model_info()
        return jsonify(info)
        
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/example', methods=['GET'])
def get_example_claim():
    """Get an example claim structure"""
    example_claim = {
        'claim_id': 'CLM_EXAMPLE_001',
        'submission_date': '2025-08-01',
        'provider_id': 'PROV_00001',
        'provider_specialty': 'Internal Medicine',
        'patient_age': 45,
        'patient_gender': 'M',
        'cpt_code': '99214',
        'icd_code': 'I10',
        'units_of_service': 1,
        'billed_amount': 200.0,
        'paid_amount': 180.0,
        'place_of_service': '11',
        'prior_authorization': 'N',
        'modifier': '',
        'is_anomaly': 0
    }
    
    return jsonify({
        'example_claim': example_claim,
        'description': 'This is an example of the required claim structure for scoring'
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Load model on startup
    if load_model():
        logger.info("API server starting...")
        app.run(host='127.0.0.1', port=8080, debug=True)
    else:
        logger.error("Failed to load model. Exiting.")
        sys.exit(1) 