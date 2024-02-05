from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.apps.registry import apps
from django.urls import reverse

from .module.content import ContentModule

content_module = ContentModule(apps.get_app_config('graph_visualizer').data_source_plugins,
                               apps.get_app_config('graph_visualizer').visualizer_plugins)


def index(request):
    context = content_module.get_context()
    context["workspaces"] = [
        {
            "name": "Workspace 1",
            "id": 1
        },
        {
            "name": "Workspace 2",
            "id": 2
        }
    ]

    return render(request, 'index.html', context)


def select_visualizer(request, visualizer_name):
    content_module.select_visualizer(visualizer_name)
    return HttpResponseRedirect(reverse('index'))


def load_views(request):
    # TODO: Load main, bird and tree views
    pass


def search(request, query):
    content_module.search(query)
    return HttpResponseRedirect(reverse('index'))


def provide_data(request):
    if request.method != 'POST':
        return
    kwargs = request.body.decode('utf-8')
    content_module.provide_data(kwargs)
    return HttpResponseRedirect(reverse('index'))


def workspace(request, workspace_id):
    return render(request, 'index.html', {
        "workspaces": [
            {
                "name": "Workspace 1",
                "id": 1
            },
            {
                "name": "Workspace 2",
                "id": 2
            },
        ],
        "visualizers": [
            {
                "name": "Simple visualizer",
                "id": 1
            },
            {
                "name": "Block visualizer",
                "id": 2
            }
        ],
        "main_views": [
            {
                "visualizer_id": 2,
                "html": "<h2>Visualizer 2</h2>",
            },
            {
                "visualizer_id": 1,
                "html": "<h2>Visualizer 1</h2>",
            }
        ],
        "bird_views": [
            {
                "visualizer_id": 2,
                "html": "<h2>Bird view 2</h2>",
            },
            {
                "visualizer_id": 1,
                "html": "<h2>Bird view 1</h2>",
            }
        ]

    })
