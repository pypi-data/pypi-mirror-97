"""Report building from multiple items."""

from collections import OrderedDict
import uuid

from bokeh.embed import components
from bokeh.model import Model
from bokeh.models.sources import ColumnDataSource
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.resources import INLINE
from jinja2 import Template
import markdown
import pkg_resources


class HTMLSection(OrderedDict):
    """A section of a report."""

    def __init__(self, require_keys=False):
        """Initialize the report item collection.

        :param title: report title.
        :param lead: report strapline, shown below title.
        :param require_keys: require keys when adding items.
        """
        self.require_keys = require_keys
        self.plots = list()
        self.md = markdown.Markdown()

    def _add_item(self, item, key=None):
        """Add an item to the report.

        :param item: item to add.
        :param key: unique key for item.
        """
        if key is None:
            if self.require_keys:
                raise ValueError('A key is required.')
            else:
                key = str(uuid.uuid4())
        self[key] = item

    def placeholder(self, key):
        """Add a placeholder to be filled in later."""
        self._add_item(None, key=key)

    def plot(self, plot, key=None):
        """Add a plot to the report.

        :param plot: bokeh plot instance.
        :param key: unique key for item.
        """
        self._add_item(plot, key=key)

    def table(self, df, index=True, key=None, shrink=True, **kwargs):
        """Add a pandas dataframe to the report.

        :param df: pandas dataframe instance.
        :param index: include dataframe index in output.
        :param key: unique key for item.
        :param shrink: shrink wrap the table to avoid whitespace.
        :param kwargs: passed to bokeh DataTable.
        """
        plot = bokeh_table(df, index=index, **kwargs)
        plot.height = min(plot.height, 25*(len(df) + 1))
        self.plot(plot, key)

    def markdown(self, text, key=None):
        """Add markdown formatted text to the report.

        :param text: markdown formatted text.
        :param key: unique key for item.
        """
        if text is None or text == '':
            return
        html = self.md.convert(text)
        self.md.reset()
        self._add_item(html, key=key)


class HTMLReport(HTMLSection):
    """Generate HTML Report from a series of bokeh figures.

    Items added to the report take an optional key argument, adding items
    with the same key allows an update in place whilst maintaining the order
    in which items were added. Items can be grouped into sections for easier
    out of order addition.
    """

    def __init__(self, title="", lead="", require_keys=False):
        """Initialize the report item collection.

        :param title: report title.
        :param lead: report strapline, shown below title.
        :param require_keys: require keys when adding items.
        """
        super().__init__(require_keys=require_keys)
        self.title = title
        self.lead = lead
        self.sections = OrderedDict()
        self.sections['main'] = self
        self.template = Template(
            """\
            <!doctype html>
            <html lang="en">
            <head>
                <meta charset="utf-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                    <title>{{ title }}</title>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">

                    {{ resources }}
                    {{ script }}
                </head>
                <body>
            <div class="container">
              <h1>{{ title }}</h1>
              <p class="lead">{{ lead }}
            {{ div }}
                </body>
            </html>
            """  # noqa
        )

    def add_section(self, key=None):
        """Add a section (grouping of items) to the report.

        :param key: unique key for section.

        :returns: the report section.

        """
        if key is None:
            key = str(uuid.uuid4())
        self.sections[key] = HTMLSection(require_keys=self.require_keys)
        return self.sections[key]

    def render(self):
        """Generate HTML report containing figures."""
        resources = INLINE.render()

        all_divs = list()
        scripts = list()
        for sec_name, section in self.sections.items():
            plot_divs = dict()

            # handle bokeh plots
            plots = {k: v for k, v in section.items() if isinstance(v, Model)}
            if len(plots) > 0:
                script, plots = components(plots)
                scripts.append(script)
                plot_divs.update(plots)

            # nextclade
            for k, v in section.items():
                if isinstance(v, NextClade):
                    scripts.append(v.script)
                    plot_divs[k] = v.div

            # put things together in order
            section_divs = list()
            for k in section.keys():
                try:
                    section_divs.append(plot_divs[k])
                except KeyError:
                    if section[k] is None:
                        raise ValueError(
                            "Placeholder `{}` was not assigned "
                            "a value.".format(k)
                            )
                    section_divs.append(section[k])
            all_divs.extend(section_divs)

        divs = '\n'.join(all_divs)
        script = '\n'.join(scripts)
        return self.template.render(
            title=self.title, lead=self.lead,
            resources=resources, script=script, div=divs)

    def write(self, path):
        """Write html report to file."""
        with open(path, "w", encoding='utf8') as outfile:
            outfile.write(self.render())


class NextClade:
    """A nextclade report component."""

    def __init__(self, json):
        """Initialize a report component.

        :param json: json data output by nextclade
        """
        template = Template(
            """\
            <div>
            <nxt-table>
                <script defer="">
                const data = {{ data }}
                var nxt = document.querySelector('nxt-table')
                nxt.data = data
                </script>
            </nxt-table>
            </div>
            """  # noqa
        )
        self.div = template.render(data=json)

        script = pkg_resources.resource_filename(
            __package__, 'data/nextclade.html')
        with open(script, encoding='utf8') as fh:
            self.script = fh.read()


def bokeh_table(df, index=True, **kwargs):
    """Generate a bokeh table from a pandas dataframe."""
    columns = [TableColumn(field=x, title=x) for x in df.columns]
    if index:
        columns = [TableColumn(field="index", title="Feature")] + columns
    return DataTable(
            columns=columns, source=ColumnDataSource(df), index_position=None,
            **kwargs)
