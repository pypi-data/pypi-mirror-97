from faker import Faker
from scarlet.cache.groups import CacheGroup

fake = Faker()
CACHE_KEY = fake.pystr()

cache_group = CacheGroup(CACHE_KEY)
