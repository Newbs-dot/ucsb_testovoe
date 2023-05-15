from aiohttp import web
from converter import *
import redis.asyncio as redis
import asyncio


routes = web.RouteTableDef()


@routes.post('/database')
async def merge_handler(request):
    try:
        flag = request.rel_url.query['merge']
        assert (flag == '0' or flag == '1')
    except:
        return web.json_response(
            data={"error": "Bad request"},
            status=404
        )
    async with request.app['redis'] as redis_connection:
        if request.rel_url.query['merge'] == '0':
            await redis_connection.flushdb()
            return web.json_response(
                data={"success": "Deleted cache in db"},
                status=200
            )
        elif request.rel_url.query['merge'] == '1':
            await update_rates(redis_connection)
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

    responce = {'from': from_currency, 'to': to_currency, 'amount': amount}

    async with request.app['redis'] as redis_connection:
        cache = await redis_connection.json().get('rates')
        if cache:
            try:
                rate = cache[to_currency] / cache[from_currency]
                responce['result'] = await convert_currencies(float(rate), amount)
                return web.json_response(responce)
            except Exception as e:
                return web.json_response(
                    data={"error": str(e)},
                    status=404
                )
        else:
            try:
                cache = await update_rates(redis_connection)
                rate = cache[to_currency] / cache[from_currency]
                responce['result'] = await convert_currencies(rate, amount)
                return web.json_response(responce)
            except Exception as e:
                return web.json_response(
                    data={"error": str(e)},
                    status=404
                )


async def update_rates(redis_connection):
    new_rates = await get_all_currencies()
    await redis_connection.json().set('rates', '$', new_rates)
    return new_rates


async def init_app():
    app = web.Application()
    redis_db = await redis.Redis(host='redis-stack', port=6379, db=0, decode_responses=True)
    app['redis'] = redis_db
    app.add_routes(routes)

    return app

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app())
    web.run_app(app)
