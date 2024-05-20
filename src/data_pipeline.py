import numpy as np
import pandas as pd

from src.utils import clean_abrv
from src.params import list_regions

class DataPipeline:

    def __init__(self, CONFLICT_DATA_PATH, ISO_CODE_PATH):

        self.CONFLICT_DATA_PATH = CONFLICT_DATA_PATH
        self.ISO_CODE_PATH = ISO_CODE_PATH

        self.data_conflict = self.build_data_conflict(
            self.CONFLICT_DATA_PATH, 
            self.ISO_CODE_PATH
        )



    
    def build_data_conflict(self, CONFLICT_DATA_PATH, ISO_CODE_PATH):

        # read conflict data
        df_conflict = pd.read_csv(CONFLICT_DATA_PATH)
        df_conflict.columns = ['country', 'alpha-3', 'year', 'deaths']
        df_conflict['alpha-3'] = df_conflict['alpha-3'].apply(lambda row: clean_abrv(row))

        # read iso and region data
        df_iso = pd.read_csv(ISO_CODE_PATH)
        df_iso = df_iso[['alpha-3', 'region', 'sub-region']]
        df_iso.columns = ['alpha-3', 'region', 'sub-region']

        # merge
        data_conflict = df_conflict.merge(df_iso, on = ['alpha-3'], how = 'left')
        data_conflict = data_conflict.dropna()
        data_conflict = data_conflict[['country', 'alpha-3', 'region', 'sub-region', 'year', 'deaths']]

        # year with conflict column
        data_conflict['year_conflict'] = data_conflict['deaths'].apply(
            lambda row: 1 if row > 0 else 0)
        data_conflict.sort_values(['country', 'year'], inplace=True)

        # deaths cumsum
        list_cumsum = []
        for country in data_conflict['country'].unique():
            sub_df = data_conflict[data_conflict['country'] == country].copy()
            # print(sub_df)
            sub_df['death_cumsum'] = sub_df['deaths'].cumsum()
            list_cumsum.append(sub_df)

        data_conflict = pd.concat(list_cumsum)

        return data_conflict

    def get_data_conflict(self):

        return self.data_conflict

    def get_chart_race_data(self):

        chart_race_data = pd.pivot_table(
            self.get_data_conflict(), 
            values='death_cumsum', 
            index=['year'],
            columns=['country']
        )

        return chart_race_data
    

    def get_deaths_by_continent(self):

        deaths_by_continent = (self.data_conflict
            .groupby('region')
            .agg(sum_deaths=('deaths', 'sum'))
            .reset_index()
            .sort_values('sum_deaths', ascending=False)
            .reset_index(drop=True)
            .head(10)
        )

        return deaths_by_continent
    

    def get_deaths_by_region(self, region):
        
        deaths_by_subregion = (self.data_conflict[self.data_conflict['region'] == region]
            .groupby('sub-region')
            .agg(sum_deaths=('deaths', 'sum'))
            .reset_index()
            .sort_values('sum_deaths', ascending=False)
            .reset_index(drop=True)
        )

        return deaths_by_subregion
    

    def get_top10_deaths_by_country(self):

        top10_deaths_by_country = (self.data_conflict
            .groupby('country')
            .agg(sum_deaths=('deaths', 'sum'))
            .reset_index()
            .sort_values('sum_deaths', ascending=False)
            .reset_index(drop=True)
            .head(10)
        )
        
        return top10_deaths_by_country
    

    def get_worst_conflict_years(self):

        list_countries = self.data_conflict['country'].unique()
        worst_conflict_years = []

        for country in list_countries:

            mask_country = self.data_conflict['country'] == country
            selected_columns = ['country', 'year', 'deaths']

            df_country = (
                self.data_conflict[mask_country][selected_columns]
                    .copy()
                    .sort_values('deaths', ascending=False)
                    .head(1)
            )
            worst_conflict_years.append(df_country)

        worst_conflict_years = pd.concat(worst_conflict_years)
        worst_conflict_years = (worst_conflict_years
            .sort_values('deaths', ascending=False)
            .reset_index(drop=True)
        )

        years_with_conflict = (self.data_conflict
            .groupby(['country', 'region', 'sub-region'])
            .agg(years_with_conflict=('year_conflict', 'sum'))
            .reset_index()
        )

        worst_conflict_years = worst_conflict_years.merge(years_with_conflict,
                                                        on = 'country',
                                                        how='left'
                                                    )
        columns = ['year', 'country', 'region', 'sub-region', 'deaths', 'years_with_conflict']
        worst_conflict_years = worst_conflict_years[columns]
        
        return worst_conflict_years

















