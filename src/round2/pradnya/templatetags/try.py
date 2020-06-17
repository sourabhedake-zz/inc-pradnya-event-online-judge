from django import template
from datetime import date, timedelta

register = template.Library()

@register.filter(name='cut')
def cut(value, arg):
    return value[arg]


class SetVarNode(template.Node):
 
    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value
 
    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value
        return u""
        
def set_var(parser, token):
    """
        {% set <var_name>  = <var_value> %}
    """
    parts = token.split_contents() 
    return SetVarNode(parts[1], parts[3])
 
register.tag('set', set_var)