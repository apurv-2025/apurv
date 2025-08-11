"""
Streaming Data Processor
Real-time processing of healthcare claims and denials
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
import redis
from pydantic import BaseModel, Field

from models.database import SessionLocal, Claim, DenialRecord
from features.feature_engineering import FeatureEngineer
from models.denial_predictor import DenialPredictor

logger = logging.getLogger(__name__)

@dataclass
class StreamEvent:
    """Represents a streaming event"""
    event_type: str  # claim_submitted, denial_received, payment_received
    event_id: str
    timestamp: datetime
    data: Dict[str, Any]
    source: str  # edi, api, manual_entry
    priority: int = 1  # 1-10, 10 being highest

class StreamProcessor:
    """Real-time streaming processor for healthcare data"""
    
    def __init__(self, redis_client: redis.Redis, batch_size: int = 100):
        self.redis = redis_client
        self.batch_size = batch_size
        self.feature_engineer = FeatureEngineer()
        self.predictor = DenialPredictor()
        self.event_handlers = self._initialize_event_handlers()
        self.processing_queue = asyncio.Queue()
        self.is_running = False
        
    def _initialize_event_handlers(self) -> Dict[str, Callable]:
        """Initialize handlers for different event types"""
        return {
            "claim_submitted": self._handle_claim_submitted,
            "denial_received": self._handle_denial_received,
            "payment_received": self._handle_payment_received,
            "authorization_requested": self._handle_authorization_requested,
            "authorization_received": self._handle_authorization_received,
            "appeal_submitted": self._handle_appeal_submitted,
            "appeal_decision": self._handle_appeal_decision
        }
    
    async def start_processing(self):
        """Start the streaming processor"""
        logger.info("Starting streaming processor")
        self.is_running = True
        
        # Start background tasks
        tasks = [
            asyncio.create_task(self._process_events()),
            asyncio.create_task(self._process_batches()),
            asyncio.create_task(self._update_features()),
            asyncio.create_task(self._cleanup_old_data())
        ]
        
        try:
            await asyncio.gather(*tasks)
        except Exception as e:
            logger.error(f"Error in streaming processor: {e}")
            self.is_running = False
    
    async def stop_processing(self):
        """Stop the streaming processor"""
        logger.info("Stopping streaming processor")
        self.is_running = False
    
    async def submit_event(self, event: StreamEvent):
        """Submit an event for processing"""
        await self.processing_queue.put(event)
        
        # Also store in Redis for persistence
        event_key = f"event:{event.event_id}"
        event_data = {
            "event_type": event.event_type,
            "event_id": event.event_id,
            "timestamp": event.timestamp.isoformat(),
            "data": event.data,
            "source": event.source,
            "priority": event.priority
        }
        self.redis.setex(event_key, 3600, json.dumps(event_data))  # 1 hour TTL
    
    async def _process_events(self):
        """Process individual events"""
        while self.is_running:
            try:
                # Get event from queue
                event = await asyncio.wait_for(
                    self.processing_queue.get(), timeout=1.0
                )
                
                # Process based on priority
                if event.priority >= 8:
                    # High priority - process immediately
                    await self._process_single_event(event)
                else:
                    # Lower priority - add to batch processing
                    await self._add_to_batch(event)
                
                self.processing_queue.task_done()
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error processing event: {e}")
    
    async def _process_single_event(self, event: StreamEvent):
        """Process a single high-priority event"""
        try:
            handler = self.event_handlers.get(event.event_type)
            if handler:
                await handler(event)
            else:
                logger.warning(f"No handler for event type: {event.event_type}")
                
        except Exception as e:
            logger.error(f"Error processing event {event.event_id}: {e}")
    
    async def _add_to_batch(self, event: StreamEvent):
        """Add event to batch processing queue"""
        batch_key = f"batch:{datetime.utcnow().strftime('%Y%m%d_%H')}"
        
        # Add to Redis list
        event_data = {
            "event_type": event.event_type,
            "event_id": event.event_id,
            "timestamp": event.timestamp.isoformat(),
            "data": event.data,
            "source": event.source,
            "priority": event.priority
        }
        
        self.redis.lpush(batch_key, json.dumps(event_data))
        self.redis.expire(batch_key, 7200)  # 2 hours TTL
    
    async def _process_batches(self):
        """Process batched events"""
        while self.is_running:
            try:
                # Process batches every 5 minutes
                await asyncio.sleep(300)
                
                current_hour = datetime.utcnow().strftime('%Y%m%d_%H')
                batch_key = f"batch:{current_hour}"
                
                # Get all events in batch
                events = []
                while True:
                    event_data = self.redis.rpop(batch_key)
                    if not event_data:
                        break
                    events.append(json.loads(event_data))
                
                if events:
                    await self._process_batch(events)
                    
            except Exception as e:
                logger.error(f"Error processing batches: {e}")
    
    async def _process_batch(self, events: List[Dict[str, Any]]):
        """Process a batch of events"""
        logger.info(f"Processing batch of {len(events)} events")
        
        # Group events by type
        grouped_events = {}
        for event_data in events:
            event_type = event_data["event_type"]
            if event_type not in grouped_events:
                grouped_events[event_type] = []
            grouped_events[event_type].append(event_data)
        
        # Process each group
        for event_type, event_list in grouped_events.items():
            try:
                await self._process_event_group(event_type, event_list)
            except Exception as e:
                logger.error(f"Error processing event group {event_type}: {e}")
    
    async def _process_event_group(self, event_type: str, events: List[Dict[str, Any]]):
        """Process a group of events of the same type"""
        if event_type == "claim_submitted":
            await self._process_claim_batch(events)
        elif event_type == "denial_received":
            await self._process_denial_batch(events)
        elif event_type == "payment_received":
            await self._process_payment_batch(events)
    
    async def _process_claim_batch(self, events: List[Dict[str, Any]]):
        """Process a batch of claim submissions"""
        db = SessionLocal()
        try:
            claims_data = []
            for event in events:
                claim_data = event["data"]
                claims_data.append(claim_data)
            
            # Batch predict denials
            predictions = await self._batch_predict_denials(claims_data)
            
            # Store predictions
            for i, prediction in enumerate(predictions):
                claim_id = claims_data[i]["claim_id"]
                await self._store_prediction_result(claim_id, prediction)
                
        finally:
            db.close()
    
    async def _process_denial_batch(self, events: List[Dict[str, Any]]):
        """Process a batch of denials"""
        db = SessionLocal()
        try:
            for event in events:
                denial_data = event["data"]
                await self._handle_denial_received(StreamEvent(
                    event_type="denial_received",
                    event_id=event["event_id"],
                    timestamp=datetime.fromisoformat(event["timestamp"]),
                    data=denial_data,
                    source=event["source"]
                ))
        finally:
            db.close()
    
    async def _process_payment_batch(self, events: List[Dict[str, Any]]):
        """Process a batch of payments"""
        db = SessionLocal()
        try:
            for event in events:
                payment_data = event["data"]
                await self._handle_payment_received(StreamEvent(
                    event_type="payment_received",
                    event_id=event["event_id"],
                    timestamp=datetime.fromisoformat(event["timestamp"]),
                    data=payment_data,
                    source=event["source"]
                ))
        finally:
            db.close()
    
    async def _handle_claim_submitted(self, event: StreamEvent):
        """Handle claim submission event"""
        logger.info(f"Processing claim submission: {event.event_id}")
        
        claim_data = event.data
        db = SessionLocal()
        
        try:
            # Store claim
            claim = Claim(
                claim_id=claim_data["claim_id"],
                provider_id=claim_data["provider_id"],
                payer_id=claim_data["payer_id"],
                patient_id=claim_data["patient_id"],
                cpt_codes=claim_data["cpt_codes"],
                icd_codes=claim_data["icd_codes"],
                claim_amount=claim_data["claim_amount"],
                service_date=datetime.fromisoformat(claim_data["service_date"]),
                submission_date=event.timestamp,
                patient_age=claim_data["patient_age"],
                patient_gender=claim_data["patient_gender"],
                place_of_service=claim_data["place_of_service"]
            )
            db.add(claim)
            db.commit()
            
            # Predict denial probability
            features = self.feature_engineer.create_features(claim_data)
            prediction = self.predictor.predict(features)
            
            # Store prediction
            await self._store_prediction_result(claim_data["claim_id"], prediction)
            
            # Update real-time metrics
            await self._update_realtime_metrics("claim_submitted", claim_data)
            
        except Exception as e:
            logger.error(f"Error handling claim submission: {e}")
            db.rollback()
        finally:
            db.close()
    
    async def _handle_denial_received(self, event: StreamEvent):
        """Handle denial received event"""
        logger.info(f"Processing denial received: {event.event_id}")
        
        denial_data = event.data
        db = SessionLocal()
        
        try:
            # Store denial record
            denial_record = DenialRecord(
                claim_id=denial_data["claim_id"],
                denial_date=event.timestamp,
                denial_codes=json.dumps(denial_data["denial_codes"]),
                denial_reason_text=denial_data["denial_reason"],
                resolution_status="pending"
            )
            db.add(denial_record)
            db.commit()
            
            # Update claim status
            claim = db.query(Claim).filter(Claim.claim_id == denial_data["claim_id"]).first()
            if claim:
                claim.is_denied = True
                claim.denial_reason = denial_data["denial_reason"]
                db.commit()
            
            # Update real-time metrics
            await self._update_realtime_metrics("denial_received", denial_data)
            
        except Exception as e:
            logger.error(f"Error handling denial received: {e}")
            db.rollback()
        finally:
            db.close()
    
    async def _handle_payment_received(self, event: StreamEvent):
        """Handle payment received event"""
        logger.info(f"Processing payment received: {event.event_id}")
        
        payment_data = event.data
        db = SessionLocal()
        
        try:
            # Update claim status
            claim = db.query(Claim).filter(Claim.claim_id == payment_data["claim_id"]).first()
            if claim:
                claim.is_denied = False
                db.commit()
            
            # Update real-time metrics
            await self._update_realtime_metrics("payment_received", payment_data)
            
        except Exception as e:
            logger.error(f"Error handling payment received: {e}")
            db.rollback()
        finally:
            db.close()
    
    async def _handle_authorization_requested(self, event: StreamEvent):
        """Handle authorization request event"""
        logger.info(f"Processing authorization request: {event.event_id}")
        await self._update_realtime_metrics("authorization_requested", event.data)
    
    async def _handle_authorization_received(self, event: StreamEvent):
        """Handle authorization received event"""
        logger.info(f"Processing authorization received: {event.event_id}")
        await self._update_realtime_metrics("authorization_received", event.data)
    
    async def _handle_appeal_submitted(self, event: StreamEvent):
        """Handle appeal submission event"""
        logger.info(f"Processing appeal submitted: {event.event_id}")
        await self._update_realtime_metrics("appeal_submitted", event.data)
    
    async def _handle_appeal_decision(self, event: StreamEvent):
        """Handle appeal decision event"""
        logger.info(f"Processing appeal decision: {event.event_id}")
        await self._update_realtime_metrics("appeal_decision", event.data)
    
    async def _batch_predict_denials(self, claims_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Batch predict denials for multiple claims"""
        predictions = []
        
        for claim_data in claims_data:
            try:
                features = self.feature_engineer.create_features(claim_data)
                prediction = self.predictor.predict(features)
                predictions.append(prediction)
            except Exception as e:
                logger.error(f"Error predicting for claim {claim_data.get('claim_id')}: {e}")
                predictions.append({"error": str(e)})
        
        return predictions
    
    async def _store_prediction_result(self, claim_id: str, prediction: Dict[str, Any]):
        """Store prediction result"""
        try:
            db = SessionLocal()
            # Store in database or cache
            prediction_key = f"prediction:{claim_id}"
            self.redis.setex(prediction_key, 86400, json.dumps(prediction))  # 24 hours TTL
        except Exception as e:
            logger.error(f"Error storing prediction: {e}")
        finally:
            db.close()
    
    async def _update_realtime_metrics(self, metric_type: str, data: Dict[str, Any]):
        """Update real-time metrics"""
        try:
            # Update counters
            counter_key = f"metrics:{metric_type}:count"
            self.redis.incr(counter_key)
            
            # Update rolling averages
            if "claim_amount" in data:
                amount_key = f"metrics:{metric_type}:amount"
                self.redis.lpush(amount_key, data["claim_amount"])
                self.redis.ltrim(amount_key, 0, 999)  # Keep last 1000 values
            
            # Update time-based metrics
            hour_key = f"metrics:{metric_type}:{datetime.utcnow().strftime('%Y%m%d_%H')}"
            self.redis.incr(hour_key)
            self.redis.expire(hour_key, 7200)  # 2 hours TTL
            
        except Exception as e:
            logger.error(f"Error updating metrics: {e}")
    
    async def _update_features(self):
        """Periodically update cached features"""
        while self.is_running:
            try:
                await asyncio.sleep(3600)  # Every hour
                
                # Update provider features
                await self._update_provider_features()
                
                # Update payer features
                await self._update_payer_features()
                
            except Exception as e:
                logger.error(f"Error updating features: {e}")
    
    async def _update_provider_features(self):
        """Update provider-level features"""
        db = SessionLocal()
        try:
            # Calculate recent denial rates for providers
            # This would query the database and update feature store
            pass
        finally:
            db.close()
    
    async def _update_payer_features(self):
        """Update payer-level features"""
        db = SessionLocal()
        try:
            # Calculate recent denial rates for payers
            # This would query the database and update feature store
            pass
        finally:
            db.close()
    
    async def _cleanup_old_data(self):
        """Clean up old data and metrics"""
        while self.is_running:
            try:
                await asyncio.sleep(86400)  # Every day
                
                # Clean up old events
                cutoff_time = datetime.utcnow() - timedelta(days=7)
                
                # Clean up old metrics
                old_metric_keys = self.redis.keys("metrics:*")
                for key in old_metric_keys:
                    # Check if key is older than 30 days
                    if "2024" in key:  # Simple check for old keys
                        self.redis.delete(key)
                
            except Exception as e:
                logger.error(f"Error cleaning up old data: {e}")
    
    async def get_realtime_metrics(self) -> Dict[str, Any]:
        """Get real-time metrics"""
        try:
            metrics = {}
            
            # Get counts for different event types
            event_types = [
                "claim_submitted", "denial_received", "payment_received",
                "authorization_requested", "authorization_received",
                "appeal_submitted", "appeal_decision"
            ]
            
            for event_type in event_types:
                count_key = f"metrics:{event_type}:count"
                count = self.redis.get(count_key)
                metrics[f"{event_type}_count"] = int(count) if count else 0
            
            # Get current hour metrics
            current_hour = datetime.utcnow().strftime('%Y%m%d_%H')
            for event_type in event_types:
                hour_key = f"metrics:{event_type}:{current_hour}"
                count = self.redis.get(hour_key)
                metrics[f"{event_type}_hourly"] = int(count) if count else 0
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error getting real-time metrics: {e}")
            return {} 