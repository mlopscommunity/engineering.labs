# Front end application
Simple flask app to get predictions from the torchserve server

## Starting the application
If your torchserve server is running at `http://104.198.209.50:8080`, run:
```bash
docker build -t news_classification . && docker run -p 5000:5000 -e FLASK_APP=app.py -e SERVE_URI="http://104.198.209.50:8080" news_classification
```
The application is now running at http://localhost:5000

For local development, pass `-e FLASK_ENV=development`
### .env file
Instead of passing env variables to docker run, you can create a .env file containing any env variables you need
```bash
FLASK_APP=app.py
SERVE_URI="http://104.198.209.50:8080"
```