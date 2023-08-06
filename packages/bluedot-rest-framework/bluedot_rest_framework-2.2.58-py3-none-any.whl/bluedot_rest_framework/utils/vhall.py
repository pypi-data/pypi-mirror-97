import time
import requests
import hashlib
# from utils.commons import md5_str
# from online.utils.vhall.settings import APP_ID, SECRET_KEY


def md5_str(_str):
    md5_obj = hashlib.md5()
    md5_obj.update(_str.encode('utf8'))
    return md5_obj.hexdigest()


class Vhall:
    # APP_ID = 'b37675d5'
    # SECRET_KEY = '68a181fdcb17818a92044402367a6c91'
    APP_ID = '8aa54812'
    SECRET_KEY = 'aad0ade20fd8b595264312a3e78bd923'

    def _public_param(self, new_params=None):

        try:
            params = {
                'app_id': self.APP_ID,
                'signed_at': str(int(time.time())),
                'third_party_user_id': 'bluemiddle'
            }
            if new_params:
                # 循环加新参数
                for t_param in new_params:
                    params[t_param[0]] = t_param[1]
            params_keys = list(params.keys())
            params_keys.sort()  # 按字母顺序排序

            # 拼接字符串，用于md5
            sign_param = ''
            for key in params_keys:
                sign_param += key
                sign_param += str(params[key])
            sign_param = self.SECRET_KEY + sign_param+self.SECRET_KEY

            params['sign'] = md5_str(sign_param)
            return params

        except:
            return None

    def list_room(self, pos=None, limit=None):
        """
        room列表
        """
        try:
            param_list = []
            if pos:
                pos_t = ('pos', pos)
                param_list.append(pos_t)
            if limit:
                limit_t = ('limit', limit)
                param_list.append(limit_t)
            params = self._public_param(param_list)
            res = requests.get(url='http://api.vhallyun.com/api/v2/room/lists',
                               params=params)
            if res.status_code != 200:
                return None
            res = res.json()
            return res['data']

        except Exception:
            return None

    def room_create(self):
        """
        创建直播室
        """
        try:
            params = self._public_param()
            res = requests.get(
                url='http://api.vhallyun.com/api/v2/room/create',
                params=params)
            res = res.json()
            return res['data']['room_id']
        except:
            return None

    def get_push_info(self, room_id, expire_time):
        """
        推流信息：http://www.vhallyun.com/docs/show/704
        params: room_id, expire_time
        """
        try:
            param_list = [('room_id', room_id), ('expire_time', expire_time)]
            params = self._public_param(param_list)
            res = requests.get(
                url='http://api.vhallyun.com/api/v2/room/get-push-info',
                params=params)

            res = res.json()
            return res['data']
        except Exception:
            return None

    def delete_room(self, room_id):
        """
        删除直播室
        """
        try:
            params = self.public_param([('room_id', room_id)])
            # params['room_id'] = room_id

            res = requests.get(
                url='http://api.vhallyun.com/api/v2/room/delete',
                params=params)
            if res.status_code != 200:
                return None

            res = res.json()
            delete_room_id = res['data']['delete_room_id']
            return delete_room_id

        except Exception:
            return None

    def get_token(self, room_id, third_party_user_id, live_inav_id=None):
        """
        获取access_token,默认有效期一天
        thrid_party_user_id用于表示前台用户，这里需要一个规则用于解析用户
        """
        try:
            param_list = [('publish_stream', room_id),
                          ('third_party_user_id', third_party_user_id),
                          ('publish_inav_stream', live_inav_id),
                          ('publish_inav_another', live_inav_id), ]
            params = self._public_param(param_list)
            res = requests.get(
                url='http://api.vhallyun.com/api/v1/base/create-v2-access-token',
                params=params)
            res = res.json()
            return res['data']['access_token']

        except Exception:
            return None

    def get_access_token_pull(self, third_party_user_id):
        """
        获取access_token,默认有效期一点
        thrid_party_user_id用于表示前台用户，这里需要一个规则用于解析用户
        """
        try:
            param_list = [('third_party_user_id', third_party_user_id)]
            params = self.public_param(param_list)

            print('params', params)

            res = requests.get(
                url='http://api.vhallyun.com/api/v1/base/create-v2-access-token',
                params=params)

            if res.status_code != 200:
                return None

            res = res.json()
            print(res)
            access_token = res['data']['access_token']
            return access_token

        except Exception:
            return None

    def get_room_join_info(self, room_id, start_time, pos):
        """
        此数据非实时数据，访问记录数据每分钟汇总一次，每次数据延时六分钟。
        """
        try:
            param_list = [('room_id', room_id),
                          ('start_time', start_time),
                          ('pos', pos),
                          ('limit', 1000)]
            params = self.public_param(param_list)

            print('params', params)

            res = requests.get(
                url='http://api.vhallyun.com/api/v2/room/get-room-join-info',
                params=params)

            if res.status_code != 200:
                return None

            res = res.json()
            # print(res)

            return res["data"]

        except Exception:
            return None

    def create_inav(self):
        """
        创建互动房间
        """
        try:
            params = self._public_param()
            res = requests.get(
                url='http://api.vhallyun.com/api/v2/inav/create',
                params=params)
            res = res.json()
            print(res)
            return res['data']['inav_id']
        except:
            return None

    def push_inav(self, inav_id, room_id):
        """
        发起旁路直播
        """
        try:
            param_list = [('inav_id', inav_id),
                          ('room_id', room_id),
                          ('layout', 'CANVAS_LAYOUT_PATTERN_TILED_5_1L4R'), ]
            params = self._public_param(param_list)
            res = requests.get(
                url='http://api.vhallyun.com/api/v2/inav/push-another',
                params=params)
            res = res.json()
            print(res)
            return res['data']['inav_id']
        except:
            return None

    def create_vod(self, **kwargs):
        """
        生成回放:http://www.vhallyun.com/docs/show/472
        params:action(SubmitCreateRecordTasks),stream_id(room_id),instant
        截取时间，剔除时间暂时不考虑
        """
        param_list = []
        param_dic = kwargs

        param_keys = param_dic.keys()
        for param_key in param_keys:
            param_list.append((param_key, param_dic[param_key]))

        params = self._public_param(param_list)

        res = requests.get(url='http://api.vhallyun.com/api/v2/vod',
                           params=params)
        if res.status_code != 200:
            return None

        res = res.json()
        print('res', res)
        vod = res['data']
        return vod

    def delete_vod(self, **kwargs):
        """
        删除点播:http://www.vhallyun.com/docs/show/488
        params:action(SubmitDeleteVodTasks),vod_id(多个用逗号隔开，最多10个)
        """
        try:
            param_list = []
            param_dic = kwargs

            param_keys = param_dic.keys()
            for param_key in param_keys:
                param_list.append(param_key, param_dic[param_key])
            params = self.public_param(param_list)

            res = requests.get(url='http://api.vhallyun.com/api/v2/vod',
                               params=params)
            if res.status_code != 200:
                return None

            res = res.json()
            print(res)
            deleted_vod_list = res['data']['deleted_vod_list']
            return deleted_vod_list

        except Exception:
            return None

    def transcode(self, **kwargs):
        """
        转码，上传的视频需要转码
        params：action(SubmitTranscodeTasks),vod_id,quality(same),format(hls)
        """
        try:
            param_list = []
            param_dic = kwargs

            param_keys = param_dic.keys()
            for param_key in param_keys:
                param_list.append(param_key, param_dic[param_key])
            params = self.public_param(param_list)

            res = requests.get(url='http://api.vhallyun.com/api/v2/vod',
                               params=params)
            if res.status_code != 200:
                return None

            res = res.json()
            print(res)
            task_id = res['data']['task_id']
            return task_id

        except Exception:
            return None

    def addkey(self, **kwargs):
        """
        上传打点
        params: action(AddKeyFrameDesc),vod_id,point_sections
        [
            {
                "time_point": 12, #打点相对时间点
                "desc": "abc" #打点文字信息
            },
            {
                "time_point": 52, #打点相对时间点
                "desc": “xxx” #打点文字信息
            }
        ]
        """
        try:
            param_list = []
            param_dic = kwargs

            param_keys = param_dic.keys()
            for param_key in param_keys:
                param_list.append(param_key, param_dic[param_key])
            params = self.public_param(param_list)

            res = requests.get(url='http://api.vhallyun.com/api/v2/vod',
                               params=params)
            if res.status_code != 200:
                return None
            return True

        except Exception:
            return None


Vhall = Vhall()
