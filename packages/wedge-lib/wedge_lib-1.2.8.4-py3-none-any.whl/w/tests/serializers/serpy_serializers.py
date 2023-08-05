from w.serializers import serializer


class RequestResponseSerializer(serializer.SerpySerializer):
    content = serializer.Field()
    success = serializer.Field()
    status_code = serializer.Field()
    redirect_location = serializer.Field()


class MailOutboxSerializer(serializer.SerpySerializer):
    to = serializer.Field()
    bcc = serializer.Field()
    cc = serializer.Field()
    from_email = serializer.Field()
    reply_to = serializer.Field()
    subject = serializer.Field()
    body = serializer.Field()
    content_subtype = serializer.Field()
