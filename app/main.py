from aiohttp import web
from converter import *
import redis
import json
#from aiohttp_swagger import *

routes = web.RouteTableDef()

# host - redis-stack
@routes.post('/database')
async def merge_handler(request):
    r = redis.Redis(host='localhost', port=6379,db=0,decode_responses=True) # async
    try:
        flag = request.rel_url.query['merge']
        assert (flag == '0' or flag=='1') 
    except:
        return web.json_response(
            data={"error": "Bad request"},
            status=404
        )
    
    if request.rel_url.query['merge'] == '0':
        r.flushdb()
        return web.json_response(
            data={"success": "Deleted cache in db"},
            status=200
        )
    elif request.rel_url.query['merge'] == '1':
        update_rates()
        return web.json_response(
            data={"success": "Updated rates"},
            status=200
        )
        
    

@routes.get('/convert')
async def convert_handler(request):
    try:
        from_currency = request.rel_url.query['from']
        to_currency = request.rel_url.query['to']
        amount = request.rel_url.query['amount']
    except:
        return web.json_response(
            data={"error": "Bad request"},
            status=404
        )

    responce = {'from':from_currency,'to':to_currency,'amount':amount}
    r = redis.Redis(host='localhost', port=6379,db=0,decode_responses=True) # async

    cache = r.hget('rates',f"{from_currency}:{to_currency}")
    
    if cache:
        try:
            responce['result'] = convert_currencies(float(cache),amount)
            return web.json_response(responce)
        except Exception as e:
            return web.json_response(
                data={"error": str(e)},
                status=404
            )
    else:
        try:
            rate = cache_rate(from_currency,to_currency)
            responce['result'] = convert_currencies(rate,amount)
            return web.json_response(responce)
        except Exception as e:
            return web.json_response(
                data={"error": str(e)},
                status=404
            )
    
def cache_rate(from_currency:str,to_currency:str):
    r = redis.Redis(host='localhost', port=6379,db=0,decode_responses=True)
    rate = get_currency_rate(from_currency,to_currency)
    r.hset('rates',f"{from_currency}:{to_currency}",rate)
    r.hset('rates',f"{to_currency}:{from_currency}",1/rate) #та же валютная пара, но обратно 
    return rate
    

#add flush at start
def update_rates():
    new_rates = get_all_currencies()
    r = redis.Redis(host='localhost', port=6379,db=0,decode_responses=True)
    current_rates = r.hgetall('rates')

    for pair in current_rates:
        p = pair.split(':')
        base_currency = new_rates[p[1]]
        to_currency = new_rates[p[0]]

        r.hset('rates',pair,base_currency/to_currency)

app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    #setup_swagger(app, swagger_url="/doc", ui_version=3,swagger_from_file='./templates/swagger.yaml')
    web.run_app(app)

