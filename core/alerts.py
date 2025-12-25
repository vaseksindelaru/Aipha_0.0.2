"""
Alerts System - Notifica eventos críticos del sistema Aipha.
Soporta logging por defecto y es extensible a Telegram/Email.
"""
import logging
from datetime import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class AlertsSystem:
    """Gestiona las notificaciones y alertas del sistema."""
    
    def __init__(self, memory_manager=None):
        self.memory = memory_manager
        logger.info("AlertsSystem inicializado")

    def notify(self, level: str, title: str, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        """
        Envía una notificación.
        
        Args:
            level: "INFO", "WARNING", "CRITICAL"
            title: Título de la alerta
            message: Cuerpo del mensaje
            details: Datos adicionales
        """
        timestamp = datetime.now().isoformat()
        
        # Formatear para log
        log_msg = f"[{level}] {title}: {message}"
        if details:
            log_msg += f" | Details: {details}"
            
        if level == "CRITICAL":
            logger.error(f"🚨 ALERT: {log_msg}")
        elif level == "WARNING":
            logger.warning(f"⚠️  ALERT: {log_msg}")
        else:
            logger.info(f"ℹ️  ALERT: {log_msg}")
            
        # Registrar en memoria si está disponible
        if self.memory:
            # Soporte para ContextSentinel (add_action)
            if hasattr(self.memory, "add_action"):
                self.memory.add_action(
                    agent="AlertsSystem",
                    action_type="NOTIFICATION_SENT",
                    details={
                        "level": level,
                        "title": title,
                        "message": message,
                        "extra": details
                    }
                )
            # Soporte para MemoryManager (record_action) - Legacy
            elif hasattr(self.memory, "record_action"):
                self.memory.record_action(
                    agent="AlertsSystem",
                    component="System",
                    action="notification_sent",
                    details={
                        "level": level,
                        "title": title,
                        "message": message,
                        "extra": details
                    },
                    status="success"
                )

    def critical(self, title: str, message: str, details: Optional[Dict[str, Any]] = None):
        self.notify("CRITICAL", title, message, details)

    def warning(self, title: str, message: str, details: Optional[Dict[str, Any]] = None):
        self.notify("WARNING", title, message, details)

    def info(self, title: str, message: str, details: Optional[Dict[str, Any]] = None):
        self.notify("INFO", title, message, details)
