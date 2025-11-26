import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "resource_reservation.settings")
django.setup()

from django.contrib.auth.models import Group, User
from rest_framework.authtoken.models import Token


def run():
    worker_group, _ = Group.objects.get_or_create(name="worker")
    manager_group, _ = Group.objects.get_or_create(name="manager")

    worker, _ = User.objects.get_or_create(username="worker1")
    worker.set_password("workerpass")
    worker.save()

    manager, _ = User.objects.get_or_create(username="manager1")
    manager.set_password("managerpass")
    manager.save()

    worker.groups.add(worker_group)
    manager.groups.add(manager_group)

    # Define fixed tokens
    worker_token_value = "WORKER_TEST_TOKEN_12345"
    manager_token_value = "MANAGER_TEST_TOKEN_12345"

    # Create or update token
    worker_token, _ = Token.objects.update_or_create(
        user=worker, defaults={"key": worker_token_value}
    )
    manager_token, _ = Token.objects.update_or_create(
        user=manager, defaults={"key": manager_token_value}
    )

    print("Worker token:", worker_token.key)
    print("Manager token:", manager_token.key)


if __name__ == "__main__":
    run()
