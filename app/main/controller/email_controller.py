from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.main.database import get_db
from app.main.model.models import Student
from app.main.services import email_service
from app.main.schemas import Schemas as schemas

router = APIRouter(prefix="/email",
                   tags=["email"])


@router.post('/send-email/asynchronous')
async def send_email_asynchronous(req: schemas.EmailDao):
    var = {'title': 'Test email', 'content': req.content, 'btn_text': 'Click here',
           'btn_url': 'https://www.google.com'}
    body = schemas.EmailBody(**var)

    await email_service.send_email_async(req.subject,
                                         req.recipient,
                                         body)

    return {'message': 'Email sent successfully'}


@router.post('/send-email/backgroundtasks')
def send_email_backgroundTasks(background_tasks: BackgroundTasks, req: schemas.EmailDao):
    var = {'title': 'Test email', 'content': req.content, 'btn_text': 'Click here',
           'btn_url': 'https://www.google.com'}
    body = schemas.EmailBody(**var)

    email_service.send_email_background(background_tasks,
                                        req.subject,
                                        req.recipient,
                                        body)

    return {'message': 'Email sent successfully'}


@router.post('/to-all')
def send_email_to_all(background_tasks: BackgroundTasks, subject: str, content: str, db: Session = Depends(get_db)):
    var = {'title': 'Hey', 'content': content, 'btn_text': 'Click here',
           'btn_url': 'https://www.google.com'}
    body = schemas.EmailBody(**var)
    recipients = [(student.email, student.first_name) for student in db.query(Student).all()]


    email_service.send_email_to_all(background_tasks,
                                    recipients,
                                    subject,
                                    body)

    return {'message': 'Email sent successfully'}
