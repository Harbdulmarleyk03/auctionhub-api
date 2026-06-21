import factory
from django.utils import timezone
from apps.accounts.tests.factories import UserFactory
from apps.auction.models import Auction, Bid

class AuctionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Auction

    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("paragraph")
    user = factory.SubFactory(UserFactory)
    starting_price = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    current_price = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    start_time = factory.LazyFunction(timezone.now)
    end_time = factory.LazyFunction(lambda: timezone.now() + timezone.timedelta(days=7))

class BidFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Bid

    user = factory.SubFactory(UserFactory)
    auction = factory.SubFactory(AuctionFactory)
    bid_price = factory.Faker(
        "pydecimal", left_digits=4, right_digits=2, positive=True
    )
    created_at = factory.LazyFunction(timezone.now)