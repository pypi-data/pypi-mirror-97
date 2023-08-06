from rest_framework.routers import DefaultRouter
from bluedot_rest_framework import import_string
from bluedot_rest_framework.event.survey.views import EventSurveyUserView
from bluedot_rest_framework.event.live.views import EventLivePPTCurrentView

EventView = import_string('event.views')
EventQuestionView = import_string('event.question.views')
EventQuestionUserView = import_string('event.question.user_views')
EventScheduleView = import_string('event.schedule.views')
EventSpeakerView = import_string('event.speaker.views')
EventDataDownloadView = import_string('event.data_download.views')
EventRegisterView = import_string('event.register.views')
EventChatView = import_string('event.chat.views')
EventConfigurationView = import_string('event.configuration.views')
EventCommentView = import_string('event.comment.views')
EventVoteView = import_string('event.vote.views')
EventVoteUserView = import_string('event.vote.user_views')
EventVenueView = import_string('event.venue.views')
EventRegisterConfigView = import_string('event.register.config_views')

router = DefaultRouter(trailing_slash=False)
router.register(r'event/live/ppt/current', EventLivePPTCurrentView,
                basename='event-live-ppt-current')
router.register(r'event/vote/user', EventVoteUserView,
                basename='event-vote-user')
router.register(r'event/venue', EventVenueView,
                basename='event-venue')
router.register(r'event/vote', EventVoteView,
                basename='event-vote')
router.register(r'event/configuration', EventConfigurationView,
                basename='event-configuration')
router.register(r'event/question/user', EventQuestionUserView,
                basename='event-question-user')
router.register(r'event/question', EventQuestionView,
                basename='event-question')
router.register(r'event/chat', EventChatView,
                basename='event-chat')
router.register(r'event/register/config', EventRegisterConfigView,
                basename='event-register-config')
router.register(r'event/register', EventRegisterView,
                basename='event-register')
router.register(r'event/comments', EventCommentView,
                basename='event-comments')
router.register(r'event/data-download', EventDataDownloadView,
                basename='event-data-download')
router.register(r'event/speaker', EventSpeakerView,
                basename='event-speaker')
router.register(r'event/schedule', EventScheduleView,
                basename='event-schedule')
router.register(r'event/survey/user', EventSurveyUserView,
                basename='event-survey-user')
router.register(r'event', EventView,
                basename='event')

urlpatterns = router.urls
