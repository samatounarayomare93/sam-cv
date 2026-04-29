"""
🧪 A/B TESTING SYSTEM (100% FREE)
Continuously optimize email performance through data-driven testing

Test variations:
- Subject lines (short vs long, formal vs casual)
- Email length (concise vs detailed)
- Tone (professional vs friendly)
- Timing (morning vs afternoon)
- Call-to-action (direct vs soft)

Automatically selects winning variations
"""

import logging
import os
import json
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Test configurations
TEST_CONFIGS = {
    "subject_line": {
        "variations": ["short_direct", "long_detailed", "question_based", "value_prop"],
        "enabled": True
    },
    "email_length": {
        "variations": ["concise", "detailed"],
        "enabled": True
    },
    "tone": {
        "variations": ["formal", "friendly", "confident"],
        "enabled": True
    },
    "timing": {
        "variations": ["morning", "afternoon"],
        "enabled": True
    },
    "cta": {
        "variations": ["direct", "soft", "question"],
        "enabled": True
    }
}

# Results tracking file
RESULTS_FILE = Path("cache/ab_test_results.json")
RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)

# Enable/disable A/B testing
AB_TESTING_ENABLED = os.getenv("AB_TESTING_ENABLED", "true").lower() == "true"

# Minimum sample size before declaring winner
MIN_SAMPLE_SIZE = 20


class ABTesting:
    """A/B testing system for email optimization."""
    
    def __init__(self):
        self.results = self._load_results()
    
    def _load_results(self) -> Dict:
        """Load test results from file."""
        try:
            if RESULTS_FILE.exists():
                with open(RESULTS_FILE, 'r') as f:
                    return json.load(f)
            return self._initialize_results()
        except Exception as e:
            logging.warning(f"Failed to load A/B test results: {e}")
            return self._initialize_results()
    
    def _initialize_results(self) -> Dict:
        """Initialize empty results structure."""
        results = {}
        
        for test_name, config in TEST_CONFIGS.items():
            if config["enabled"]:
                results[test_name] = {
                    "variations": {},
                    "winner": None,
                    "confidence": 0.0
                }
                
                for variation in config["variations"]:
                    results[test_name]["variations"][variation] = {
                        "sent": 0,
                        "opened": 0,
                        "responded": 0,
                        "open_rate": 0.0,
                        "response_rate": 0.0
                    }
        
        return results
    
    def _save_results(self):
        """Save test results to file."""
        try:
            with open(RESULTS_FILE, 'w') as f:
                json.dump(self.results, f, indent=2)
        except Exception as e:
            logging.warning(f"Failed to save A/B test results: {e}")
    
    def select_variation(self, test_name: str) -> str:
        """
        Select variation for a test (exploration vs exploitation).
        
        Uses epsilon-greedy strategy:
        - 80% of time: use best performing variation (exploitation)
        - 20% of time: try random variation (exploration)
        
        Args:
            test_name: Name of test (e.g., "subject_line")
        
        Returns:
            Selected variation name
        """
        if not AB_TESTING_ENABLED or test_name not in self.results:
            # Return default variation
            return TEST_CONFIGS[test_name]["variations"][0]
        
        test_data = self.results[test_name]
        
        # Check if we have a clear winner
        if test_data["winner"] and test_data["confidence"] > 0.95:
            # Use winner 90% of time, explore 10%
            if random.random() < 0.9:
                return test_data["winner"]
        
        # Epsilon-greedy: 80% exploit, 20% explore
        if random.random() < 0.8:
            # Exploit: choose best performing variation
            best_variation = None
            best_score = -1
            
            for variation, stats in test_data["variations"].items():
                # Score = response_rate * 2 + open_rate
                score = stats["response_rate"] * 2 + stats["open_rate"]
                
                if score > best_score:
                    best_score = score
                    best_variation = variation
            
            if best_variation:
                return best_variation
        
        # Explore: random variation
        variations = list(test_data["variations"].keys())
        return random.choice(variations)
    
    def record_sent(self, test_name: str, variation: str):
        """
        Record that an email was sent with specific variation.
        
        Args:
            test_name: Name of test
            variation: Variation used
        """
        if not AB_TESTING_ENABLED or test_name not in self.results:
            return
        
        if variation in self.results[test_name]["variations"]:
            self.results[test_name]["variations"][variation]["sent"] += 1
            self._update_rates(test_name, variation)
            self._save_results()
    
    def record_opened(self, test_name: str, variation: str):
        """
        Record that an email was opened.
        
        Args:
            test_name: Name of test
            variation: Variation used
        """
        if not AB_TESTING_ENABLED or test_name not in self.results:
            return
        
        if variation in self.results[test_name]["variations"]:
            self.results[test_name]["variations"][variation]["opened"] += 1
            self._update_rates(test_name, variation)
            self._check_for_winner(test_name)
            self._save_results()
    
    def record_responded(self, test_name: str, variation: str):
        """
        Record that a response was received.
        
        Args:
            test_name: Name of test
            variation: Variation used
        """
        if not AB_TESTING_ENABLED or test_name not in self.results:
            return
        
        if variation in self.results[test_name]["variations"]:
            self.results[test_name]["variations"][variation]["responded"] += 1
            self._update_rates(test_name, variation)
            self._check_for_winner(test_name)
            self._save_results()
    
    def _update_rates(self, test_name: str, variation: str):
        """Update open and response rates for variation."""
        stats = self.results[test_name]["variations"][variation]
        
        if stats["sent"] > 0:
            stats["open_rate"] = round((stats["opened"] / stats["sent"]) * 100, 2)
            stats["response_rate"] = round((stats["responded"] / stats["sent"]) * 100, 2)
    
    def _check_for_winner(self, test_name: str):
        """
        Check if we have a statistically significant winner.
        
        Uses simple confidence calculation based on sample size and difference.
        """
        test_data = self.results[test_name]
        variations = test_data["variations"]
        
        # Need minimum sample size
        total_sent = sum(v["sent"] for v in variations.values())
        if total_sent < MIN_SAMPLE_SIZE:
            return
        
        # Find best performing variation
        best_variation = None
        best_score = -1
        
        for variation, stats in variations.items():
            if stats["sent"] < 5:  # Need at least 5 samples per variation
                continue
            
            # Score = response_rate * 2 + open_rate
            score = stats["response_rate"] * 2 + stats["open_rate"]
            
            if score > best_score:
                best_score = score
                best_variation = variation
        
        if not best_variation:
            return
        
        # Calculate confidence (simplified)
        best_stats = variations[best_variation]
        
        # Compare to second best
        second_best_score = -1
        for variation, stats in variations.items():
            if variation == best_variation or stats["sent"] < 5:
                continue
            
            score = stats["response_rate"] * 2 + stats["open_rate"]
            if score > second_best_score:
                second_best_score = score
        
        if second_best_score < 0:
            confidence = 0.5
        else:
            # Confidence based on difference and sample size
            difference = best_score - second_best_score
            confidence = min(0.99, 0.5 + (difference / 100) + (total_sent / 1000))
        
        test_data["winner"] = best_variation
        test_data["confidence"] = round(confidence, 3)
        
        if confidence > 0.95:
            logging.info(
                f"🏆 WINNER FOUND for {test_name}: {best_variation} "
                f"(confidence: {confidence:.1%})"
            )
    
    def get_test_results(self, test_name: str = None) -> Dict[str, Any]:
        """
        Get test results.
        
        Args:
            test_name: Specific test name, or None for all tests
        
        Returns:
            Test results
        """
        if test_name:
            return self.results.get(test_name, {})
        return self.results
    
    def get_recommendations(self) -> Dict[str, str]:
        """
        Get current recommendations based on test results.
        
        Returns:
            Dict mapping test names to recommended variations
        """
        recommendations = {}
        
        for test_name, test_data in self.results.items():
            if test_data["winner"] and test_data["confidence"] > 0.8:
                recommendations[test_name] = test_data["winner"]
            else:
                # No clear winner yet, recommend best performing
                best_variation = None
                best_score = -1
                
                for variation, stats in test_data["variations"].items():
                    score = stats["response_rate"] * 2 + stats["open_rate"]
                    if score > best_score:
                        best_score = score
                        best_variation = variation
                
                if best_variation:
                    recommendations[test_name] = best_variation
        
        return recommendations
    
    def reset_test(self, test_name: str):
        """Reset a specific test."""
        if test_name in self.results:
            self.results[test_name] = self._initialize_results()[test_name]
            self._save_results()
            logging.info(f"🔄 Reset A/B test: {test_name}")
    
    def reset_all_tests(self):
        """Reset all tests."""
        self.results = self._initialize_results()
        self._save_results()
        logging.info("🔄 Reset all A/B tests")


# Global instance
_ab_testing = None


def get_ab_testing() -> ABTesting:
    """Get global A/B testing instance."""
    global _ab_testing
    if _ab_testing is None:
        _ab_testing = ABTesting()
    return _ab_testing


def select_variation(test_name: str) -> str:
    """Select variation for test."""
    return get_ab_testing().select_variation(test_name)


def record_email_sent(test_name: str, variation: str):
    """Record email sent."""
    get_ab_testing().record_sent(test_name, variation)


def record_email_opened(test_name: str, variation: str):
    """Record email opened."""
    get_ab_testing().record_opened(test_name, variation)


def record_email_responded(test_name: str, variation: str):
    """Record response received."""
    get_ab_testing().record_responded(test_name, variation)


def get_recommendations() -> Dict[str, str]:
    """Get current recommendations."""
    return get_ab_testing().get_recommendations()


# Example usage
if __name__ == "__main__":
    ab = ABTesting()
    
    print("🧪 A/B Testing System")
    print("=" * 50)
    
    # Simulate some tests
    for i in range(50):
        # Select variations
        subject_var = ab.select_variation("subject_line")
        tone_var = ab.select_variation("tone")
        
        # Record sent
        ab.record_sent("subject_line", subject_var)
        ab.record_sent("tone", tone_var)
        
        # Simulate opens (short_direct performs better)
        if subject_var == "short_direct" and random.random() < 0.5:
            ab.record_opened("subject_line", subject_var)
        elif random.random() < 0.3:
            ab.record_opened("subject_line", subject_var)
        
        # Simulate responses
        if random.random() < 0.05:
            ab.record_responded("subject_line", subject_var)
    
    # Show results
    print("\n📊 Test Results:")
    results = ab.get_test_results("subject_line")
    
    for variation, stats in results["variations"].items():
        print(f"\n  {variation}:")
        print(f"    Sent: {stats['sent']}")
        print(f"    Open rate: {stats['open_rate']}%")
        print(f"    Response rate: {stats['response_rate']}%")
    
    if results["winner"]:
        print(f"\n🏆 Winner: {results['winner']} (confidence: {results['confidence']:.1%})")
    
    # Show recommendations
    print("\n💡 Current Recommendations:")
    recommendations = ab.get_recommendations()
    for test, variation in recommendations.items():
        print(f"  {test}: {variation}")
