# coding: utf8
#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
from flask import Flask
from flask import request
from flask import make_response
import json
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
install_aliases()

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = process_request(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def process_request(req):
    """
    result -> action
    result -> parameters -> "원하는 parameter 이름"
    :param req:
    :return:
    """
    if req.get("result").get("action") == "definition_intent":
        result = req.get("result")
        parameters = result.get("parameters")
        game_name = parameters.get("game_name")
        game_item = parameters.get("game_item")
        # game_item = parameters.get("game_item")
        speech = ""

        if game_item is None or not game_item:
            speech = "알려고 하는 아이템을 적어주세요. (ex, 신전)"
        else:
            if game_name == '아이언쓰론' and game_item == '신전':
                speech = game_item + ": 매일 일정 횟수 만큼 무료로 소원을 빌거나 골드를 소모해, 5종의 자원 중 한가지를 선택해 소량 획득할 수 있습니다." \
                                     "또한, 조건에 따라 전투에서 사망한 병력을 부활시킬 수도 있습니다." \
                                     "레벨이 오를 수록 획득 가능한 자원량과 무료 소원 횟수가 증가합니다."
            else:
                speech = "알수 없는 게임입니다."

        return {
            "speech": speech,
            "displayText": speech,
            "source": "Iron Throne service "
        }
    else:
        return {}


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
