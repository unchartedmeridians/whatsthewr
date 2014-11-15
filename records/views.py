import pdb
import json
import string

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator
from records.models import Game, Record, Category
from records.forms import RecordForm


class BrowseView(ListView):
    model = Game
    template_name = 'browse.html'
    context_object_name = 'game_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(BrowseView, self).get_context_data(**kwargs)
        page = context.get('page_obj').number or 1
        paginator = context.get('paginator')
        context['pages'] = \
            range(max(1, page-2), min(page+3, paginator.num_pages + 1))
        context['letter'] = self.kwargs.get('letter') or 'a'
        context['letter'] = context['letter'].lower()
        context['letters'] = \
            [char for char in string.ascii_lowercase] + ['num']
        return context

    def get_queryset(self):
        letter = self.kwargs.get('letter') or 'a'
        queryset = super(BrowseView, self).get_queryset()
        if letter == 'num':
            return queryset.filter(name__regex=r'^\d.*')
        else:
            return queryset.filter(name__istartswith=letter)

class PendingView(ListView):
    model = Record
    template_name = 'pending.html'
    context_object_name = 'pending_list'
    paginate_by = 10

    def get_queryset(self):
        return super(PendingView, self).get_queryset().filter(approved=False)

class ListLatest(ListView):
    model = Record
    template_name = 'index.html'
    context_object_name = 'record_list'
    paginate_by = 5

    def get_queryset(self):
        return super(ListLatest, self).get_queryset().filter(approved=True)

    def get_context_data(self, **kwargs):
        context = super(ListLatest, self).get_context_data(**kwargs)
        page = context.get('page_obj').number or 1
        paginator = context.get('paginator')
        context['pages'] = \
            range(max(1, page-2), min(page+3, paginator.num_pages + 1))
        return context

class SubmitView(CreateView):
    template_name = 'submit.html'
    form_class = RecordForm
    success_url = '/submit/success'

    def post(self, request, *args, **kwargs):
        post_data = request.POST.copy()
        if 'category-choice' in post_data:
            if post_data['category-choice'] == 'new':
                post_data['category'] = post_data['new-category']
            else:
                post_data['category'] = post_data['category-choice']
        request.POST = post_data
        return super(SubmitView, self).post(request, *args, **kwargs)

    def get_initial(self):
        initial = super(CreateView, self).get_initial()
        initial['game_as_text'] = self.kwargs.get('game') or ""
        initial['category_as_text'] = self.kwargs.get('category') or ""
        return initial

    def form_valid(self, form):
        form.instance.submitted_by_ip = self.request.META['REMOTE_ADDR']
        if self.request.user.is_authenticated():
            form.instance.submitted_by = self.request.user
        return super(SubmitView, self).form_valid(form)

# View for retrieving the AJAX data for autocompletion of the Category field
def ajax_category_autocomplete(request):
    if 'term' in request.GET:
        try:
            categories = \
                    [cat.name for cat in Game.objects
                     .get(name__iexact=request.GET['term'])
                     .category_set.order_by('tab_index')]
        except Game.DoesNotExist:
            categories = []
            return HttpResponse()
    return HttpResponse(json.dumps(categories))

# View for retrieving the AJAX data for autocompletion of the Game field
def ajax_game_autocomplete(request):
    results = {}
    if 'term' in request.GET:
        results['games'] = [game.name for game in Game.objects.filter(
            name__istartswith=request.GET['term'])[:5]]
        return HttpResponse(json.dumps(results))
    return HttpResponse()

def record(request, game_name, category):
    game = get_object_or_404(Game, name__iexact=game_name)
    categories = [cat for cat in game.category_set.order_by('tab_index')]
    if category:
        record = get_object_or_404(Record,
                                   category__name__iexact=category, game=game)
    else:
        record = Record.objects.get(category=categories[0])

    context = { 'game': game, 'record': record, 'categories': categories }
    return render(request, 'record.html', context)
