# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.http import JsonResponse

from tcms.core import forms
from tcms.testcases.forms import CaseCategoryForm
from tcms.testcases.models import TestCaseCategory


__all__ = ('CategoryActions',)


class BaseActions:
    """Base class for all Actions"""

    def __init__(self, request):
        self.request = request
        self.product_id = request.POST.get('product')

    def get_testcases(self):
        from tcms.testcases.views import get_selected_testcases
        return get_selected_testcases(self.request)

    def render_ajax(self, data):
        """Return JSON response"""
        return JsonResponse(data)


class CategoryActions(BaseActions):
    """Category actions used by view function `category`"""

    def __get_form(self):
        self.form = CaseCategoryForm(self.request.POST)
        self.form.populate(product_id=self.product_id)
        return self.form

    def __check_form_validation(self):
        form = self.__get_form()
        if not form.is_valid():
            return 0, self.render_ajax(forms.errors_to_list(form))

        return 1, form

    def __check_perms(self, perm):
        return 1, True

    def update(self):
        is_valid, perm = self.__check_perms('change')
        if not is_valid:
            return perm

        is_valid, form = self.__check_form_validation()
        if not is_valid:
            return form

        category_pk = self.request.POST.get('o_category')
        # FIXME: no exception hanlder when pk does not exist.
        category = TestCaseCategory.objects.get(pk=category_pk)
        # FIXME: lower performance. It's not necessary to update each TestCase
        # in this way.
        tcs = self.get_testcases()
        for tc in tcs:
            tc.category = category
            tc.save()
        return JsonResponse({})

    def render_form(self):
        form = CaseCategoryForm(initial={
            'product': self.product_id,
            'category': self.request.POST.get('o_category'),
        })
        form.populate(product_id=self.product_id)

        return HttpResponse(form.as_p())
