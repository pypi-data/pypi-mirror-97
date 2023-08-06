import pandas
import datetime


def get_data() -> str:
    """
    This is where you specify your SQL query for tracking.

    Args:
        track_date (datetime.datetime): the time and date the user was started tracking your insight.

    Returns:
        str: A valid SQL query
    """
    return None  # Must be a SQL string!


def track_kpi(data: pandas.DataFrame, track_date: datetime.datetime) -> str:
    """
    This is where you produce a graph to track your kpi. Make sure you mark a horizontal line
    where the user started to track their insight. 

    Args:
        data (pandas.DataFrame): The result of the get_data query.

        track_date (datetime.datetime): the time and date the user was started tracking your insight. 

    Returns:
        str: A valid html representation of your graph. 

    Hints:
        Graphs from most common plotting librares can be converted to html with a function or method.
        e.g.- Plotly: `html = fig.to_html()'
            - Bokeh: `html = bokeh.embed.file_html(plot, bokeh.resources.CDN, "MyPLot")`

        Maplotlib is a little more involved but this functions should help you:

        ```
        def mpl_to_html(fig: matplotlib.pyplot.figure, html_head: str, html_footer: str) -> str:
            temp_file = io.BytesIO()
            fig.savefig(temp_file, format='png')
            encoded = base64.b64encode(temp_file.getvalue()).decode('utf-8')
            return html_head + '<img src=\'data:image/png;base64,{}\'>'.format(encode) + html_footer
        ```
        Source: https://stackoverflow.com/a/48717971/9327848

    """
    return None
