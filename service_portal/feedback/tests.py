from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Feedback, RequestType
from .forms import FeedbackForm


class FeedbackModelTest(TestCase):
    def setUp(self):
        self.feedback = Feedback.objects.create(
            request_type=RequestType.ISSUE,
            theme="Test Theme",
            full_text="Test full text"
        )

    def test_str_method(self):
        result = str(self.feedback)
        self.assertTrue(result.startswith("issue:"))
        self.assertIn("Test full text", result)

    def test_verbose_name(self):
        self.assertEqual(Feedback._meta.verbose_name, "Обращение")
        self.assertEqual(Feedback._meta.verbose_name_plural, "Обращения")

    def test_ordering(self):
        f1 = Feedback.objects.create(
            request_type=RequestType.WISH,
            theme="Theme1",
            full_text="Text1"
        )
        f2 = Feedback.objects.create(
            request_type=RequestType.WISH,
            theme="Theme2",
            full_text="Text2"
        )
        all_feedbacks = list(Feedback.objects.all())
        self.assertEqual(all_feedbacks[0], f2)
        self.assertEqual(all_feedbacks[1], f1)
        self.assertEqual(all_feedbacks[2], self.feedback)


class FeedbackFormTest(TestCase):
    def test_form_valid_without_file(self):
        form_data = {
            'request_type': RequestType.ISSUE,
            'theme': 'Theme',
            'full_text': 'Some text'
        }
        form = FeedbackForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_valid_with_small_file(self):
        small_file = SimpleUploadedFile(
            'test.txt', b'content', content_type='text/plain'
        )
        form_data = {
            'request_type': RequestType.WISH,
            'theme': 'Theme',
            'full_text': 'Some text'
        }
        form = FeedbackForm(data=form_data, files={'file': small_file})
        self.assertTrue(form.is_valid())

    def test_form_invalid_large_file(self):
        large_content = b'a' * (10 * 1024 * 1024 + 1)
        large_file = SimpleUploadedFile(
            'large.txt', large_content, content_type='text/plain'
        )
        form = FeedbackForm(
            data={
                'request_type': RequestType.WISH,
                'theme': 'Theme',
                'full_text': 'text'
            },
            files={'file': large_file}
        )
        self.assertFalse(form.is_valid())
        self.assertIn('file', form.errors)
        self.assertEqual(
            form.errors['file'], ['Размер файла не должен превышать 10 Мб']
        )


class FeedbackViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.feedback = Feedback.objects.create(
            request_type=RequestType.CLAIM,
            theme="Theme",
            full_text="Detail text"
        )

    def test_list_view(self):
        response = self.client.get(reverse('feedback_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feedback/list.html')
        self.assertIn('feedbacks', response.context)
        self.assertContains(response, self.feedback.theme)

    def test_new_post_get(self):
        response = self.client.get(reverse('feedback_new_post'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feedback/new_post.html')
        self.assertIn('form', response.context)

    def test_new_post_valid(self):
        form_data = {
            'request_type': RequestType.OTHER,
            'theme': 'Th',
            'full_text': 'Some'
        }
        response = self.client.post(reverse('feedback_new_post'), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('feedback_list'))

    def test_new_post_invalid(self):
        form_data = {
            'request_type': '',
            'theme': '',
            'full_text': ''
        }
        response = self.client.post(reverse('feedback_new_post'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feedback/new_post.html')
        self.assertContains(response, 'Форма заполнена некорректно')

    def test_detail_view(self):
        response = self.client.get(
            reverse('feedback_detail', args=[self.feedback.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feedback/detail_view.html')
        self.assertContains(response, self.feedback.full_text)
