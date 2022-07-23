from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from datetime import datetime

from backend.database import Base


class MonitorInfo(Base):
    __tablename__ = "monitor_info"

    id = Column(Integer, primary_key=True, index=True)
    monitor_date = Column(String(64), unique=True, index=True)
    port_of_loading = Column(String(256), comment="装货港")
    port_of_discharge = Column(String(256), comment="卸货港")
    container_detail = Column(String(1024), comment="线路详情")
    monitor_time = Column(DateTime, comment="监控时间")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
