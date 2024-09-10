from django import template

register = template.Library()

# @register.filter(name = "sum_of_attribute")
# def sum_of_attribute(queryset, attribute):
#     return sum(getattr(item, attribute) for item in queryset)



# @register.filter(name = "zip_lists")
# def zip_lists(a, b):
#     """Zips two lists together."""
#     return zip(a, b)

@register.filter
def multiply(value, arg):
    """Multiplies the value by the arg."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0  # Return 0 or some default value in case of an error