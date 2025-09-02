"""
NLP Service - Text processing, Named Entity Recognition, and summarization.
"""

import asyncio
from typing import Dict, Any, List, Optional
import spacy
import nltk
from textblob import TextBlob
import re

from app.core.config import settings
from app.core.logging import get_logger


class NLPService:
    """Service for Natural Language Processing tasks."""
    
    def __init__(self):
        self.logger = get_logger("nlp_service")
        self.nlp = None
        self._initialize_nlp()
    
    def _initialize_nlp(self):
        """Initialize NLP models."""
        try:
            # Initialize spaCy model
            try:
                self.nlp = spacy.load(settings.SPACY_MODEL)
            except OSError:
                self.logger.warning(f"spaCy model {settings.SPACY_MODEL} not found. Using basic NLP.")
                self.nlp = None
            
            # Download NLTK data if needed
            try:
                nltk.data.find('tokenizers/punkt')
            except LookupError:
                nltk.download('punkt')
            
            try:
                nltk.data.find('corpora/stopwords')
            except LookupError:
                nltk.download('stopwords')
            
            self.logger.info("NLP service initialized")
            
        except Exception as e:
            self.logger.error(f"Error initializing NLP service: {e}")
    
    async def extract_property_features(self, text: str) -> List[str]:
        """Extract property features from text description."""
        try:
            if not text:
                return []
            
            features = []
            
            # Use spaCy for NER if available
            if self.nlp:
                doc = self.nlp(text)
                
                # Extract entities
                for ent in doc.ents:
                    if ent.label_ in ["QUANTITY", "CARDINAL", "ORG", "FAC"]:
                        features.append(f"{ent.text} ({ent.label_})")
                
                # Extract noun phrases
                for chunk in doc.noun_chunks:
                    if any(keyword in chunk.text.lower() for keyword in ["room", "bedroom", "bathroom", "kitchen", "garage"]):
                        features.append(chunk.text)
            
            # Fallback to regex patterns
            if not features:
                features = self._extract_features_regex(text)
            
            return features[:20]  # Limit to 20 features
            
        except Exception as e:
            self.logger.error(f"Error extracting property features: {e}")
            return []
    
    def _extract_features_regex(self, text: str) -> List[str]:
        """Extract features using regex patterns."""
        features = []
        
        # Property features patterns
        patterns = {
            "bedrooms": r"(\d+)\s*(?:bedroom|bed|br)",
            "bathrooms": r"(\d+(?:\.\d+)?)\s*(?:bathroom|bath|ba)",
            "square_feet": r"(\d+)\s*(?:sq\s*ft|square\s*feet|sf)",
            "acres": r"(\d+(?:\.\d+)?)\s*acres?",
            "stories": r"(\d+)\s*(?:story|stories|floor)",
            "garage": r"(\d+)\s*(?:car\s*)?garage",
            "pool": r"(pool|swimming\s*pool)",
            "fireplace": r"(fireplace|fire\s*place)",
            "hardwood": r"(hardwood|hard\s*wood)",
            "granite": r"(granite|countertop)",
            "stainless": r"(stainless\s*steel|stainless)",
            "updated": r"(updated|renovated|remodeled|modern)",
            "new": r"(new|recently\s*built|newly\s*constructed)"
        }
        
        for feature_type, pattern in patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if feature_type in ["bedrooms", "bathrooms", "square_feet", "acres", "stories", "garage"]:
                    features.append(f"{match} {feature_type}")
                else:
                    features.append(match)
        
        return features
    
    async def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities from text."""
        try:
            entities = {
                "locations": [],
                "organizations": [],
                "dates": [],
                "numbers": [],
                "money": []
            }
            
            if not text:
                return entities
            
            # Use spaCy for NER if available
            if self.nlp:
                doc = self.nlp(text)
                
                for ent in doc.ents:
                    if ent.label_ == "GPE" or ent.label_ == "LOC":
                        entities["locations"].append(ent.text)
                    elif ent.label_ == "ORG":
                        entities["organizations"].append(ent.text)
                    elif ent.label_ == "DATE":
                        entities["dates"].append(ent.text)
                    elif ent.label_ == "CARDINAL":
                        entities["numbers"].append(ent.text)
                    elif ent.label_ == "MONEY":
                        entities["money"].append(ent.text)
            
            # Fallback to regex patterns
            if not any(entities.values()):
                entities = self._extract_entities_regex(text)
            
            return entities
            
        except Exception as e:
            self.logger.error(f"Error extracting entities: {e}")
            return {"locations": [], "organizations": [], "dates": [], "numbers": [], "money": []}
    
    def _extract_entities_regex(self, text: str) -> Dict[str, List[str]]:
        """Extract entities using regex patterns."""
        entities = {
            "locations": [],
            "organizations": [],
            "dates": [],
            "numbers": [],
            "money": []
        }
        
        # Money patterns
        money_pattern = r'\$\d+(?:,\d{3})*(?:\.\d{2})?'
        entities["money"] = re.findall(money_pattern, text)
        
        # Number patterns
        number_pattern = r'\d+(?:\.\d+)?'
        entities["numbers"] = re.findall(number_pattern, text)
        
        # Date patterns
        date_pattern = r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}'
        entities["dates"] = re.findall(date_pattern, text)
        
        return entities
    
    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text."""
        try:
            if not text:
                return {"sentiment": "neutral", "score": 0.0, "confidence": 0.0}
            
            # Use TextBlob for sentiment analysis
            blob = TextBlob(text)
            sentiment_score = blob.sentiment.polarity
            subjectivity_score = blob.sentiment.subjectivity
            
            # Determine sentiment
            if sentiment_score > 0.1:
                sentiment = "positive"
            elif sentiment_score < -0.1:
                sentiment = "negative"
            else:
                sentiment = "neutral"
            
            return {
                "sentiment": sentiment,
                "score": sentiment_score,
                "subjectivity": subjectivity_score,
                "confidence": abs(sentiment_score)
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing sentiment: {e}")
            return {"sentiment": "neutral", "score": 0.0, "confidence": 0.0}
    
    async def summarize_text(self, text: str, max_sentences: int = 3) -> str:
        """Summarize text using extractive summarization."""
        try:
            if not text:
                return ""
            
            # Use spaCy for summarization if available
            if self.nlp:
                doc = self.nlp(text)
                
                # Simple extractive summarization based on sentence length and position
                sentences = list(doc.sents)
                
                if len(sentences) <= max_sentences:
                    return text
                
                # Score sentences based on length and position
                sentence_scores = []
                for i, sent in enumerate(sentences):
                    score = len(sent) * 0.1  # Length factor
                    score += (1.0 - i / len(sentences)) * 0.5  # Position factor (first sentences get higher scores)
                    sentence_scores.append((score, sent.text))
                
                # Sort by score and take top sentences
                sentence_scores.sort(reverse=True)
                top_sentences = [sent for score, sent in sentence_scores[:max_sentences]]
                
                # Sort back to original order
                sentence_indices = [sentences.index(sent) for sent in top_sentences]
                sentence_indices.sort()
                
                summary = " ".join([sentences[i].text for i in sentence_indices])
                return summary
            
            # Fallback to simple summarization
            else:
                return self._simple_summarize(text, max_sentences)
            
        except Exception as e:
            self.logger.error(f"Error summarizing text: {e}")
            return text[:200] + "..." if len(text) > 200 else text
    
    def _simple_summarize(self, text: str, max_sentences: int) -> str:
        """Simple extractive summarization."""
        try:
            # Split into sentences
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            if len(sentences) <= max_sentences:
                return text
            
            # Take first few sentences
            summary_sentences = sentences[:max_sentences]
            return ". ".join(summary_sentences) + "."
            
        except Exception as e:
            self.logger.error(f"Error in simple summarization: {e}")
            return text[:200] + "..." if len(text) > 200 else text
    
    async def extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """Extract keywords from text."""
        try:
            if not text:
                return []
            
            keywords = []
            
            # Use spaCy for keyword extraction if available
            if self.nlp:
                doc = self.nlp(text)
                
                # Extract nouns, adjectives, and proper nouns
                for token in doc:
                    if (token.pos_ in ["NOUN", "PROPN", "ADJ"] and 
                        not token.is_stop and 
                        len(token.text) > 2):
                        keywords.append(token.text.lower())
            
            # Fallback to simple keyword extraction
            else:
                keywords = self._extract_keywords_simple(text)
            
            # Remove duplicates and limit
            unique_keywords = list(set(keywords))
            return unique_keywords[:max_keywords]
            
        except Exception as e:
            self.logger.error(f"Error extracting keywords: {e}")
            return []
    
    def _extract_keywords_simple(self, text: str) -> List[str]:
        """Simple keyword extraction using regex."""
        try:
            # Remove punctuation and convert to lowercase
            text_clean = re.sub(r'[^\w\s]', '', text.lower())
            
            # Split into words
            words = text_clean.split()
            
            # Filter out common stop words
            stop_words = {
                'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'
            }
            
            keywords = [word for word in words if word not in stop_words and len(word) > 2]
            
            return keywords
            
        except Exception as e:
            self.logger.error(f"Error in simple keyword extraction: {e}")
            return []
    
    async def classify_property_type(self, text: str) -> str:
        """Classify property type from description."""
        try:
            if not text:
                return "unknown"
            
            text_lower = text.lower()
            
            # Property type patterns
            patterns = {
                "house": ["house", "home", "single family", "detached"],
                "condo": ["condo", "condominium", "apartment", "unit"],
                "townhouse": ["townhouse", "town home", "row house"],
                "duplex": ["duplex", "multi-family", "two family"],
                "land": ["land", "lot", "acre", "plot"],
                "commercial": ["commercial", "office", "retail", "industrial"]
            }
            
            for prop_type, keywords in patterns.items():
                if any(keyword in text_lower for keyword in keywords):
                    return prop_type
            
            return "house"  # Default to house
            
        except Exception as e:
            self.logger.error(f"Error classifying property type: {e}")
            return "unknown"
    
    async def extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract contact information from text."""
        try:
            contact_info = {
                "phone": "",
                "email": "",
                "website": ""
            }
            
            if not text:
                return contact_info
            
            # Phone number pattern
            phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
            phone_matches = re.findall(phone_pattern, text)
            if phone_matches:
                contact_info["phone"] = phone_matches[0]
            
            # Email pattern
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            email_matches = re.findall(email_pattern, text)
            if email_matches:
                contact_info["email"] = email_matches[0]
            
            # Website pattern
            website_pattern = r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?'
            website_matches = re.findall(website_pattern, text)
            if website_matches:
                contact_info["website"] = website_matches[0]
            
            return contact_info
            
        except Exception as e:
            self.logger.error(f"Error extracting contact info: {e}")
            return {"phone": "", "email": "", "website": ""}
