from cc import app
import os


if __name__ == '__main__':
	app.config.update(SECRET_KEY=os.urandom(24))

	app.run(debug=True,threaded=True,processes=1)