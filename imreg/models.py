import hashlib
import random
import re
import datetime
from django.contrib.auth.models import User

from django.db import models, transaction

from registration.models import RegistrationManager, RegistrationProfile
from django.conf import settings
from django.template.loader import render_to_string

from IM.models import Klient, DaneKontaktowe, Adres


try:
    from django.utils.timezone import now as datetime_now
except ImportError:
    datetime_now = datetime.datetime.now

SHA1_RE = re.compile('^[a-f0-9]{40}$')


class CRegistrationManager(RegistrationManager):
    def activate_user(self, activation_key):
        """
        Basically it does the same as the super.activate_user but
        this action is preceded with creating IM.models.Klient object
        """
        return super(CRegistrationManager, self).activate_user(activation_key)

    def create_inactive_user_im(self,
                                username,
                                firstname,
                                lastname,
                                city,
                                cityPostalCode,
                                cityStreet,
                                cityStreetNumber,
                                phoneNumber,
                                email,
                                password,
                                site,
                                companyName,
                                companyNIP,
                                companyREGON,
                                send_email=True):
        """
        Creates inactive user with persisting IM.models.Klient as well
        """
        self.companyName = companyName
        self.companyNIP = companyNIP
        self.companyREGON = companyREGON

        self.userFN = firstname
        self.userLN = lastname
        self.city = city
        self.cityPostalCode = cityPostalCode
        self.cityStreet = cityStreet
        self.cityStreetNumber = cityStreetNumber

        self.phoneNumber = phoneNumber

        return self.create_inactive_user(username, email, password, site, send_email)

    def create_inactive_user(self, username, email, password, site, send_email=True):
        new_user = User.objects.create_user(
            username=username,
            email=email,
            password=password)
        new_user.is_active = False
        new_user.first_name = self.userFN
        new_user.last_name = self.userLN
        new_user.save()

        client = Klient.objects.create(
            nazwa=username,
            firma=self.companyName,
            nip=self.companyNIP,
            regon=self.companyREGON,
            typ=Klient.STALY
        )
        client.save()

        phoneNumber = DaneKontaktowe.objects.create(
            kontakt=self.phoneNumber,
            typ=DaneKontaktowe.TELEFON,
            klient=client
        )
        phoneNumber.save()

        mail = DaneKontaktowe.objects.create(
            kontakt=new_user.email,
            typ=DaneKontaktowe.MAIL,
            klient=client
        )
        mail.save()

        address = Adres.objects.create(
            miasto=self.city,
            kodPocztowy=self.cityPostalCode,
            ulica=self.cityStreet,
            nrBudynku=self.cityStreetNumber,
            klient=client
        )
        address.save()

        registration_profile = self.create_profile_with_client(new_user, client)

        if send_email:
            registration_profile.send_activation_email(site)

        return new_user

    create_inactive_user = transaction.commit_on_success(create_inactive_user)

    def create_profile_with_client(self, user, client):
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        username = user.username
        if isinstance(username, unicode):
            username = username.encode('utf-8')
        activation_key = hashlib.sha1(salt + username).hexdigest()
        return self.create(user=user,
                           client=client,
                           activation_key=activation_key)

    def delete_expired_users(self):
        """
        Extends custom behavior with removing IM.models.Klient as well
        """
        for profile in self.all():
            if profile.activation_key_expired():
                user = profile.user
                if not user.is_active:
                    object = Klient.objects.get(nazwa=user.username)
                    object.delete()
                    object = Adres.objects.get(nazwa=user.username)
                    object.delete()
                    object = DaneKontaktowe.objects.get(nazwa=user.username)
                    object.delete()
        super(CRegistrationManager, self).delete_expired_users()


class CRegistrationProfile(RegistrationProfile):
    client = models.ForeignKey(Klient, unique=True, verbose_name=u'client')
    objects = CRegistrationManager()

    def send_activation_email(self, site):
        ctx_dict = {'activation_key': self.activation_key,
                    'client': self.client.firma,
                    'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                    'site': site}

        subject = render_to_string('registration/activation_email_subject.txt',
                                   ctx_dict)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())

        message = render_to_string('registration/activation_email.txt',
                                   ctx_dict)

        self.user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)


