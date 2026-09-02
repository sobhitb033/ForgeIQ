import html
import logging
import smtplib
import ssl
from email.message import EmailMessage

from app.core.config import settings


logger = logging.getLogger(__name__)


class EmailService:
    """Reusable SMTP email service for ForgeIQ."""

    @staticmethod
    def send_email(
        to_email: str,
        subject: str,
        text_body: str,
        html_body: str | None = None,
    ) -> None:
        if not settings.MAIL_ENABLED:
            logger.info("Email sending is disabled. Skipping email to %s.", to_email)
            return

        if not settings.MAIL_USERNAME or not settings.MAIL_PASSWORD:
            logger.error("Email sending is enabled but SMTP credentials are missing.")
            return

        sender_email = settings.MAIL_FROM or settings.MAIL_USERNAME
        sender_name = settings.MAIL_FROM_NAME or "ForgeIQ"

        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = f"{sender_name} <{sender_email}>"
        message["To"] = to_email
        message.set_content(text_body)

        if html_body:
            message.add_alternative(html_body, subtype="html")

        try:
            context = ssl.create_default_context()

            with smtplib.SMTP(
                settings.MAIL_SERVER,
                settings.MAIL_PORT,
                timeout=20,
            ) as smtp:
                smtp.ehlo()
                smtp.starttls(context=context)
                smtp.ehlo()
                smtp.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
                smtp.send_message(message)

            logger.info("Email sent successfully to %s.", to_email)

        except (smtplib.SMTPException, OSError) as exc:
            # Registration/password-reset operations should not fail just because
            # the mail server is temporarily unavailable.
            logger.exception("Failed to send email to %s: %s", to_email, exc)

    @staticmethod
    def send_welcome_email(
        to_email: str,
        full_name: str | None = None,
    ) -> None:
        display_name = full_name.strip() if full_name and full_name.strip() else "there"
        safe_name = html.escape(display_name)

        subject = "Welcome to ForgeIQ 🚀"

        text_body = f"""Hi {display_name},

Welcome to ForgeIQ!

Your account has been created successfully. You can now upload software projects and explore their architecture, dependencies, code metrics, health, and engineering recommendations.

We're glad to have you with us.

— Team ForgeIQ
"""

        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #222;">
                <h2>Welcome to ForgeIQ 🚀</h2>
                <p>Hi {safe_name},</p>
                <p>Your ForgeIQ account has been created successfully.</p>
                <p>
                    You can now upload software projects and explore their
                    architecture, dependencies, code metrics, project health,
                    and engineering recommendations.
                </p>
                <p>We're glad to have you with us!</p>
                <p>— Team ForgeIQ</p>
            </body>
        </html>
        """

        EmailService.send_email(
            to_email=to_email,
            subject=subject,
            text_body=text_body,
            html_body=html_body,
        )

    @staticmethod
    def send_password_reset_otp(
        recipient: str,
        full_name: str | None,
        otp: str,
    ):
        """Send a password-reset OTP email."""

        name = full_name or "there"

        subject = "Your ForgeIQ Password Reset OTP"

        text_body = f"""
    Hello {name},

    We received a request to reset your ForgeIQ password.

    Your one-time password (OTP) is:

    {otp}

    This OTP is valid for 3 minutes.

    If you did not request a password reset, you can safely ignore this email.

    Regards,
    ForgeIQ Team
    """

        html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>ForgeIQ Password Reset</title>
    </head>

    <body style="font-family: Arial, sans-serif; background-color: #f4f6f8; padding: 30px;">

        <div style="
            max-width: 520px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 12px;
            text-align: center;
        ">

            <h1 style="margin-bottom: 10px;">
                ForgeIQ
            </h1>

            <h2>
                Password Reset
            </h2>

            <p>
                Hello {name},
            </p>

            <p>
                We received a request to reset your ForgeIQ password.
            </p>

            <p>
                Your one-time password is:
            </p>

            <div style="
                font-size: 32px;
                font-weight: bold;
                letter-spacing: 8px;
                margin: 25px 0;
            ">
                {otp}
            </div>

            <p>
                This OTP is valid for
                <strong>3 minutes</strong>.
            </p>

            <p style="font-size: 14px; color: #666;">
                If you did not request a password reset,
                you can safely ignore this email.
            </p>

            <hr style="margin: 25px 0;">

            <p style="font-size: 13px; color: #888;">
                ForgeIQ Team
            </p>

        </div>

    </body>
    </html>
    """

        EmailService.send_email(
            to_email=recipient,
            subject=subject,
            text_body=text_body,
            html_body=html_body,
        )
