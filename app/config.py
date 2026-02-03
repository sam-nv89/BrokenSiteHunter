"""
Конфигурация приложения BrokenSite Hunter
Загружает переменные окружения и предоставляет централизованный доступ к настройкам
"""
import os
from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field, validator


class Settings(BaseSettings):
    """Настройки приложения с валидацией через Pydantic"""
    
    # ============================================
    # API Keys
    # ============================================
    google_places_api_key: Optional[str] = Field(None, env="GOOGLE_PLACES_API_KEY")
    hunter_io_api_key: Optional[str] = Field(None, env="HUNTER_IO_API_KEY")
    twocaptcha_api_key: Optional[str] = Field(None, env="TWOCAPTCHA_API_KEY")
    
    # ============================================
    # Database
    # ============================================
    database_url: str = Field("sqlite:///./database.db", env="DATABASE_URL")
    
    # ============================================
    # Scraping Settings
    # ============================================
    max_requests_per_minute: int = Field(30, env="MAX_REQUESTS_PER_MINUTE")
    min_delay_seconds: float = Field(2.0, env="MIN_DELAY_SECONDS")
    max_delay_seconds: float = Field(5.0, env="MAX_DELAY_SECONDS")
    user_agent_rotation: bool = Field(True, env="USER_AGENT_ROTATION")
    headless_mode: bool = Field(True, env="HEADLESS_MODE")
    page_load_timeout: int = Field(30, env="PAGE_LOAD_TIMEOUT")
    
    # ============================================
    # Proxy Settings
    # ============================================
    use_proxy: bool = Field(False, env="USE_PROXY")
    proxy_list: Optional[str] = Field(None, env="PROXY_LIST")
    tor_proxy: Optional[str] = Field(None, env="TOR_PROXY")
    
    @validator("proxy_list")
    def parse_proxy_list(cls, v) -> Optional[List[str]]:
        """Парсинг списка прокси из строки"""
        if v:
            return [proxy.strip() for proxy in v.split(",")]
        return None
    
    # ============================================
    # Email Enrichment
    # ============================================
    enable_whois: bool = Field(True, env="ENABLE_WHOIS")
    enable_email_guessing: bool = Field(True, env="ENABLE_EMAIL_GUESSING")
    enable_smtp_verification: bool = Field(False, env="ENABLE_SMTP_VERIFICATION")
    max_email_patterns: int = Field(10, env="MAX_EMAIL_PATTERNS")
    
    # ============================================
    # Technical Audit
    # ============================================
    enable_ssl_check: bool = Field(True, env="ENABLE_SSL_CHECK")
    enable_pagespeed: bool = Field(True, env="ENABLE_PAGESPEED")
    enable_mobile_test: bool = Field(True, env="ENABLE_MOBILE_TEST")
    enable_broken_links_check: bool = Field(False, env="ENABLE_BROKEN_LINKS_CHECK")
    
    # ============================================
    # Export Settings
    # ============================================
    default_export_format: str = Field("csv", env="DEFAULT_EXPORT_FORMAT")
    export_dir: Path = Field(Path("./exports"), env="EXPORT_DIR")
    auto_cleanup_days: int = Field(30, env="AUTO_CLEANUP_DAYS")
    
    @validator("export_dir")
    def create_export_dir(cls, v: Path) -> Path:
        """Создание директории для экспорта, если не существует"""
        v.mkdir(parents=True, exist_ok=True)
        return v
    
    # ============================================
    # Logging & Monitoring
    # ============================================
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_dir: Path = Field(Path("./logs"), env="LOG_DIR")
    telegram_bot_token: Optional[str] = Field(None, env="TELEGRAM_BOT_TOKEN")
    telegram_chat_id: Optional[str] = Field(None, env="TELEGRAM_CHAT_ID")
    
    @validator("log_dir")
    def create_log_dir(cls, v: Path) -> Path:
        """Создание директории для логов, если не существует"""
        v.mkdir(parents=True, exist_ok=True)
        return v
    
    # ============================================
    # Application Settings
    # ============================================
    debug_mode: bool = Field(True, env="DEBUG_MODE")
    streamlit_port: int = Field(8501, env="STREAMLIT_PORT")
    app_name: str = Field("BrokenSite Hunter", env="APP_NAME")
    app_version: str = Field("0.1.0-alpha", env="APP_VERSION")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Синглтон инстанс настроек
settings = Settings()


# ============================================
# Email Patterns для угадывания
# ============================================
EMAIL_PATTERNS = [
    "{first}.{last}@{domain}",
    "{first}{last}@{domain}",
    "{first}@{domain}",
    "{last}@{domain}",
    "{f}{last}@{domain}",
    "{first}{l}@{domain}",
    "info@{domain}",
    "contact@{domain}",
    "admin@{domain}",
    "director@{domain}",
    "manager@{domain}",
]


# ============================================
# User-Agent Pool
# ============================================
USER_AGENTS = [
    # Chrome on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    # Chrome on macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    # Firefox on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    # Safari on macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    # Edge on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
]


# ============================================
# Константы для технического аудита
# ============================================
class AuditThresholds:
    """Пороговые значения для классификации проблем"""
    
    # PageSpeed Scores (0-100)
    PERFORMANCE_GOOD = 90
    PERFORMANCE_NEEDS_IMPROVEMENT = 50
    
    # SSL Certificate
    SSL_EXPIRY_WARNING_DAYS = 30
    
    # Page Load Time (seconds)
    FAST_LOAD = 2.0
    ACCEPTABLE_LOAD = 4.0
    
    # Mobile
    MOBILE_FRIENDLY_REQUIRED = True


# Экспорт всех настроек
__all__ = [
    "settings",
    "Settings",
    "EMAIL_PATTERNS",
    "USER_AGENTS",
    "AuditThresholds",
]
