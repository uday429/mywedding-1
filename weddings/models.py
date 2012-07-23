from django.db import models


class Invitation(models.Model):
    invite_code = models.CharField(
            help_text="leave it empty, it will be generated automatically on creation of invitation",
            max_length=6)
    invitation_text = models.ForeignKey("InvitationTextTemplate")

    def __unicode__(self):
        return self.invite_code


class InvitationTextTemplate(models.Model):
    name = models.CharField(max_length=150)
    title = models.CharField(max_length=255)
    body = models.TextField()

    def __unicode__(self):
        return self.name


class WeddingGuest(models.Model):
    RSVP_ANSWERS = (
            (0, "Not answered"),
            (1, "Will attend"),
            (2, "Will not attend"),
            (3, "Maybe")
        )

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    invitation = models.ForeignKey('Invitation', blank=True, null=True, on_delete=models.SET_NULL)

    # invited by others
    invited = models.BooleanField(default=False)
    invited_by = models.ForeignKey('WeddingGuest', blank=True, null=True)

    email = models.CharField(max_length=255)

    rsvp_answer = models.PositiveSmallIntegerField(choices=RSVP_ANSWERS, default=0)

    def fullname(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __unicode__(self):
        return "%s %s <%s>" % (self.first_name, self.last_name, self.email)


class CodeGuess(models.Model):
    ip = models.IPAddressField()
    when_tried = models.DateTimeField(auto_now=True, auto_now_add=True)
    guess_code = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return "%s - %s - %s" % (self.when_tried, self.ip, self.guess_code)
