from celery import shared_task
from .models import ScrapingJob, ScrapingTask
from .coinmarketcap import CoinMarketCap

@shared_task
def scrape_coin_data(job_id, coin):
    job = ScrapingJob.objects.get(job_id=job_id)
    task = ScrapingTask.objects.create(job=job, coin=coin)
    scraper = CoinMarketCap()
    data = scraper.get_coin_data(coin)
    task.data = data
    task.status = 'COMPLETED' if 'error' not in data else 'FAILED'
    task.save()
