"""
Security utilities for authentication, authorization, and PHI/PII protection.
"""

import re
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from .config import settings


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# PHI/PII patterns for redaction
PHI_PATTERNS = {
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "phone": re.compile(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"),
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
    "credit_card": re.compile(r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b"),
    "date_of_birth": re.compile(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b"),
    "mrn": re.compile(r"\b[Mm][Rr][Nn][-:]?\s*\d+\b"),  # Medical Record Number
}


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Payload data to encode in the token
        expires_delta: Optional expiration time delta

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    return encoded_jwt


def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Decode and verify a JWT access token.

    Args:
        token: JWT token to decode

    Returns:
        Decoded token payload

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def redact_phi(text: str, redaction_char: str = "*") -> str:
    """
    Redact PHI/PII from text based on pattern matching.

    Args:
        text: Input text potentially containing PHI/PII
        redaction_char: Character to use for redaction

    Returns:
        Text with PHI/PII redacted
    """
    if not settings.PHI_REDACTION_ENABLED:
        return text

    redacted_text = text

    for pattern_name, pattern in PHI_PATTERNS.items():
        matches = pattern.findall(redacted_text)
        for match in matches:
            # Replace with redacted placeholder
            placeholder = f"[REDACTED_{pattern_name.upper()}]"
            redacted_text = redacted_text.replace(match, placeholder)

    return redacted_text


def redact_phi_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively redact PHI/PII from dictionary values.

    Args:
        data: Dictionary potentially containing PHI/PII

    Returns:
        Dictionary with PHI/PII redacted
    """
    if not isinstance(data, dict):
        return data

    redacted_data = {}
    for key, value in data.items():
        if isinstance(value, str):
            redacted_data[key] = redact_phi(value)
        elif isinstance(value, dict):
            redacted_data[key] = redact_phi_dict(value)
        elif isinstance(value, list):
            redacted_data[key] = [
                redact_phi(item) if isinstance(item, str) else
                redact_phi_dict(item) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            redacted_data[key] = value

    return redacted_data


def sanitize_sql_input(input_str: str) -> str:
    """
    Sanitize SQL input to prevent SQL injection.
    This is a basic implementation - always use parameterized queries.

    Args:
        input_str: Input string to sanitize

    Returns:
        Sanitized string
    """
    # Remove common SQL injection patterns
    dangerous_patterns = [
        r";\s*DROP\s+TABLE",
        r";\s*DELETE\s+FROM",
        r";\s*UPDATE\s+",
        r"--",
        r"/\*.*\*/",
        r"xp_cmdshell",
        r"exec\s*\(",
    ]

    sanitized = input_str
    for pattern in dangerous_patterns:
        sanitized = re.sub(pattern, "", sanitized, flags=re.IGNORECASE)

    return sanitized


def validate_user_role(user_role: str, required_roles: list) -> bool:
    """
    Validate if user has required role.

    Args:
        user_role: User's role
        required_roles: List of acceptable roles

    Returns:
        True if user has required role
    """
    return user_role in required_roles


# Role definitions
class UserRole:
    """User role constants."""
    ADMIN = "admin"
    CLINICIAN = "clinician"
    PATIENT = "patient"
    STAFF = "staff"

    @classmethod
    def all_roles(cls):
        """Get all available roles."""
        return [cls.ADMIN, cls.CLINICIAN, cls.PATIENT, cls.STAFF]
