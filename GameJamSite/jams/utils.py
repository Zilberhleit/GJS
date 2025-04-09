from datetime import datetime, timedelta
import random

def rand_date():
    """ Функция генерирующая случайную дату в некотором промежутке """
    start = datetime.now()
    end = start + timedelta(days=3)
    return start + (end - start) * random.random()