# task1

@Работает с DB MongoDB  
Создать каталог mkdir rockertdata  
Перейти в каталог cd rockertdata  
Клонировать каталог проекта с github  
git clone URL  
Устанавливаем виртуальное окружение  
python -m venv .venv  
Активировать виртуальное окружение  
source .venv/bin/activate  

Перейти в каталог проекта  
cd rockertdata  
Устанавливаем зависимости  
pip install -r requirements.txt  

Переходим в каталог spiders  
cd spiders  

Редактирем файл settings.py  

Если использовать без докера, то достаточно изменить это  

MONGO_LOGIN = 'your_login'  
MONGO_PASSWORD = 'your_password'  
MONGO_DATABASE = 'your_nameDB'  
MONGO_COLLECTION = 'git_spideraaaa'  

Переходим в следующий каталог проекта  
cd spiders  
Запускаем проект  
scrapy crawl git_spider  
Он попросит ввести Логин профиля, допустим scrapy или MariyaSha  

В зависимости от того проект это или юзер, будут работать разные сценарии.  
У проект url выглядит так https://github.com/orgs/NAMEORG  
У юзеров url выглядит так https://github.com/MariyaSha  




Если использовать mongodb через докер, то нужно  

создать каталог mongo_db_docker находясь в корне проекта  
mkdir mongo_db_docker  
cd mongo_db_docker  

Прописывайте путь к каталогу в зависимости от того, куда вы клонировали проект!  
Если в Documents то так:  
docker run -d -p 2717:27017 -v ~/Documents/spider/mongo_db_docker:/data/db --name mymongo mongo:latest  
Если в другое место, то изменяйте под ваше место клонирования  
Флаг -d запускает в фоновом режиме. Флаг -p для проброса портов.Флаг -v для удаления неиспользуемых томов mongo  
Флаг --name назначает имя новому контейнеру.latest для скачивания последней версии mongo  
Для проверки работы запускаем "mongo localhost:2717" в этом же каталоге mongo_db_docker  
Если все заработало, то отлично, а если нет, то в случае MacOs делаем это  
______________________  
brew tap mongodb/brew  
brew install mongodb-community@4.2  
brew services start mongodb-community@4.2  
_____________________________________  
echo 'export PATH="/usr/local/opt/mongodb-community@4.2/bin:$PATH"' >> ~/.zshrc  
mongod --config /usr/local/etc/mongod.conf   
_____________________________________  
А потом так же запускаем "mongo localhost:2717", проверяем!Если заработало, то выходит из каталога mongo_db_docker  
cd ..  
Переходим cd rocketdata/rocketdata  
Здесь в меняем настройки файла settings.py  
Необходимо закомментировать константу MONGO_URL которая идет для mongodb+srv  
И раскомментировать  
MONGO_URL = "localhost"  
MONGO_PORT = 2717  
Настроить под себя:  
MONGO_DATABASE = 'your_nameDB'  
MONGO_COLLECTION = 'git_spider'  

Переходим в pipelines.py  
Тут так-же, self.conn = pymongo.MongoClient который для докера раскомментировать  
Второй MongoClient, который раскомментирован - закомментировать  


Переходим в каталог spiders  
cd spiders  
Запускаем проект  
scrapy crawl git_spider  
Он попросит ввести Логин профиля, допустим scrapy или MariyaSha  

В зависимости от того проект это или юзер, будут работать разные сценарии.  
У проект url выглядит так https://github.com/orgs/NAMEORG  
У юзеров url выглядит так https://github.com/MariyaSha  

Посмотреть результаты можно подключишься к "mongo localhost:2717"  
Покажет существующие БД:  
show dbs  
Чтобы использовать БД:  
use NAMEDB  
Посмотреть значения:  
Где - git_spider название вашей коллекции которую вы прописали в settings.py  
db.git_spider.find().pretty()  



