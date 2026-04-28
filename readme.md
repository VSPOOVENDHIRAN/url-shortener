xvenv\Scripts\activate //for activate virtual environment
pip freeze > requirements.txt  //update requirements 
http://127.0.0.1:8000/docs //for endpoint testing
uvicorn app.main:app --reload
docker run -d -p 6379:6379 redis //for run the redis on docker

