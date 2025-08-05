import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings
from app.models.models import User, Organization, Invitation

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.host = settings.email_host
        self.port = settings.email_port
        self.user = settings.email_user
        self.password = settings.email_password

    def _send_email(self, to_email: str, subject: str, body: str) -> bool:
        """Send email helper method"""
        if not self.user or not self.password:
            print("Email credentials not configured")
            return False
            
        try:
            msg = MIMEMultipart()
            msg["From"] = self.user
            msg["To"] = to_email
            msg["Subject"] = subject
            
            msg.attach(MIMEText(body, "html"))
            
            server = smtplib.SMTP(self.host, self.port)
            server.starttls()
            server.login(self.user, self.password)
            server.send_message(msg)
            server.quit()
            
            return True
        except Exception as e:
            print(f"Email sending failed: {e}")
            return False

    def send_verification_email(self, email: str, token: str) -> bool:
        """Send verification email to user"""
        verification_link = f"http://localhost:3000/verify?token={token}"
        body = f"""
        <html>
            <body>
                <h2>Welcome to Agentic Practice</h2>
                <p>Please click the link below to verify your email address:</p>
                <a href="{verification_link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Verify Email</a>
                <p>Or copy and paste this link: {verification_link}</p>
                <p>This link will expire in 24 hours.</p>
            </body>
        </html>
        """
        
        return self._send_email(email, "Verify Your Account", body)

    def send_invitation_email(self, invitation: Invitation, organization: Organization, inviter: User) -> bool:
        """Send invitation email to user"""
        invitation_link = f"http://localhost:3000/invite?token={invitation.token}"
        body = f"""
        <html>
            <body>
                <h2>You're invited to join {organization.name}!</h2>
                <p>{inviter.first_name} {inviter.last_name} has invited you to join their team as a <strong>{invitation.role}</strong>.</p>
                <p>Click the link below to accept the invitation:</p>
                <a href="{invitation_link}" style="background-color: #667eea; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">Accept Invitation</a>
                <p>Or copy and paste this link: {invitation_link}</p>
                <p>This invitation will expire on {invitation.expires_at.strftime('%B %d, %Y')}.</p>
            </body>
        </html>
        """
        
        return self._send_email(invitation.email, f"You're invited to join {organization.name}", body)


    #
    #password_reset
    #
    def send_password_reset_email(self, to_email: str, reset_url: str) -> bool:
        """Send password reset email asynchronously"""
        try:            # HTML email template
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Password Reset</title>
            </head>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 30px;">
                    <h1 style="color: white; margin: 0; font-size: 28px;">Password Reset Request</h1>
                </div>
                
                <div style="background: #f8f9fa; padding: 30px; border-radius: 10px; margin-bottom: 30px;">
                    <p style="font-size: 16px; margin-bottom: 20px;">Hello,</p>
                    <p style="font-size: 16px; margin-bottom: 20px;">
                        You requested a password reset for your account. Click the button below to reset your password:
                    </p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{reset_url}" 
                           style="background: #667eea; color: white; padding: 15px 30px; text-decoration: none; 
                                  border-radius: 8px; font-weight: 600; font-size: 16px; display: inline-block;
                                  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);">
                            Reset Password
                        </a>
                    </div>
                    
                    <p style="font-size: 14px; color: #666; margin-top: 20px;">
                        <strong>This link will expire in 1 hour.</strong>
                    </p>
                    
                    <p style="font-size: 14px; color: #666; margin-top: 20px;">
                        If you didn't request this reset, please ignore this email. Your password will remain unchanged.
                    </p>
                </div>
                
                <div style="text-align: center; color: #666; font-size: 12px;">
                    <p>If the button doesn't work, copy and paste this link into your browser:</p>
                    <p style="word-break: break-all;">{reset_url}</p>
                </div>
            </body>
            </html>
            """
            
            # Plain text fallback
            text_body = f"""
            Password Reset Request
            
            You requested a password reset for your account.
            
            Click this link to reset your password: {reset_url}
            
            This link will expire in 1 hour.
            
            If you didn't request this reset, please ignore this email.
            """
            
            return self._send_email(to_email, "Reset your Password", html_body)
            
            logger.info(f"Password reset email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send password reset email to {to_email}: {str(e)}")
            return False


# Singleton instance
email_service = EmailService()
