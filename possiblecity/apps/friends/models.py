from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

from .managers import RelationshipManager, SuggestionManager
from .signals import (
    relationship_accepted,
    relationship_declined,
    relationship_removed,
    relationship_created
)


class Relationship(models.Model):
    
    from_user = models.ForeignKey(User, related_name="+")
    to_user = models.ForeignKey(User, related_name="+")
    created = models.DateTimeField(default=timezone.now)
    accepted = models.DateTimeField(null=True, blank=True)
    
    objects = RelationshipManager()
    
    class Meta:
        unique_together = [("from_user", "to_user")]
    
    def clean(self):
        super(Relationship, self).clean()
        if self.from_user == self.to_user:
            raise ValidationError(
                "User cannot form a relationship with themselves."
            )
        relationship = Relationship.objects.for_users(self.from_user, self.to_user)
        if relationship is not None and relationship != self:
            raise ValidationError(
                "Relationship between {0} and {1} already exists.".format(
                    self.from_user, self.to_user
                )
            )
    
    def save(self, *args, **kwargs):
        self.full_clean()
        if self.pk is None:
            created = True
        else:
            created = False
        relationship = super(Relationship, self).save(*args, **kwargs)
        if created:
            relationship_created.send(
                sender=Relationship,
                relationship=relationship
            )
        return relationship
    
    def accept(self):
        self.accepted = timezone.now()
        self.save()
        self.user = self.from_user
        relationship_accepted.send(
            sender=Relationship,
            relationship=self
        )
    
    def decline(self):
        self.delete()
        relationship_declined.send(
            sender=Relationship,
            relationship=self
        )
    
    def remove(self):
        self.delete()
        relationship_removed.send(
            sender=Relationship,
            relationship=self
        )


class Suggestion(models.Model):
    
    from_user = models.ForeignKey(User, related_name="+")
    to_user = models.ForeignKey(User, related_name="+")
    relationship = models.ForeignKey(Relationship, null=True, blank=True)
    ignored = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    
    objects = SuggestionManager()
    
    class Meta:
        unique_together = [("from_user", "to_user")]
    
    @property
    def reverse_suggestion(self):
        if not hasattr(self, "_reverse_suggestion"):
            qs = Suggestion.objects.filter(from_user=self.to_user, to_user=self.from_user)
            if qs.exists():
                self._reverse_suggestion = qs.get()
        return self._reverse_suggestion
    
    def establish_relationship(self, relationship):
        self.relationship = relationship
        self.save()
        if self.reverse_suggestion:
            self.reverse_suggestion.relationship = relationship
            self.reverse_suggestion.save()
    
    def request(self):
        if self.relationship is not None:
            return
        
        relationship = Relationship.objects.for_users(self.from_user, self.to_user)
        if relationship is not None:
            self.establish_relationship(relationship)
            return
        
        if self.ignored is not None:
            return
        
        relationship = Relationship.objects.create(
            from_user=self.from_user,
            to_user=self.to_user
        )
        self.establish_relationship(relationship)
    
    def ignore(self):
        self.ignored = timezone.now()
        self.save()
