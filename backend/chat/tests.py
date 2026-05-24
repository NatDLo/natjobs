from rest_framework import status
from rest_framework.test import APITestCase

from chat.models import Conversation
from users.models import User


class ChatApiTests(APITestCase):
    """API tests for conversation list/create/detail permissions and behavior."""

    def create_user(self, username, role, email=None, password="pass12345"):
        if email is None:
            email = f"{username}@example.com"
        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
        )

    def test_list_returns_only_user_conversations(self):
        """Conversation list should include only conversations where user participates."""
        recruiter_a = self.create_user("rec_a_chat", "recruiter")
        seeker_a = self.create_user("seek_a_chat", "seeker")
        recruiter_b = self.create_user("rec_b_chat", "recruiter")
        seeker_b = self.create_user("seek_b_chat", "seeker")

        own = Conversation.objects.create(recruiter=recruiter_a, seeker=seeker_a)
        Conversation.objects.create(recruiter=recruiter_b, seeker=seeker_b)

        self.client.force_authenticate(user=seeker_a)
        response = self.client.get("/api/chat/conversations/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [item["id"] for item in response.data]
        self.assertIn(own.id, ids)
        self.assertEqual(len(response.data), 1)

    def test_participant_can_create_conversation(self):
        """Requester can create conversation only if they are one of participants."""
        recruiter = self.create_user("rec_create_chat", "recruiter")
        seeker = self.create_user("seek_create_chat", "seeker")

        self.client.force_authenticate(user=seeker)
        response = self.client.post(
            "/api/chat/conversations/create/",
            {"recruiter": recruiter.id, "seeker": seeker.id},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Conversation.objects.count(), 1)

    def test_conversation_creation_is_idempotent(self):
        """Creating same recruiter-seeker pair twice should return same conversation."""
        recruiter = self.create_user("rec_idem", "recruiter")
        seeker = self.create_user("seek_idem", "seeker")

        self.client.force_authenticate(user=seeker)
        first = self.client.post(
            "/api/chat/conversations/create/",
            {"recruiter": recruiter.id, "seeker": seeker.id},
            format="json",
        )
        second = self.client.post(
            "/api/chat/conversations/create/",
            {"recruiter": recruiter.id, "seeker": seeker.id},
            format="json",
        )

        self.assertEqual(first.status_code, status.HTTP_200_OK)
        self.assertEqual(second.status_code, status.HTTP_200_OK)
        self.assertEqual(Conversation.objects.count(), 1)
        self.assertEqual(first.data["id"], second.data["id"])

    def test_user_cannot_create_conversation_for_other_people(self):
        """Requester cannot create conversation where they are not a participant."""
        recruiter = self.create_user("rec_private", "recruiter")
        seeker = self.create_user("seek_private", "seeker")
        outsider = self.create_user("outsider_private", "seeker")

        self.client.force_authenticate(user=outsider)
        response = self.client.post(
            "/api/chat/conversations/create/",
            {"recruiter": recruiter.id, "seeker": seeker.id},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_is_visible_only_to_participants(self):
        """Conversation detail queryset should hide records from non-participants."""
        recruiter = self.create_user("rec_detail", "recruiter")
        seeker = self.create_user("seek_detail", "seeker")
        outsider = self.create_user("outsider_detail", "seeker")
        conversation = Conversation.objects.create(recruiter=recruiter, seeker=seeker)

        self.client.force_authenticate(user=seeker)
        ok_response = self.client.get(f"/api/chat/conversations/{conversation.id}/")
        self.assertEqual(ok_response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=outsider)
        hidden_response = self.client.get(f"/api/chat/conversations/{conversation.id}/")
        self.assertEqual(hidden_response.status_code, status.HTTP_404_NOT_FOUND)