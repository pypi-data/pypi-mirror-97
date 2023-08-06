#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import io
import base64
import requests
import os
import warnings

# noinspection PyPackageRequirements
import ipywidgets as widgets

from collections import defaultdict, OrderedDict
from contextlib import redirect_stdout

from dli import connect
from ipywidgets import Layout, HTML
from IPython.core.magic import (Magics, magics_class, line_magic)  # noqa: I900
from IPython import get_ipython  # noqa: I900
from IPython.display import Javascript, display  # noqa: I900


warnings.filterwarnings('ignore')


def help(obj):
    print("This is a " + type(obj).__name__ + "\n" + "*"*20,
        "\nIt has these functions:\n" + "\n".join(
          ["." + method_name for method_name in dir(obj)
                  if callable(getattr(obj, method_name))
           and ((not method_name.startswith("_")) or method_name=='__iter__')])
        ,
        "\n\nIt has these properties:\n" + "\n".join(
          ["." + method_name for method_name in dir(obj)
                  if not callable(getattr(obj, method_name))
           and ((not method_name.startswith("_")) or method_name=='__iter__')])
    + "\n\nAnd it looks like this:\n" + str(obj)
         )


def redirect(fun):
    with io.StringIO() as buf, redirect_stdout(buf):
        try:
            fun()
            output = buf.getvalue()
        except AttributeError:
            output = ""
        return output


def embedded_image(url):
    response = requests.get(url)
    uri = ("data:" +
           response.headers['Content-Type'] + ";" +
           "base64," + str(
                base64.b64encode(response.content).decode('utf-8')))
    return uri


class mockRefresh():

        def __init__(self, msg="Refreshing"):
            self.msg = msg

        def __str__(self):
            return self.msg

        def __repr__(self):
            return self.msg

        def datasets(self):
            return []

        def contents(self):
            return ""

        def shape(self):
            return ""

        def description(self):
            return ""

        @property
        def instances(self):
            class mockInstance():

                def all(self):
                    return []

            return mockInstance()


class SelectorWidget:
    def __init__(self, ipython):
        #  self.evaluate_login()

        self.ipython = ipython
        self._name_counts = defaultdict(lambda: 0)
        self.packages = []
        self.datasets = []
        self.current_obj = None
        self.current_package = None
        self.dl = None
        self.mockrefresh = mockRefresh()
        self.mocknoitems = mockRefresh("No entries")

        html = f'<img src="{embedded_image("https://cdn.ihsmarkit.com/www2/a/p/media/images/ihsmarkit.svg")}" />'
        self.imagery = HTML(html, layout=Layout(width='20%', height='60px'))
        self.env_map = {
            '1':'https://catalogue.datalake.ihsmarkit.com/__api',
            '2':'https://catalogue-uat.datalake.ihsmarkit.com/__api',
            '3':'https://catalogue-qa.udpmarkit.net/__api',
            '4': 'https://catalogue-dev.udpmarkit.net/__api'
        }

        # Widgets ---------------------------------------------------------
        self.api_key = widgets.Text(
            value='',
            placeholder='Enter your api key',
            description='Api key',
            disabled=False,
            layout=Layout(width='100%', height='30px'),
            style={'border-radius': '5px'}
        )

        self.env_dd = widgets.Dropdown(
            options=[('Prod', 1), ('UAT', 2), ('QA', 3), ('DEV', 4)],
            value=1,
            description='Environment',
            disabled=False,
            layout=Layout(width='100%'),
            style={'border-radius': '5px'}
        )

        self.package_dd = widgets.Select(
            options=[],
            description='Packages',
            disabled=False,
            layout=Layout(width='99%', height='100%'),
            style={'border-radius': '5px'}
        )

        self.dataset_dd = widgets.Select(
            options=[],
            description='Datasets',
            disabled=False,
            layout=Layout(width='99%', height='100%')
        )

        self.search_package = widgets.Text(
            value='',
            placeholder='Search Package',
            description='Search:',
            disabled=False,
            style={'border-radius': '5px'},
            layout=Layout(width='99%')
        )

        # self.search_dataset = widgets.Text(
        #     value='',
        #     placeholder='Search Dataset',
        #     description='Search:',
        #     disabled=False,
        #     style={'border-radius': '5px'},
        #     layout=Layout(width='99%')
        # )

        # Buttons ---------------------------------------------------------
        self.connect_button = widgets.Button(
            description='Connect',
            disabled=False,
            button_style='',
            tooltip='Click me',
            icon='check',
            style={'border-radius': '5px'}
        )

        self.to_api_button = widgets.Button(
            description='switch login...',
            disabled=False,
            button_style='',
            tooltip='to api login',
            # icon='check',
            style={'border-radius': '5px'}
        )

        self.to_ccred_button = widgets.Button(
            description='switch login...',
            disabled=False,
            button_style='',
            tooltip='to client credentials login',
            # icon='check',
            style={'border-radius': '5px'}
        )

        self.copy_button = widgets.Button(
            description='Copy current dataset',
            disabled=False,
            button_style='',
            tooltip='Click me',
            icon='check',
            layout=Layout(width='100%', height='30px')
        )

        self.copy_package_button = widgets.Button(
            description='Copy current package',
            disabled=False,
            button_style='',
            tooltip='Click me',
            icon='check',
            layout=Layout(width='100%', height='30px')
        )

        # Dropdowns ---------------------------------------------------------
        self.which_login = widgets.Dropdown(
            options=[('Single sign-on', 1),
                     ('Client credentials', 2),
                     # ('Api key', 3)
                     ],
            value=1,
            button_style='',
            tooltip='to client credentials login',
            icon='check',
            disabled=False,
            layout=Layout(width='15%'),
            style={'border-radius': '5px'}
        )

        self.which_packages = widgets.ToggleButtons(
            options=['Only Mine', 'All Packages'],
            disabled=False,
            button_style='',
            style={'border-radius': '5px'},
            layout=Layout(width='100%', height='10%'),
            description='View',
        )

        # Handlers ---------------------------------------------------------
        self.connect_button.on_click(self.connect_button_handler)
        self.copy_button.on_click(self.copy_button_handler)
        self.copy_package_button.on_click(self.copy_package_button_handler)

        # Observers ---------------------------------------------------------
        self.search_package.observe(self.on_search_package)
        # self.search_dataset.observe(self.on_search_dataset)
        self.package_dd.observe(self.on_change_package)
        self.dataset_dd.observe(self.on_change_dataset)
        self.which_packages.observe(self.on_change_view)

        # Search --------------------------------------------------------
        items = [
            widgets.VBox([self.search_package, self.package_dd], layout=Layout(width='50%')),
            widgets.VBox([self.dataset_dd], layout=Layout(width='50%'))
        ]

        # Results -------------------------------------------------------
        tab_contents = ['print', '.description', '.contents()', '.shape', '__iter__']
        children = [widgets.Textarea(
            value='',
            placeholder='',
            disabled=False,
            layout=Layout(width='100%', height='180px')
        ) for name in tab_contents]
        children2 = [widgets.Textarea(
            value='',
            placeholder='',
            disabled=False,
            layout=Layout(width='100%', height='180px')
        ) for name in tab_contents]

        self.tab = widgets.Tab(
            layout=Layout(width='100%', height='250px'),
        )

        self.tab2 = widgets.Tab(
            layout=Layout(width='100%', height='250px'),
        )

        self.tab.children = children
        self.tab2.children = children2
        [self.tab.set_title(num, name) for num, name in enumerate(tab_contents)]
        [self.tab2.set_title(num, name) for num, name in enumerate(tab_contents)]

        vbox_logo = widgets.VBox([self.imagery])
        login = [widgets.HBox([self.env_dd,self.which_login, self.connect_button])]
        vbox1 = widgets.VBox(login)
        vbox2 = widgets.HBox([items[0], self.tab])
        vbox3 = widgets.HBox([self.which_packages], layout=Layout(width='100%', height='60px'))
        vbox5 = widgets.HBox([items[1], self.tab2], layout=Layout(width='100%'))

        self.root = widgets.VBox([vbox_logo, vbox1, vbox2, vbox3, self.copy_package_button, vbox5, self.copy_button])


    def _generate_name(self, type_):
        while True:
            self._name_counts[type_] = (
                self._name_counts[type_] + 1
            )

            name = '{}_{}'.format(
                type_, self._name_counts[type_]
            )

            if name not in self.ipython.user_global_ns:
                break
            else:
                return self._generate_name(type_)

        return name

    def copy_button_handler(self, obj):
        _name_alias = {
            'StructuredDatasetModel': 'structured_dataset',
            'UnstructuredDatasetModel': 'unstructured_dataset',
        }

        if ('DatasetModel' not in type(self.current_obj).__name__):
            print('Cannot retrieve object currently.')
        else:
            name = self._generate_name(
                _name_alias[type(self.current_obj).__name__]
            )
            self.ipython.user_global_ns[name] = self.current_obj
            encoded_code = base64.b64encode(name.encode()).decode()
            display(Javascript("""
                var code = IPython.notebook.insert_cell_{0}('code');
                code.set_text(atob("{1}"));
            """.format('below', encoded_code)))

    def copy_package_button_handler(self, obj):
        _name_alias = {
            'PackageModel': 'package',
        }

        if (type(self.current_package).__name__ != 'PackageModel' and
            'DatasetModel' not in type(self.current_package).__name__):
            print('Cannot retrieve object currently.')
        else:
            name = self._generate_name(
                _name_alias[type(self.current_package).__name__]
            )
            self.ipython.user_global_ns[name] = self.current_package
            encoded_code = base64.b64encode(name.encode()).decode()
            display(Javascript("""
                var code = IPython.notebook.insert_cell_{0}('code');
                code.set_text(atob("{1}"));
            """.format('below', encoded_code)))


    def on_change_view(self, change):
        if change['type'] == 'change' and change['name'] == 'value':
            self.package_dd.options = [self.mockrefresh]
            self.dataset_dd.options = []

            if change["new"] == 'All Packages':
                self.packages = self.dl.packages()
            else:
                self.packages = self.dl.packages(only_mine=True)

            self.package_dd.options = self.packages
            if len(self.packages.keys()) > 0:
                self.datasets = self.packages[
                    list(self.packages.keys())[0]].datasets()
                self.dataset_dd.options = self.datasets
            else:
                self.package_dd.options = [self.mocknoitems]
                self.dataset_dd.options = [self.mocknoitems]

    def start_api_session(self):
        self.dl = connect(
            self.api_key.value,
            root_url=self.env_map[str(self.env_dd.value)]
        )

    def start_clientcred_session(self):
        user = os.environ.get("DLI_ACCESS_KEY_ID")
        pasw = os.environ.get("DLI_SECRET_ACCESS_KEY")
        if user is not None and pasw is not None:
            self.dl = connect(root_url=self.env_map[str(self.env_dd.value)])
        else:
            print(f'Set DLI_ACCESS_KEY_ID and DLI_SECRET_ACCESS_KEY '
                  f'environment variables for client credentials login, '
                  f'alternatively use the api/web flow.')

    def start_web_session(self):
        self.dl = connect(root_url=self.env_map[str(self.env_dd.value)])

    def connect_button_handler(self, obj):
        login_options = {'1': self.start_web_session,
                         '2': self.start_clientcred_session,
                         '3': self.start_api_session,
                         }
        try:
            login_options[str(self.which_login.value)].__call__()
        except Exception as e:
            print(f'Session was not started. {e}')

        if self.dl is not None:
            self.packages = self.dl.packages()
            self.package_dd.options = self.packages
            if len(self.packages.keys()) > 0:
                self.datasets = self.packages[list(self.packages.keys())[0]].datasets()
                self.dataset_dd.options = self.datasets
            else:
                self.package_dd.options = [self.mocknoitems]
                self.dataset_dd.options = [self.mocknoitems]

    def on_change_package(self, change):
        if change['type'] == 'change' and change['name'] == 'value':
     
            self.current_package = change["new"]
            if self.current_package is not None:
                self.dataset_dd.options = self.current_package.datasets()
            if self.current_package:
                self.tab.children[2].value = redirect(self.current_package.contents)
                self.tab.children[3].value = str(self.current_package.shape)
                self.tab.children[1].value = str(self.current_package.description)
                self.tab.children[0].value = str(self.current_package.__str__())
                self.tab.children[4].value = "\n".join([str(x) for x in
                                                   self.current_package.datasets()])

    def on_change_dataset(self, change):
        if change['type'] == 'change' and change['name'] == 'value':
            self.current_obj = change["new"]

            if self.current_obj:
                self.tab2.children[2].value = redirect(self.current_obj.contents)
                self.tab2.children[3].value = ""
                self.tab2.children[1].value = ""
                self.tab2.children[0].value = str(self.current_obj.__str__())
                if hasattr(self.current_obj, "instances"):
                    try:
                        self.tab2.children[4].value = "\n".join([str(x) for x in
                                                           self.current_obj.instances.all()])
                    except:
                        self.tab2.children[4].value = ""
                else:
                    self.tab2.children[4].value = ""

    def on_search_package(self, change):
        if change['type'] == 'change' and change['name'] == 'value':
            self.current_package = change["new"]
            if self.current_package:
                lst = list(filter((lambda x: self.current_package.lower() in x[0].lower()),
                                  self.packages.items()))
                if len(lst) > 0:
                    try:
                        self.package_dd.options = OrderedDict(lst)
                        self.dataset_dd.options = lst[0][1].datasets()
                    except Exception as e:
                        print(e)
                else:
                    self.package_dd.options = [self.mocknoitems]
                    self.dataset_dd.options = [self.mocknoitems]
            else:
                self.package_dd.options = self.packages
                first = self.packages[list(self.packages.keys())[0]]
                self.dataset_dd.options = first.datasets()

    def on_search_dataset(self, change):
        if change['type'] == 'change' and change['name'] == 'value':
            self.current_obj = change["new"]
            if self.current_obj:
                lst = list(filter((lambda x: self.current_obj.lower() in x[0].lower()),
                                  self.datasets))
                if len(lst) > 0:
                    self.dataset_dd.options = OrderedDict(lst)
                else:
                    self.dataset_dd.options = [self.mocknoitems]
            else:
                self.dataset_dd.options = self.datasets


@magics_class
class DatasetSelectorMagic(Magics):

    @line_magic
    def dataset_selector(self, line):
        disp = SelectorWidget(self.parent)
        self.parent.user_global_ns['_widget'] = disp
        display(disp.root)


def load_ipython_extension(ipython):
    # The `ipython` argument is the currently active `InteractiveShell`
    # instance, which can be used in any way. This allows you to register
    # new magics or aliases, for example.
    ipython.register_magics(DatasetSelectorMagic)


def unload_ipython_extension(ipython):
    # If you want your extension to be unloadable, put that logic here.
    pass


test = {}


def show():
    get_ipython().magic('dataset_selector')


if __name__ != '__main__':
    get_ipython().extension_manager.load_extension('dli.gui')
    show()