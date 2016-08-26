from bcycle import app


@app.route('/')
def index():
    return "Hello"
