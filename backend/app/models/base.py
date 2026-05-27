"""
Base declarativa de SQLAlchemy
================================
Todas las entidades heredan de aquí.

NOTA DISTRIBUCIÓN FUTURA:
En una arquitectura distribuida, podría haber múltiples Base
para diferentes grupos de tablas que viven en diferentes nodos:
- BaseLocal    → tablas de un nodo específico
- BaseCentral  → tablas compartidas/replicadas
- BasePagos    → tablas del nodo de pagos
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base para todos los modelos SQLAlchemy."""
    pass
