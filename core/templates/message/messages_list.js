{
"sEcho": {{page}},
"iTotalRecords": {{total}},
"iTotalDisplayRecords": {{total}},
"aaData" : [
{%for m in messages%}
[
"{{m.id}}",
"{{ m.title|default:'Без заголовка'}}",
"{{m.messageType__name}}",
"{{m.dateAdd|date:'d.m.Y H:i:s'}}", 
"{{m.subdomain__title|default:'Общее'}}", 
"{{m.status}}",
"{{m.mm_count}}"
{%if forloop.last%}]{%else%}],{%endif%}
{%endfor%}
]
}
