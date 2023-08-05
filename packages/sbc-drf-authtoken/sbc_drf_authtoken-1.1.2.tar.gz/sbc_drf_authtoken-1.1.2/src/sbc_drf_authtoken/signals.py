from django.dispatch import Signal

post_login = Signal(providing_args=['instance', 'masquerade'])
