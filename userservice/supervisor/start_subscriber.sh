# !/bin/sh

# Reading .env file and setting environment variables in system
ENV_FILE="/code/.env"
CMD=${@:2}

while IFS= read -r line;
do
   export $line
done < "$ENV_FILE"

$CMD

echo "Starting subscriber through shell script."
cd /code && python manage.py start_subscriber

