import datetime
from django.views.generic import ListView, DetailView, TemplateView, View, UpdateView
from .models import Specialty, Company, Vacancy, Application, Resume
from .forms import MyCompanyForm, MyVacancyForm, MyAuthenticationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import MyUserCreationForm, ApplicationForm, MyResumeForm
from django.shortcuts import render, redirect


class MainView(ListView):
    template_name = 'vacancies/index.html'
    model = Specialty

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['companies'] = Company.objects.all()
        return context


class AllVacanciesView(ListView):
    template_name = 'vacancies/vacancies.html'
    model = Vacancy


class SpecialVacanciesView(ListView):
    template_name = 'vacancies/vacancies.html'
    model = Vacancy

    def get_queryset(self):
        specialty = self.kwargs.get('specialty', None)
        queryset = Vacancy.objects.filter(specialty=Specialty.objects.get(code=specialty))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SpecialVacanciesView, self).get_context_data(**kwargs)
        context['specialty'] = Specialty.objects.filter(
            code=self.kwargs.get('specialty', None))[0].title
        return context


class CompanyView(DetailView):
    template_name = 'vacancies/company.html'
    model = Company


class VacancyView(CreateView):
    template_name = 'vacancies/vacancy.html'
    model = Application
    form_class = ApplicationForm

    def form_valid(self, form):
        application = form.save(commit=False)
        application.user = self.request.user
        application.vacancy = Vacancy.objects.get(
            id=self.request.resolver_match.kwargs.get('pk', None))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(VacancyView, self).get_context_data(**kwargs)
        context['object'] = Vacancy.objects.get(id=int(self.kwargs.get('pk', None)))
        print(context)
        return context

    def get_success_url(self):

        return reverse_lazy('send_vacancy',
                            kwargs={'pk': self.request.resolver_match.kwargs.get('pk')})


class MySignupView(CreateView):
    form_class = MyUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'vacancies/authorization/register.html'


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'vacancies/authorization/login.html'
    form_class = MyAuthenticationForm


class SendView(TemplateView):
    template_name = 'vacancies/sent.html'


class MyCompanyInviteToCreateView(View):

    def get(self, request, *args, **kwargs):
        company = Company.objects.filter(owner=request.user)
        if company:
            return redirect('my_company_update', pk=company.first().id)
        else:
            return render(request, template_name='vacancies/company-create.html')


class MyCompanyCreateView(CreateView):
    template_name = 'vacancies/company-edit.html'
    model = Company
    form_class = MyCompanyForm

    def form_valid(self, form):
        company = form.save(commit=False)
        company.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('my_company_update',
                            kwargs={'pk': Company.objects.filter(
                                owner=self.request.user).first().id})


class MyCompanyUpdateView(UpdateView):
    form_class = MyCompanyForm
    model = Company
    template_name = 'vacancies/company-edit.html'

    def get_success_url(self):
        return reverse_lazy('my_company_update',
                            kwargs={'pk': Company.objects.filter(
                                owner=self.request.user).first().id})


class MyVacanciesListView(ListView):
    model = Vacancy
    template_name = 'vacancies/vacancy-list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MyVacanciesListView, self).get_context_data(**kwargs)
        company = Company.objects.filter(owner=self.request.user)
        if company:
            context['user_vacancies'] = Vacancy.objects.filter(
                company=company[0]).order_by('-published_at')

        context['company'] = company
        print(context)
        return context


class MyVacancyCreateView(CreateView):
    template_name = 'vacancies/vacancy-edit.html'
    model = Vacancy
    form_class = MyVacancyForm
    success_url = reverse_lazy('my_vacancies')

    def form_valid(self, form):
        vacancy = form.save(commit=False)
        vacancy.company = Company.objects.filter(owner=self.request.user).first()
        vacancy.published_at = datetime.datetime.now()
        return super().form_valid(form)


class MyVacancyUpdateView(UpdateView):
    template_name = 'vacancies/vacancy-edit.html'
    model = Vacancy
    form_class = MyVacancyForm

    def get_success_url(self):
        return reverse_lazy('my_vacancy_update',
                            kwargs={'pk': self.request.resolver_match.kwargs.get('pk')})


class SearchView(ListView):
    model = Vacancy
    template_name = 'vacancies/search.html'

    def get_queryset(self):
        arg = self.request.GET.get('query')
        print(arg)
        vacancies = Vacancy.objects.filter(title__icontains=arg)
        return vacancies

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query')
        return context


class MyResumeInviteToCreateView(View):
    def get(self, request, *args, **kwargs):
        resume = Resume.objects.filter(owner=request.user)
        if resume:
            return redirect('my_resume_update', pk=resume.first().id)
        else:
            return render(request, template_name='vacancies/resume-create.html')


class MyResumeCreateView(CreateView):
    template_name = 'vacancies/resume-edit.html'
    model = Resume
    form_class = MyResumeForm

    def form_valid(self, form):
        resume = form.save(commit=False)
        resume.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('my_resume_update',
                            kwargs={'pk': Resume.objects.filter(
                                owner=self.request.user).first().id})


class MyResumeUpdateView(UpdateView):
    template_name = 'vacancies/resume-edit.html'
    model = Resume
    form_class = MyResumeForm

    def get_success_url(self):
        return reverse_lazy('my_resume_update',
                            kwargs={'pk': self.request.resolver_match.kwargs.get('pk')})
