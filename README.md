<h1>Мемный бот в телеграм</h1>
<br>
Данный бот является промежуточным этапом к более совершеенной его форме. <br>
В следующем апдейте будет использван json вместо базы данных, чтобы бота можно было легче запустить. 
Если есть комментарии по коду то пишите на почту: yakovishintimofey@gmail.com
Я не волшебник, я только учусь

:blush:
<br>
В этой версии бота тебе нужно будет:
<br>
1. Cоздать .env файл для конфига.
<br>
2. Указать данные сервера в переменных
<br>

````python
db_host = server.username.com
db_user = username
db_password = password
db_db_name = db_name
````
3. Получить токен вк ([см. в документации как это сделать](https://dev.vk.com/api/getting-started))

````python
vk_access_token = 84qw1ewqw1qe5wq1e5wqewq6e51wq6e16wqe16qw
````

4. Получить токен телеграм ([см. в документации как это сделать](https://dev.vk.com/api/getting-started))

````python
tg_access_token = 45454515:gfgdftregfdsgdfgdfgGDFGSDFGSDG
````
<br>
<h3> Устройство базы данных
<br> 