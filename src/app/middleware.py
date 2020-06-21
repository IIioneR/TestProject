import time


class TimingLog:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        t1 = time.time()
        response = self.get_response(request)
        t2 = time.time()
        print(f"TOTAL TIME:{t2 - t1}")
        return response
