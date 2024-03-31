def res(data=None,message="OK",code='0000',status=200):
    return {
        'code':code,
        'msg':message,
        'data':data
    },status
def format_datetime_to_json(datetime,format="%Y-%m-%d %H:%M:%S"):
    return datetime.strftime(format)