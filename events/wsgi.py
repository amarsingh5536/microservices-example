from settings import get_app
import os

app = get_app()
if __name__ == "__main__":
    app.run(debug=True)
