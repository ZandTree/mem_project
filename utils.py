from django.utils.text import slugify
from random import choice
import string


# using only uppercase + digits

def make_random_id(chars=(string.ascii_uppercase + string.digits), size=8):
    """
    return string made of random (ascii-chars,digits)of length = size
    """
    output = [choice(chars) for _ in range(size)]
    return "".join(output)


def create_profile_uid(instance):
    """
    create unique id for instance based on random letters and digits
    which have attr = uid
    """
    klass = instance.__class__
    start_unid = make_random_id()
    if klass.objects.filter(unid=start_unid).exists():
        instance.unid = make_random_id()
        return create_profile_uid(instance)
    return start_unid


def generate_random_str(length=4):
    long_str = string.hexdigits
    return "".join([choice(long_str) for i in range(length)])


def generate_unique_unid_slug(instance, new_unid=None):
    """ instance of model with slug attr and char(title)
        named as unid(instead of slug) in order to user
        later the same mixin for views """
    if new_unid is not None:
        unid = new_unid
    else:
        unid = slugify(instance.title)
    Klass = instance.__class__
    if Klass.objects.filter(unid=unid).exists():
        new_unid = unid + generate_random_str()
        return generate_unique_unid_slug(instance, new_unid=new_unid)
    return unid
