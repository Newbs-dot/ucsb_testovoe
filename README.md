# Конвертер валют

## Принцип работы приложения
При первом запросе конвертации, курсы валют с внешнего api кешируются в redis в виде json. При последующих запросах конвертации данные получаем из redis, не отправляя запросов к внешнему api.
POST запросом merge == 0 очищаем базу данных. Merge == 1 обновляет курсы валют, отправляя запрос к внешнему api  

## Запуск
Перед началом работы следует скачать .env файл в корневую директорию приложения по ссылке:
```
https://drive.google.com/drive/folders/1qV9VBRAOP_7Z3uumr1AS_Y4QzhB_ncA5?usp=sharing
```
Далее запускаем докер через compose

## Запрос
Пример запроса GET
```
http://localhost:8080/convert?from=USD&to=RUB&amount=100
```
Пример ответа
```
{"from": "USD", "to": "RUB", "amount": "100", "result": 7736.01}
```
Пример запроса POST
```
curl -XPOST 'http://localhost:8080/database?merge=1'
```
Пример ответа
```
{"success": "Updated rates"}
```

## Доступные валютные тикеры внешнего API с данными о курсах валют
```
Документация api https://freecurrencyapi.com/docs
EUR	Euro
USD	US Dollar
JPY	Japanese Yen
BGN	Bulgarian Lev
CZK	Czech Republic Koruna
DKK	Danish Krone
GBP	British Pound Sterling
HUF	Hungarian Forint
PLN	Polish Zloty
RON	Romanian Leu
SEK	Swedish Krona
CHF	Swiss Franc
ISK	Icelandic Króna
NOK	Norwegian Krone
HRK	Croatian Kuna
RUB	Russian Ruble
TRY	Turkish Lira
AUD	Australian Dollar
BRL	Brazilian Real
CAD	Canadian Dollar
CNY	Chinese Yuan
HKD	Hong Kong Dollar
IDR	Indonesian Rupiah
ILS	Israeli New Sheqel
INR	Indian Rupee
KRW	South Korean Won
MXN	Mexican Peso
MYR	Malaysian Ringgit
NZD	New Zealand Dollar
PHP	Philippine Peso
SGD	Singapore Dollar
THB	Thai Baht
ZAR	South African Rand
```
