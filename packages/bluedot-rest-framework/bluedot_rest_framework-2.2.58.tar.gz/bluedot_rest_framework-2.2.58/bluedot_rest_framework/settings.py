import datetime
from django.conf import settings
from rest_framework.settings import APISettings


USER_SETTINGS = getattr(settings, 'BLUEDOT_REST_FRAMEWORK', None)

DEFAULTS_SETTINGS = {
    'event': {
        'models': 'bluedot_rest_framework.event.models.Event',
        'serializers': 'bluedot_rest_framework.event.serializers.EventSerializer',
        'views': 'bluedot_rest_framework.event.views.EventView',
        'live': {
            'consumers': 'bluedot_rest_framework.event.live.consumers.LiveConsumer',
            'routing': 'bluedot_rest_framework.event.live.routing.websocket_urlpatterns',
        },
        'chat': {
            'models': 'bluedot_rest_framework.event.chat.models.EventChat',
            'serializers': 'bluedot_rest_framework.event.chat.serializers.EventChatSerializer',
            'views': 'bluedot_rest_framework.event.chat.views.EventChatView',
            'consumers': 'bluedot_rest_framework.event.chat.consumers.ChatConsumer',
            'routing': 'bluedot_rest_framework.event.chat.routing.websocket_urlpatterns',
        },
        'configuration': {
            'models': 'bluedot_rest_framework.event.configuration.models.EventConfiguration',
            'serializers': 'bluedot_rest_framework.event.configuration.serializers.EventConfigurationSerializer',
            'views': 'bluedot_rest_framework.event.configuration.views.EventConfigurationView',
        },
        'data_download': {
            'models': 'bluedot_rest_framework.event.data_download.models.EventDataDownload',
            'serializers': 'bluedot_rest_framework.event.data_download.serializers.EventDataDownloadSerializer',
            'views': 'bluedot_rest_framework.event.data_download.views.EventDataDownloadView',
        },
        'question': {
            'models': 'bluedot_rest_framework.event.question.models.EventQuestion',
            'serializers': 'bluedot_rest_framework.event.question.serializers.EventQuestionSerializer',
            'views': 'bluedot_rest_framework.event.question.views.EventQuestionView',
            'user_models': 'bluedot_rest_framework.event.question.models.EventQuestionUser',
            'user_serializers': 'bluedot_rest_framework.event.question.serializers.EventQuestionUserSerializer',
            'user_views': 'bluedot_rest_framework.event.question.views.EventQuestionUserView',
        },
        'register': {
            'models': 'bluedot_rest_framework.event.register.models.EventRegister',
            'serializers': 'bluedot_rest_framework.event.register.serializers.EventRegisterSerializer',
            'views': 'bluedot_rest_framework.event.register.views.EventRegisterView',
            'config_models': 'bluedot_rest_framework.event.register.models.EventRegisterConfig',
            'config_serializers': 'bluedot_rest_framework.event.register.serializers.EventRegisterConfigSerializer',
            'config_views': 'bluedot_rest_framework.event.register.views.EventRegisterConfigView',

        },
        'schedule': {
            'models': 'bluedot_rest_framework.event.schedule.models.EventSchedule',
            'serializers': 'bluedot_rest_framework.event.schedule.serializers.EventScheduleSerializer',
            'views': 'bluedot_rest_framework.event.schedule.views.EventScheduleView',
        },
        'speaker': {
            'models': 'bluedot_rest_framework.event.speaker.models.EventSpeaker',
            'serializers': 'bluedot_rest_framework.event.speaker.serializers.EventSpeakerSerializer',
            'views': 'bluedot_rest_framework.event.speaker.views.EventSpeakerView',
        },
        'comment': {
            'models': 'bluedot_rest_framework.event.comment.models.EventComment',
            'serializers': 'bluedot_rest_framework.event.comment.serializers.EventCommentSerializer',
            'views': 'bluedot_rest_framework.event.comment.views.EventCommentView',
            'like_models': 'bluedot_rest_framework.event.comment.models.EventCommentLike',
            'like_serializers': 'bluedot_rest_framework.event.comment.serializers.EventCommentLikeSerializer',
            'like_views': 'bluedot_rest_framework.event.comment.views.EventCommentLikeView',
            'consumers': 'bluedot_rest_framework.event.comment.consumers.CommentConsumer',
            'routing': 'bluedot_rest_framework.event.comment.routing.websocket_urlpatterns',
        },
        'vote': {
            'models': 'bluedot_rest_framework.event.vote.models.EventVote',
            'serializers': 'bluedot_rest_framework.event.vote.serializers.EventVoteSerializer',
            'views': 'bluedot_rest_framework.event.vote.views.EventVoteView',
            'user_models': 'bluedot_rest_framework.event.vote.models.EventVoteUser',
            'user_serializers': 'bluedot_rest_framework.event.vote.serializers.EventVoteUserSerializer',
            'user_views': 'bluedot_rest_framework.event.vote.views.EventVoteUserView',
        },
        'venue': {
            'models': 'bluedot_rest_framework.event.venue.models.EventVenue',
            'serializers': 'bluedot_rest_framework.event.venue.serializers.EventVenueSerializer',
            'views': 'bluedot_rest_framework.event.venue.views.EventVenueView',
        },
    },
    'user': {
        'models': 'bluedot_rest_framework.user.models.User',
        'serializers': 'bluedot_rest_framework.user.serializers.UserSerializer',
        'views': 'bluedot_rest_framework.user.views.UserView',
    },
    'material': {
        'models': 'bluedot_rest_framework.material.models.Material',
        'serializers': 'bluedot_rest_framework.material.serializers.MaterialSerializer',
        'views': 'bluedot_rest_framework.material.views.MaterialView',
        'tags': {
            'models': 'bluedot_rest_framework.material.tags.models.Tags',
            'serializers': 'bluedot_rest_framework.material.tags.serializers.TagsSerializer',
            'views': 'bluedot_rest_framework.material.tags.views.TagsView',
        },
    },
    'question': {
        'models': 'bluedot_rest_framework.question.models.Question',
        'serializers': 'bluedot_rest_framework.question.serializers.QuestionSerializer',
        'views': 'bluedot_rest_framework.question.views.QuestionView',
        'user_models': 'bluedot_rest_framework.question.models.QuestionUser',
        'user_serializers': 'bluedot_rest_framework.question.serializers.QuestionUserSerializer',
        'user_views': 'bluedot_rest_framework.question.views.QuestionUserView',
    },
    'category': {
        'models': 'bluedot_rest_framework.category.models.Category',
        'serializers': 'bluedot_rest_framework.category.serializers.CategorySerializer',
        'views': 'bluedot_rest_framework.category.views.CategoryView',
    },
    'config': {
        'models': 'bluedot_rest_framework.config.models.Config',
        'serializers': 'bluedot_rest_framework.config.serializers.ConfigSerializer',
        'views': 'bluedot_rest_framework.config.views.ConfigView',
    },
    'data_download': {
        'models': 'bluedot_rest_framework.data_download.models.DataDownload',
        'serializers': 'bluedot_rest_framework.data_download.serializers.DataDownloadSerializer',
        'views': 'bluedot_rest_framework.data_download.views.DataDownloadView',
        'user_models': 'bluedot_rest_framework.data_download.models.DataDownloadUser',
        'user_serializers': 'bluedot_rest_framework.data_download.serializers.DataDownloadUserSerializer',
        'user_views': 'bluedot_rest_framework.data_download.views.DataDownloadUserView',
    },
    'wechat': {
        'qrcode': {
            'models': 'bluedot_rest_framework.wechat.response.models.WeChatQrcode',
            'serializers': 'bluedot_rest_framework.wechat.response.serializers.WeChatQrcodeSerializer',
        },
        'response': 'bluedot_rest_framework.wechat.response.response.Response',
        'models': 'bluedot_rest_framework.wechat.models.WeChatUser',
        'serializers': 'bluedot_rest_framework.wechat.serializers.WeChatUserSerializer',
        'miniprogram': {
            'APPID': '',
            'SECRET': ''
        },
        'offiaccount': {
            'APPID': 'wx7c33b1edc5934d81',
            'SECRET': 'da0330d7394e1f620b43ccd118646d5e',
            'TOKEN': 'X1GOUqQcLipgwyhVYMPfagGIFqgbDHlF',
            'EncodingAESKey': 'uLVsTEJU6M20Ks1h2Bc9Rh4Y2FGG5IFrLcEhOjtmdqy'
        },
        'redis_client': 'redis://127.0.0.1:6379/0',
        'login': {
            'consumers': 'bluedot_rest_framework.wechat.login.consumers.WechatLoginConsumer',
            'routing': 'bluedot_rest_framework.wechat.login.routing.websocket_urlpatterns',
        },
        'templates_url': ''

    },
    'utils': {
        'AES': {
            'iv': 'aSEDKOOuic5BDks1',
            'key': '9B1niuSzcISIHV5i',
        },
        'OSS': {
            'access_key_id': 'LTAI4Fsv96kxGi33PNNUd4z6',
            'access_key_secret': 'qGbegKc3fmVYZ2Z7qowlXCyTq04iTm',
            'endpoint': 'http://oss-cn-beijing.aliyuncs.com',
            'bucket_name': 'cpa-global'
        }
    }
}


def merge_settings(DEFAULTS_SETTINGS, USER_SETTINGS):
    for key in USER_SETTINGS:
        if isinstance(USER_SETTINGS[key], dict) and isinstance(DEFAULTS_SETTINGS[key], dict):
            merge_settings(DEFAULTS_SETTINGS[key], USER_SETTINGS[key])
        else:
            DEFAULTS_SETTINGS[key] = USER_SETTINGS[key]
    return DEFAULTS_SETTINGS


DEFAULTS_SETTINGS = merge_settings(DEFAULTS_SETTINGS, USER_SETTINGS)
api_settings = APISettings(DEFAULTS_SETTINGS, DEFAULTS_SETTINGS)
