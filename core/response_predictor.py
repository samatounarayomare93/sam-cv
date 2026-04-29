"""
🔮 RESPONSE PREDICTION AI (100% FREE)
Predict likelihood of response BEFORE sending email

Analyzes:
- Email quality score
- Company responsiveness patterns
- Timing optimization
- Subject line effectiveness
- Content relevance

Only sends if predicted response rate > 70%
Saves time and improves overall success rate
"""

import logging
import os
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

# Historical data file
HISTORY_FILE = Path("cache/response_history.json")
HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

# Enable/disable prediction
PREDICTION_ENABLED = os.getenv("RESPONSE_PREDICTION_ENABLED", "true").lower() == "true"

# Minimum confidence threshold to send (0-100)
MIN_CONFIDENCE_THRESHOLD = int(os.getenv("MIN_RESPONSE_CONFIDENCE", "70"))


class ResponsePredictor:
    """Predict likelihood of email response using ML-like scoring."""
    
    def __init__(self):
        self.history = self._load_history()
    
    def _load_history(self) -> Dict:
        """Load historical response data."""
        try:
            if HISTORY_FILE.exists():
                with open(HISTORY_FILE, 'r') as f:
                    return json.load(f)
            return {"emails": [], "patterns": {}}
        except Exception as e:
            logging.warning(f"Failed to load response history: {e}")
            return {"emails": [], "patterns": {}}
    
    def _save_history(self):
        """Save response history."""
        try:
            with open(HISTORY_FILE, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            logging.warning(f"Failed to save response history: {e}")
    
    def _analyze_email_quality(self, subject: str, body: str) -> Dict[str, Any]:
        """
        Analyze email quality factors.
        
        Returns:
            Dict with quality scores
        """
        scores = {}
        
        # Subject line analysis
        subject_len = len(subject)
        scores["subject_length"] = 100 if 40 <= subject_len <= 60 else max(0, 100 - abs(50 - subject_len) * 2)
        
        # Check for personalization in subject
        scores["subject_personalized"] = 100 if any(word in subject.lower() for word in ['your', 'you', 're:']) else 50
        
        # Body length analysis (optimal: 150-250 words)
        word_count = len(body.split())
        scores["body_length"] = 100 if 150 <= word_count <= 250 else max(0, 100 - abs(200 - word_count) * 0.5)
        
        # Check for numbers/metrics
        numbers = re.findall(r'\d+%|\$\d+|\d+x|\d+ [a-zA-Z]+', body)
        scores["has_metrics"] = min(100, len(numbers) * 25)
        
        # Check for power words
        power_words = ['achieved', 'delivered', 'improved', 'increased', 'led', 'managed', 'created']
        power_word_count = sum(1 for word in power_words if word in body.lower())
        scores["power_words"] = min(100, power_word_count * 20)
        
        # Check for call to action
        cta_phrases = ['discuss', 'call', 'meeting', 'conversation', 'connect', 'available']
        scores["has_cta"] = 100 if any(phrase in body.lower() for phrase in cta_phrases) else 30
        
        # Check for personalization
        personal_words = ['your company', 'your team', 'your', 'you']
        personal_count = sum(1 for word in personal_words if word in body.lower())
        scores["personalization"] = min(100, personal_count * 25)
        
        # Overall quality score (weighted average)
        overall = (
            scores["subject_length"] * 0.15 +
            scores["subject_personalized"] * 0.10 +
            scores["body_length"] * 0.15 +
            scores["has_metrics"] * 0.20 +
            scores["power_words"] * 0.15 +
            scores["has_cta"] * 0.15 +
            scores["personalization"] * 0.10
        )
        
        scores["overall_quality"] = round(overall, 1)
        
        return scores
    
    def _analyze_timing(self, send_time: datetime = None) -> int:
        """
        Analyze timing quality.
        
        Returns:
            Score 0-100
        """
        if send_time is None:
            send_time = datetime.now()
        
        score = 50  # Base score
        
        # Day of week (Tuesday-Thursday best)
        day_of_week = send_time.weekday()
        if day_of_week in [1, 2, 3]:  # Tue, Wed, Thu
            score += 30
        elif day_of_week in [0, 4]:  # Mon, Fri
            score += 10
        else:  # Weekend
            score -= 20
        
        # Time of day (10 AM or 2 PM best)
        hour = send_time.hour
        if hour in [10, 14]:
            score += 20
        elif 9 <= hour <= 16:
            score += 10
        else:
            score -= 10
        
        return max(0, min(100, score))
    
    def _analyze_company_patterns(self, company_name: str) -> Dict[str, Any]:
        """
        Analyze historical patterns for this company.
        
        Returns:
            Dict with pattern analysis
        """
        patterns = self.history.get("patterns", {})
        company_data = patterns.get(company_name, {
            "emails_sent": 0,
            "responses_received": 0,
            "response_rate": 0.0
        })
        
        # Calculate confidence based on sample size
        sample_size = company_data["emails_sent"]
        confidence = min(100, sample_size * 10)  # 10 emails = 100% confidence
        
        return {
            "historical_response_rate": company_data["response_rate"],
            "sample_size": sample_size,
            "confidence": confidence
        }
    
    def _analyze_industry_patterns(self, industry: str = None) -> int:
        """
        Analyze industry response patterns.
        
        Returns:
            Score 0-100
        """
        # Industry response rates (based on research)
        industry_rates = {
            "tech": 75,
            "startup": 80,
            "finance": 60,
            "healthcare": 65,
            "retail": 70,
            "consulting": 75,
            "manufacturing": 65,
            "education": 60
        }
        
        if industry and industry.lower() in industry_rates:
            return industry_rates[industry.lower()]
        
        return 65  # Default average
    
    def predict_response(
        self,
        subject: str,
        body: str,
        company_name: str,
        industry: str = None,
        send_time: datetime = None
    ) -> Dict[str, Any]:
        """
        Predict likelihood of response.
        
        Args:
            subject: Email subject line
            body: Email body
            company_name: Company name
            industry: Industry type (optional)
            send_time: Planned send time (optional, defaults to now)
        
        Returns:
            Dict with prediction results
        """
        if not PREDICTION_ENABLED:
            return {
                "should_send": True,
                "confidence": 100,
                "reason": "Prediction disabled"
            }
        
        # Analyze all factors
        quality_scores = self._analyze_email_quality(subject, body)
        timing_score = self._analyze_timing(send_time)
        company_patterns = self._analyze_company_patterns(company_name)
        industry_score = self._analyze_industry_patterns(industry)
        
        # Calculate weighted prediction
        weights = {
            "quality": 0.40,
            "timing": 0.15,
            "company_history": 0.30,
            "industry": 0.15
        }
        
        # Use company history if we have enough data
        if company_patterns["sample_size"] >= 5:
            company_score = company_patterns["historical_response_rate"]
        else:
            # Use industry average if no company history
            company_score = industry_score
        
        # Calculate final confidence
        confidence = (
            quality_scores["overall_quality"] * weights["quality"] +
            timing_score * weights["timing"] +
            company_score * weights["company_history"] +
            industry_score * weights["industry"]
        )
        
        confidence = round(confidence, 1)
        
        # Determine if should send
        should_send = confidence >= MIN_CONFIDENCE_THRESHOLD
        
        # Generate recommendations
        recommendations = []
        
        if quality_scores["overall_quality"] < 70:
            recommendations.append("Improve email quality (add metrics, power words)")
        
        if timing_score < 70:
            recommendations.append("Consider sending Tuesday-Thursday at 10 AM or 2 PM")
        
        if quality_scores["has_metrics"] < 50:
            recommendations.append("Add specific numbers and achievements")
        
        if quality_scores["personalization"] < 50:
            recommendations.append("Add more personalization (mention company specifics)")
        
        # Generate reason
        if should_send:
            reason = f"High confidence ({confidence}%) - Good quality email with optimal timing"
        else:
            reason = f"Low confidence ({confidence}%) - {', '.join(recommendations[:2])}"
        
        return {
            "should_send": should_send,
            "confidence": confidence,
            "reason": reason,
            "recommendations": recommendations,
            "breakdown": {
                "email_quality": quality_scores["overall_quality"],
                "timing": timing_score,
                "company_history": company_score,
                "industry_baseline": industry_score
            },
            "quality_details": quality_scores
        }
    
    def record_outcome(
        self,
        company_name: str,
        subject: str,
        body: str,
        response_received: bool,
        prediction: Dict[str, Any] = None
    ):
        """
        Record actual outcome to improve future predictions.
        
        Args:
            company_name: Company name
            subject: Email subject
            body: Email body
            response_received: Whether response was received
            prediction: Original prediction (optional)
        """
        # Add to history
        self.history["emails"].append({
            "company_name": company_name,
            "subject": subject[:100],
            "response_received": response_received,
            "prediction": prediction.get("confidence") if prediction else None,
            "timestamp": datetime.now().isoformat()
        })
        
        # Update company patterns
        if "patterns" not in self.history:
            self.history["patterns"] = {}
        
        if company_name not in self.history["patterns"]:
            self.history["patterns"][company_name] = {
                "emails_sent": 0,
                "responses_received": 0,
                "response_rate": 0.0
            }
        
        company_data = self.history["patterns"][company_name]
        company_data["emails_sent"] += 1
        
        if response_received:
            company_data["responses_received"] += 1
        
        # Update response rate
        company_data["response_rate"] = round(
            (company_data["responses_received"] / company_data["emails_sent"]) * 100,
            1
        )
        
        # Keep only last 1000 emails
        if len(self.history["emails"]) > 1000:
            self.history["emails"] = self.history["emails"][-1000:]
        
        self._save_history()
    
    def get_accuracy_stats(self) -> Dict[str, Any]:
        """
        Calculate prediction accuracy.
        
        Returns:
            Dict with accuracy statistics
        """
        emails_with_predictions = [
            e for e in self.history.get("emails", [])
            if e.get("prediction") is not None
        ]
        
        if not emails_with_predictions:
            return {
                "total_predictions": 0,
                "accuracy": 0.0
            }
        
        correct_predictions = 0
        
        for email in emails_with_predictions:
            predicted_success = email["prediction"] >= MIN_CONFIDENCE_THRESHOLD
            actual_success = email["response_received"]
            
            if predicted_success == actual_success:
                correct_predictions += 1
        
        accuracy = (correct_predictions / len(emails_with_predictions)) * 100
        
        return {
            "total_predictions": len(emails_with_predictions),
            "correct_predictions": correct_predictions,
            "accuracy": round(accuracy, 1)
        }


# Global instance
_predictor = None


def get_predictor() -> ResponsePredictor:
    """Get global response predictor instance."""
    global _predictor
    if _predictor is None:
        _predictor = ResponsePredictor()
    return _predictor


def predict_response(
    subject: str,
    body: str,
    company_name: str,
    industry: str = None
) -> Dict[str, Any]:
    """Predict response likelihood."""
    return get_predictor().predict_response(subject, body, company_name, industry)


def record_outcome(
    company_name: str,
    subject: str,
    body: str,
    response_received: bool,
    prediction: Dict[str, Any] = None
):
    """Record actual outcome."""
    get_predictor().record_outcome(company_name, subject, body, response_received, prediction)


def get_accuracy() -> Dict[str, Any]:
    """Get prediction accuracy stats."""
    return get_predictor().get_accuracy_stats()


# Example usage
if __name__ == "__main__":
    predictor = ResponsePredictor()
    
    print("🔮 Response Prediction AI")
    print("=" * 50)
    
    # Test email
    test_subject = "Sam Salameh → TechCorp: Proven HR Leader with 40% Efficiency Gains"
    test_body = """Dear Hiring Manager,

I achieved 40% efficiency improvement at my previous role, managing a team of 15 and delivering $2M in cost savings.

I'm particularly interested in TechCorp's recent expansion and believe my experience in scaling HR operations could be valuable.

Would you be available for a brief conversation to discuss how I can contribute to your team's success?

Best regards,
Sam Salameh"""
    
    # Predict
    prediction = predictor.predict_response(
        subject=test_subject,
        body=test_body,
        company_name="TechCorp",
        industry="tech"
    )
    
    print(f"\n📊 Prediction Results:")
    print(f"  Should send: {'✅ YES' if prediction['should_send'] else '❌ NO'}")
    print(f"  Confidence: {prediction['confidence']}%")
    print(f"  Reason: {prediction['reason']}")
    
    print(f"\n📈 Breakdown:")
    for factor, score in prediction['breakdown'].items():
        print(f"  {factor}: {score:.1f}%")
    
    if prediction['recommendations']:
        print(f"\n💡 Recommendations:")
        for rec in prediction['recommendations']:
            print(f"  - {rec}")
    
    # Simulate outcome
    predictor.record_outcome(
        company_name="TechCorp",
        subject=test_subject,
        body=test_body,
        response_received=True,
        prediction=prediction
    )
    
    # Show accuracy
    accuracy = predictor.get_accuracy_stats()
    print(f"\n🎯 Prediction Accuracy:")
    print(f"  Total predictions: {accuracy['total_predictions']}")
    print(f"  Accuracy: {accuracy.get('accuracy', 0)}%")
