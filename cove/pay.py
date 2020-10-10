def pay(result):

    if result["code"] == "1":
        return "success"
    else:
        return "fail"