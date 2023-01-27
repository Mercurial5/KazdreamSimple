import json

from flask import Flask, request

from shopkz.parser import Parser

app = Flask(__name__)


@app.route('/smartphones/parse', methods=['GET'])
def parse():
    parser = Parser()
    items = parser.get_items()

    # I used `w` flag because if I will append items, I need to take care about duplicates.
    # It's just a headache in this test task...
    json.dump(list(items), open('shopkz/parser/smartphones.json', 'w'))

    return 'All items are parsed and saved!'


@app.route('/smartphones/', methods=['GET'])
def show():
    try:
        items = json.load(open('shopkz/parser/smartphones.json', 'r'))
    except FileNotFoundError:
        return {'hint': f'Did you parsed items by going to `{request.host_url}/smartphones/parse/`?'}

    price = request.args.get('price')
    if price:
        items = [item for item in items if item['price'] == int(price)]

    response = {'items': items, 'amount': len(items)}

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0')
