from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView, ListView
from django.shortcuts import redirect
from django.contrib import messages
from random_codes import models
from random_codes import forms


class CodeListView(PermissionRequiredMixin, ListView):
    model = models.Code
    permission_required = 'random_codes.view_code'
    ordering = ['-pk']
    paginate_by = 10


class GenerateCodesView(PermissionRequiredMixin, TemplateView):
    template_name = 'random_codes/generate_code.html'
    permission_required = 'random_codes.add_code'

    def get_context_data(self, **kwargs):
        context = super(GenerateCodesView, self).get_context_data()
        context['form'] = forms.CodesForm()
        return context

    def post(self, request):
        form = forms.CodesForm(request.POST)

        if form.is_valid():
            for i in range(int(form.data['qty'])):
                models.Code.objects.create()
            messages.success(request, "%s codes has been added." % form.data['qty'])
            return redirect('codes:codes')

        else:
            messages.error(request, "Check your data and try again.")
            return super(GenerateCodesView, self).get(request)
