Installation
==============================================
```
# 1. Create virtual env

python -m venv /path/to/new/virtual/environment

# 2. Activate the env

source <venv>/bin/activate

# 3.a Clone the repo

git clone https://github.com/Rishi-jha/task_scheduler.git

# 3.b Move to task_scheduler directory

cd task_scheduler 

# 3. Install the requirements

pip install -r requirements.txt

# 4. Migrate the models

python manage.py migrate

# 5. Create Super user

python manage.py createsuperuser

# 6. Create a cron entry for task processor

crontab -e

* * * * * <path to folder>/manage.py run_task_processor

# 7.a Update Celery Broker URL in task_scheduler.task_scheduler.settings.py based on user created in your local rabbitmq-server:

CELERY_BROKER_URL = "amqp://dev:dev@localhost:5672"

# For more info on rabbitmq setup, please visit: https://www.rabbitmq.com/download.html

# 7.b Running celery worker 


python -m celery -A task_scheduler worker -l INFO

# 8. Running server

python manage.py runserver

# 9. Go to http://localhost:8000
```

Design of the Application
==========================================================


The Task scheduler is a simple web application, which allows user to create and schedule tasks and then allow them to view status of the tasks and as well as the executions.


The design principle is simple, contains web server to host the application and serve content, and a few background services to help processing of the tasks

The first background service is a cronjob which runs every minute in order to execute scheduled tasks at their scheduled time.

The execution is triggered by celery tasks asyncronously to not hog a lot of bandwidth.

The application also provides a feature to cancel a task if the task is not completed.
