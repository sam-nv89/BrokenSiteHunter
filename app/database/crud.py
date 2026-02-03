"""CRUD операции для работы с базой данных"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.database.models import Company, Contact, Audit


# ============================================
# Company CRUD
# ============================================

def create_company(db: Session, company_data: Dict[str, Any]) -> Company:
    """Создание новой компании"""
    company = Company(**company_data)
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def get_company_by_id(db: Session, company_id: int) -> Optional[Company]:
    """Получение компании по ID"""
    return db.query(Company).filter(Company.id == company_id).first()


def get_company_by_place_id(db: Session, place_id: str) -> Optional[Company]:
    """Получение компании по Google Place ID (для избежания дубликатов)"""
    return db.query(Company).filter(Company.place_id == place_id).first()


def get_companies_by_filters(
    db: Session,
    city: Optional[str] = None,
    country: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
) -> List[Company]:
    """Получение компаний с фильтрами"""
    query = db.query(Company)
    
    if city:
        query = query.filter(Company.city == city)
    if country:
        query = query.filter(Company.country == country)
    if category:
        query = query.filter(Company.category == category)
    
    return query.offset(offset).limit(limit).all()


def update_company(db: Session, company_id: int, update_data: Dict[str, Any]) -> Optional[Company]:
    """Обновление данных компании"""
    company = get_company_by_id(db, company_id)
    if company:
        for key, value in update_data.items():
            setattr(company, key, value)
        db.commit()
        db.refresh(company)
    return company


# ============================================
# Contact CRUD
# ============================================

def create_contact(db: Session, company_id: int, contact_data: Dict[str, Any]) -> Contact:
    """Создание контакта для компании"""
    contact = Contact(company_id=company_id, **contact_data)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


def get_contact_by_company(db: Session, company_id: int) -> Optional[Contact]:
    """Получение контакта компании (обычно один контакт на компанию)"""
    return db.query(Contact).filter(Contact.company_id == company_id).first()


def update_contact(db: Session, contact_id: int, update_data: Dict[str, Any]) -> Optional[Contact]:
    """Обновление контакта"""
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        for key, value in update_data.items():
            setattr(contact, key, value)
        db.commit()
        db.refresh(contact)
    return contact


# ============================================
# Audit CRUD
# ============================================

def create_audit(db: Session, company_id: int, audit_data: Dict[str, Any]) -> Audit:
    """Создание аудита для компании"""
    audit = Audit(company_id=company_id, **audit_data)
    db.add(audit)
    db.commit()
    db.refresh(audit)
    return audit


def get_latest_audit(db: Session, company_id: int) -> Optional[Audit]:
    """Получение последнего аудита компании"""
    return db.query(Audit)\
        .filter(Audit.company_id == company_id)\
        .order_by(Audit.audit_date.desc())\
        .first()


def get_companies_with_issues(db: Session, limit: int = 100) -> List[Company]:
    """Получение компаний с техническими проблемами"""
    # Companies с проблемами: SSL невалидный, низкий PageSpeed, не mobile-friendly
    return db.query(Company).join(Audit).filter(
        or_(
            Audit.ssl_valid == False,
            Audit.pagespeed_score < 50,
            Audit.mobile_friendly == False
        )
    ).limit(limit).all()


# ============================================
# Combined Queries (для экспорта)
# ============================================

def get_enriched_leads(
    db: Session,
    city: Optional[str] = None,
    category: Optional[str] = None,
    with_email_only: bool = False,
    with_issues_only: bool = False,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """
    Получение полностью обогащенных лидов с JOIN всех таблиц
    Возвращает список словарей готовых для CSV экспорта
    """
    query = db.query(Company).join(Contact, isouter=True).join(Audit, isouter=True)
    
    # Фильтры
    if city:
        query = query.filter(Company.city == city)
    if category:
        query = query.filter(Company.category == category)
    if with_email_only:
        query = query.filter(Contact.email.isnot(None))
    if with_issues_only:
        query = query.filter(
            or_(
                Audit.ssl_valid == False,
                Audit.pagespeed_score < 50,
                Audit.mobile_friendly == False
            )
        )
    
    companies = query.limit(limit).all()
    
    # Формирование результата
    results = []
    for company in companies:
        contact = company.contacts[0] if company.contacts else None
        audit = company.audits[-1] if company.audits else None  # Latest audit
        
        lead = {
            # Company info
            'name': company.name,
            'address': company.address,
            'city': company.city,
            'country': company.country,
            'category': company.category,
            'phone': company.phone,
            'website': company.website,
            'rating': company.rating,
            'reviews_count': company.reviews_count,
            
            # Contact info
            'email': contact.email if contact else None,
            'email_source': contact.email_source if contact else None,
            'contact_name': contact.contact_name if contact else None,
            'linkedin': contact.social_linkedin if contact else None,
            
            # Audit info
            'ssl_valid': audit.ssl_valid if audit else None,
            'ssl_expires_at': audit.ssl_expires_at if audit else None,
            'pagespeed_score': audit.pagespeed_score if audit else None,
            'mobile_friendly': audit.mobile_friendly if audit else None,
            'issues_summary': audit.issues_found if audit else None,
        }
        results.append(lead)
    
    return results


# Экспорт
__all__ = [
    "create_company",
    "get_company_by_id",
    "get_company_by_place_id",
    "get_companies_by_filters",
    "update_company",
    "create_contact",
    "get_contact_by_company",
    "update_contact",
    "create_audit",
    "get_latest_audit",
    "get_companies_with_issues",
    "get_enriched_leads",
]
