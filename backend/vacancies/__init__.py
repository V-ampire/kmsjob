# from rq_scheduler import Scheduler
# from redis import Redis
# import django_rq
# import os
# import django


# # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apiservices.settings")
# # django.setup()

# # scheduler = Scheduler('default', connection=Redis())
# scheduler = django_rq.get_scheduler('default')
# scheduler.cron(
#     "18 * * * *",                # A cron string (e.g. "0 0 * * 0")
#     func='jobparser.tasks.parse',                  # Function to be queued
#     queue_name='default',      # In which queue the job should be put in
# )