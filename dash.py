import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

# Cargar el archivo CSV
df = pd.read_csv('education_career_success.csv')

# --- Procesamiento de datos y creación de columnas ---
# Crear una nueva columna para el rango de edad
bins_age = [20, 22, 24, 26]
labels_age = ['20-22', '22-24', '24-26']
df['Age_Group'] = pd.cut(df['Age'], bins=bins_age, labels=labels_age, right=False)

# Crear una nueva columna para el rango de salario
bins_salary = [0, 50000, 100000, 150000, 200000]
labels_salary = ['< $50K', '$50K - $100K', '$100K - $150K', '> $150K']
df['Salary_Range'] = pd.cut(df['Starting_Salary'], bins=bins_salary, labels=labels_salary, right=False)

# --- Configuración de la página del dashboard ---
st.set_page_config(layout="wide", page_title="Análisis de Éxito Académico y Profesional")
st.title('📊 Dashboard: Éxito Académico y Profesional')
st.markdown('***Una síntesis visual ejecutiva del análisis de los factores que influyen en el éxito profesional.***')

# --- Filtros interactivos ---
st.sidebar.header('Filtros')
field_of_study = st.sidebar.multiselect(
    'Selecciona el Campo de Estudio',
    options=df['Field_of_Study'].unique(),
    default=df['Field_of_Study'].unique()
)

job_level = st.sidebar.multiselect(
    'Selecciona el Nivel de Puesto Actual',
    options=df['Current_Job_Level'].unique(),
    default=df['Current_Job_Level'].unique()
)

# Aplicar filtros
df_filtered = df[(df['Field_of_Study'].isin(field_of_study)) & (df['Current_Job_Level'].isin(job_level))]

# Manejar el caso de no selección para evitar errores
if df_filtered.empty:
    st.warning('No hay datos para la combinación de filtros seleccionada. Por favor, ajusta los filtros.')
    st.stop()

# --- KPIs Numéricos ---
col1, col2 = st.columns(2)

with col1:
    avg_salary = df_filtered['Starting_Salary'].mean()
    st.metric(label="💰 Salario Inicial Promedio", value=f"${avg_salary:,.2f}")

with col2:
    avg_gpa = df_filtered['University_GPA'].mean()
    st.metric(label="🎓 GPA Universitario Promedio", value=f"{avg_gpa:.2f}")

st.markdown('---')

# --- Visualizaciones Clave ---

st.header('📈 Visualizaciones')

# Gráfico 1: Relación entre GPA y Salario
st.subheader('Relación entre GPA Universitario y Salario Inicial por Campo de Estudio')
fig_gpa_salary = px.scatter(
    df_filtered,
    x='University_GPA',
    y='Starting_Salary',
    color='Field_of_Study',
    hover_data=['High_School_GPA', 'SAT_Score', 'Job_Offers'],
    title='El GPA y el Salario Inicial muestran una correlación positiva, destacando las diferencias por área de estudio.'
)
st.plotly_chart(fig_gpa_salary, use_container_width=True)

# Gráfico 2: Distribución de Salarios por Nivel de Puesto
st.subheader('Distribución de Salarios por Nivel de Puesto Actual')
salary_distribution_df = df_filtered.groupby('Current_Job_Level')['Starting_Salary'].mean().sort_values(ascending=False).reset_index()
fig_salary_level = px.bar(
    salary_distribution_df,
    x='Current_Job_Level',
    y='Starting_Salary',
    color='Current_Job_Level',
    title='El nivel de puesto (Senior, Mid, Entry) tiene una clara influencia en el salario promedio.'
)
st.plotly_chart(fig_salary_level, use_container_width=True)

# Gráfico 3: Impacto de las Prácticas e Internados
st.subheader('Impacto de Pasantías en los Salarios Iniciales')
internships_df = df_filtered.groupby('Internships_Completed')['Starting_Salary'].mean().reset_index()
fig_internships = px.bar(
    internships_df,
    x='Internships_Completed',
    y='Starting_Salary',
    color='Internships_Completed',
    title='Se observa una tendencia donde a mayor número de pasantías, mayor es el salario inicial.'
)
st.plotly_chart(fig_internships, use_container_width=True)

st.markdown('---')

# --- Comentarios Finales ---
st.header('✍️ Comentarios y Conclusiones del Análisis Ejecutivo')
st.markdown("""
-   **Impacto de la Preparación Académica:** Los datos sugieren una **fuerte correlación positiva** entre el **GPA universitario** y el **salario inicial**. Un mayor rendimiento académico se asocia con un mayor potencial de ingresos.

-   **Relevancia de la Experiencia Práctica:** Completar más **pasantías** se correlaciona directamente con salarios iniciales más altos. Esto subraya la importancia de la experiencia práctica junto con la formación académica formal.

-   **Nivel de Puesto y Salario:** Como es de esperar, existe una clara jerarquía salarial por **nivel de puesto**, con los roles Senior y Mid superando significativamente a los de nivel de entrada. Esto indica que la progresión profesional es un factor crítico en el crecimiento de los ingresos.
""")