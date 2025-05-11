from settings import get_app
from flask.cli import with_appcontext
# from pubsub import Consumer
from pubsub.factory import PubsubFactory



import os

app = get_app()

@app.cli.command("start_subscriber")
@with_appcontext
def start_subscriber():
    """
    Custom command to start the Kafka consumer
    """
    print("Starting pubsub Consumer...")
    subscriber=PubsubFactory()
    subscriber.start_subscriber()



if __name__ == "__main__":
    subscriber=PubsubFactory()
    subscriber.start_subscriber()
    app.run(debug=True)
