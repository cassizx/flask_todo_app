import os
from app import app


if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	debug = bool(os.getenv('DEBUG', False))
	app.run(host='0.0.0.0', port=port, debug=debug)