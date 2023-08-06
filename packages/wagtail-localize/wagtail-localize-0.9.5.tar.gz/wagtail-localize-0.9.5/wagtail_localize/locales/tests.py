from django.contrib.messages import get_messages
from django.test import TestCase, override_settings
from django.urls import reverse

from wagtail.core.models import Locale
from wagtail.tests.utils import WagtailTestUtils

from wagtail_localize.models import LocaleSynchronization
from wagtail_localize.locales.components import LOCALE_COMPONENTS


@override_settings(WAGTAIL_CONTENT_LANGUAGES=[("en", "English"), ("fr", "French")])
class TestLocaleIndexView(TestCase, WagtailTestUtils):
    def setUp(self):
        self.login()

    def get(self, params={}):
        return self.client.get(reverse('wagtaillocales:index'), params)

    def test_simple(self):
        response = self.get()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wagtaillocales/index.html')


@override_settings(WAGTAIL_CONTENT_LANGUAGES=[("en", "English"), ("fr", "French")])
class TestLocaleCreateView(TestCase, WagtailTestUtils):
    def setUp(self):
        self.login()
        self.english = Locale.objects.get()

    def get(self, params={}):
        return self.client.get(reverse('wagtaillocales:add'), params)

    def post(self, post_data={}):
        return self.client.post(reverse('wagtaillocales:add'), post_data)

    def test_default_language(self):
        # we should have loaded with a single locale
        self.assertEqual(self.english.language_code, 'en')
        self.assertEqual(self.english.get_display_name(), "English")

    def test_simple(self):
        response = self.get()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wagtaillocales/create.html')

        self.assertEqual(response.context['form'].fields['language_code'].choices, [
            ('fr', 'French')
        ])

    def test_create(self):
        response = self.post({
            'language_code': "fr",
            'component-wagtail_localize_localesynchronization-enabled': 'on',
            'component-wagtail_localize_localesynchronization-sync_from': self.english.id,
        })

        # Should redirect back to index
        self.assertRedirects(response, reverse('wagtaillocales:index'))

        # Check that the locale was created
        self.assertTrue(Locale.objects.filter(language_code='fr').exists())

        # Check the sync_from was set
        self.assertTrue(LocaleSynchronization.objects.filter(locale__language_code='fr', sync_from__language_code='en').exists())

    def test_duplicate_not_allowed(self):
        response = self.post({
            'language_code': "en",
            'component-wagtail_localize_localesynchronization-enabled': 'on',
            'component-wagtail_localize_localesynchronization-sync_from': self.english.id,
        })

        # Should return the form with errors
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'language_code', ['Select a valid choice. en is not one of the available choices.'])

    def test_language_code_must_be_in_settings(self):
        response = self.post({
            'language_code': "ja",
            'component-wagtail_localize_localesynchronization-enabled': 'on',
            'component-wagtail_localize_localesynchronization-sync_from': self.english.id,
        })

        # Should return the form with errors
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'language_code', ['Select a valid choice. ja is not one of the available choices.'])

    def test_sync_from_required_when_enabled(self):
        response = self.post({
            'language_code': "fr",
            'component-wagtail_localize_localesynchronization-enabled': 'on',
            'component-wagtail_localize_localesynchronization-sync_from': '',
        })

        # Should return the form with errors
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'component_form', 'sync_from', ['This field is required.'])

        # Check that the locale was not created
        self.assertFalse(Locale.objects.filter(language_code='fr').exists())

    def test_sync_from_not_required_when_disabled(self):
        response = self.post({
            'language_code': "fr",
            'component-wagtail_localize_localesynchronization-enabled': '',
            'component-wagtail_localize_localesynchronization-sync_from': '',
        })

        # Should redirect back to index
        self.assertRedirects(response, reverse('wagtaillocales:index'))

        # Check that the locale was created
        self.assertTrue(Locale.objects.filter(language_code='fr').exists())

        # Check the sync_from was not set
        self.assertFalse(LocaleSynchronization.objects.exists())

    def test_sync_from_required_when_component_required(self):
        LOCALE_COMPONENTS[0]['required'] = True
        try:
            response = self.post({
                'language_code': "fr",
                'component-wagtail_localize_localesynchronization-enabled': '',
                'component-wagtail_localize_localesynchronization-sync_from': '',
            })
        finally:
            LOCALE_COMPONENTS[0]['required'] = False

        # Should return the form with errors
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'component_form', 'sync_from', ['This field is required.'])

        # Check that the locale was not created
        self.assertFalse(Locale.objects.filter(language_code='fr').exists())


@override_settings(WAGTAIL_CONTENT_LANGUAGES=[("en", "English"), ("fr", "French")])
class TestLocaleEditView(TestCase, WagtailTestUtils):
    def setUp(self):
        self.login()
        self.english = Locale.objects.get()

    def get(self, params=None, locale=None):
        locale = locale or self.english
        return self.client.get(reverse('wagtaillocales:edit', args=[locale.id]), params or {})

    def post(self, post_data=None, locale=None):
        post_data = post_data or {}
        locale = locale or self.english
        post_data.setdefault('language_code', locale.language_code)
        return self.client.post(reverse('wagtaillocales:edit', args=[locale.id]), post_data)

    def test_simple(self):
        response = self.get()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wagtaillocales/edit.html')

        self.assertEqual(response.context['form'].fields['language_code'].choices, [
            ('en', 'English'),  # Note: Current value is displayed even though it's in use
            ('fr', 'French')
        ])

    def test_invalid_language(self):
        invalid = Locale.objects.create(language_code='foo')

        response = self.get(locale=invalid)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wagtaillocales/edit.html')

        self.assertEqual(response.context['form'].fields['language_code'].choices, [
            (None, 'Select a new language'),  # This is shown instead of the current value if invalid
            ('fr', 'French')
        ])

    def test_edit(self):
        response = self.post({
            'language_code': 'fr',
            'component-wagtail_localize_localesynchronization-enabled': 'on',
            'component-wagtail_localize_localesynchronization-sync_from': self.english.id,
        })

        # Should redirect back to index
        self.assertRedirects(response, reverse('wagtaillocales:index'))

        # Check that the locale was edited
        self.english.refresh_from_db()
        self.assertEqual(self.english.language_code, 'fr')

    def test_edit_duplicate_not_allowed(self):
        french = Locale.objects.create(language_code='fr')

        response = self.post({
            'language_code': "en",
            'component-wagtail_localize_localesynchronization-enabled': 'on',
            'component-wagtail_localize_localesynchronization-sync_from': self.english.id,
        }, locale=french)

        # Should return the form with errors
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'language_code', ['Select a valid choice. en is not one of the available choices.'])

    def test_edit_language_code_must_be_in_settings(self):
        response = self.post({
            'language_code': "ja",
            'component-wagtail_localize_localesynchronization-enabled': 'on',
            'component-wagtail_localize_localesynchronization-sync_from': self.english.id,
        })

        # Should return the form with errors
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'language_code', ['Select a valid choice. ja is not one of the available choices.'])

    def test_sync_from_required_when_enabled(self):
        response = self.post({
            'language_code': "fr",
            'component-wagtail_localize_localesynchronization-enabled': 'on',
            'component-wagtail_localize_localesynchronization-sync_from': '',
        })

        # Should return the form with errors
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'component_form', 'sync_from', ['This field is required.'])

    def test_sync_from_not_required_when_disabled(self):
        response = self.post({
            'language_code': "fr",
            'component-wagtail_localize_localesynchronization-enabled': '',
            'component-wagtail_localize_localesynchronization-sync_from': '',
        })

        # Should redirect back to index
        self.assertRedirects(response, reverse('wagtaillocales:index'))

        # Check that the locale was edited
        self.english.refresh_from_db()
        self.assertEqual(self.english.language_code, 'fr')

    def test_sync_from_required_when_component_required(self):
        LOCALE_COMPONENTS[0]['required'] = True
        try:
            response = self.post({
                'language_code': "fr",
                'component-wagtail_localize_localesynchronization-enabled': '',
                'component-wagtail_localize_localesynchronization-sync_from': '',
            })
        finally:
            LOCALE_COMPONENTS[0]['required'] = False

        # Should return the form with errors
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'component_form', 'sync_from', ['This field is required.'])


@override_settings(WAGTAIL_CONTENT_LANGUAGES=[("en", "English"), ("fr", "French")])
class TestLocaleDeleteView(TestCase, WagtailTestUtils):
    def setUp(self):
        self.login()
        self.english = Locale.objects.get()

    def get(self, params={}, locale=None):
        locale = locale or self.english
        return self.client.get(reverse('wagtaillocales:delete', args=[locale.id]), params)

    def post(self, post_data={}, locale=None):
        locale = locale or self.english
        return self.client.post(reverse('wagtaillocales:delete', args=[locale.id]), post_data)

    def test_simple(self):
        response = self.get()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wagtailadmin/generic/confirm_delete.html')

    def test_delete_locale(self):
        french = Locale.objects.create(language_code='fr')

        response = self.post(locale=french)

        # Should redirect back to index
        self.assertRedirects(response, reverse('wagtaillocales:index'))

        # Check that the locale was deleted
        self.assertFalse(Locale.objects.filter(language_code='fr').exists())

    def test_cannot_delete_locales_with_pages(self):
        response = self.post()

        self.assertEqual(response.status_code, 200)

        # Check error message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(messages[0].level_tag, 'error')
        self.assertEqual(messages[0].message, "This locale cannot be deleted because there are pages and/or other objects using it.\n\n\n\n\n")

        # Check that the locale was not deleted
        self.assertTrue(Locale.objects.filter(language_code='en').exists())
