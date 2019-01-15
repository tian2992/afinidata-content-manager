from django.views.generic import TemplateView


class IndexView(TemplateView):

    template_name = 'static/index.html'


class ContactView(TemplateView):

    template_name = 'static/contact.html'
