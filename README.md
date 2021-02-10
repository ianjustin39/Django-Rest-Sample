# Django-Rest-Sample

## 建立 Django Project
安裝 Django
```text
pipenv install django
```

建立 Django Project
```text
django-admin startproject django_rest_sample
```

執行 Django
```text
python manage.py runserver
```

即可啟動 Django


**可以把django_rest_sample/djang_resto_sample改成django_rest_sample/main比較好辨識。**

## 設定 Django Rest Framework

安裝 Django Rest Framework
```text
pipenv install djangorestframework
```

在 main/setting.py 內的 INSTALLED_APPS 新增：
```python
INSTALLED_APPS = (
    # 略
    'rest_framework',
    # 略
)
```

## 建立 Django App
通常依照功能建立一個app，例如：建立一個Todo List的app
```text
python manage.py startapp todoList
```
執行之後會出現todoList的資料夾。接著要將建立的app加入main/setting內INSTALLED_APPS中：
```text
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'todoList' // 新增這行
]
```


### 設定 Models
Django Model 在定義資料庫的結構（schema），並透過 Django 指令創建資料庫、資料表及欄位。
優點：轉換資料庫相當方便

到main/setting.py內設定資料庫，python預設是SQLite。
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',         # 資料庫引擎
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),   # 資料庫名稱
    }
}
```

到todoList/model.py內宣告一個class，並定義屬性。Django 會依據這個建立資料表，以及資料表裡的欄位設定：
```python
from django.db import models


class TodoList(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "todo_list"

```
接著來同步資料庫：
```
python manage.py makemigrations
---
Migrations for 'todoList':
  todoList/migrations/0001_initial.py
    - Create model TodoList
```
```
python manage.py migrate
---
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, todoList
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
  Applying todoList.0001_initial... OK

```
makemigrations ： 會幚你建立一個檔案，去記錄你更新了哪些東西。
migrate ： 根據 makemigrations 建立的檔案，去更新你的 DATABASE 。

建立完成後可以使用SQLiteBrowser觀看DB，會發現多了一個todo_list的table
