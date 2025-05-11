
# WE can also set topic retain policy(delete commited or consumed message from log file after 600000ms) by docker command for all topic but it drawback we need to restart kafka container after add new topic

* The default time for Kafka to delete messages consumed or commited messages is 7 days (168 hours) we can check broker setting log.retention.hours = 168 (7 days) so first we update retention policy and hours in yml file then for topics.
