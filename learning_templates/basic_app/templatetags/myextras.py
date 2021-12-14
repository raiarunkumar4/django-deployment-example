from django import template

register = template.Library()

@register.filter(name='mycut')
def mycut(value,arg):
    """
    This cuts out all values of "arg" from the string!
    """
    return value.replace(arg,'')

# register.filter('mycut', mycut)
