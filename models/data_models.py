# models/data_models.py
"""
Data models for the Job Search System
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class Institution(BaseModel):
    """Model for institutional data"""
    name: str
    type: str  # 'university', 'company', 'startup', 'research_institute', 'government', 'ngo'
    website_url: str
    careers_url: str
    location: Optional[str] = None
    size: Optional[str] = None  # 'small', 'medium', 'large', 'enterprise'
    industry: Optional[str] = None
    interest_match: str  # Which user interest this matches
    description: Optional[str] = None


class InstitutionBase(BaseModel):
    name: str
    description: str
    type: Optional[str]
    interest_match: str  # Which user interest this matches




class UserProfile(BaseModel):
    """Model for user profile data (future use)"""
    name: Optional[str] = None
    interests: List[str] = []
    skills: List[str] = []
    experience_level: Optional[str] = None
    preferred_locations: List[str] = []
    cv_text: Optional[str] = None

class JobPosting(BaseModel):
    """Model for job posting data (future use)"""
    title: str
    company: str
    location: Optional[str] = None
    description: str
    requirements: List[str] = []
    posting_url: str
    posted_date: Optional[datetime] = None
    match_score: Optional[float] = None
    salary_range: Optional[str] = None