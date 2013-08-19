from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from django.contrib.auth.models import User

from .models import Relationship, Suggestion


class RelationshipManagerTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="foo")
        self.user1 = User.objects.create_user(username="foo1")
        self.user2 = User.objects.create_user(username="foo2")
    
    def test_user_has_two_pending_relationships(self):
        Relationship.objects.create(from_user=self.user1, to_user=self.user)
        Relationship.objects.create(from_user=self.user2, to_user=self.user)
        self.assertEquals(Relationship.objects.pending_for_user(self.user).count(), 2)
    
    def test_user_has_two_accepted_relationships(self):
        Relationship.objects.create(from_user=self.user, to_user=self.user1, accepted=timezone.now())
        Relationship.objects.create(from_user=self.user, to_user=self.user2, accepted=timezone.now())
        self.assertEquals(Relationship.objects.accepted_for_user(self.user).count(), 2)
    
    def test_accepted_relationship_has_user_set(self):
        Relationship.objects.create(from_user=self.user, to_user=self.user1, accepted=timezone.now())
        Relationship.objects.create(from_user=self.user2, to_user=self.user, accepted=timezone.now())
        for relationship in Relationship.objects.accepted_for_user(self.user):
            if relationship.to_user == self.user:
                self.assertEquals(relationship.from_user, self.user2)
            if relationship.from_user == self.user:
                self.assertEquals(relationship.to_user, self.user1)
    
    def test_pending_relationship_has_user_set(self):
        Relationship.objects.create(from_user=self.user, to_user=self.user1)
        Relationship.objects.create(from_user=self.user2, to_user=self.user)
        for relationship in Relationship.objects.accepted_for_user(self.user):
            if relationship.to_user == self.user:
                self.assertEquals(relationship.from_user, self.user2)
            if relationship.from_user == self.user:
                self.assertEquals(relationship.to_user, self.user1)
    
    def test_users_are_releated_with_requests(self):
        Relationship.objects.create(from_user=self.user, to_user=self.user1, accepted=timezone.now())
        self.assertTrue(Relationship.objects.are_related(self.user, self.user1))
    
    def test_users_are_releated(self):
        Relationship.objects.create(from_user=self.user, to_user=self.user1)
        self.assertTrue(Relationship.objects.are_related(self.user, self.user1, with_requests=True))
    
    def test_users_are_not_related(self):
        self.assertFalse(Relationship.objects.are_related(self.user, self.user1))
    
    def test_users_are_not_related_request(self):
        Relationship.objects.create(from_user=self.user, to_user=self.user1)
        self.assertFalse(Relationship.objects.are_related(self.user, self.user1))
    
    def test_fetch_relationship_for_two_users(self):
        Relationship.objects.create(from_user=self.user, to_user=self.user2, accepted=timezone.now())
        self.assertIsNotNone(Relationship.objects.for_users(self.user, self.user2))
    
    def test_fetch_relationship_for_two_users_not_exists(self):
        self.assertIsNone(Relationship.objects.for_users(self.user, self.user2))


class RelationshipValidationTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="foo")
        self.user1 = User.objects.create_user(username="foo1")
    
    def test_cannot_create_relationship_with_self(self):
        with self.assertRaises(ValidationError):
            Relationship.objects.create(from_user=self.user, to_user=self.user)
    
    def test_cannot_create_reverse_relationship(self):
        Relationship.objects.create(from_user=self.user1, to_user=self.user)
        with self.assertRaises(ValidationError):
            Relationship.objects.create(from_user=self.user, to_user=self.user1)


class RelationshipMethodTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="foo")
        self.user1 = User.objects.create_user(username="foo1")
        self.relationship = Relationship.objects.create(from_user=self.user, to_user=self.user1)
    
    def test_accept_relationship(self):
        self.relationship.accept()
        self.assertEquals(Relationship.objects.accepted_for_user(self.user).count(), 1)
        self.assertEquals(Relationship.objects.pending_for_user(self.user).count(), 0)
    
    def test_decline_relationship(self):
        self.relationship.decline()
        self.assertEquals(Relationship.objects.accepted_for_user(self.user).count(), 0)
        self.assertEquals(Relationship.objects.pending_for_user(self.user).count(), 0)
    
    def test_remove_relationship(self):
        self.relationship.remove()
        self.assertEquals(Relationship.objects.accepted_for_user(self.user).count(), 0)
        self.assertEquals(Relationship.objects.pending_for_user(self.user).count(), 0)


class SuggestionMethodTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="foo")
        self.user1 = User.objects.create_user(username="foo1")
        self.suggestion = Suggestion.objects.create(from_user=self.user, to_user=self.user1)
        self.suggestion1 = Suggestion.objects.create(from_user=self.user1, to_user=self.user)
    
    def test_valid_reverse_relationship(self):
        self.assertEquals(self.suggestion.reverse_suggestion, self.suggestion1)
        self.assertEquals(self.suggestion1.reverse_suggestion, self.suggestion)
    
    def test_request_when_relationship_already_but_suggestion_used(self):
        relationship = Relationship.objects.create(from_user=self.user, to_user=self.user1)
        self.suggestion.request()
        self.assertEquals(Suggestion.objects.get(pk=self.suggestion.pk).relationship, relationship)
        self.assertEquals(Suggestion.objects.get(pk=self.suggestion1.pk).relationship, relationship)
    
    def test_request_when_relationship_not_already_set(self):
        self.suggestion.request()
        self.assertEquals(self.suggestion.relationship, Suggestion.objects.get(pk=self.suggestion1.pk).relationship)
    
    def test_suggestion_request_creates_pending_request(self):
        self.suggestion.request()
        self.assertEquals(Relationship.objects.pending_for_user(self.user1).count(), 1)
        self.assertEquals(Relationship.objects.requests_for_user(self.user).count(), 1)
    
    def test_request_when_relationship_already_set(self):
        self.suggestion.request()
        suggestion = Suggestion.objects.get(pk=self.suggestion.pk)
        suggestion.request()
        self.assertEquals(Relationship.objects.count(), 1)
        self.assertEquals(suggestion.relationship, self.suggestion.relationship)
    
    def test_ignore(self):
        self.suggestion.ignore()
        self.suggestion.request()
        self.assertEquals(Relationship.objects.count(), 0)
