from aiohttp import web
from converter import *
import redis
import json

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
        await update_rates()
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

    cache = r.json().get('rates')
   
    if cache:
        try:
            rate = cache[to_currency] / cache[from_currency]
            responce['result'] = convert_currencies(float(rate),amount)
            return web.json_response(responce)
        except Exception as e:
            return web.json_response(
                data={"error": str(e)},
                status=404
            )
    else:
        try:
            cache = await update_rates()
            rate = cache[to_currency] / cache[from_currency]
            responce['result'] = convert_currencies(rate,amount)
            return web.json_response(responce)
        except Exception as e:
            return web.json_response(
                data={"error": str(e)},
                status=404
            )

async def update_rates():
    new_rates = get_all_currencies()
    r = redis.Redis(host='localhost', port=6379,db=0,decode_responses=True)
    r.json().set('rates','$',new_rates)
    return new_rates

app = web.Application()
app.add_routes(routes)

def redis_connecton():
    connection_pool = redis.ConnectionPool(host='localhost', port=6379,db=0,decode_responses=True)
    return redis.StrictRedis(connection_pool=connection_pool)

if __name__ == '__main__':
    web.run_app(app)

