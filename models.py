from django.db import models
from django.contrib.auth.models import User as DjangoUser


class Craft(models.Model):
    """Trumpet, Principal Trumpet, Electrician, Short Stop, etc."""
    name = models.CharField(max_length=127)

    def __unicode__(self):
        return self.name


# TODO There's probably a nice Django document on extending their user model
# for when you need to add additional properties.  What we've got here, at is
# quirky when using the admin site.
class User(DjangoUser):
    """Let's expand Django's User model with some things we need."""
    crafts = models.ManyToManyField(Craft, related_name='users')


class Project(models.Model):
    """A series of Services"""
    name = models.CharField(max_length=127)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class Service(models.Model):
    """Any time a collection of users must show up"""
    project = models.ForeignKey('Project', related_name='services')
    type = models.ForeignKey('ServiceType', related_name='services')
    start = models.DateTimeField()
    end = models.DateTimeField()
    venue = models.ForeignKey('Venue', related_name='services')
    craft_requirements = models.ManyToManyField('Craft', through='ServiceCraft', related_name='services')
    personnel = models.ManyToManyField(User, through='Commitment', related_name='services')
    dress = models.ForeignKey('Dress', related_name='services', null=True)

    def __unicode__(self):
        return self.project.name + '.' + self.start.ctime()


class ServiceType(models.Model):
    """Rehearsal, Concert, Parade, Competition, etc."""
    name = models.CharField(max_length=127)

    def __unicode__(self):
        return self.name


class Dress(models.Model):
    """Tails, Tux, White Jacket, Summer Outdoor, etc."""
    name = models.CharField(max_length=127)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class ServiceCraft(models.Model):
    """
    Represents a requirement for a certain number of people performing the
    craft to be at the service
    """
    craft = models.ForeignKey('Craft', related_name='service_crafts')
    service = models.ForeignKey('Service', related_name='service_crafts')
    number = models.PositiveIntegerField()


class Commitment(models.Model):
    """Represents a user being hired for a service as a result of a proposal"""
    service = models.ForeignKey('Service', related_name='commitments')
    user = models.ForeignKey(User, related_name='commitments')
    proposal = models.ForeignKey('Proposal', related_name='commitments')

    def __unicode__(self):
        return self.name


class Venue(models.Model):
    name = models.CharField(max_length=127)
    directions = models.TextField()

    def __unicode__(self):
        return self.name


class Proposal(models.Model):
    crafts = models.ManyToManyField('Craft', related_name='proposals')
    sender = models.ForeignKey(User, related_name='proposals')
    accepted = models.BooleanField(default=False)
    services = models.ManyToManyField('Service', related_name='proposals')
    pay = models.DecimalField(max_digits=15, decimal_places=2)
    preceeding_proposal = models.OneToOneField('Proposal', related_name='following_proposal', null=True)
    notes = models.TextField()
    # TODO Should a proposal have a recipient?
