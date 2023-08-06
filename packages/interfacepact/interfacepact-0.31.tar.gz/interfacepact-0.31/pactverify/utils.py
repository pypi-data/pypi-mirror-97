import copy
import json
from pactverify.core import Like, EachLike


def generate_pact_json_by_response(target_data, pactverify_json=None, is_list=False, separator='$', matchcol=[],
                                   verifyfirstlist=True):
    """
    根据接口返回数据自动生成json格式断言数据
    :param target_data:  返回数据
    :param pactverify_json: 自动生成的断言数据
    :param is_list:
    :return:
    """
    base_types = (float, str, int, bool)
    like_key = separator + Like.__name__
    eachlike_key = separator + EachLike.__name__

    values_key = separator + 'values'
    params_key = separator + 'params'

    if pactverify_json is None:

        if not isinstance(target_data, (list, dict)):
            try:
                tmp = json.loads(target_data)
                if isinstance(tmp, (list, dict)):
                    target_data = tmp
            except Exception as e:
                print('【pactverify生成json断言数据异常】：{}'.format(str(e)))
                return None

        pactverify_json = {}

    if type(target_data) == dict:
        if (is_list):
            pass
        else:
            pactverify_json = {like_key: copy.deepcopy(target_data)}

        for k, v in target_data.items():

            if (is_list):
                target_data[k] = {}
            else:
                if k in matchcol:
                    pactverify_json[like_key][k] = {"$Matcher": v}
                    continue
                else:
                    pactverify_json[like_key][k] = {}
            if type(v) in base_types:
                if k in matchcol:
                    v = {"$Matcher": v}
                if (like_key in pactverify_json.keys()):
                    pactverify_json[like_key][k] = v
                else:
                    pactverify_json[k] = v
            else:
                if k in matchcol:
                    pactverify_json[k] = {"$Matcher": v}
                    continue
                if (is_list):
                    pactverify_json[k] = generate_pact_json_by_response(v, pactverify_json[k], False, separator,
                                                                        matchcol, verifyfirstlist)
                else:
                    pactverify_json[like_key][k] = generate_pact_json_by_response(v,
                                                                                  pactverify_json[like_key][
                                                                                      k],
                                                                                  False, separator, matchcol,
                                                                                  verifyfirstlist)
    elif type(target_data) == list:
        if len(target_data) == 0:
            pactverify_json = {
                eachlike_key: {
                    values_key: "",
                    params_key: {
                        "minimum": 0
                    }
                }
            }
        else:
            example_data = target_data[0]
            pactverify_json = {
                eachlike_key: example_data
            }
            if type(example_data) == dict:
                value_type = {}
            elif type(example_data) == list:
                value_type = []
            elif type(example_data) == str:
                value_type = ""
            elif type(example_data) == int:
                value_type = 1
            elif type(example_data) == bool:
                value_type = True
            if verifyfirstlist:
                pactverify_json[eachlike_key] = {
                    values_key: value_type,
                    params_key: {
                        "minimum": 1
                    }
                }
            else:
                pactverify_json[eachlike_key] = generate_pact_json_by_response(example_data,
                                                                               pactverify_json[eachlike_key],
                                                                               True, separator, matchcol,
                                                                               verifyfirstlist)


    elif type(target_data) == type(None):
        pactverify_json = {
            like_key: {
                values_key: "null占位",
                params_key: {
                    "nullable": True
                }
            }
        }

    elif type(target_data) in base_types:
        if is_list:
            pactverify_json = copy.deepcopy(target_data)
        else:
            pactverify_json = {
                like_key: copy.deepcopy(target_data)
            }
    return pactverify_json


if __name__ == '__main__':
    response_json = {"code": 0, "msg": "success", "ret": 0,
                     "args": {"err": {"errorCode": -1, "errorMsg": "SUCCESS", "errorLevel": 0},
                              "res": {"code": 0, "message": "", "items": [{"taskid": 1}], "firstInItems": [],
                                      "timeItems": [{"taskId": 59}, {"taskId": 47, }]},
                              "rsp": {"code": 0, "message": "", "items": [], "firstInItems": [], "timeItems": []}}}
    # 参数说明：响应json数据,契约关键字标识符(默认$)
    from pactverify.matchers import PactJsonVerify
    actual_data = copy.deepcopy(response_json)
    expect_format = generate_pact_json_by_response(response_json, separator='$', matchcol=["code", "msg", 'errorCode'],
                                                   verifyfirstlist=True)

    mPactJsonVerify = PactJsonVerify(expect_format, hard_mode=False, separator='$')
    # # 校验实际返回数据
    mPactJsonVerify.verify(actual_data)
    # 校验结果
    verify_result = mPactJsonVerify.verify_result
    if not verify_result:
        raise Exception('字段不一致,错误信息:{0}'.format(mPactJsonVerify.verify_info))
    else:
        print(verify_result)
