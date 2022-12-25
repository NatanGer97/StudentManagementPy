import os
from typing import List

from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv

from app.main.schemas.Schemas import EmailBody

load_dotenv('.env')


class EmailConfig:
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_FROM = os.getenv('MAIL_FROM')
    MAIL_PORT = (os.getenv('MAIL_PORT'))
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_FROM_NAME = "Admin"


conf = ConnectionConfig(
    MAIL_USERNAME=EmailConfig.MAIL_USERNAME,
    MAIL_PASSWORD=EmailConfig.MAIL_PASSWORD,
    MAIL_FROM=EmailConfig.MAIL_FROM,
    MAIL_PORT=EmailConfig.MAIL_PORT,
    # MAIL_PORT=465 in production
    # MAIL_PORT=587,
    MAIL_SERVER=EmailConfig.MAIL_SERVER,
    MAIL_FROM_NAME=EmailConfig.MAIL_FROM_NAME,
    # in production, comment this line
    MAIL_STARTTLS=True,
    # in production, comment this line
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,

)


async def send_email_async(subject: str, email_to: str, body: EmailBody):
    html = f"""
   <html>
<body style="margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, Helvetica, sans-serif;">
<div style="width: 100%; background: #efefef; border-radius: 10px; padding: 10px;">
    <div style="margin: 0 auto; width: 90%; text-align: center;">
        <h1 style="background-color: rgba(0, 53, 102, 1); padding: 5px 10px; border-radius: 5px; color: white;">{{
            body.title }}</h1>
        <div style="margin: 30px auto; background: white; width: 40%; border-radius: 10px; padding: 50px; text-align: center;">
            <h3 style="margin-bottom: 100px; font-size: 24px;">{body.title}</h3>
            <p style="margin-bottom: 30px;">{body.content}</p>
            <a style="display: block; margin: 0 auto; border: none; background-color: rgba(255, 214, 10, 1); color: white; width: 200px; line-height: 24px; padding: 10px; font-size: 24px; border-radius: 10px; cursor: pointer; text-decoration: none;"
               href="{body.btn_url}"
               target="_blank"
            >
                {body.btn_text}
            </a>
        </div>
    </div>
</div>
</body>
</html>

    """

    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=html,
        subtype='html',
    )

    fm = FastMail(conf)
    await fm.send_message(message)


def send_email_background(background_tasks: BackgroundTasks, subject: str, email_to: str, body: EmailBody):
    html = f"""
       <html>
    <body style="margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, Helvetica, sans-serif;">
    <div style="width: 100%; background: #efefef; border-radius: 10px; padding: 10px;">
        <div style="margin: 0 auto; width: 90%; text-align: center;">
            <h1 style="background-color: rgba(0, 53, 102, 1); padding: 5px 10px; border-radius: 5px; color: white;">Email</h1>
            <div style="margin: 30px auto; background: white; width: 40%; border-radius: 10px; padding: 50px; text-align: center;">
                <h3 style="margin-bottom: 100px; font-size: 24px;">{body.title}</h3>
                <p style="margin-bottom: 30px;">{body.content}</p>
                <a style="display: block; margin: 0 auto; border: none; background-color: rgba(255, 214, 10, 1); color: white; width: 200px; line-height: 24px; padding: 10px; font-size: 24px; border-radius: 10px; cursor: pointer; text-decoration: none;"
                   href="{body.btn_url}"
                   target="_blank"
                >
                    {body.btn_text}
                </a>
            </div>
        </div>
    </div>
    </body>
    </html>

        """

    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=html,
        subtype='html',
    )

    fm = FastMail(conf)
    background_tasks.add_task(
        fm.send_message,
        message)


def send_email_to_all(background_tasks: BackgroundTasks, recipients: list, subject: str,
                      body: EmailBody):

    for recipient in recipients:
        html = f"""
             <html>
          <body style="margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, Helvetica, sans-serif;">
          <div style="width: 100%; background: #efefef; border-radius: 10px; padding: 10px;">
              <div style="margin: 0 auto; width: 90%; text-align: center;">
                  <h1 style="background-color: rgba(0, 53, 102, 1); padding: 5px 10px; border-radius: 5px; color: white;">Email</h1>
                  <div style="margin: 30px auto; background: white; width: 40%; border-radius: 10px; padding: 50px; text-align: center;">
                      <h3 style="margin-bottom: 100px; font-size: 24px;">{body.title + " "  + recipient[1]}</h3>
                      <p style="margin-bottom: 30px;">{body.content}</p>
                      <a style="display: block; margin: 0 auto; border: none; background-color: rgba(255, 214, 10, 1); color: white; width: 200px; line-height: 24px; padding: 10px; font-size: 24px; border-radius: 10px; cursor: pointer; text-decoration: none;"
                         href="{body.btn_url}"
                         target="_blank"
                      >
                          {body.btn_text}
                      </a>
                  </div>
              </div>
          </div>
          </body>
          </html>

              """

        try:
            message = MessageSchema(
                subject=subject,
                recipients=[recipient[0]],
                body=html,
                subtype='html',
            )

            fm = FastMail(conf)
            background_tasks.add_task(
                fm.send_message,
                message)
        except Exception as e:
            print(e)