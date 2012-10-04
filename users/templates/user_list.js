{
    "total": {{total}},
"users":[
{% for u in users %}
[ "{{u.id}}", "{{u.metauser.firstName}}", "{{u.metauser.lastName}}", "{{u.registered|date:'d.m.Y H:i:s'}}", "{{u.last_login|date:'d.m.Y H:i:s'}}", "{{u.active}}"]
{%if forloop.last%}{%else%},{%endif%}
{%endfor%}
]
}
