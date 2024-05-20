import streamlit as st

from src.params import CONFLICT_DATA_PATH, ISO_CODE_PATH, CHART_RACE_PATH, list_regions
from src.data_pipeline import DataPipeline
from src.data_viz import PlotBuilder



data_pipeline = DataPipeline(CONFLICT_DATA_PATH, ISO_CODE_PATH)
plot_builder = PlotBuilder(data_pipeline)

### sidebar ###
st.sidebar.title('Visualización de datos - PEC 3')
st.sidebar.subheader("José Luis Rodriguez Andreu")
st.sidebar.write("Master Universitario en Ciencia de Datos")

st.sidebar.markdown('''
### Dataset empleado

**Countries in Conflict Dataset (1989-2022)**
''')

st.sidebar.markdown('''

Desde 1800, las guerras han causado la muerte de más de 37 millones de personas 
en todo el mundo, cifra que aumentaría si se consideraran las 
muertes de civiles y las derivadas del hambre y las enfermedades 
provocadas por los conflictos. 

Las guerras, además de ser una amenaza existencial en caso de 
involucrar armas nucleares, generan inseguridad, reducen el nivel 
de vida y dañan el medio ambiente. Aunque las estadísticas indican una 
disminución de las muertes en conflictos en las últimas décadas y una
tendencia hacia relaciones más pacíficas, el futuro es incierto, ya 
que las muertes en conflictos han aumentado recientemente en 
Oriente Medio, África y Europa.

La prevención de guerras futuras depende de nuestras acciones.

### Descripción del conjunto de datos:
Este conjunto de datos ofrece una visión de los países que experimentan conflictos en curso, proporcionando estimaciones de las víctimas mortales resultantes de estos conflictos a lo largo de varios años. Constituye un valioso recurso para comprender el panorama mundial de los conflictos y su coste humano.

''')
st.sidebar.link_button("Dataset en Kaggle", "https://www.kaggle.com/datasets/saurabhbadole/countries-in-conflict-dataset")
### /sidebar ###

### body ###
st.title('Las pérdidas de la guerra')
st.subheader("Países en conflicto entre 1989 y 2022")

### chart race

video_file = open(CHART_RACE_PATH, 'rb')
video_bytes = video_file.read()
st.video(video_bytes)

### world map
world_fig = plot_builder.plot_worldmap()
st.plotly_chart(world_fig, use_container_width=True)

### deaths by continent and regions
col1, col2 = st.columns(2)

with col1:
    continents_fig = plot_builder.plot_deaths_by_continent()
    st.plotly_chart(continents_fig, use_container_width=True)

with col2:
    region_fig1 = plot_builder.plot_deaths_by_region(region = list_regions[0])
    st.plotly_chart(region_fig1, use_container_width=True)


col3, col4 = st.columns(2)

with col3:
    region_fig2 = plot_builder.plot_deaths_by_region(region = list_regions[1])
    st.plotly_chart(region_fig2, use_container_width=True)

with col4:
    region_fig3 = plot_builder.plot_deaths_by_region(region = list_regions[2])
    st.plotly_chart(region_fig3, use_container_width=True)


col5, col6 = st.columns(2)

with col5:
    region_fig4 = plot_builder.plot_deaths_by_region(region = list_regions[3])
    st.plotly_chart(region_fig4, use_container_width=True)

with col6:
    region_fig5 = plot_builder.plot_deaths_by_region(region = list_regions[4])
    st.plotly_chart(region_fig5, use_container_width=True)


### deaths by country
country_fig = plot_builder.plot_deaths_br_country()
st.plotly_chart(country_fig, use_container_width=True)


### worst years
st.markdown("### Los peores años de guerra")
worst_conflict_years = data_pipeline.get_worst_conflict_years()
st.dataframe(worst_conflict_years)



### /body ###




