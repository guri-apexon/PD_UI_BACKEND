import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.utilities.config import settings
from app.models.pd_user_protocols import PD_User_Protocols
from app.models.pd_protocol_alert import ProtocolAlert
from app.models.pd_user import User
from sqlalchemy import and_
import logging

logger = logging.getLogger(settings.LOGGER_NAME)


def send_mail(from_mail:str,  subject: str, to_mail: str, html_body_part:str):
    try:
        message = MIMEMultipart("alternative")
        message['From'] = from_mail
        # message['To'] = to_mail
        message['To'] = "mouneshwara.sugappa@iqvia.com" # hardcoded email address to verify 
        message['Subject'] = subject
        part = MIMEText(html_body_part, "html")
        message.attach(part)
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.sendmail(from_mail, to_mail, message.as_string())
            server.quit()
        logger.info(f"mail sent sucess")
    except Exception as ex:
        logger.exception(f"Exception occured at send mail function {from_mail}, {to_mail}, {subject}")
        return {"sent":False}

    return {"sent":True}


def qc_complete_mail(db, doc_id):
    """
    send email once qc approved and update email sent time and sent flag in protocol alert table 
    :param db: DB instance
    :param doc_id: document id
    """
    try:
        from_mail = settings.FROM_EMAIL
        row_data = db.query(ProtocolAlert.id,ProtocolAlert.protocol,
                                            ProtocolAlert.aidocId,
                                            PD_User_Protocols.userId,
                                            User.username,
                                            User.email).join(PD_User_Protocols, and_(ProtocolAlert.emailSentFlag == False,
                                                                                    ProtocolAlert.aidocId == doc_id,
                                                                                    ProtocolAlert.id == PD_User_Protocols.id)).join(
                User, User.username.in_(('q' + PD_User_Protocols.userId, 'u' + PD_User_Protocols.userId,
                                        PD_User_Protocols.userId))).all()
        for row in row_data:
            to_mail = row.email
            username = " ".join(row.email.strip("@iqvia.com").split("."))
            doc_link = f"http://{doc_id}" # need to change URL according to UI
            protocol_number = row.protocol
            indication = ""
            doc_status = ""
            pd_activity = ""
            qc_activity = ""
            subject = f"Protocol Number: {protocol_number}, Status: {qc_activity}, QCProcess Completed."


            html_body = f"""
                <!DOCTYPE html>
                <html>
                    <body>
                        Dear {username}, <br /><br />
                        Your Protocol has been digitized and the QC Process has been completed. Please view your document
                        <a href="{doc_link}">here</a>. <br /><br />

                        <u>Protocol Details</u>
                        <ul>
                            <li>{protocol_number}</li>
                            <li>{indication}</li>
                            <li>{doc_status}</li>
                            <li>{pd_activity}</li>
                            <li>{qc_activity}</li>
                        </ul><br />

                        You can update your communication preferences in the Protocol Digitization Portal.<br /><br /><br />

                        ********************** IMPORTANT--PLEASE READ ************************<br />
                        This electronic message, including its attachments, is CONFIDENTIAL and may contain PROPRIETARY or LEGALLY
                        PRIVILEGED or PROTECTED information and is intended for the authorized recipient of the sender. 
                        If you are not the intended recipient, you are herebynotified that any use, disclosure, copying, or distribution 
                        of this message or any of the information included in it is unauthorized and strictly prohibited. If you have 
                        received this message in error, please immediately notify the sender by reply e-mail and permanently delete this 
                        message and its attachments, along with any copies thereof, from all locations received (e.g., computer, mobile device, etc.). 
                        To the extent permitted by law, we may monitor electronic communications for the purposes of ensuring compliance with our legal
                        and regulatory obligations and internal policies. We may also collect email traffic headers for analyzing patterns
                        of network traffic and managing client relationships. For further information see: <a
                            href="https://www.iqvia.com/about-us/privacy/privacy-policy">https://www.iqvia.com/about-us/privacy/privacy-policy</a>
                        <br />Thank you<br />
                        ************************************************************************
                    </body>
                </html>
            """
            send_mail(from_mail, subject, to_mail, html_body)
            logger.info(f"qc complete mail sent success for doc_id {doc_id}")
            time_ = datetime.datetime.utcnow()
            db.query(ProtocolAlert).filter(ProtocolAlert.id == row.id, ProtocolAlert.protocol == row.protocol, ProtocolAlert.aidocId == row.aidocId).update({ProtocolAlert.emailSentFlag: True,
            ProtocolAlert.timeUpdated : time_, ProtocolAlert.emailSentTime : time_})
            db.commit()
            logger.info(f"Qc complete mail sent information added to db protocol id in protocol table {row.id}")
    except Exception as ex:
        logger.exception(f"exception occurend qc complete mail send for doc_id {doc_id}")
        return False
    return True