import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brochure.settings")
from django_cron import CronJobBase, Schedule
from spider.bestbuy import BestBuySpider
from spider.homedepot import HomeDepotSpider
from spider.msstore import MSStoreSpider
from spider.radioshack import RadioShackSpider
from spider.staples import StaplesSpider
from django.core import management


class UpdateCronJob(CronJobBase):
    RUN_EVERY_MINS = 1  # every 10 min

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'brochure.update_cron_job'    # a unique code

    def do(self):
        print 'UpdateCronJob runs~'
        b = BestBuySpider()
        b.run()
        h = HomeDepotSpider()
        h.run()
        m = MSStoreSpider()
        m.run()
        r = RadioShackSpider()
        r.run()
        s = StaplesSpider()
        s.run()
        print 'UpdateCronJob finished~'

if __name__ == '__main__':
    management.call_command('runcrons')