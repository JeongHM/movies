import json
from copy import deepcopy
from flask import Response


def response_object_formatting(func):
    def wrapper(*args, **kwargs):
        res, result, errors, status = func(*args, **kwargs)

        if result or errors:
            res_copy = deepcopy(res)
            res_copy["result"] = result if result else {}
            res_copy["errors"] = errors if errors else []

            if errors:
                error = {
                    "user_message": str(errors).split(":")[0],
                    "internal_message": str(errors).split(":")[1]
                }
                res_copy["errors"] = error

            res = res_copy

        resp = json.dumps(obj=res,
                          ensure_ascii=False,
                          default=str).encode(encoding="utf-8")
        return Response(response=resp,
                        status=status,
                        content_type="application/json; charset=utf-8")
    return wrapper