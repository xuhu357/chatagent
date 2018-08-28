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

            # 게임아이템 혹은 게임 이름을 지정하지 않았을 경우.
            if game_name is None or not game_name:
                speech = "게임이름 및 아이템 이름을 알려주세요~."

            # 게임에 관핸서 물어볼 경우.
            elif game_name == '아이언쓰론':
                speech = game_name + ': 왕좌를 향한 위대한 전략 게임! 아이언쓰론. 아이언쓰론은 마법과 드래곤이 부활한 시대를 배경으로,' \
                         '왕좌를 차지하기 위한 장대한 전투를 체험할 수 있는 실시간 전략 게임입니다.'
            # 알려고 하는 게임이 아이언쓰론이 아닌 경우.
            else:
                speech = "알려고 하는 아이템을 적어주세요. (ex, 신전)"

        else:
            if game_item == '신전':
                speech = game_item + ": 매일 일정 횟수 만큼 무료로 소원을 빌거나 골드를 소모해, 5종의 자원 중 한가지를 선택해 소량 획득할 수 있습니다." \
                                     "또한, 조건에 따라 전투에서 사망한 병력을 부활시킬 수도 있습니다." \
                                     "레벨이 오를 수록 획득 가능한 자원량과 무료 소원 횟수가 증가합니다."
            else:
                speech = "지원예정인 아이템입니다. (현재는 신전만 지원)"

        return {
            "speech": speech,
            "displayText": speech,
            "source": "Iron Throne service "
        }
    elif req.get("result").get("action") == "method_action":
        result = req.get("result")
        parameters = result.get("parameters")
        game_goal = parameters.get("game_goal")
        speech = ""

        if game_goal == '영지 발전':
            speech = '1. 건물 건설과 업그레이드.\\r\\n' \
                     '2. 성벽 밖 건물의 이용. \\r\\n' \
                     '3. 연구로 효율 향상. \\r\\n' \
                     '4. 영주 레별과 영주 스킬.\\r\\n' \
                     '알려고 하는 내용을 입력해 주세요. (ex, 건물 건설, 연구 등)\\r\\n'
        elif game_goal == '최고 영주':
            speech = '1. 토지를 개간하고, 자원을 수집. ' \
                     '2. 영웅과 병력을 모아 강력한 군대를 만들자. ' \
                     '3. 다양한 건물의 효과를 익히고 영지를 더욱 발전시키자. ' \
                     '4. 전장에서 나의 전략과 힘을 시험해보자. ' \
                     '5. 마을 모드에서 영지의 주민들을 도와, 유용한 버프와 보상도 챙기자.' \
                     '감사합니다.'


        return {
            "speech": speech,
            "displayText": speech,
            "source": "Iron Throne service "
        }
    elif req.get("result").get("action") == "method.details-contexts:game-goal":
        result = req.get("result")
        parameters = result.get("parameters")
        game_contents = parameters.get("game_contents")
        speech = ""

        if game_contents == '건물 건설':
            speech = '영지의 건물들 중, 성벽 안쪽의 건물들 일부는 궁성레벨이 오르면 자동으로 건설되어 이용이' \
                     ' 가능하며, 성벽 바깥 구역의 경작지는 직접 한 곳을 선택해서 건물을 지을 수 있습니다.'
        elif game_contents == '연구':
            speech = '영지 내부 건물 중 아카데미에서는 전투, 생산, 도시, 행군 속도, 차원전, 제작, 부대 숙련 등' \
                     ' 영주님의 영지 발전과 전투에 도움이 되는 다양한 연구를 진행할 수 있습니다. 연구를 ' \
                     '진행하는 방법은 건물을 업그레이드 하는 방법과 동일하게 일정 조건 만족 후 재료를 소모하여 ' \
                     '진행하실 수 있습니다.'

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
