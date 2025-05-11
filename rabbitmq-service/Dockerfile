FROM rabbitmq:3-management

ARG RABBITMQ_USER
ARG RABBITMQ_PWD

ENV RABBITMQ_PID_FILE /var/lib/rabbitmq/mnesia/rabbitmq

ADD init.sh /init.sh
RUN chmod +x /init.sh

# Expose ports.
EXPOSE 5672
EXPOSE 15672


# Define default command
CMD ["/init.sh"]

