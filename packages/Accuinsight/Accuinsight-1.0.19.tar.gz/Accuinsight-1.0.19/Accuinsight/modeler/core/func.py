import uuid
import datetime

def get_run_id():
    random_id = str(uuid.uuid4()) 
    random_id = random_id.upper()
    return(random_id)

class get_time(object):
    def now():
        return(datetime.datetime.now())
    def logging_time():
        dt = datetime.datetime.now()
        return(dt.strftime('%Y-%m-%d %H:%M:%S'))
