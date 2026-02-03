"""
Database models для BrokenSite Hunter
Определяет структуру таблиц через SQLAlchemy ORM
"""
from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, 
    DateTime, Text, ARRAY, ForeignKey, create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from app.config import settings

# Base class для всех моделей
Base = declarative_base()


class Company(Base):
    """Модель компании (бизнеса)"""
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True, index=True)
    country = Column(String(100), nullable=True)
    category = Column(String(100), nullable=True, index=True)
    phone = Column(String(50), nullable=True)
    website = Column(String(255), nullable=True)
    rating = Column(Float, nullable=True)
    reviews_count = Column(Integer, nullable=True)
    
    # Google Maps specific
    place_id = Column(String(255), unique=True, nullable=True)
    google_maps_url = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    contacts = relationship("Contact", back_populates="company", cascade="all, delete-orphan")
    audits = relationship("Audit", back_populates="company", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}', city='{self.city}')>"
    
    def to_dict(self):
        """Конвертация в словарь для экспорта"""
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'country': self.country,
            'category': self.category,
            'phone': self.phone,
            'website': self.website,
            'rating': self.rating,
            'reviews_count': self.reviews_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class Contact(Base):
    """Модель контактных данных компании"""
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    
    # Email enrichment
    email = Column(String(255), nullable=True, index=True)
    email_source = Column(String(50), nullable=True)  # 'website', 'whois', 'guessed', 'hunter'
    verified = Column(Boolean, default=False)
    
    # Social media
    social_linkedin = Column(String(255), nullable=True)
    social_facebook = Column(String(255), nullable=True)
    social_instagram = Column(String(255), nullable=True)
    social_twitter = Column(String(255), nullable=True)
    
    # Contact person (если найден)
    contact_name = Column(String(255), nullable=True)
    contact_title = Column(String(100), nullable=True)  # CEO, Manager, etc.
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="contacts")
    
    def __repr__(self):
        return f"<Contact(id={self.id}, email='{self.email}', source='{self.email_source}')>"
    
    def to_dict(self):
        return {
            'email': self.email,
            'email_source': self.email_source,
            'verified': self.verified,
            'contact_name': self.contact_name,
            'contact_title': self.contact_title,
            'social_linkedin': self.social_linkedin,
            'social_facebook': self.social_facebook,
        }


class Audit(Base):
    """Модель технического аудита сайта"""
    __tablename__ = "audits"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    
    # SSL Check
    ssl_valid = Column(Boolean, nullable=True)
    ssl_expires_at = Column(DateTime, nullable=True)
    ssl_issuer = Column(String(255), nullable=True)
    ssl_error = Column(Text, nullable=True)
    
    # PageSpeed (Lighthouse)
    pagespeed_score = Column(Integer, nullable=True)  # 0-100
    fcp_ms = Column(Integer, nullable=True)  # First Contentful Paint (milliseconds)
    lcp_ms = Column(Integer, nullable=True)  # Largest Contentful Paint
    ttfb_ms = Column(Integer, nullable=True)  # Time To First Byte
    
    # Mobile
    mobile_friendly = Column(Boolean, nullable=True)
    
    # Issues found
    # Для PostgreSQL используем ARRAY, для SQLite будет JSON
    issues_found = Column(Text, nullable=True)  # JSON array of issues
    
    # Metadata
    audit_date = Column(DateTime, default=datetime.utcnow)
    audit_duration_seconds = Column(Float, nullable=True)
    
    # Relationships
    company = relationship("Company", back_populates="audits")
    
    def __repr__(self):
        return f"<Audit(id={self.id}, company_id={self.company_id}, score={self.pagespeed_score})>"
    
    def to_dict(self):
        return {
            'ssl_valid': self.ssl_valid,
            'ssl_expires_at': self.ssl_expires_at.isoformat() if self.ssl_expires_at else None,
            'pagespeed_score': self.pagespeed_score,
            'fcp_ms': self.fcp_ms,
            'lcp_ms': self.lcp_ms,
            'mobile_friendly': self.mobile_friendly,
            'issues_found': self.issues_found,
            'audit_date': self.audit_date.isoformat() if self.audit_date else None,
        }
    
    @property
    def has_issues(self) -> bool:
        """Проверка наличия критических проблем"""
        return (
            not self.ssl_valid or
            (self.pagespeed_score and self.pagespeed_score < 50) or
            not self.mobile_friendly
        )


# ============================================
# Database Engine & Session
# ============================================

def get_engine():
    """Создание database engine"""
    return create_engine(
        settings.database_url,
        echo=settings.debug_mode,  # SQL logging в debug режиме
        pool_pre_ping=True,  # Проверка соединения перед использованием
    )


def get_session():
    """Создание database session"""
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


def init_db():
    """Инициализация базы данных (создание таблиц)"""
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully")


def drop_db():
    """Удаление всех таблиц (осторожно!)"""
    engine = get_engine()
    Base.metadata.drop_all(bind=engine)
    print("⚠️ Database dropped")


# Экспорт
__all__ = [
    "Base",
    "Company",
    "Contact",
    "Audit",
    "get_engine",
    "get_session",
    "init_db",
    "drop_db",
]
