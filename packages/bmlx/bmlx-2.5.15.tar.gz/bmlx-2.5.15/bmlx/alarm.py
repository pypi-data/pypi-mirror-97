import enum
import requests
import json
import logging
import smtplib
import datetime

from typing import Dict, Any, Text, List, Optional
from bmlx.utils.import_utils import import_class_by_path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

EMAIL_ACCOUNT = "bmlx@bigo.sg"
EMAIL_PASSWORD = "bmlx@bigo.sg123A"
BMLX_PROD_ADDR = "http://www.mlp.bigo.inner"
BMLX_DEV_ADDR = "http://bmlx-ci.mlp.bigo.inner"


class Level(enum.Enum):
    INFO = 0
    ERROR = 1
    WARNING = 2


class Alarm(object):
    __slots__ = ["level", "vars", "time"]

    def __init__(self, level: Level, vars: {}):
        self.level = level
        self.time = datetime.datetime.now()
        self.vars = vars.copy()
        assert "message" in vars
        assert "context" in vars
        self.vars["level"] = level


class AlarmTpl(object):
    def generate_run_link(self, env: str, exp_run_id: str):
        return "%s/runs/%s" % (
            BMLX_PROD_ADDR if env == "prod" else BMLX_DEV_ADDR,
            exp_run_id,
        )

    def renderEmail(self, alarm: Alarm) -> MIMEMultipart:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ACCOUNT
        if alarm.level == Level.INFO:
            msg["Subject"] = "BMLX通知"

        else:
            msg["Subject"] = "BMLX报警"

        content = '<a href="{link}">任务链接</a><br/>pipeline名称{pipeline_name}<br/> 信息: {message} '.format(
            message=alarm.vars["message"].replace("\n", "<br/>"),
            pipeline_name="unknown"
            if "pipeline" not in alarm.vars
            else alarm.vars["pipeline"].meta.name,
            link=self.generate_run_link(
                alarm.vars["context"].env, alarm.vars["pipeline_execution"].id
            ),
        )

        msg.attach(MIMEText(content, "html"))
        return msg

    def renderWxwork(self, alarm: Alarm) -> Text:
        if alarm.level == Level.INFO:
            header = '<font color="green">BMLX通知</font>'
        else:
            header = "BMLX报警"
        content = "{header}\n[任务链接]( {link} )\npipeline:{pipeline_name}\n{message}".format(
            header=header,
            message=alarm.vars["message"],
            pipeline_name="unknown"
            if "pipeline" not in alarm.vars
            else alarm.vars["pipeline"].meta.name,
            link=self.generate_run_link(
                alarm.vars["context"].env, alarm.vars["pipeline_execution"].id
            ),
        )

        return content


class ConsoleEmitter(object):
    def send(self, receivers, content):
        print(content)


class WXWorkEmitter(object):
    def send(self, alarm, alarm_render: AlarmTpl, receivers: List[Text]):
        for receiver in receivers:
            try:
                content = alarm_render.renderWxwork(alarm)
                resp = requests.post(
                    receiver["url"],
                    headers={"Content-Type": "application/json"},
                    data=json.dumps(
                        {
                            "msgtype": "text",
                            "text": {
                                "content": content,
                                "mentioned_list": receiver.get(
                                    "mentioned_list", []
                                ),
                                "mentioned_mobile_list": receiver.get(
                                    "mentioned_mobile_list", []
                                ),
                            },
                        }
                    ),
                )
                resp.raise_for_status()
            except Exception as e:
                logging.exception(
                    "request %s error, exception: %s" % receiver, e
                )
                raise


class EmailEmitter(object):
    def send(self, alarm, alarm_render: AlarmTpl, receivers: List[Text]):
        try:
            s = smtplib.SMTP(host="mail.bigo.sg", timeout=3)
            s.ehlo()
            s.starttls()
            s.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        except smtplib.SMTPException as e:
            logging.exception("connect to mail server error")
            raise (e)

        for receiver in receivers:
            try:
                msg = alarm_render.renderEmail(alarm)
                msg["To"] = receiver
                s.send_message(msg)
            except smtplib.SMTPException as e:
                logging.exception("send mail error")
                raise (e)


class Receipt(object):
    class Type(enum.Enum):
        WXWORK = 0  # 企业微信报警
        EMAIL = 1  # 邮箱报警
        CONSOLE = 2  # 打印到日志

    EMITTERS = {
        Type.WXWORK: WXWorkEmitter(),
        Type.EMAIL: EmailEmitter(),
        Type.CONSOLE: ConsoleEmitter(),
    }

    def __init__(self, receipt_type: Type, receivers: List[Text]):
        self.receipt_type = receipt_type
        self.receivers = receivers
        self._emitters = self.EMITTERS.copy()

    @property
    def emitters(self):
        return self._emitters

    @emitters.setter
    def emitters(self, emitter_types: List[Type]):
        self._emitters.clear()
        for emitter_type in emitter_types:
            assert emitter_type in self.EMITTERS
            self._emitters[emitter_type] = self.EMITTERS[emitter_type]
        logging.info("enables open emitters %s" % self._emitters.keys())

    def emit(self, alarm, alert_render):
        emitter = self.emitters.get(self.receipt_type)
        if not emitter:
            logging.warning(
                "skip to emit alarm for receipt type %s", self.receipt_type
            )
            return
        emitter.send(alarm, alert_render, self.receivers)


class Notification(object):
    def __init__(self, level: Level, receipts: List[Receipt.Type]):
        self.level = level
        self.receipts = receipts


class AlarmManager(object):
    def __init__(
        self,
        receipts: Dict[Text, Receipt],
        notifications: Dict[Level, Notification],
        alarm_tpl: AlarmTpl,
    ):
        self.receipts = receipts
        self.notifications = notifications
        self.alarm_render = alarm_tpl()

    def emit_alarms(self, alarms: List[Alarm]):
        for alarm in alarms:
            if alarm.level in self.notifications:
                for receipt in self.notifications[alarm.level].receipts:
                    receipt.emit(alarm, self.alarm_render)

    # 启用的通知器，比如本地模式不启动微信报警和邮件报警
    def limit_receipt_types(self, receipt_types: List[Receipt.Type]):
        for t, receipt in self.receipts.items():
            receipt.emitters = receipt_types

    @classmethod
    def load_from_config(cls, project, config):
        if config["render"].exists():
            cls = import_class_by_path(config["render"].as_str())
            if not issubclass(cls, AlarmTpl):
                raise RuntimeError(
                    "class '%s' must be subclass of bmlx.alarm.AlarmTpl"
                )
        else:
            alarm_tpl = AlarmTpl

        receipts = {}

        for receipt_conf in config["receipts"]:
            receipt_type_str = receipt_conf["type"].as_str()
            if receipt_type_str == "mail":
                receipt_type = Receipt.Type.EMAIL
            elif receipt_type_str == "wxwork":
                receipt_type = Receipt.Type.WXWORK
            elif receipt_type_str == "console":
                receipt_type = Receipt.Type.CONSOLE
            else:
                raise RuntimeError(
                    "unexpect receipt type %s" % receipt_conf["type"].as_str()
                )

            if receipt_type in receipts:
                raise RuntimeError(
                    "Duplicated receipt config '%s'" % receipt_type
                )

            receivers = []
            for receiver_conf in receipt_conf["receivers"]:
                if receipt_type == Receipt.Type.WXWORK:
                    obj = {}
                    if not receiver_conf["url"].exists():
                        raise RuntimeError("wxwork url not exists")
                    obj["url"] = receiver_conf["url"].as_str()
                    if receiver_conf["mentioned_list"].exists():
                        obj["mentioned_list"] = receiver_conf[
                            "mentioned_list"
                        ].as_str_seq()
                    if receiver_conf["mentioned_mobile_list"].exists():
                        obj["mentioned_mobile_list"] = receiver_conf[
                            "mentioned_mobile_list"
                        ].as_str_seq()
                    receivers.append(obj)
                else:
                    receivers.append(receiver_conf.as_str())
            receipts[receipt_type_str] = Receipt(receipt_type, receivers)

        notifications = {}
        for notification_conf in config["notifications"]:
            if notification_conf["level"].as_str() == "info":
                notify_level = Level.INFO
            elif notification_conf["level"].as_str() == "warning":
                notify_level = Level.WARNING
            elif notification_conf["level"].as_str() == "error":
                notify_level = Level.ERROR
            else:
                raise RuntimeError(
                    "unknown notification level '%s'"
                    % notification_conf["level"].as_str()
                )

            if notify_level in notifications:
                raise RuntimeError(
                    "duplicated notificiation level found %s" % notify_level
                )

            receipt_refs = []
            for receipt_conf in notification_conf["receipts"]:
                if receipt_conf.as_str() not in receipts:
                    raise RuntimeError(
                        "unknown receipt '%s'" % (receipt_conf.as_str())
                    )

                receipt_refs.append(receipts[receipt_conf.as_str()])

            notifications[notify_level] = Notification(
                notify_level, receipt_refs
            )
        return AlarmManager(
            receipts=receipts, notifications=notifications, alarm_tpl=alarm_tpl
        )
