from django import template

register = template.Library()


@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})


@register.simple_tag
def checkvote(obj, user_id, action):
    return obj.votes.exists(user_id, action)


@register.simple_tag
def votecount(obj):
    return obj.votes.count(action=0) - obj.votes.count(action=1)



