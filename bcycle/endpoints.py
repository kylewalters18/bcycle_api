from flask import jsonify

from bcycle import app


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'endpoint does not exist'}), 404
