"""
Smart Job Filtering System
AI-powered job matching and filtering
"""

import re
from typing import Dict, List, Any, Tuple

class SmartJobFilter:
    """Intelligent job filtering based on skills, experience, and preferences"""
    
    def __init__(self):
        # Sam's profile
        self.skills = [
            # Core Skills
            "network", "networking", "cisco", "juniper", "aruba",
            "routing", "switching", "firewall", "security",
            "vpn", "wan", "lan", "vlan", "bgp", "ospf", "eigrp",
            
            # Technologies
            "tcp/ip", "dns", "dhcp", "nat", "acl",
            "mpls", "sd-wan", "wireless", "wifi",
            "load balancer", "f5", "nginx",
            
            # Certifications
            "ccna", "ccnp", "ccie", "jncia", "jncip",
            "comptia", "network+", "security+",
            
            # Tools
            "wireshark", "solarwinds", "nagios", "zabbix",
            "ansible", "python", "bash", "powershell",
            
            # Cloud
            "aws", "azure", "gcp", "cloud networking",
            
            # General IT
            "linux", "windows server", "active directory",
            "vmware", "virtualization", "docker",
        ]
        
        self.job_titles = [
            "network engineer", "network administrator",
            "network architect", "network specialist",
            "network analyst", "network technician",
            "senior network engineer", "lead network engineer",
            "network security engineer", "network operations",
            "infrastructure engineer", "systems engineer",
            "it engineer", "it specialist", "it administrator",
            "network consultant", "network manager",
            "noc engineer", "noc analyst",
            "devops engineer", "site reliability engineer",
        ]
        
        self.preferred_locations = [
            "lebanon", "beirut", "dubai", "uae", "abu dhabi",
            "saudi arabia", "riyadh", "jeddah",
            "qatar", "doha", "kuwait", "bahrain",
            "remote", "work from home", "hybrid",
        ]
        
        self.blacklist_keywords = [
            "senior management", "c-level", "ceo", "cto", "cio",
            "director", "vp", "vice president",
            "sales", "marketing", "business development",
            "intern", "internship", "junior" , "entry level",
            "unpaid", "volunteer", "commission only",
        ]
    
    def calculate_match_score(self, job: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
        """
        Calculate match score (0-100) for a job
        Returns: (score, details)
        """
        score = 0
        details = {
            "title_match": 0,
            "skills_match": 0,
            "location_match": 0,
            "description_match": 0,
            "blacklist_hit": False,
            "matched_skills": [],
            "matched_keywords": []
        }
        
        title = job.get("title", "").lower()
        description = job.get("description", "").lower()
        location = job.get("location", "").lower()
        company = job.get("company", "").lower()
        
        full_text = f"{title} {description} {location} {company}"
        
        # 1. Check blacklist (instant disqualification)
        for keyword in self.blacklist_keywords:
            if keyword in full_text:
                details["blacklist_hit"] = True
                return 0, details
        
        # 2. Title match (30 points)
        title_score = 0
        for job_title in self.job_titles:
            if job_title in title:
                title_score = 30
                details["matched_keywords"].append(job_title)
                break
            elif any(word in title for word in job_title.split()):
                title_score = max(title_score, 15)
        
        details["title_match"] = title_score
        score += title_score
        
        # 3. Skills match (40 points)
        matched_skills = []
        for skill in self.skills:
            if skill in full_text:
                matched_skills.append(skill)
        
        skills_score = min(40, len(matched_skills) * 3)
        details["skills_match"] = skills_score
        details["matched_skills"] = matched_skills[:10]  # Top 10
        score += skills_score
        
        # 4. Location match (20 points)
        location_score = 0
        for pref_location in self.preferred_locations:
            if pref_location in location or pref_location in full_text:
                location_score = 20
                break
        
        details["location_match"] = location_score
        score += location_score
        
        # 5. Description quality (10 points)
        if len(description) > 200:
            details["description_match"] = 10
            score += 10
        elif len(description) > 100:
            details["description_match"] = 5
            score += 5
        
        return min(100, score), details
    
    def should_apply(self, job: Dict[str, Any], min_score: int = 40) -> Tuple[bool, int, Dict]:
        """
        Determine if should apply to this job
        Returns: (should_apply, score, details)
        """
        score, details = self.calculate_match_score(job)
        
        # Additional checks
        if details["blacklist_hit"]:
            return False, 0, details
        
        if score < min_score:
            return False, score, details
        
        # Must have at least title match OR 3+ skills
        if details["title_match"] == 0 and len(details["matched_skills"]) < 3:
            return False, score, details
        
        return True, score, details
    
    def prioritize_jobs(self, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Sort jobs by match score (highest first)
        Adds match_score and match_details to each job
        """
        scored_jobs = []
        
        for job in jobs:
            should_apply, score, details = self.should_apply(job)
            if should_apply:
                job["match_score"] = score
                job["match_details"] = details
                job["priority"] = self._calculate_priority(score, details)
                scored_jobs.append(job)
        
        # Sort by priority (high to low)
        scored_jobs.sort(key=lambda x: x["priority"], reverse=True)
        
        return scored_jobs
    
    def _calculate_priority(self, score: int, details: Dict) -> int:
        """Calculate priority (higher = more urgent)"""
        priority = score
        
        # Boost for perfect title match
        if details["title_match"] == 30:
            priority += 20
        
        # Boost for many skills
        if len(details["matched_skills"]) >= 5:
            priority += 15
        
        # Boost for preferred locations
        if details["location_match"] == 20:
            priority += 10
        
        return priority
    
    def get_application_reason(self, job: Dict[str, Any]) -> str:
        """Generate reason for applying (for cover letter)"""
        details = job.get("match_details", {})
        reasons = []
        
        if details.get("title_match", 0) > 0:
            reasons.append("The position aligns perfectly with my network engineering expertise")
        
        matched_skills = details.get("matched_skills", [])
        if len(matched_skills) >= 3:
            top_skills = ", ".join(matched_skills[:3])
            reasons.append(f"I have extensive experience with {top_skills}")
        
        if details.get("location_match", 0) > 0:
            reasons.append("The location is ideal for my career goals")
        
        if not reasons:
            reasons.append("This opportunity matches my professional background")
        
        return ". ".join(reasons) + "."


# Global instance
_filter = None

def get_smart_filter():
    """Get or create filter instance"""
    global _filter
    if _filter is None:
        _filter = SmartJobFilter()
    return _filter


def filter_jobs(jobs: List[Dict[str, Any]], min_score: int = 40) -> List[Dict[str, Any]]:
    """Quick filter helper"""
    smart_filter = get_smart_filter()
    return smart_filter.prioritize_jobs(jobs)


def calculate_match(job: Dict[str, Any]) -> Tuple[int, Dict]:
    """Quick match calculation helper"""
    smart_filter = get_smart_filter()
    return smart_filter.calculate_match_score(job)
