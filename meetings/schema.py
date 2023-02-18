import datetime
from graphene_django.types import DjangoObjectType

from core.models import User
from .middleware import get_request
from .models import ScheduleMeeting
import graphene
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery


class UserType(DjangoObjectType):
    class Meta:
        model = User


class ScheduleMeetingType(DjangoObjectType):
    meeting_creator = graphene.List(UserType)

    class Meta:
        model = ScheduleMeeting
        field = ('meeting_creator')

    def resolve_meeting_creator(self, info, **kwargs):
        return User.objects.filter(id=self.meeting_creator.id)



class Query(UserQuery, MeQuery, graphene.ObjectType):
    all_schedule_meeting = graphene.List(ScheduleMeetingType)
    schedule_meeting = graphene.Field(ScheduleMeetingType, id=graphene.ID())
    all_scheduling_meeting_of_owner = graphene.List(ScheduleMeetingType)
    all_scheduling_meeting_of_user = graphene.List(ScheduleMeetingType, meeting_creator=graphene.String())

    def resolve_all_schedule_meeting(self, info, **kwargs):
        return ScheduleMeeting.objects.all().order_by('-id')

    def resolve_schedule_meeting(root, info, id):
        return ScheduleMeeting.objects.get(id=id)

    def resolve_all_scheduling_meeting_of_owner(root, info):
        return ScheduleMeeting.objects.filter(meeting_creator=get_request().user).order_by('-id')

    def resolve_all_scheduling_meeting_of_user(root, info, meeting_creator):
        return ScheduleMeeting.objects.filter(meeting_creator__username=meeting_creator)


class CreateMeeting(graphene.Mutation):
    class Arguments:
        from_meeting_date_time = graphene.types.DateTime()
        meeting_time_interval = graphene.String()

    meeting = graphene.Field(ScheduleMeetingType)

    def mutate(self, info, from_meeting_date_time, meeting_time_interval):
        to_meeting_date_time = from_meeting_date_time + datetime.timedelta(
            minutes=int(meeting_time_interval.split(" ")[0])
        )
        meeting = ScheduleMeeting.objects.filter(meeting_creator__id=get_request().user.id, from_meeting_date_time__lte=to_meeting_date_time,
                                       to_meeting_date_time__gte=from_meeting_date_time)
        if meeting:
            return

        meeting = ScheduleMeeting.objects.create(
            from_meeting_date_time=from_meeting_date_time,
            to_meeting_date_time=to_meeting_date_time,
            meeting_time_interval=meeting_time_interval,
        )
        meeting.save()
        return CreateMeeting(meeting=meeting)


class DeleteMeeting(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    meeting = graphene.Field(ScheduleMeetingType)

    def mutate(self, info, id):
        meeting = ScheduleMeeting.objects.get(pk=id)
        if meeting is not None:
            meeting.delete()
        return "Record Deleted SuccessFully"


class UpdateMeeting(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        user_name = graphene.String(required=False)
        user_email = graphene.String(required=False)
        from_meeting_date_time = graphene.types.DateTime(required=False)
        meeting_time_interval = graphene.String(required=False)
        is_book = graphene.Boolean()

    meeting = graphene.Field(ScheduleMeetingType)

    def mutate(self, root, id, user_name=None, user_email=None, from_meeting_date_time=None, meeting_time_interval=None, is_book=None):
        meeting = ScheduleMeeting.objects.get(pk=id)
        meeting.from_meeting_date_time = (
            from_meeting_date_time
            if from_meeting_date_time is not None
            else meeting.from_meeting_date_time
        )
        meeting.meeting_time_interval = (
            meeting_time_interval
            if meeting_time_interval is not None
            else meeting.meeting_time_interval
        )
        if from_meeting_date_time and meeting_time_interval:
            to_meeting_date_time = from_meeting_date_time + datetime.timedelta(
                minutes=int(meeting_time_interval.split(" ")[0])
            )
            meeting_exists = ScheduleMeeting.objects.filter(meeting_creator__id=get_request().user.id, from_meeting_date_time__lte=to_meeting_date_time,
                                                     to_meeting_date_time__gte=from_meeting_date_time)
            if meeting_exists:
                return
            meeting.to_meeting_date_time = to_meeting_date_time

        if user_name and user_email:
            meeting.user_name = user_name
            meeting.user_email = user_email
            meeting.is_booked = True
        meeting.save()
        return UpdateMeeting(meeting=meeting)


class Mutation(graphene.ObjectType):
    create_meeting = CreateMeeting.Field()
    update_meeting = UpdateMeeting.Field()
    delete_meeting = DeleteMeeting.Field()
    register = mutations.Register.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
