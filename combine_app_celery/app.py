import os
from flask import Flask, render_template
from flask import url_for
from tasks import celery
from celery.result import AsyncResult
import celery.states as states
import uuid
import time
from tasks import add_task
import socket
env=os.environ
app = Flask(__name__)
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler('log/app.log', maxBytes=1024000*1024000, backupCount=2)
logger.addHandler(handler)
container_id = socket.gethostname()

@app.route('/add/<int:param1>/<int:param2>/<param3>')
def add(param1,param2,param3):
    task = add_task.apply_async(args=[param1, param2], kwargs={}, task_id=param3)
    # add.apply_async()
    # t1 = time.time()
    # task = celery.send_task('mytasks.add', args=[param1, param2], kwargs={}, task_id=str(uuid.uuid4()))
    # a = time.time() - t1
    # print(time.time() - t1)
    logger.info(container_id)
    return "<a href='{url}'>check status of {id} time add to queue </a>".format(id=task.id,
            url=url_for('check_task',id=task.id,_external=True))

@app.route('/check/<string:id>')
def check_task(id):
    res = celery.AsyncResult(id)
    if res.state==states.PENDING:
        return res.state
    else:
        return str(res.result)

