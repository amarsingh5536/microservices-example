from pubsub.factory import PubsubFactory
publisher = PubsubFactory()


def publish_user_created_welcome_email(user, **kwargs):
    """Publishes an event to send the welcome email."""
    publisher.publish(
        "user.events.send_template_email",
        {
            "recipients":[user.email],
            "subject":"Welcome! Let's Get Started",
            "template_code":"welcome_user_registration",
            "context":{
                "user_id": user.id,
                "full_name": user.get_full_name(),
            }
            
        }
    )

def publish_forgot_password_otp_email(user, otp, **kwargs):
    """Publishes an event to send the OTP email for password reset."""
    publisher.publish(
        "user.events.send_template_email",
        {
            "recipients": [user.email],
            "subject": "Password Reset Request",
            "template_code": "forgot_password_otp",
            "context": {
                "user_id": user.id,
                "full_name": user.get_full_name(),
                "otp_code": otp
            }
        }
    )


def publish_user_welcome_notification(user, **kwargs):
    """Publishes an event to send the password email."""
    publisher.publish(
        "user.events.create_notification",
        {
            "user_id": user.id,
            "actor_id": user.id,
            "actor_name": user.get_full_name(),
            "title": "Welcome Aboard!",
            "message": f"Hi {user.get_full_name()}, welcome! We're excited to have you. \
                            Explore and make the most of your experience.",
            "notification_type": "Info",
        }
    )
