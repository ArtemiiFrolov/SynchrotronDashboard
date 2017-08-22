from rest_framework import routers

from main.api import viewsets


api_router = routers.DefaultRouter()
api_router.register(r'stations', viewsets.StationViewSet, base_name='station')
api_router.register(r'organizations', viewsets.OrganizationViewSet, base_name='organization')
api_router.register(r'approaches', viewsets.ApproachViewSet, base_name='approach')
api_router.register(r'equipment', viewsets.EquipmentViewSet, base_name='equipment')
api_router.register(r'complete_statuses', viewsets.CompleteStatusViewSet, base_name='complete_status')
api_router.register(r'stage_statuses', viewsets.StageStatusViewSet, base_name='stage_status')
api_router.register(r'journal_statuses', viewsets.JournalStatusViewSet, base_name='journal_status')
api_router.register(r'event_lists', viewsets.EventsListViewSet, base_name='event')
api_router.register(r'users', viewsets.UserViewSet, base_name='user')
api_router.register(r'applications', viewsets.ApplicationViewSet, base_name='application')
api_router.register(r'experiment_plans', viewsets.ExperimentPlanViewSet, base_name='experiment_plan')
api_router.register(r'experiments', viewsets.ExperimentViewSet, base_name='experiment')
api_router.register(r'events', viewsets.EventViewSet, base_name='event')
api_router.register(r'comment', viewsets.CommentViewSet, base_name='comment')
api_router.register(r'application_counter', viewsets.ApplicationCounterViewSet, base_name='application_counter')
api_router.register(r'station_marks', viewsets.StationMarkViewSet, base_name='station_mark')
api_router.register(r'station_marks_values', viewsets.StationMarkValueViewSet, base_name='station_mark_value')
