from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = "Seed default users for each role"
    
    def handle(self, *args, **kwargs):
        groups = ["manager", "user"]
        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f"Group {group_name} created.")
            else:
                self.stdout.write(f"Group {group_name} already exists.")

        users = [
            {
                "username": "manager1",
                "email": "manager1@example.com",
                "group": "manager",
            },
            {
                "username": "user1",
                "email": "user1@example.com",
                "group": "user",
            },
        ]
        
        for data in users:
            if User.objects.filter(username=data['username']).exists():
                self.stdout.write(f"User {data['username']} already exists.")
                continue
            
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password='password'
            )
            
            if data["group"]:
                try:
                    group = Group.objects.get(name=data["group"])
                    user.groups.add(group)
                except Exception as e:
                    self.stdout.write(f"Error adding user {data['username']} to group {data['group']}: {e}")
            self.stdout.write(f"User {data['username']} created and added to group {data['group']}.")