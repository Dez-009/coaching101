"""Natural language query parser service."""
from typing import Dict, Optional
import spacy
import logging

logger = logging.getLogger(__name__)

class NLService:
    def __init__(self):
        # Load spaCy model for English
        self.nlp = spacy.load("en_core_web_sm")

    async def parse_query(self, query: str) -> Dict:
        """Parse natural language query to structured format."""
        logger.info(f"Parsing query: {query}")
        doc = self.nlp(query)
        
        # Extract key components
        target_db = self._detect_database(doc)
        operation = self._detect_operation(doc)
        conditions = self._extract_conditions(doc)

        # Print tokens and their dependencies for debugging
        print("\nToken analysis:")
        for token in doc:
            print(f"{token.text}: pos={token.pos_}, dep={token.dep_}, head={token.head.text}")
        
        return {
            "target_db": target_db,
            "operation": operation,
            "conditions": conditions
        }

    def _detect_database(self, doc) -> str:
        """Detect which database to query based on keywords."""
        keywords = {
            "postgres": ["postgres", "postgresql", "users", "user", "admin"],
            "mongo": ["mongo", "mongodb", "sessions", "logs"],
            "mysql": ["mysql", "sql", "journals", "articles"],
            "elasticsearch": ["elasticsearch", "es", "search", "full-text"]
        }
        
        text = doc.text.lower()
        for db, kws in keywords.items():
            if any(kw in text for kw in kws):
                return db
                
        return "postgres"  # default to postgres if no match

    def _detect_operation(self, doc) -> str:
        """Detect the type of operation (select, insert, update, delete)."""
        text = doc.text.lower()
        
        if any(w in text for w in ["find", "get", "select", "show", "search"]):
            return "select"
        elif any(w in text for w in ["insert", "add", "create"]):
            return "insert"
        elif any(w in text for w in ["update", "modify", "change"]):
            return "update"
        elif any(w in text for w in ["delete", "remove"]):
            return "delete"
            
        return "select"  # default to select if no match

    def _extract_conditions(self, doc) -> Dict:
        """Extract conditions from the query."""
        conditions = {}
        
        text = doc.text.lower()
        for token in doc:
            # Print token info for debugging
            print(f"{token.text}: pos={token.pos_}, dep={token.dep_}, head={token.head.text}")
            
            if token.dep_ == "nsubj" and token.head.pos_ == "VERB":
                # Skip common words like "Find"
                if token.text.lower() not in ["find", "get", "show", "list"]:
                    conditions["subject"] = token.text
            elif token.dep_ == "dobj" and token.head.pos_ == "VERB":
                conditions["object"] = token.text
            elif token.text.lower() == "role":
                # Look for the next word after "role"
                next_token = doc[token.i + 1] if token.i + 1 < len(doc) else None
                if next_token:
                    conditions["role"] = next_token.text.lower()
                
        return conditions
