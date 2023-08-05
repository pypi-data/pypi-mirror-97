from .call import call

class qllb:
    def __init__(self, key):
        self.url = "http://qllb.vlute.edu.vn"
        self.key = key
        self.call = call()
        if len(key) == 0:
            print('KEY không hợp lệ')

    def ds_phong(self):
        url = self.url + "/api/phong"
        params = { 'key': self.key }
        response = self.call.get(url=url, params=params)
        return response

    def diem_danh(self, mssv, phong):
        url = self.url + "/api/diem-danh"
        params = { 'key': self.key, 'mssv': mssv, 'phong':  phong}
        response = self.call.get(url=url, params=params)
        return {
            'code': response['code'],
            'message': response['message'],
            'success': response['code'] == 200
        }