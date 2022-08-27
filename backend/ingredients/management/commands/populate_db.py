
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

COMMANDS = {
    'populate_ingredients': 'ingredients.csv',
    'populate_tags': 'tags.csv',
}


class Command(BaseCommand):
    help = 'populates db'

    def handle(self, *args, **options):
        for command, csv in COMMANDS.items():
            try:
                call_command(command, csv)
            except Exception as e:
                raise CommandError(
                    f'Cannot run {command} with {csv}. Error: {e}'
                )
        self.stdout.write(self.style.SUCCESS(
            'db is successfully populated with all data needed'
        ))