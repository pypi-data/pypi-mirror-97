from djangoldp.views import LDPViewSet


class ContactViewSet(LDPViewSet):

    def is_safe_create(self, user, validated_data, *args, **kwargs):
        try:
            if validated_data['user']['urlid'] == user.urlid:
                return True
        except KeyError:
            # may be in a nested field
            if hasattr(self, 'get_parent'):
                if self.get_parent() == user:
                    return True

        return False
