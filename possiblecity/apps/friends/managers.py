from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q


class RelationshipManager(models.Manager):
    
    def are_related(self, u1, u2, **kwargs):
        """
        Validates that two users have a relationship or not
        """
        extra = {
            "accepted__isnull": kwargs.get("with_requests", False)
        }
        return self.filter(
            Q(from_user=u1, to_user=u2, **extra) | Q(to_user=u2, from_user=u1, **extra)
        ).exists()
    
    def accepted_for_user(self, user):
        """
        Returns a queryset of all accepted relationships for `user`
        """
        relationships = self.filter(
            accepted__isnull=False
        ).filter(
            Q(from_user=user) | Q(to_user=user)
        )
        for relationship in relationships:
            if relationship.to_user == user:
                relationship.user = relationship.from_user
            else:
                relationship.user = relationship.to_user
        return relationships
    
    def pending_for_user(self, user):
        """
        Returns a queryset of all pending relationships for `user`
        """
        relationships = self.filter(accepted__isnull=True).filter(to_user=user)
        for relationhip in relationships:
            relationhip.user = relationhip.from_user
        return relationships
    
    def requests_for_user(self, user):
        """
        Returns a queryset of all requested relationships for `user`
        """
        relationships = self.filter(accepted__isnull=True).filter(from_user=user)
        for relationship in relationships:
            relationship.user = relationship.to_user
        return relationships
    
    def for_users(self, u1, u2):
        """
        Returns a relationship, regardless of acceptance, for the two users
        """
        try:
            r = self.filter(
                Q(from_user=u1, to_user=u2) | Q(from_user=u2, to_user=u1)
            ).select_related(depth=1).get()
        except ObjectDoesNotExist:
            r = None
        return r


class SuggestionManager(models.Manager):
    
    def create_suggestions(self, user1, user2):
        suggest1, _ = self.get_or_create(
            from_user=user1,
            to_user=user2
        )
        suggest2, _ = self.get_or_create(
            from_user=user2,
            to_user=user1
        )
        return (suggest1, suggest2)
    
    def filter(self, *args, **kwargs):
        qs = super(SuggestionManager, self).filter(*args, **kwargs)
        return qs.exclude(relationship__isnull=False)
    
    def ignored(self):
        return self.filter(ignored__isnull=False)
    
    def active(self):
        return self.filter(ignored__isnull=True)
    
    def for_user(self, user):
        return self.active().filter(from_user=user)
