from django.db import models


class TodoList(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "todo_list"

def fun_raw_sql_query(**kwargs):
    title = kwargs.get('title')
    if title:
        result = TodoList.objects.raw('SELECT * FROM todo_list WHERE title = %s', [title])
    else:
        result = TodoList.objects.raw('SELECT * FROM todo_list')
    return result
