
from src.params import CONFLICT_DATA_PATH, ISO_CODE_PATH, list_regions

from src.data_pipeline import DataPipeline


data_pipeline = DataPipeline(CONFLICT_DATA_PATH, ISO_CODE_PATH)

data_conflict = data_pipeline.get_data_conflict()
print(data_conflict.head(5))

chart_race_data = data_pipeline.get_chart_race_data()
print(chart_race_data.head(5))

deaths_by_continent = data_pipeline.get_deaths_by_continent()
print(deaths_by_continent.head(5))

for region in list_regions:
    print(region)
    deaths_by_region = data_pipeline.get_deaths_by_region(region)
    print(deaths_by_region.head(5))

top10_deaths_by_country = data_pipeline.get_top10_deaths_by_country()
print(top10_deaths_by_country.head(5))

worst_conflict_years = data_pipeline.get_worst_conflict_years()
print(worst_conflict_years.head(5))