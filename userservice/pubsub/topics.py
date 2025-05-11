# Format: <publishing_service>.<consumer_service>.<event_name>  
# - `user` → Service publishing the event (User Service)  
# - `events` → Target consumer service (Event Service)  
# - `send_template_email` → Triggered function in the consumer service 

REGISTERED_TOPICS = [
    "user.events.send_template_email",
    "user.events.create_notification",
]