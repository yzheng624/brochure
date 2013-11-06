import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brochure.settings")
from django_cron import CronJobBase, Schedule
from spider.bestbuy import BestBuySpider
from django.core import management


class UpdateCronJob(CronJobBase):
    RUN_EVERY_MINS = 10  # every 10 min

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'brochure.update_cron_job'    # a unique code

    def do(self):
        print 'UpdateCronJob runs~'
        b = BestBuySpider()
        b.run()

if __name__ == '__main__':
    management.call_command('runcrons')