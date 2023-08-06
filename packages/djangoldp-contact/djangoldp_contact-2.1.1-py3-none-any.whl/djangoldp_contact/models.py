from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from djangoldp.fields import LDPUrlField
from djangoldp.models import Model
from djangoldp_contact.views import ContactViewSet
from djangoldp_notification.models import Notification


class Contact(Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="contacts", null=True, blank=True)
    contact = LDPUrlField(null=True, blank=True)

    def __str__(self):
        return '{} -> {} ({})'.format(self.user.username, self.contact, self.urlid)

    class Meta(Model.Meta):
        verbose_name = _('contact')
        verbose_name_plural = _("contacts")
        auto_author = 'user'
        owner_field = 'user'
        anonymous_perms = []
        authenticated_perms = ['add']
        owner_perms = ['view', 'delete']
        superuser_perms = []
        unique_together = [['user', 'contact']]
        view_set = ContactViewSet
        rdf_type = "sib:contact"

@receiver(post_save, sender=Notification)
def create_contact_on_notification(sender, instance, created, **kwargs):
    if created:
        if instance.type == "Message":
            Contact.objects.get_or_create(user=instance.user, contact=instance.author)