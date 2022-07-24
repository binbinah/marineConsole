from sqlalchemy import Boolean, Column, Integer, String, DateTime
from datetime import datetime

from backend.database import Base


class MonitorInfo(Base):
    """监控结果记录表"""

    __tablename__ = "monitor_info"

    id = Column(Integer, primary_key=True, index=True)
    port_of_loading = Column(String(256), comment="装货港")
    port_of_discharge = Column(String(256), comment="卸货港")
    container_detail = Column(String(1024), comment="线路详情")
    monitor_time = Column(DateTime, comment="监控时间")
    monitor_type = Column(String(256), comment="类型，「could: 可以下单」或者「waiting: 等待开仓」")
    email_status = Column(Boolean, comment="邮件发送状态,1:已发送，0:未发送")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
