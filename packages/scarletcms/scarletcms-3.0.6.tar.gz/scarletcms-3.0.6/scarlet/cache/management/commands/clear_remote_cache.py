from django.core.management.base import BaseCommand

from scarlet.cache.utils import purge_remote_cache


class Command(BaseCommand):
    """
    Command to purge saved pages on remote Cache.
    At the moment only Cloudflare is supported.
    """
    help = "Clear remote (Cloudflare) cache - by url if specified"

    def add_arguments(self, parser):
        parser.add_argument(
            "-u", "--urls", action="append", help="Clear cache only for given URLs",
        )

    def handle(self, *args, **options):
        if options["urls"]:
            success, msg = purge_remote_cache(options["urls"])
        else:
            success, msg = purge_remote_cache()

        if success:
            self.stdout.write(self.style.SUCCESS(msg))
        else:
            self.stderr.write(msg)
