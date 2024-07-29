from flask import Flask, request, jsonify
from celery import Celery
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from websitecrawl.spiders.lapollo import LapolloSpider
from extractors import extractor_manager
from redis import Redis

# Test Redis connection
try:
    redis_client = Redis(host='localhost', port=6379, db=0)
    redis_client.ping()
    print("Successfully connected to Redis")
except Exception as e:
    print(f"Failed to connect to Redis: {e}")

app = Flask(__name__)

celery = Celery('app', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@app.route('/crawl', methods=['POST'])
def start_crawl():
    data = request.json
    domain = data.get('domain')
    search_types = data.get('search_types', [])
    if not domain:
        return jsonify({"error": "Domain is required"}), 400
    for search_type in search_types:
        try:
            extractor_manager.get_extractor(search_type)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
    task = crawl_task.delay(domain, search_types)
    return jsonify({"task_id": task.id}), 202

@celery.task(name='app.crawl_task')
def crawl_task(domain, search_types):
    process = CrawlerProcess(get_project_settings())
    process.crawl(LapolloSpider, domain=domain, search_types=search_types)
    process.start()
    return f"Crawl completed for {domain}"

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Test successful"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
