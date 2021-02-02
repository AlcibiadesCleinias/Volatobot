import krakenex
from settings import kraken_api_key, kraken_private_api_key

# Instantiate an instance of kraken api
k = krakenex.API()
k.key = kraken_api_key
k.secret = kraken_private_api_key


class KrakenApiError(Exception):
    pass


def extract_result(json_response):
    try:
        if not json_response['error']:
            if json_response['result']:
                return json_response['result']
            else:
                raise KrakenApiError('empty result')
        else:
            raise KrakenApiError(json_response['error'])
    except Exception as e:
        raise KrakenApiError(str(e))


def get_current_price(pairs: list):
    # Prepare a parameter with currency pairs list
    pair_list = ''
    for pair in pairs:
        pair_list += f'{pair},'
    pair_list = pair_list[:-1]

    # Call Kraken API and get response
    try:
        response_result = k.query_public(method='Ticker', data={'pair': pair_list})
    except Exception as e:
        raise KrakenApiError(str(e))

    # Generate easy to use result
    result = {}

    try:
        raw_result = extract_result(response_result)
        # fill result with pair prices
        for pair_name, price_info in raw_result.items():
            result[pair_name] = float(price_info['c'][0])

    except Exception as e:
        raise KrakenApiError(str(e))

    # Finish
    return result


def get_open_orders():
    # Call Kraken API and get response
    try:
        response_result = k.query_private(method='OpenOrders')
    except Exception as e:
        raise KrakenApiError(str(e))

    # Generate easy to use result
    result = []

    try:
        raw_result = extract_result(response_result)
        for order_id, order_info in raw_result['open'].items():
            order = {'id': order_id,
                     'type': order_info['descr']['type'],
                     'amount': float(order_info['vol']),
                     'price': float(order_info['descr']['price']),
                     'open_position': float(order_info['vol']) - float(order_info['vol_exec']),
                     'closed_position': float(order_info['vol_exec']),
                     'status': order_info['status']}
            result.append(order)

    except Exception as e:
        raise KrakenApiError(str(e))

    # Finish
    return result


def post_order(pair, type, price, volume, order_type="limit"):
    # Form data for request
    data = {'pair': pair,
            'type': type,
            'ordertype': order_type,
            'price': price,
            'volume': volume}

    # Post order via API
    try:
        response_result = k.query_private(method='AddOrder', data=data)
    except Exception as e:
        raise KrakenApiError(str(e))

    # Generate easy to use result
    result = {}

    try:
        raw_result = extract_result(response_result)
        result['id'] = raw_result['txid'][0]
        result['descr'] = raw_result['descr']['order']
    except Exception as e:
        raise KrakenApiError(str(e))

    # Finish
    return result


def cancel_order(id):
    # Form data for request
    data = {'txid': id}

    # Post order via API
    try:
        response_result = k.query_private(method='CancelOrder', data=data)
    except Exception as e:
        raise KrakenApiError(str(e))

    # Generate easy to use result
    result = {}

    try:
        raw_result = extract_result(response_result)
        result['count'] = raw_result['count']
    except Exception as e:
        raise KrakenApiError(str(e))

    # Finish
    return result