from backend.config import MarineConfig
from backend.app.cma.crud import MarineMonitorCRUD
from backend.utils.notification import Email


class MonitorService(MarineConfig):
    """
    监控的一些逻辑处理相关的方法
    """

    def __init__(self):
        super(MonitorService, self).__init__()

    def send_monitor_info_email(self, monitor_info_item):
        """
        发送监控邮件
        :param monitor_info_item:
        :return:
        """
        monitor_crud = MarineMonitorCRUD()
        resp = monitor_crud.get_monitor_info_by_item(
            monitor_time=monitor_info_item.monitor_time,
            monitor_type=monitor_info_item.monitor_type,
        )
        if resp:
            print("监控邮件发送过")
            return False
        else:
            print("监控邮件未发送")
            email = Email(
                mail_from=self.config["mail_from"],
                mail_to=self.config["mail_to"],
                mail_key=self.config["mail_key"],
            )
            subject = f"{monitor_info_item.monitor_time} 舱位情况通知"
            content = (
                f"监控到有如下航线情况可以下单，情根据实际情况操作：\n"
                f"<p>类型：{monitor_info_item.monitor_type}</p>"
                f"<p>装货港：{monitor_info_item.port_of_loading}</p>"
                f"<p>卸货港：{monitor_info_item.port_of_discharge}</p>"
                f"<p>线路详情：{monitor_info_item.container_detail}</p>"
            )

            return email.send(subject, content)
