
from running_log import rltime
from running_log import services
from running_log import utils

from .. import factories
from . import RunningLogFrontendTestCase


class TestServices(RunningLogFrontendTestCase):

    def test_user_with_runs(self):
        user = factories.UserWithRunsFactory()
        for run in user.runs:
            assert run.miles >= 0
            assert run.miles <= 10
            assert utils.is_date_editable(run.date)

    def test_add_user_to_group(self):
        user = factories.UserWithRunsFactory()
        group = factories.GroupFactory()
        services.groups.add_user(group, user)
        assert user in group.users

    def test_group_runs(self):
        group = factories.GroupFactory()
        other = factories.GroupFactory()
        user1 = factories.UserWithRunsFactory()
        user2 = factories.UserWithRunsFactory()
        user3 = factories.UserWithRunsFactory()
        services.groups.add_user(group, user1)
        services.groups.add_user(group, user2)
        services.groups.add_user(other, user2)
        services.groups.add_user(other, user3)
        group_runs = services.runs.get_group_runs(group, *utils.editable_range())
        other_runs = services.runs.get_group_runs(other, *utils.editable_range())
        today = rltime.now()
        def miles_today(gruns):
            return sum([user_runs.miles_for_date(today) 
                for user_runs in gruns.runs_by_user.values()])
        assert group_runs.miles_for_date(today) == miles_today(group_runs)
        assert other_runs.miles_for_date(today) == miles_today(other_runs)
