import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px

from src.data_pipeline import DataPipeline


class PlotBuilder:

    def __init__(self, data_pipeline: DataPipeline):
        self.data_pipeline = data_pipeline


    def plot_worldmap(self, debug = False):

        data_conflict = self.data_pipeline.get_data_conflict()

        fig = px.choropleth(data_conflict, locations='alpha-3', color='deaths', hover_name='country',
                            projection='natural earth', animation_frame='year',
                            color_continuous_scale=px.colors.sequential.Burgyl,
                            title='Muertes en conflictos por país')
        if debug:
            fig.show()
        else:
            return fig


    def plot_deaths_by_continent(self, debug=False):

        top10_deaths_by_continent = self.data_pipeline.get_deaths_by_continent()

        fig = px.pie(top10_deaths_by_continent, 
                    values='sum_deaths',
                    names='region',
                    hole=.5, 
                    title='Muertes en conflictos por continente')
        if debug:
            fig.show()
        else:
            return fig

    def plot_deaths_by_region(self, region: str, debug=False):

        deaths_by_region = self.data_pipeline.get_deaths_by_region(region)

        fig = px.pie(deaths_by_region, 
                    values='sum_deaths',
                    names='sub-region',
                    hole=.5, 
                    title=f'Muertes totales en conflictos ({region})')
        if debug:
            fig.show()
        else:
            return fig

    def plot_deaths_br_country(self, debug=False):

        top10_deaths_by_country = self.data_pipeline.get_top10_deaths_by_country()

        fig = px.bar(top10_deaths_by_country, 
                    x="country", 
                    y="sum_deaths", 
                    color='country',
                    labels={
                            "country": "Country",
                            "sum_deaths": "Total deaths"
                        },
                    title="Top 10 Países con más muertes en conflictos"
                )
        fig.update_layout(showlegend=False)
        if debug:
            fig.show()
        else:
            return fig