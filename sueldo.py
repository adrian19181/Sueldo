import datetime
from datetime import date
import io
from calendar import monthrange
import os
import subprocess
import sys
import pandas as pd
import plotly.express as px
import requests
import streamlit as st
import streamlit.components.v1 as components

# ---------------------------------------------------------
# AUTO-LANZADOR AUTOMÁTICO AL HACER DOBLE CLIC EN WINDOWS
# ---------------------------------------------------------
if __name__ == "__main__" and not st.runtime.exists():
  script_path = os.path.abspath(__file__)
  subprocess.run([sys.executable, "-m", "streamlit", "run", script_path])
  sys.exit()

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA (OPTIMIZADA PARA MÓVIL)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Sueldos - KPIs e Ingresos",
    page_icon="💵",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------
# SCRIPT INVISIBLE: CIERRE AUTOMÁTICO EN MÓVIL (POPOVER)
# ---------------------------------------------------------
components.html(
    """
    <script>
    const doc = window.parent.document;
    doc.addEventListener('change', function(e) {
        if (e.target.closest('div[data-testid="stPopoverBody"]') || e.target.closest('div[data-baseweb="popover"]')) {
            setTimeout(function() {
                doc.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', keyCode: 27, bubbles: true, cancelable: true }));
            }, 120);
        }
    });
    </script>
    """,
    height=0,
    width=0,
)

# ---------------------------------------------------------
# ESTILOS CSS PERSONALIZADOS (MODO OSCURO Y MÓVIL RESPONSIVE)
# ---------------------------------------------------------
st.markdown(
    """
    <style>
        /* FONDO GENERAL Y CONTENEDOR MÓVIL */
        html, body, .stApp, [data-testid="stAppViewContainer"] {
            background-color: #0E1117 !important;
            color: #FAFAFA !important;
        }
        [data-testid="stHeader"] { background-color: rgba(0, 0, 0, 0) !important; }
        .block-container { 
            padding: 0.8rem 0.4rem 2rem 0.4rem !important; 
            max-width: 740px !important; 
        }

        /* TÍTULOS Y TEXTOS */
        h1, h2, h3, h4, h5, h6, [data-testid="stMarkdownContainer"] h3 {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }

        /* RADIO BUTTONS ADAPTADOS A PANTALLA TÁCTIL */
        div[data-testid="stRadio"] label p {
            color: #FFFFFF !important;
            font-size: 0.92rem !important;
            font-weight: 700 !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] {
            gap: 12px !important;
            flex-wrap: wrap !important;
        }

        /* BOTÓN REFRESCAR */
        div[data-testid="stButton"] > button {
            background-color: #1E222B !important;
            border: 1.5px solid #107C41 !important;
            border-radius: 8px !important;
            padding: 0.4rem 0.6rem !important;
            width: 100% !important; 
        }
        div[data-testid="stButton"] > button * {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            font-weight: 700 !important;
        }
        div[data-testid="stButton"] > button:hover {
            background-color: #107C41 !important;
            border-color: #107C41 !important;
        }

        /* TARJETA DE TIEMPO TRANSCURRIDO ACUMULADO */
        .time-card-box {
            background: linear-gradient(135deg, #1E1B4B 0%, #111827 100%);
            border: 1.8px solid #6366F1;
            border-radius: 12px;
            padding: 12px 12px;
            margin-top: 10px;
            margin-bottom: 14px;
            box-shadow: 0 4px 16px rgba(99, 102, 241, 0.25);
        }

        .time-card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding-bottom: 8px;
            flex-wrap: wrap;
            gap: 6px;
        }

        .time-card-title {
            font-size: 1.00rem !important;
            font-weight: 800 !important;
            color: #818CF8 !important;
            margin: 0;
        }

        .time-card-range {
            font-size: 0.78rem !important;
            color: #C7D2FE !important;
            background: rgba(99, 102, 241, 0.2) !important;
            padding: 3px 8px !important;
            border-radius: 8px !important;
            font-weight: 700 !important;
            border: 1px solid rgba(99, 102, 241, 0.4) !important;
        }

        .time-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 6px;
            text-align: center;
        }

        .time-unit-box {
            background-color: #1F2937;
            border: 1px solid #374151;
            padding: 8px 3px;
            border-radius: 8px;
        }

        .time-unit-lbl {
            font-size: 0.65rem;
            text-transform: uppercase;
            color: #9CA3AF;
            font-weight: 800;
            margin-bottom: 2px;
        }

        .time-unit-val-years { font-size: 1.25rem; font-weight: 900; color: #38BDF8; }
        .time-unit-val-months { font-size: 1.25rem; font-weight: 900; color: #FBBF24; }
        .time-unit-val-days { font-size: 1.25rem; font-weight: 900; color: #00E676; }

        /* SECCIONES Y GRIDS DE KPIS ORGANIZADOS Y RESPONSIVOS */
        .section-header {
            font-size: 0.92rem !important;
            font-weight: 800 !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 14px;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .kpi-grid-3 {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 6px;
            margin-bottom: 12px;
        }

        .kpi-grid-2 {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 6px;
            margin-bottom: 12px;
        }

        .kpi-card-box {
            background-color: #1E222B;
            border: 1.5px solid #2D323E;
            border-radius: 12px;
            padding: 10px 4px;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }

        .kpi-card-total {
            background: linear-gradient(135deg, #0D472B 0%, #1E222B 100%);
            border: 2px solid #00E676;
            border-radius: 12px;
            padding: 12px 8px;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            box-shadow: 0 4px 16px rgba(0, 230, 118, 0.2);
            margin-top: 12px;
            margin-bottom: 8px;
        }

        .kpi-card-subtotal {
            background: linear-gradient(135deg, #1A2E3B 0%, #1E222B 100%);
            border: 1.5px solid #38BDF8;
            border-radius: 12px;
            padding: 10px 6px;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            box-shadow: 0 4px 12px rgba(56, 189, 248, 0.15);
        }

        .kpi-lbl {
            font-size: 0.65rem;
            text-transform: uppercase;
            color: #94A3B8;
            font-weight: 800;
            letter-spacing: 0.3px;
            margin-bottom: 4px;
        }

        .kpi-val-base { font-size: 1.05rem; font-weight: 800; color: #38BDF8; }
        .kpi-val-extra { font-size: 1.05rem; font-weight: 800; color: #FBBF24; }
        .kpi-val-bono { font-size: 1.05rem; font-weight: 800; color: #F59E0B; }

        .kpi-val-dec3 { font-size: 1.05rem; font-weight: 800; color: #A7F3D0; }
        .kpi-val-dec4 { font-size: 1.05rem; font-weight: 800; color: #818CF8; }
        .kpi-val-fondo { font-size: 1.05rem; font-weight: 800; color: #C084FC; }

        .kpi-val-iess { font-size: 1.05rem; font-weight: 800; color: #FF5252; }
        .kpi-val-cesantia { font-size: 1.05rem; font-weight: 800; color: #E879F9; }

        .kpi-val-neto { font-size: 1.40rem; font-weight: 900; color: #00E676; }
        .kpi-val-promedio { font-size: 1.15rem; font-weight: 800; color: #38BDF8; }
        .kpi-val-eficiencia { font-size: 1.15rem; font-weight: 800; color: #FBBF24; }

        /* AJUSTES RESPONSIVOS PARA PANTALLAS PEQUEÑAS DE CELULAR (< 480PX) */
        @media (max-width: 480px) {
            .block-container { padding: 0.5rem 0.2rem 1.5rem 0.2rem !important; }
            .kpi-val-base, .kpi-val-extra, .kpi-val-bono, 
            .kpi-val-dec3, .kpi-val-dec4, .kpi-val-fondo, 
            .kpi-val-iess, .kpi-val-cesantia,
            .kpi-val-promedio, .kpi-val-eficiencia { font-size: 0.95rem !important; }
            .kpi-val-neto { font-size: 1.25rem !important; }
            .time-unit-val-years, .time-unit-val-months, .time-unit-val-days { font-size: 1.10rem !important; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# CONEXIÓN INTELIGENTE A GOOGLE DRIVE
# ---------------------------------------------------------
DRIVE_FILE_ID = "1ua-Go3LFKaBswhoeCdlVCVY-sTRlydL2"


@st.cache_data(ttl=300)
def load_sueldos_data():
  session = requests.Session()

  urls_to_try = [
      f"https://docs.google.com/spreadsheets/d/{DRIVE_FILE_ID}/export?format=xlsx",
      f"https://drive.google.com/uc?export=download&id={DRIVE_FILE_ID}",
  ]

  excel_bytes = None
  for url in urls_to_try:
    try:
      res = session.get(url, timeout=30)
      for key, val in res.cookies.items():
        if key.startswith("download_warning"):
          res = session.get(
              f"{url}&confirm={val}"
              if "export?format=xlsx" not in url
              else url,
              timeout=30,
          )
          break

      if res.content.startswith(b"PK\x03\x04"):
        excel_bytes = res.content
        break
    except Exception:
      continue

  if not excel_bytes:
    raise ValueError(
        "No se pudo descargar el archivo de Excel. Revisa que en Google Drive"
        " el archivo tenga acceso 'Cualquier persona con el enlace'."
    )

  df = pd.read_excel(
      io.BytesIO(excel_bytes), sheet_name="Consulta1", engine="openpyxl"
  )
  df.columns = [str(c).strip().upper() for c in df.columns]

  # Extraer año numérico de la columna ANO
  df["AÑO"] = (
      df["ANO"].astype(str).str.extract(r"(\d{4})").astype(float).fillna(0).astype(int)
  )

  # Ordenar números de mes
  orden_meses = [
      "ENERO",
      "FEBRERO",
      "MARZO",
      "ABRIL",
      "MAYO",
      "JUNIO",
      "JULIO",
      "AGOSTO",
      "SEPTIEMBRE",
      "OCTUBRE",
      "NOVIEMBRE",
      "DICIEMBRE",
  ]
  df["MES_NUM"] = df["MESES"].apply(
      lambda x: orden_meses.index(str(x).strip().upper()) + 1
      if str(x).strip().upper() in orden_meses
      else 99
  )

  # Columnas numéricas
  num_cols = [
      "SUELDO BASE",
      "HORAS EXTRAS",
      "BONOS",
      "DECIMO TERCERO",
      "DECIMO CUARTO",
      "FONDOS DE RESERVA",
      "IESS",
  ]
  for c in num_cols:
    if c in df.columns:
      df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)

  # Filtrar registros vacíos o sin valor
  df["INGRESO_BRUTO"] = df[num_cols[:-1]].sum(axis=1)
  df = df[df["INGRESO_BRUTO"] > 0].copy()

  # Calcular Ingreso Neto
  df["INGRESO_NETO"] = df["INGRESO_BRUTO"] - df["IESS"]

  return df


try:
  with st.spinner("Cargando ingresos desde Google Drive..."):
    df_raw = load_sueldos_data()
except Exception as e:
  st.error(f"Error al conectar con Google Drive: {e}")
  st.stop()

# ---------------------------------------------------------
# CABECERA & BOTÓN REFRESCAR
# ---------------------------------------------------------
header_col1, header_col2 = st.columns([2.5, 1.5], vertical_alignment="center")
with header_col1:
  st.markdown(
      "<h3 style='margin: 0; color: #FFFFFF !important;'>💵 Sueldos"
      " Detallados</h3>",
      unsafe_allow_html=True,
  )
with header_col2:
  if st.button("🔄 Refrescar", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

# ---------------------------------------------------------
# FILTRO PRINCIPAL POR AÑO (ESTILO RADIO BUTTONS)
# ---------------------------------------------------------
anios_disponibles = ["Todos"] + sorted(list(df_raw["AÑO"].unique()), reverse=True)
st.markdown("<div style='margin-top: 6px;'></div>", unsafe_allow_html=True)

f_anio = st.radio(
    "Filtrar por Año:", options=anios_disponibles, index=0, horizontal=True
)

df_filtrado = df_raw.copy()
if f_anio != "Todos":
  df_filtrado = df_filtrado[df_filtrado["AÑO"] == int(f_anio)]

# ---------------------------------------------------------
# KPI 1: TIEMPO TRANSCURRIDO DE TRABAJO (ARRIBA)
# ---------------------------------------------------------
df_sorted = df_filtrado.sort_values(by=["AÑO", "MES_NUM"], ascending=True)

if not df_sorted.empty:
  min_row = df_sorted.iloc[0]
  max_row = df_sorted.iloc[-1]

  min_y = int(min_row["AÑO"])
  min_m_num = int(min_row["MES_NUM"])
  min_m_name = str(min_row["MESES"]).strip().capitalize()

  max_y = int(max_row["AÑO"])
  max_m_num = int(max_row["MES_NUM"])
  max_m_name = str(max_row["MESES"]).strip().capitalize()

  total_months_count = (max_y - min_y) * 12 + (max_m_num - min_m_num + 1)
  total_years_decimal = round(total_months_count / 12, 1)

  start_dt = date(min_y, min_m_num, 1)
  _, last_day = monthrange(max_y, max_m_num)
  end_dt = date(max_y, max_m_num, last_day)
  total_days_elapsed = (end_dt - start_dt).days + 1

  rango_fechas_str = f"📅 {min_m_name} {min_y} ➔ {max_m_name} {max_y}"
else:
  total_years_decimal, total_months_count, total_days_elapsed = 0.0, 0, 0
  rango_fechas_str = "Sin datos"

st.markdown(
    f"""
    <div class="time-card-box">
        <div class="time-card-header">
            <span class="time-card-title">⏳ Tiempo Transcurrido de Trabajo</span>
            <span class="time-card-range">{rango_fechas_str}</span>
        </div>
        <div class="time-grid">
            <div class="time-unit-box">
                <div class="time-unit-lbl">Años Totales</div>
                <div class="time-unit-val-years">{total_years_decimal:.1f}</div>
            </div>
            <div class="time-unit-box">
                <div class="time-unit-lbl">Meses Totales</div>
                <div class="time-unit-val-months">{total_months_count}</div>
            </div>
            <div class="time-unit-box">
                <div class="time-unit-lbl">Días Totales</div>
                <div class="time-unit-val-days">{total_days_elapsed:,}</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# CÁLCULOS FINANCIEROS Y KPIS AVANZADOS
# ---------------------------------------------------------
tot_sueldo_base = df_filtrado["SUELDO BASE"].sum()
tot_horas_extras = df_filtrado["HORAS EXTRAS"].sum()
tot_bonos = df_filtrado["BONOS"].sum()
tot_materia_gravable = tot_sueldo_base + tot_horas_extras + tot_bonos

tot_decimo_tercero = df_filtrado["DECIMO TERCERO"].sum()
tot_decimo_cuarto = df_filtrado["DECIMO CUARTO"].sum()
tot_fondos_reserva = df_filtrado["FONDOS DE RESERVA"].sum()

tot_iess = df_filtrado["IESS"].sum()
tot_cesantia_est = tot_materia_gravable * 0.03

tot_ingreso_neto = df_filtrado["INGRESO_NETO"].sum()
tot_ingreso_bruto = (
    tot_materia_gravable
    + tot_decimo_tercero
    + tot_decimo_cuarto
    + tot_fondos_reserva
)

n_meses = len(df_filtrado)
promedio_neto_mensual = tot_ingreso_neto / n_meses if n_meses > 0 else 0.0
porcentaje_eficiencia = (
    (tot_ingreso_neto / tot_ingreso_bruto * 100) if tot_ingreso_bruto > 0 else 0.0
)

subtitulo_periodo = (
    f"Periodo: {f_anio} ({n_meses} meses)"
    if f_anio != "Todos"
    else f"Historial Completo ({n_meses} meses)"
)

# ---------------------------------------------------------
# DESPLIEGUE ORGANIZADO DE SECCIONES DE KPIS
# ---------------------------------------------------------

# SECCIÓN 1: INGRESOS GRAVABLES
st.markdown(
    f"""
    <div class="section-header" style="color: #38BDF8;">
        💵 1. Ingresos Gravables ({subtitulo_periodo})
    </div>
    <div class="kpi-grid-3">
        <div class="kpi-card-box">
            <div class="kpi-lbl">Sueldo Base</div>
            <div class="kpi-val-base">${tot_sueldo_base:,.2f}</div>
        </div>
        <div class="kpi-card-box">
            <div class="kpi-lbl">Horas Extras</div>
            <div class="kpi-val-extra">${tot_horas_extras:,.2f}</div>
        </div>
        <div class="kpi-card-box">
            <div class="kpi-lbl">Bonos</div>
            <div class="kpi-val-bono">${tot_bonos:,.2f}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# SECCIÓN 2: BENEFICIOS DE LEY
st.markdown(
    f"""
    <div class="section-header" style="color: #C084FC;">
        🎁 2. Beneficios de Ley
    </div>
    <div class="kpi-grid-3">
        <div class="kpi-card-box">
            <div class="kpi-lbl">Décimo Tercero</div>
            <div class="kpi-val-dec3">${tot_decimo_tercero:,.2f}</div>
        </div>
        <div class="kpi-card-box">
            <div class="kpi-lbl">Décimo Cuarto</div>
            <div class="kpi-val-dec4">${tot_decimo_cuarto:,.2f}</div>
        </div>
        <div class="kpi-card-box">
            <div class="kpi-lbl">Fondos de Reserva</div>
            <div class="kpi-val-fondo">${tot_fondos_reserva:,.2f}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# SECCIÓN 3: APORTACIONES Y FONDO DE CESANTÍA
st.markdown(
    f"""
    <div class="section-header" style="color: #F472B6;">
        🛡️ 3. Aportaciones e IESS / Cesantía
    </div>
    <div class="kpi-grid-2">
        <div class="kpi-card-box">
            <div class="kpi-lbl">Aportes IESS (-)</div>
            <div class="kpi-val-iess">${tot_iess:,.2f}</div>
        </div>
        <div class="kpi-card-box">
            <div class="kpi-lbl">Cesantía Est. (IESS 3%)</div>
            <div class="kpi-val-cesantia">${tot_cesantia_est:,.2f}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# SECCIÓN 4: INGRESO NETO TOTAL Y KPIS DE FLUJO Y EFICIENCIA
st.markdown(
    f"""
    <div class="kpi-card-total">
        <div class="kpi-lbl" style="color: #A7F3D0; font-size: 0.82rem;">🌟 Ingresos Netos Totales Recibidos</div>
        <div class="kpi-val-neto">${tot_ingreso_neto:,.2f}</div>
    </div>
    <div class="kpi-grid-2">
        <div class="kpi-card-subtotal">
            <div class="kpi-lbl">📈 Promedio Neto Mensual</div>
            <div class="kpi-val-promedio">${promedio_neto_mensual:,.2f} <span style="font-size:0.75rem; color:#94A3B8;">/ mes</span></div>
        </div>
        <div class="kpi-card-subtotal">
            <div class="kpi-lbl">💡 Eficiencia del Ingreso</div>
            <div class="kpi-val-eficiencia">{porcentaje_eficiencia:.2f}% <span style="font-size:0.75rem; color:#94A3B8;">Líquido</span></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# SECCIÓN 5: GRÁFICOS DINÁMICOS - EVOLUCIÓN ANUAL EN BARRAS HORIZONTALES (ESTÁTICO)
# ---------------------------------------------------------
st.markdown(
    """
    <div class="section-header" style="color: #00E676; margin-bottom: 8px;">
        📊 Análisis Gráfico de Distribución
    </div>
    """,
    unsafe_allow_html=True,
)

vista_grafico = st.radio(
    "Seleccionar Vista de Gráfico:",
    options=[
        "Evolución Anual",
        "Ingresos Netos",
        "Ingresos Gravables",
        "Beneficios de Ley",
    ],
    index=0,
    horizontal=True,
)

if vista_grafico == "Evolución Anual":
  df_evo_anual = (
      df_raw.groupby("AÑO")["INGRESO_NETO"]
      .sum()
      .reset_index()
      .sort_values(by="AÑO", ascending=True)
  )
  df_evo_anual["AÑO_STR"] = df_evo_anual["AÑO"].astype(str)

  fig = px.bar(
      df_evo_anual,
      x="INGRESO_NETO",
      y="AÑO_STR",
      orientation="h",
      text_auto="$,.0f",
      color="INGRESO_NETO",
      color_continuous_scale=["#107C41", "#00E676", "#38BDF8"],
  )

  fig.update_traces(
      textposition="outside",
      hovertemplate=(
          "<b>Año %{y}</b><br>Ingreso Neto Total: $%{x:,.2f}<extra></extra>"
      ),
      marker=dict(line=dict(color="#0E1117", width=1.5)),
  )

  fig.update_xaxes(
      showgrid=False,
      zeroline=False,
      showticklabels=False,
      fixedrange=True,
  )

  fig.update_yaxes(
      showgrid=False,
      type="category",
      fixedrange=True,
      title_text="",
  )

  fig.update_layout(
      title=dict(
          text="<b>Evolución Anual</b>",
          x=0.5,
          xanchor="center",
          y=0.92,
          yanchor="top",
          font=dict(size=18, color="#FFFFFF", family="sans-serif"),
      ),
      coloraxis_showscale=False,
      paper_bgcolor="rgba(0,0,0,0)",
      plot_bgcolor="rgba(0,0,0,0)",
      font=dict(color="#FAFAFA", family="sans-serif", size=13),
      margin=dict(t=50, b=20, l=10, r=60),
      height=320,
  )

  st.plotly_chart(
      fig,
      use_container_width=True,
      config={"displayModeBar": False},
  )

elif vista_grafico == "Ingresos Netos":
  if f_anio == "Todos":
    df_pie_neto = df_raw.groupby("AÑO")["INGRESO_NETO"].sum().reset_index()
    df_pie_neto["LABEL"] = df_pie_neto["AÑO"].astype(str)
    df_pie_neto = df_pie_neto.sort_values(by="AÑO", ascending=True)
    t1 = "Distribución de Ingresos Netos"
    t2 = "por Año (Todos)"
  else:
    df_pie_neto = (
        df_filtrado.groupby(["MESES", "MES_NUM"])["INGRESO_NETO"]
        .sum()
        .reset_index()
    )
    df_pie_neto = df_pie_neto.sort_values(by="MES_NUM", ascending=True)
    df_pie_neto["LABEL"] = df_pie_neto["MESES"].astype(str).str.capitalize()
    t1 = "Distribución Mensual de Ingresos Netos"
    t2 = f"Año {f_anio}"

  colors_neto = [
      "#38BDF8",
      "#00E676",
      "#FBBF24",
      "#A855F7",
      "#FF5252",
      "#EC4899",
      "#00B4D8",
      "#F59E0B",
      "#C084FC",
      "#2EC4B6",
      "#E879F9",
      "#3B82F6",
  ]

  title_html = (
      f"<b>{t1}</b><br><span style='font-size: 0.90rem; font-weight:"
      f" 600;'>{t2}</span>"
  )

  fig = px.pie(
      df_pie_neto,
      names="LABEL",
      values="INGRESO_NETO",
      color="LABEL",
      color_discrete_sequence=colors_neto,
      hole=0.45,
  )

  fig.update_traces(
      textposition="outside",
      textinfo="percent+label",
      hovertemplate=(
          "<b>%{label}</b><br>Ingreso Neto:"
          " $%{value:,.2f}<br>Porcentaje: %{percent}<extra></extra>"
      ),
      marker=dict(line=dict(color="#0E1117", width=2.5)),
      domain=dict(y=[0.02, 0.74]),
  )

  fig.update_layout(
      title=dict(
          text=title_html,
          x=0.5,
          xanchor="center",
          y=0.94,
          yanchor="top",
          font=dict(size=17, color="#FFFFFF", family="sans-serif"),
      ),
      paper_bgcolor="rgba(0,0,0,0)",
      plot_bgcolor="rgba(0,0,0,0)",
      font=dict(color="#FAFAFA", family="sans-serif", size=13),
      showlegend=True,
      legend=dict(
          title=dict(
              text="💡 Leyenda (Clic para filtrar / ocultar):",
              font=dict(size=14, color="#FFFFFF"),
          ),
          orientation="h",
          yanchor="top",
          y=-0.20,
          xanchor="center",
          x=0.5,
          font=dict(size=13, color="#E2E8F0"),
      ),
      margin=dict(t=85, b=85, l=15, r=15),
      height=430,
  )

  st.plotly_chart(
      fig,
      use_container_width=True,
      config={"displayModeBar": False, "responsive": True},
  )

elif vista_grafico == "Ingresos Gravables":
  df_grav_pie = pd.DataFrame([
      {"Categoría": "Sueldo<br>Base", "Monto": tot_sueldo_base},
      {"Categoría": "Horas<br>Extras", "Monto": tot_horas_extras},
      {"Categoría": "Bonos", "Monto": tot_bonos},
  ])
  df_grav_pie = df_grav_pie[df_grav_pie["Monto"] > 0]

  colors_grav_map = {
      "Sueldo<br>Base": "#38BDF8",
      "Horas<br>Extras": "#FBBF24",
      "Bonos": "#EC4899",
  }

  sub_txt = "Historial Completo" if f_anio == "Todos" else f"Año {f_anio}"
  t1 = "Composición de Ingresos Gravables"
  t2 = f"({sub_txt})"

  title_html = (
      f"<b>{t1}</b><br><span style='font-size: 0.90rem; font-weight:"
      f" 600;'>{t2}</span>"
  )

  fig = px.pie(
      df_grav_pie,
      names="Categoría",
      values="Monto",
      color="Categoría",
      color_discrete_map=colors_grav_map,
      hole=0.42,
  )

  fig.update_traces(
      textposition="outside",
      textinfo="percent+label",
      hovertemplate=(
          "<b>%{label}</b><br>Monto:"
          " $%{value:,.2f}<br>Porcentaje: %{percent}<extra></extra>"
      ),
      marker=dict(line=dict(color="#0E1117", width=2.5)),
      domain=dict(y=[0.02, 0.74]),
  )

  fig.update_layout(
      title=dict(
          text=title_html,
          x=0.5,
          xanchor="center",
          y=0.94,
          yanchor="top",
          font=dict(size=17, color="#FFFFFF", family="sans-serif"),
      ),
      paper_bgcolor="rgba(0,0,0,0)",
      plot_bgcolor="rgba(0,0,0,0)",
      font=dict(color="#FAFAFA", family="sans-serif", size=13),
      showlegend=True,
      legend=dict(
          title=dict(
              text="💡 Leyenda (Clic para filtrar / ocultar):",
              font=dict(size=14, color="#FFFFFF"),
          ),
          orientation="h",
          yanchor="top",
          y=-0.20,
          xanchor="center",
          x=0.5,
          font=dict(size=13, color="#E2E8F0"),
      ),
      margin=dict(t=85, b=90, l=15, r=15),
      height=440,
  )

  st.plotly_chart(
      fig,
      use_container_width=True,
      config={"displayModeBar": False, "responsive": True},
  )

elif vista_grafico == "Beneficios de Ley":
  df_ben_pie = pd.DataFrame([
      {"Beneficio": "Décimo<br>Tercero", "Monto": tot_decimo_tercero},
      {"Beneficio": "Décimo<br>Cuarto", "Monto": tot_decimo_cuarto},
      {"Beneficio": "Fondos de<br>Reserva", "Monto": tot_fondos_reserva},
  ])
  df_ben_pie = df_ben_pie[df_ben_pie["Monto"] > 0]

  colors_ben_map = {
      "Décimo<br>Tercero": "#00E676",
      "Décimo<br>Cuarto": "#818CF8",
      "Fondos de<br>Reserva": "#C084FC",
  }

  sub_txt = "Historial Completo" if f_anio == "Todos" else f"Año {f_anio}"
  t1 = "Composición de Beneficios de Ley"
  t2 = f"({sub_txt})"

  title_html = (
      f"<b>{t1}</b><br><span style='font-size: 0.90rem; font-weight:"
      f" 600;'>{t2}</span>"
  )

  fig = px.pie(
      df_ben_pie,
      names="Beneficio",
      values="Monto",
      color="Beneficio",
      color_discrete_map=colors_ben_map,
      hole=0.42,
  )

  fig.update_traces(
      textposition="outside",
      textinfo="percent+label",
      hovertemplate=(
          "<b>%{label}</b><br>Monto:"
          " $%{value:,.2f}<br>Porcentaje: %{percent}<extra></extra>"
      ),
      marker=dict(line=dict(color="#0E1117", width=2.5)),
      domain=dict(y=[0.02, 0.74]),
  )

  fig.update_layout(
      title=dict(
          text=title_html,
          x=0.5,
          xanchor="center",
          y=0.94,
          yanchor="top",
          font=dict(size=17, color="#FFFFFF", family="sans-serif"),
      ),
      paper_bgcolor="rgba(0,0,0,0)",
      plot_bgcolor="rgba(0,0,0,0)",
      font=dict(color="#FAFAFA", family="sans-serif", size=13),
      showlegend=True,
      legend=dict(
          title=dict(
              text="💡 Leyenda (Clic para filtrar / ocultar):",
              font=dict(size=14, color="#FFFFFF"),
          ),
          orientation="h",
          yanchor="top",
          y=-0.20,
          xanchor="center",
          x=0.5,
          font=dict(size=13, color="#E2E8F0"),
      ),
      margin=dict(t=85, b=90, l=15, r=15),
      height=440,
  )

  st.plotly_chart(
      fig,
      use_container_width=True,
      config={"displayModeBar": False, "responsive": True},
  )