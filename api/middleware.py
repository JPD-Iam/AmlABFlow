from prometheus_client import Counter,Histogram,Gauge,generate_latest

REQUEST_COUNT=Counter(
    'django_http_requests_total','Total number of HTTP requests',['method','endpoint','status_code']
)

REQUEST_LATENCY=Histogram(
    'django_http_request_duration_seconds','Duration of HTTP requests in seconds',['method','endpoint']
)

REQUEST_IN_PROGRESS=Gauge(
    'django_http_requests_in_progress','Number of HTTP requests in progress',['method','endpoint']
)

class PrometheusMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response

    def __call__(self,request):
        method=request.method
        endpoint=request.path

        REQUEST_IN_PROGRESS.labels(method,endpoint).inc()
        with REQUEST_LATENCY.labels(method, endpoint).time():
            response = self.get_response(request)
        REQUEST_IN_PROGRESS.labels(method, endpoint).dec()

        REQUEST_COUNT.labels(method, endpoint, response.status_code).inc()
        return response

    @staticmethod
    def metrics_view(request):
        from django.http import HttpResponse
        return HttpResponse(generate_latest(), content_type='text/plain')