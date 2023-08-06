import idk
from idk.insight import InsightGenerator
from idk.io import InsightData
import pandas as pd


class _DeveloperInsight_(InsightGenerator):

    def __init__(self, context: dict = None, *args, **kwargs):
        """
        Args:
            context (dict, optional): A dict where keys correspond to those given in context.json, values are provided
                dynamically by insights engine. E.g. if you specify in context.json, '{"customerCodes": [1]}' then this 
                gives users the option to specify any customer code they have access to as input to this insight.
                Defaults to None.
        """
        super().__init__(*args, **kwargs)
        self.context = context  # Available to your other methods

    def define_query(self) -> str:
        """This is where the you define the query that fetches the nessecary data.

        Avaliable Tables:
            data_table: This table contains all the data that the end user has permission to see. Be mindfulk fo this when writing insights; the amount of data your code receive can change a lot. Try and write your insight to handle that.

            fs_total_spend: This tables contains... blah blah

        Returns:
            str: a SQL query.

        Example:
        ```
            class MyInsight(idk.insight.InsightGenerator):
                def define_query(self):
                    return "SELECT * FROM data_table"
        ```
        [REQUIRED] You must implement this method.
        """
        return None  # Your query building code here!

    def transform(self, data: pd.DataFrame) -> InsightData:
        """This is where you transform the data from your get_data query into a actionable insight.


        Args:
            data (pd.DataFrame): Contains the results of the query built in 

        Returns:
            idk.io.InsightData: A container class to pass data to the system. For details see it's doc string in io.py.

        Hints:
        Special attention here must be paid to calculating the statistical "significance" of your result. When the significance measure is
        accuratly placed between 0 and 1, it helps the system decide when to pass your insight to a user.

        [REQUIRED] You must implement this method.
        """

        return InsightData(
            # It can be useful to automatically tag your insights contents, think subjects and entities
            tags=[],
            # From 0-1, how important is the data generated in this insight relative to other instances of the same insight?
            significance=0.0,
            data=dict(),            # This where you store the data you've generated and you want to pass to your transcribe function in ./transcription/transcribe.py
        )

    def provide_evidence(self, data: pd.DataFrame) -> str:
        """This function is where you can provide evidence of your insights correctness as a data plot. The main aim of this plot
        is to convince your targeted user that your insight is accurate enough for them to action on.

        Args:
            data (pd.DataFrame): The same data that is passed to the transform function.

        Returns:
            str: An embedable HTML of a graph.

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
        Source: https://stackoverflow.com/a/48717971/9327848 (altered)

        [OPTIONAL] You need to provide this evidence piece for it to go into production.
        """
