import os
from datetime import datetime
from rest_framework.decorators import action
from rest_framework.response import Response
from bluedot_rest_framework.utils.vhall import Vhall
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet
from bluedot_rest_framework.utils.func import md5_str, orm_bulk_update
from .models import EventLivePPT, EventLivePPTCurrent
from .serializers import EventLivePPTCurrentSerializer
from .ppt import ppt2images


class LiveView:

    @action(detail=False, methods=['post'], url_path='live-room-create', url_name='live-room-create')
    def live_room_create(self, request, *args, **kwargs):
        _id = request.data.get('event_id', None)
        room_id = Vhall.room_create()
        quesyset = self.model_class.objects.get(pk=_id)
        update_dict = {
            'live_room_id': room_id,
            'live_create_room_time': datetime.now(),
        }
        if quesyset.live_type == 2:
            update_dict['live_inav'] = {'id': Vhall.create_inav()}
        orm_bulk_update(quesyset, update_dict)
        return Response({'room_id': room_id})

    @action(detail=False, methods=['post'], url_path='live-room-inav-push', url_name='live-room-inav-push', permission_classes=[])
    def live_room_inav_push(self, request, *args, **kwargs):
        _id = request.data.get('event_id', None)
        quesyset = self.model_class.objects.get(pk=_id)
        Vhall.push_inav(
            inav_id=quesyset.live_inav['id'], room_id=quesyset.live_room_id)
        return Response()

    @action(detail=False, methods=['get'], url_path='live-room-token', url_name='live-room-token')
    def live_room_token(self, request, *args, **kwargs):
        live_room_id = request.query_params.get('live_room_id', None)
        live_inav_id = request.query_params.get('inav_id', '')
        third_party_user_id = request.query_params.get(
            'third_party_user_id', None)
        token = Vhall.get_token(
            room_id=live_room_id, third_party_user_id=third_party_user_id, live_inav_id=live_inav_id)
        return Response({'token': token})

    @action(detail=False, methods=['post'], url_path='live-room-delete', url_name='live-room-delete')
    def room_delete(self, request, *args, **kwargs):
        _id = request.data.get('event_id', None)
        delete_room_id = Vhall.delete_room()
        self.model_class.objects.get(pk=_id).delete(
            live_room_id=delete_room_id)
        return Response({'room_id': delete_room_id})

    @action(detail=False, methods=['get'], url_path='live-room-current-time', url_name='live-room-current-time')
    def live_room_current_time(self, request, *args, **kwargs):
        event_id = request.query_params.get('event_id', None)
        queryset = self.model_class.objects.get(pk=event_id)
        now_time = datetime.now()
        code = 0
        if now_time >= queryset.start_time and now_time <= queryset.end_time:
            code = 1
        current_time = (now_time - queryset.start_time)
        return Response({'code': code, 'current_time': current_time})

    @action(detail=False, methods=['post'], url_path='live-room-create-vod', url_name='live-room-create-vod')
    def live_room_create_vod(self, request, *args, **kwargs):
        queryset = self.model_class.objects.get(
            pk=request.data.get('event_id', None))

        start_time = str(queryset.live_create_room_time)[:19]
        end_time = str(datetime.now())[:19]
        vod = Vhall.create_vod(action='SubmitCreateRecordTasks',
                               app_id='8aa54812',
                               stream_id=queryset.live_room_id,
                               start_time=start_time,
                               end_time=end_time)
        if vod:
            orm_bulk_update(queryset, {
                'live_playback': 1,
                'live_vod_id': vod['vod_id'],
                'live_task_id': vod['task_id'],
            })
            return Response({'code': 1})
        return Response({'code': 0})

    @action(detail=False, methods=['get', 'post'], url_path='live-ppt', url_name='live-ppt')
    def live_ppt(self, request, *args, **kwargs):
        if request.method == 'GET':
            event_id = request.query_params.get('event_id')
            queryset = EventLivePPT.objects.filter(event_id=event_id).first()
            if queryset:
                return Response({'image_list': queryset.image_list})
            return Response({'image_list': []})
        elif request.method == 'POST':
            ppt = request.data.get('file')
            event_id = request.data.get('event_id')
            ppt_name = md5_str(
                ppt._name) + '.' + ppt._name.split('.')[-1].strip('"')
            # ppt大小限制20M，部署后nginx也有一个限制
            if ppt and ppt.size > 20480000:
                return Response({'code': 1003, 'msg': 'over size limit'})

            ppt_path = os.getcwd()+'/tmp_ppt/' + ppt_name
            with open(ppt_path, 'wb') as f:
                data = ppt.read()
                f.write(data)
            image_list = ppt2images(ppt_path, ppt_name, event_id)
            queryset = EventLivePPT.objects.filter(event_id=event_id).first()
            if queryset:
                queryset.image_list = image_list
                queryset.save()
            else:
                EventLivePPT.objects.create(
                    event_id=event_id, image_list=image_list)
            return Response({'image_list': image_list})


class EventLivePPTCurrentView(CustomModelViewSet):
    model_class = EventLivePPTCurrent
    serializer_class = EventLivePPTCurrentSerializer
    filterset_fields = {
        'event_id': {
            'field_type': 'int',
            'lookup_expr': ''
        },
    }

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset[0:1], many=True)
        return Response(serializer.data[0])
