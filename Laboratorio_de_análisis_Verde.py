import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as stats

# ═══════════════════════════════════════════════════════
# MAPEOS LIKERT — Conversión de respuestas de texto a numérico
# ═══════════════════════════════════════════════════════

# Escala de frecuencia general: Nunca → Siempre
MAPEO_FRECUENCIA = {
    'Nunca': 1, 'A veces': 2, 'Frecuentemente': 3, 'Siempre': 4,
    # variantes con coma (ej: "Nunca, A veces")
    'Nunca, A veces': 1,
}

# Escala de acuerdo: Totalmente en desacuerdo → Totalmente de acuerdo
MAPEO_ACUERDO = {
    'Totalmente en desacuerdo': 1, 'En desacuerdo': 2,
    'De acuerdo': 3, 'Totalmente de acuerdo': 4,
}

# Tiempo diario en redes
MAPEO_TIEMPO_DIA = {
    'Menos de 1 hora': 1, '1–2 horas': 2, '3–4 horas': 3, '5 o más horas': 4,
}

# Desbloqueos del celular al día
MAPEO_DESBLOQUEOS = {
    'Menos de 5 veces al día': 1, '5–10 veces al día': 2,
    '11–20 veces al día': 3, 'Más de 20 veces al día': 4,
}

# Tipo de interacciones
MAPEO_INTERACCION = {
    'Negativas': 1, 'Neutras': 2, 'Mixtas': 3, 'Positivas': 4,
}

# Preferencia de interacción
MAPEO_PREFERENCIA = {
    'No': 1, 'Depende de la situación': 2, 'Sí': 3,
}

# Etiquetas legibles para mostrar en la app
ETIQUETAS_COLUMNAS = {
    '1-¿Cuánto tiempo al día usas redes sociales en promedio?':
        'P1 - Tiempo diario en redes (1=<1h, 4=5h+)',
    '2- ¿Con qué frecuencia revisas redes sociales mientras realizas tareas académicas?':
        'P2 - Revisión durante tareas (1=Nunca, 4=Siempre)',
    '3-¿Con qué frecuencia usas redes sociales durante clases presenciales o en línea?  ':
        'P3 - Uso en clases (1=Nunca, 4=Siempre)',
    '4-Las notificaciones de redes sociales interrumpen tu concentración cuando estudias  ':
        'P4 - Notificaciones interrumpen concentración (1=Tot. desacuerdo, 4=Tot. acuerdo)',
    '5-¿Has pospuesto tareas o estudios por usar redes sociales?  ':
        'P5 - Posposición de tareas (1=Nunca, 4=Siempre)',
    '6-Las redes sociales afectan mi rendimiento en exámenes':
        'P6 - Afectan rendimiento en exámenes (1=Tot. desacuerdo, 4=Tot. acuerdo)',
    '8-Cuando estás estresado por trabajos o exámenes, usas redes sociales para distraerte  ':
        'P8 - Uso como distracción ante estrés (1=Nunca, 4=Siempre)',
    '9-¿Con qué frecuencia desbloqueas el celular solo para revisar notificaciones de redes sociales?  ':
        'P9 - Desbloqueos diarios del celular (1=<5/día, 4=20+/día)',
    '10-¿Silencias notificaciones de redes sociales mientras estudias?  ':
        'P10 - Silencia notificaciones al estudiar (1=Nunca, 4=Siempre)',
    '11-El número de seguidores o amigos en redes sociales es importante para ti  ':
        'P11 - Importancia de seguidores (1=Tot. desacuerdo, 4=Tot. acuerdo)',
    '12-¿Te comparas con otras personas en redes sociales?  ':
        'P12 - Comparación social en redes (1=Nunca, 4=Siempre)',
    '13-El uso de redes sociales ha afectado tu autoestima  ':
        'P13 - Afecta autoestima (1=Tot. desacuerdo, 4=Tot. acuerdo)',
    '14-¿Con qué frecuencia tienes discusiones o conflictos a causa de redes sociales?  ':
        'P14 - Conflictos por redes (1=Nunca, 4=Siempre)',
    '15-¿Sientes que recibes apoyo emocional a través de redes sociales?  ':
        'P15 - Apoyo emocional en redes (1=Nunca, 4=Siempre)',
    '16-La mayoría de tus interacciones en redes sociales son:  ':
        'P16 - Tipo de interacciones (1=Negativas, 4=Positivas)',
    '17-¿Prefieres interactuar socialmente más en redes que en persona?  ':
        'P17 - Prefiere redes a interacción presencial (1=No, 3=Sí)',
}

# Columnas a ignorar siempre (texto libre, email, timestamp)
COLUMNAS_IGNORAR = {
    'Marca temporal',
    'Dirección de correo electrónico',
    '7-¿Qué actividades académicas sueles aplazar por usar redes sociales?',
    '18-Describe brevemente cómo las redes sociales han influido en tus hábitos de estudio',
    '19-Menciona un aspecto positivo del uso de redes sociales en tu vida académica',
    '20-Menciona un aspecto negativo del uso de redes sociales en tu vida académica',
}


def convertir_likert(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str], bool]:
    """
    Detecta si el DataFrame tiene columnas de tipo Likert (texto) y las
    convierte a numérico. Devuelve (df_convertido, columnas_convertidas, fue_convertido).
    """
    mapeos_por_col = {
        '1-¿Cuánto tiempo al día usas redes sociales en promedio?': MAPEO_TIEMPO_DIA,
        '2- ¿Con qué frecuencia revisas redes sociales mientras realizas tareas académicas?': MAPEO_FRECUENCIA,
        '3-¿Con qué frecuencia usas redes sociales durante clases presenciales o en línea?  ': MAPEO_FRECUENCIA,
        '4-Las notificaciones de redes sociales interrumpen tu concentración cuando estudias  ': MAPEO_ACUERDO,
        '5-¿Has pospuesto tareas o estudios por usar redes sociales?  ': MAPEO_FRECUENCIA,
        '6-Las redes sociales afectan mi rendimiento en exámenes': MAPEO_ACUERDO,
        '8-Cuando estás estresado por trabajos o exámenes, usas redes sociales para distraerte  ': MAPEO_FRECUENCIA,
        '9-¿Con qué frecuencia desbloqueas el celular solo para revisar notificaciones de redes sociales?  ': MAPEO_DESBLOQUEOS,
        '10-¿Silencias notificaciones de redes sociales mientras estudias?  ': MAPEO_FRECUENCIA,
        '11-El número de seguidores o amigos en redes sociales es importante para ti  ': MAPEO_ACUERDO,
        '12-¿Te comparas con otras personas en redes sociales?  ': MAPEO_FRECUENCIA,
        '13-El uso de redes sociales ha afectado tu autoestima  ': MAPEO_ACUERDO,
        '14-¿Con qué frecuencia tienes discusiones o conflictos a causa de redes sociales?  ': MAPEO_FRECUENCIA,
        '15-¿Sientes que recibes apoyo emocional a través de redes sociales?  ': MAPEO_FRECUENCIA,
        '16-La mayoría de tus interacciones en redes sociales son:  ': MAPEO_INTERACCION,
        '17-¿Prefieres interactuar socialmente más en redes que en persona?  ': MAPEO_PREFERENCIA,
    }

    df_conv = df.copy()
    convertidas = []
    fue_convertido = False

    for col, mapeo in mapeos_por_col.items():
        if col in df_conv.columns and df_conv[col].dtype == object:
            df_conv[col] = df_conv[col].map(mapeo)
            # Renombrar a etiqueta legible si existe
            nombre_legible = ETIQUETAS_COLUMNAS.get(col, col)
            df_conv.rename(columns={col: nombre_legible}, inplace=True)
            convertidas.append(nombre_legible)
            fue_convertido = True

    # Eliminar columnas de texto libre e irrelevantes
    for col in list(COLUMNAS_IGNORAR):
        if col in df_conv.columns:
            df_conv.drop(columns=[col], inplace=True)

    return df_conv, convertidas, fue_convertido


st.set_page_config(
    page_title="Verde Analytics Lab",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

def aplicar_estilos_visuales():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Space Grotesk', sans-serif;
        }

        /* ── Encabezado principal ── */
        .header-wrap {
            background: linear-gradient(135deg, #002418 0%, #004d35 50%, #007a55 100%);
            border-radius: 20px;
            padding: 44px 52px 40px;
            margin-bottom: 36px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0, 77, 53, 0.35);
        }
        .header-wrap::before {
            content: "";
            position: absolute;
            top: -60px; right: -60px;
            width: 280px; height: 280px;
            border-radius: 50%;
            background: rgba(255,255,255,0.04);
        }
        .header-wrap::after {
            content: "";
            position: absolute;
            bottom: -80px; left: 25%;
            width: 360px; height: 360px;
            border-radius: 50%;
            background: rgba(0,200,140,0.06);
        }
        .header-badge {
            display: inline-block;
            background: rgba(255,255,255,0.1);
            color: #7fffd4;
            border: 1px solid rgba(127,255,212,0.3);
            border-radius: 20px;
            padding: 5px 16px;
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            margin-bottom: 16px;
        }
        .header-title {
            color: #ffffff;
            font-size: 42px;
            font-weight: 700;
            letter-spacing: -1px;
            margin: 0 0 8px;
            line-height: 1.1;
        }
        .header-title span {
            color: #7fffd4;
        }
        .header-sub {
            color: rgba(255,255,255,0.6);
            font-size: 15px;
            font-weight: 400;
            margin: 0;
            letter-spacing: 0.2px;
        }

        /* ── Títulos de sección ── */
        .section-title {
            background: linear-gradient(90deg, #e8f8f0 0%, #f5fffe 100%);
            color: #004d35;
            font-size: 17px;
            font-weight: 700;
            padding: 14px 22px;
            border-radius: 12px;
            border-left: 5px solid #00b87a;
            margin: 28px 0 20px;
            letter-spacing: -0.3px;
        }

        /* ── Tarjeta resultado ── */
        .result-card {
            background: #f5fffe;
            padding: 20px 24px;
            border-radius: 14px;
            border: 1px solid #b2eed8;
            border-left: 5px solid #00b87a;
            margin-bottom: 16px;
            line-height: 1.8;
        }

        /* ── Tarjeta métrica ── */
        .metric-card {
            background: #ffffff;
            border: 1px solid #d6f5e8;
            border-radius: 16px;
            padding: 22px 18px;
            text-align: center;
            margin-bottom: 14px;
            box-shadow: 0 2px 8px rgba(0,180,120,0.07);
            transition: box-shadow 0.2s;
        }
        .metric-card:hover {
            box-shadow: 0 6px 20px rgba(0,180,120,0.14);
        }
        .metric-label {
            color: #6b7280;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }
        .metric-value {
            color: #002418;
            font-size: 26px;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
        }
        .metric-value.red  { color: #be123c; }
        .metric-value.green { color: #15803d; }

        /* ── Hipótesis box ── */
        .hipotesis-box {
            background: #ffffff;
            border: 1.5px solid #b2eed8;
            border-radius: 14px;
            padding: 18px 22px;
            margin-bottom: 16px;
            font-family: 'JetBrains Mono', monospace;
        }
        .hipotesis-title {
            color: #6b7280;
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 10px;
            font-family: 'Space Grotesk', sans-serif;
        }
        .hipotesis-h0 {
            color: #15803d;
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 6px;
        }
        .hipotesis-h1 {
            color: #b91c1c;
            font-size: 18px;
            font-weight: 600;
        }

        /* ── Decisión H0 ── */
        .decision-h0 {
            font-weight: 700;
            font-size: 22px;
            padding: 20px;
            border-radius: 14px;
            text-align: center;
            letter-spacing: -0.3px;
        }
        .rechazo    { background: #fff1f2; color: #be123c; border: 2px solid #fda4af; }
        .no-rechazo { background: #f0fdf4; color: #166534; border: 2px solid #86efac; }

        /* ── Interpretación automática ── */
        .interpretacion-box {
            background: linear-gradient(135deg, #f0fdf8, #e8faf2);
            border: 1px solid #b2eed8;
            border-radius: 14px;
            padding: 20px 24px;
            margin-top: 14px;
            font-size: 14px;
            line-height: 1.7;
            color: #1f2937;
        }
        .interpretacion-box strong { color: #004d35; }

        /* ── Advertencia sigma ── */
        .sigma-warning {
            background: #fffbeb;
            border: 1px solid #fcd34d;
            border-left: 4px solid #f59e0b;
            border-radius: 10px;
            padding: 12px 16px;
            font-size: 13px;
            color: #78350f;
            margin-top: 8px;
        }

        /* ── Sidebar ── */
        .sidebar-header {
            background: linear-gradient(135deg, #002418, #004d35);
            color: white;
            padding: 18px 22px;
            border-radius: 14px;
            font-size: 17px;
            font-weight: 700;
            margin-bottom: 22px;
            text-align: center;
            letter-spacing: -0.3px;
        }

        /* ── Botones ── */
        div.stButton > button {
            background-color: #d1fae5 !important;
            color: #065f46 !important;
            border: 1.5px solid #6ee7b7 !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            font-family: 'Space Grotesk', sans-serif !important;
            padding: 8px 20px !important;
            transition: all 0.2s ease !important;
        }
        div.stButton > button:hover {
            background-color: #a7f3d0 !important;
            border-color: #34d399 !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(0,166,124,0.2) !important;
        }

        /* ── Respuesta IA ── */
        .ia-response {
            background: #f8fffc;
            border: 1px solid #6ee7b7;
            border-left: 5px solid #00b87a;
            border-radius: 14px;
            padding: 22px 26px;
            font-size: 14.5px;
            line-height: 1.8;
            color: #1f2937;
            white-space: pre-wrap;
        }

        /* ── Comparación decisiones ── */
        .comparacion-box {
            border-radius: 14px;
            padding: 16px 20px;
            margin-top: 12px;
            font-size: 14px;
            font-weight: 600;
            text-align: center;
        }
        .coincide    { background: #f0fdf4; color: #166534; border: 2px solid #86efac; }
        .no-coincide { background: #fff1f2; color: #be123c; border: 2px solid #fda4af; }

        /* ── Footer ── */
        .footer {
            text-align: center;
            color: #9ca3af;
            font-size: 12px;
            padding: 36px 0 14px;
            border-top: 1px solid #e5e7eb;
            margin-top: 48px;
            letter-spacing: 0.2px;
        }
        </style>

        <div class="header-wrap">
            <div class="header-badge">🔬 Laboratorio Estadístico</div>
            <div class="header-title">Verde <span>Analytics</span> Lab</div>
            <p class="header-sub">Distribuciones de Probabilidad · Pruebas de Hipótesis · Asistente IA (Gemini)</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# INICIALIZACIÓN DE ESTADOS
def inicializar_estado():
    defaults = {
        'df': None,
        'api_key': "AIzaSyCdQrhpeU23vy2cAU1w93wyeLgZPcOSta8", 
        'resultados_z': None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ═══════════════════════════════════════════════════════
# SECCIÓN 1: CARGA DE DATOS
# ═══════════════════════════════════════════════════════
def seccion_carga_datos():
    st.markdown('<div class="section-title">☘️ 1. Adquisición de Datos</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        st.markdown("#### Configuración")
        origen = st.radio(
            "Origen de datos:",
            ("📂 Subir Archivo CSV", "🧪 Generación Sintética"),
            label_visibility="collapsed"
        )

        if origen == "📂 Subir Archivo CSV":
            archivo = st.file_uploader("Cargar CSV", type=["csv"])
            if archivo:
                try:
                    df_raw = pd.read_csv(archivo)
                    df_conv, cols_conv, fue_conv = convertir_likert(df_raw)
                    st.session_state.df = df_conv
                    if fue_conv:
                        st.success(f"✅ Archivo cargado. Se convirtieron **{len(cols_conv)} columnas** Likert a numérico automáticamente.")
                        with st.expander("🔢 Ver columnas convertidas"):
                            for c in cols_conv:
                                st.caption(f"• {c}")
                    else:
                        st.success("✅ Archivo cargado correctamente.")
                except Exception as e:
                    st.error(f"Error al leer el archivo: {e}")
        else:
            st.markdown("**Generar datos distribuidos normalmente**")
            n     = st.number_input("Tamaño de muestra (n ≥ 30)", min_value=30, value=100)
            media = st.number_input("Media real (μ)", value=50.0)
            desv  = st.number_input("Desviación estándar (σ)", min_value=0.1, value=10.0)
            if st.button("⚙️ Generar Muestra"):
                datos = np.random.normal(loc=media, scale=desv, size=int(n))
                st.session_state.df = pd.DataFrame({"Variable_Sintetica": datos})
                st.success("✅ Datos sintéticos generados.")

    with col2:
        st.markdown("#### Vista Previa")
        if st.session_state.df is not None:
            df = st.session_state.df
            st.dataframe(df.head(8), use_container_width=True)
            cols_num = df.select_dtypes(include=[np.number]).columns.tolist()
            st.caption(f"📋 {len(df)} registros · {len(df.columns)} columnas · {len(cols_num)} numéricas")
        else:
            st.info("⏳ Esperando carga de datos...")


# ═══════════════════════════════════════════════════════
# SECCIÓN 2: VISUALIZACIÓN
# ═══════════════════════════════════════════════════════
def seccion_visualizacion():
    st.markdown('<div class="section-title">📊 2. Análisis Exploratorio de Distribuciones</div>', unsafe_allow_html=True)

    if st.session_state.df is None:
        st.warning("⚠️ Primero carga datos en la sección 1.")
        return

    df = st.session_state.df
    columnas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
    if not columnas_numericas:
        st.error("❌ No se encontraron columnas numéricas.")
        return

    col_izq, col_der = st.columns([1, 2], gap="large")

    with col_izq:
        st.markdown("#### Selección de Variable")
        variable = st.selectbox("Variable a analizar:", columnas_numericas)
        datos    = df[variable].dropna()

        # Estadísticas descriptivas
        media    = datos.mean()
        mediana  = datos.median()
        desv_std = datos.std()
        asimetria = datos.skew()
        q1, q3  = datos.quantile(0.25), datos.quantile(0.75)
        iqr     = q3 - q1
        outliers = ((datos < (q1 - 1.5 * iqr)) | (datos > (q3 + 1.5 * iqr))).sum()

        st.markdown(f"""
        <div class="result-card">
            <strong style="color:#004d35;">Estadísticas descriptivas</strong><br><br>
            📐 Media: <strong>{media:.3f}</strong><br>
            📍 Mediana: <strong>{mediana:.3f}</strong><br>
            📏 Desv. Std: <strong>{desv_std:.3f}</strong><br>
            〰️ Asimetría: <strong>{asimetria:.3f}</strong><br>
            ⚠️ Outliers detectados: <strong>{outliers}</strong><br>
            🔢 N total: <strong>{len(datos)}</strong>
        </div>
        """, unsafe_allow_html=True)

        # ── Autoevaluación mejorada con respuestas visibles ──
        st.markdown("#### 🤔 Autoevaluación")

        # Determinar sugerencias automáticas (solo como guía visual)
        es_normal_auto = "Sí parece normal" if abs(asimetria) < 0.5 else "Presenta sesgo"
        st.text_area(
            "1. ¿La distribución parece normal?",
            key="q1",
            placeholder=f"Observa la forma de la curva y la simetría del histograma...\n"
                        f"(Pista: asimetría = {asimetria:.3f} → {es_normal_auto})"
        )
        tiene_outliers_auto = f"Sí, {outliers} outlier(s) detectado(s)" if outliers > 0 else "Sin outliers evidentes"
        st.text_area(
            "2. ¿Hay sesgo evidente u outliers?",
            key="q2",
            placeholder=f"Revisa el Boxplot y la distancia entre media y mediana...\n"
                        f"(Pista: {tiene_outliers_auto})"
        )

    with col_der:
        tab1, tab2, tab3 = st.tabs(["📈 Histograma + KDE", "📦 Boxplot", "📉 Q-Q Plot"])

        color_hist = "#00b87a"
        color_kde  = "#003d2e"

        with tab1:
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=datos, name="Frecuencia",
                histnorm="probability density",
                marker_color=color_hist, opacity=0.65,
                marker_line=dict(color="#005a3e", width=0.5)
            ))
            kde    = stats.gaussian_kde(datos)
            x_range = np.linspace(datos.min(), datos.max(), 300)
            fig.add_trace(go.Scatter(
                x=x_range, y=kde(x_range),
                mode="lines", name="KDE",
                line=dict(color=color_kde, width=2.5)
            ))
            fig.add_vline(x=media,   line_dash="dash", line_color="#f59e0b", annotation_text="Media")
            fig.add_vline(x=mediana, line_dash="dot",  line_color="#6366f1", annotation_text="Mediana")
            fig.update_layout(
                title=f"Distribución de {variable}",
                xaxis_title=variable, yaxis_title="Densidad",
                template="plotly_white", bargap=0.04, height=360
            )
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            fig_box = go.Figure()
            fig_box.add_trace(go.Box(
                y=datos, name=variable,
                marker_color=color_hist, boxmean="sd",
                boxpoints="outliers", line_color=color_kde
            ))
            fig_box.update_layout(
                title=f"Boxplot de {variable}",
                template="plotly_white", height=360
            )
            st.plotly_chart(fig_box, use_container_width=True)

        with tab3:
            (osm, osr), (slope, intercept, r) = stats.probplot(datos, dist="norm")
            fig_qq = go.Figure()
            fig_qq.add_trace(go.Scatter(
                x=osm, y=osr, mode="markers", name="Datos",
                marker=dict(color=color_hist, size=5, opacity=0.7)
            ))
            linea_x = np.array([osm[0], osm[-1]])
            fig_qq.add_trace(go.Scatter(
                x=linea_x, y=slope * linea_x + intercept,
                mode="lines", name="Línea teórica",
                line=dict(color=color_kde, dash="dash", width=2)
            ))
            fig_qq.update_layout(
                title=f"Q-Q Plot — Normal (R²={r**2:.4f})",
                xaxis_title="Cuantiles teóricos",
                yaxis_title="Cuantiles observados",
                template="plotly_white", height=360
            )
            st.plotly_chart(fig_qq, use_container_width=True)
            st.caption(f"R² = {r**2:.4f} — Valores cercanos a 1.0 indican mayor normalidad.")


# ═══════════════════════════════════════════════════════
# SECCIÓN 3: PRUEBA Z
# ═══════════════════════════════════════════════════════
def seccion_inferencia():
    st.markdown('<div class="section-title">🔬 3. Prueba de Hipótesis — Prueba Z</div>', unsafe_allow_html=True)

    if st.session_state.df is None:
        st.warning("⚠️ Carga datos para habilitar la inferencia.")
        return

    df = st.session_state.df
    columnas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
    if not columnas_numericas:
        return

    # ── Sidebar ──
    with st.sidebar:
        st.markdown('<div class="sidebar-header">🔬 Verde Analytics Lab</div>', unsafe_allow_html=True)

        # ── API Key aquí para que no interfiera con la prueba Z ──
        with st.expander("🔑 API Key de Gemini", expanded=(st.session_state.api_key == "")):
            api_input = st.text_input(
                "API Key:", type="password",
                value=st.session_state.api_key, placeholder="AIza...",
                key="api_key_input"
            )
            if st.button("💾 Guardar Key", key="guardar_key_sidebar"):
                st.session_state.api_key = api_input.strip()
                st.success("✅ Key guardada.")

        st.divider()
        st.markdown("### ⚙️ Parámetros Prueba Z")

        variable_z    = st.selectbox("Variable:", columnas_numericas, key="sb_varz")
        datos_z       = df[variable_z].dropna()
        n_z           = len(datos_z)
        media_muestral = datos_z.mean()
        desv_muestral  = datos_z.std()

        if n_z < 30:
            st.error(f"❌ n = {n_z} < 30. La Prueba Z no es válida.")
            st.stop()

        st.metric("Tamaño de muestra (n)", n_z)
        st.metric("Media muestral (x̄)", f"{media_muestral:.4f}")
        st.divider()

        h0_val   = st.number_input("H₀: μ =", value=float(round(media_muestral, 2)))
        tipo_h1  = st.selectbox("Hipótesis alternativa H₁:", (
            "Bilateral (μ ≠ h₀)",
            "Cola Derecha (μ > h₀)",
            "Cola Izquierda (μ < h₀)"
        ))
        alpha    = st.selectbox("Nivel de significancia (α)", (0.01, 0.05, 0.10), index=1)
        st.divider()

        sigma_conocida = st.number_input(
            "σ poblacional conocida:",
            min_value=0.01, value=10.0, step=0.5
        )

        # ── ADVERTENCIA si σ ingresada difiere mucho de la muestral ──
        diferencia_pct = abs(sigma_conocida - desv_muestral) / desv_muestral * 100
        if diferencia_pct > 30:
            st.markdown(f"""
            <div class="sigma-warning">
                ⚠️ <strong>Nota:</strong> La σ ingresada ({sigma_conocida:.2f}) difiere
                un {diferencia_pct:.0f}% de la desv. muestral ({desv_muestral:.2f}).
                Este valor <strong>debe ser conocido previamente</strong> (no estimado de la muestra).
                Asegúrate de que sea el parámetro poblacional real.
            </div>
            """, unsafe_allow_html=True)

        ejecutar = st.button("🚀 Ejecutar Prueba Z")

    # ── Cálculos — solo se ejecutan al presionar el botón ──
    if ejecutar:
        error_estandar = sigma_conocida / np.sqrt(n_z)
        z_score        = (media_muestral - h0_val) / error_estandar
        z_critico_inf = z_critico_sup = None

        if "Bilateral" in tipo_h1:
            p_value       = 2 * (1 - stats.norm.cdf(abs(z_score)))
            z_critico_sup = stats.norm.ppf(1 - alpha / 2)
            z_critico_inf = -z_critico_sup
            rechazo_h0    = abs(z_score) > z_critico_sup
            h1_texto      = f"μ ≠ {h0_val}"
            region_texto  = f"|Z| > ±{z_critico_sup:.4f}"
        elif "Derecha" in tipo_h1:
            p_value       = 1 - stats.norm.cdf(z_score)
            z_critico_sup = stats.norm.ppf(1 - alpha)
            rechazo_h0    = z_score > z_critico_sup
            h1_texto      = f"μ > {h0_val}"
            region_texto  = f"Z > {z_critico_sup:.4f}"
        else:
            p_value       = stats.norm.cdf(z_score)
            z_critico_inf = stats.norm.ppf(alpha)
            rechazo_h0    = z_score < z_critico_inf
            h1_texto      = f"μ < {h0_val}"
            region_texto  = f"Z < {z_critico_inf:.4f}"

        texto_decision = "⛔ Rechazar H₀" if rechazo_h0 else "✅ No Rechazar H₀"
        clase_decision = "rechazo" if rechazo_h0 else "no-rechazo"

        # ── Interpretación automática textual ──
        if rechazo_h0:
            interpretacion_auto = (
                f"Con un nivel de significancia α = {alpha}, existe evidencia estadística "
                f"suficiente para <strong>rechazar la hipótesis nula</strong>. "
                f"El estadístico Z = {z_score:.4f} cae en la región crítica ({region_texto}), "
                f"y el p-value ({p_value:.4e}) es menor que α ({alpha}). "
                f"Esto sugiere que la media poblacional <strong>no es igual a {h0_val}</strong> "
                f"bajo la hipótesis alternativa ({h1_texto})."
            )
        else:
            interpretacion_auto = (
                f"Con un nivel de significancia α = {alpha}, <strong>no existe evidencia "
                f"estadística suficiente para rechazar la hipótesis nula</strong>. "
                f"El estadístico Z = {z_score:.4f} no cae en la región crítica ({region_texto}), "
                f"y el p-value ({p_value:.4e}) es mayor o igual que α ({alpha}). "
                f"Los datos son consistentes con la hipótesis de que μ = {h0_val}."
            )

        # ── Guardar TODO en session_state para que persista entre recargas ──
        st.session_state.resultados_z = {
            "variable_nombre":            variable_z,
            "n":                          n_z,
            "media_muestral":             media_muestral,
            "h0_media":                   h0_val,
            "h1_texto":                   h1_texto,
            "sigma_poblacional_supuesta": sigma_conocida,
            "tipo_prueba":                tipo_h1,
            "alpha":                      alpha,
            "estadistico_z":              z_score,
            "p_value":                    p_value,
            "z_critico_sup":              z_critico_sup,
            "z_critico_inf":              z_critico_inf,
            "region_critica":             region_texto,
            "decision_automatica":        texto_decision,
            "clase_decision":             clase_decision,
            "interpretacion_auto":        interpretacion_auto,
        }

    # ── Mostrar resultados si ya hay datos calculados (persiste aunque se recargue) ──
    if st.session_state.resultados_z is not None:
        r = st.session_state.resultados_z
        z_score        = r["estadistico_z"]
        p_value        = r["p_value"]
        h0_val         = r["h0_media"]
        h1_texto       = r["h1_texto"]
        alpha          = r["alpha"]
        region_texto   = r["region_critica"]
        texto_decision = r["decision_automatica"]
        clase_decision = r["clase_decision"]
        interpretacion_auto = r["interpretacion_auto"]
        z_critico_sup  = r["z_critico_sup"]
        z_critico_inf  = r["z_critico_inf"]
        tipo_h1        = r["tipo_prueba"]

        # ── Layout de resultados ──
        c1, c2 = st.columns([1, 2], gap="large")

        with c1:
            # ── Hipótesis formales ──
            st.markdown("#### Hipótesis Planteadas")
            st.markdown(f"""
            <div class="hipotesis-box">
                <div class="hipotesis-title">📐 Hipótesis Estadísticas</div>
                <div class="hipotesis-h0">H₀: μ = {h0_val}</div>
                <div class="hipotesis-h1">H₁: {h1_texto}</div>
            </div>
            """, unsafe_allow_html=True)

            # ── Métricas numéricas ──
            st.markdown("#### Resultados Numéricos")
            clase_p = "green" if p_value > alpha else "red"

            z_critico_display = (
                f"±{z_critico_sup:.4f}" if z_critico_sup is not None and z_critico_inf is not None
                else f"{z_critico_sup:.4f}" if z_critico_sup is not None
                else f"{z_critico_inf:.4f}"
            )

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Estadístico Z calculado</div>
                <div class="metric-value">{z_score:.4f}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">p-value</div>
                <div class="metric-value {clase_p}">{p_value:.4e}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Valor crítico Zc (α={alpha})</div>
                <div class="metric-value">{z_critico_display}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Región de Rechazo</div>
                <div class="metric-value" style="font-size:16px;">{region_texto}</div>
            </div>
            """, unsafe_allow_html=True)

            # ── Decisión ──
            st.markdown(f"#### Decisión Estadística (α = {alpha})")
            st.markdown(
                f"<div class='decision-h0 {clase_decision}'>{texto_decision}</div>",
                unsafe_allow_html=True
            )

            # ── Interpretación automática textual ──
            st.markdown("#### Interpretación Automática")
            st.markdown(
                f'<div class="interpretacion-box">{interpretacion_auto}</div>',
                unsafe_allow_html=True
            )

        with c2:
            st.markdown("#### Región Crítica — Curva Normal")
            x = np.linspace(-4, 4, 600)
            y = stats.norm.pdf(x)

            fig_z = go.Figure()

            # Curva principal
            fig_z.add_trace(go.Scatter(
                x=x, y=y, mode="lines", name="N(0,1)",
                line=dict(color="#003d2e", width=2.5)
            ))

            color_rojo  = "rgba(190, 18, 60, 0.30)"
            color_verde = "rgba(0, 180, 120, 0.10)"

            # Zona NO rechazo (verde)
            x_verde_min = z_critico_inf if z_critico_inf is not None else -4
            x_verde_max = z_critico_sup if z_critico_sup is not None else 4
            x_nrec = np.linspace(x_verde_min, x_verde_max, 400)
            fig_z.add_trace(go.Scatter(
                x=x_nrec, y=stats.norm.pdf(x_nrec),
                fill="tozeroy", fillcolor=color_verde,
                mode="none", name="No rechazo H₀", showlegend=True
            ))

            # Zona rechazo (roja)
            if z_critico_sup is not None:
                x_der = np.linspace(z_critico_sup, 4, 200)
                fig_z.add_trace(go.Scatter(
                    x=x_der, y=stats.norm.pdf(x_der),
                    fill="tozeroy", fillcolor=color_rojo,
                    mode="none", name="Zona rechazo", showlegend=True
                ))
            if z_critico_inf is not None:
                x_izq = np.linspace(-4, z_critico_inf, 200)
                fig_z.add_trace(go.Scatter(
                    x=x_izq, y=stats.norm.pdf(x_izq),
                    fill="tozeroy", fillcolor=color_rojo,
                    mode="none", name="Zona rechazo (izq)", showlegend=False
                ))

            # Línea Z calculado
            fig_z.add_vline(
                x=z_score, line_width=3, line_dash="dash",
                line_color="#f59e0b",
                annotation_text=f"Z={z_score:.2f}",
                annotation_font_color="#f59e0b",
                annotation_position="top"
            )

            # Líneas críticas
            if z_critico_sup is not None:
                fig_z.add_vline(
                    x=z_critico_sup, line_width=1.5, line_dash="dot",
                    line_color="#be123c",
                    annotation_text=f"Zc={z_critico_sup:.2f}",
                    annotation_font_color="#be123c"
                )
            if z_critico_inf is not None:
                fig_z.add_vline(
                    x=z_critico_inf, line_width=1.5, line_dash="dot",
                    line_color="#be123c",
                    annotation_text=f"Zc={z_critico_inf:.2f}",
                    annotation_font_color="#be123c",
                    annotation_position="top left"
                )

            fig_z.update_layout(
                title=f"Distribución N(0,1) · {tipo_h1} · α={alpha}",
                xaxis_title="Valor Z", yaxis_title="Densidad",
                template="plotly_white", height=400,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_z, use_container_width=True)

        # ── Módulo IA ──
        seccion_ia()


# ═══════════════════════════════════════════════════════
# SECCIÓN 4: ASISTENTE IA (GEMINI)
# ═══════════════════════════════════════════════════════

MODELO_GEMINI = "gemini-2.5-flash"

def llamar_gemini_api(key: str, resumen: dict) -> str:
    """
    Llama a Gemini usando el SDK oficial google-genai.
    Requiere: pip install google-genai
    """
    try:
        from google import genai as google_genai
        from google.genai import types as genai_types
    except ImportError:
        return ("Error: Falta instalar el SDK. Ejecuta en tu terminal:\n"
                "pip install google-genai\n"
                "y luego reinicia la app.")

    try:
        interpretacion = resumen.get("interpretacion_estudiante", "(sin interpretación)")
        decision_auto  = resumen.get("decision_automatica", "")

        prompt_text = f"""Eres un asistente de laboratorio estadístico profesional, serio y didáctico.

Se realizó una Prueba Z para la media con los siguientes parámetros:

DATOS DE LA PRUEBA:
- Variable analizada: {resumen['variable_nombre']}
- Tamaño de muestra (n): {resumen['n']}
- Media muestral (x̄): {resumen['media_muestral']:.4f}
- Hipótesis Nula H₀: μ = {resumen['h0_media']}
- Hipótesis Alternativa H₁: {resumen['h1_texto']}
- Nivel de significancia (α): {resumen['alpha']}
- Desviación estándar poblacional (σ): {resumen['sigma_poblacional_supuesta']}
- Tipo de prueba: {resumen['tipo_prueba']}

RESULTADOS:
- Estadístico Z calculado: {resumen['estadistico_z']:.4f}
- p-value: {resumen['p_value']:.4e}
- Región crítica: {resumen['region_critica']}
- Decisión automática del sistema: {decision_auto}

INTERPRETACIÓN DEL ESTUDIANTE:
"{interpretacion}"

Por favor realiza las siguientes tareas:

1. VERIFICACIÓN DE LA DECISIÓN: Confirma si la decisión '{decision_auto}' es correcta, explicando la relación entre el p-value y α, y si el estadístico Z cae o no en la región crítica.

2. SUPUESTOS DE LA PRUEBA Z: Evalúa si los supuestos (n ≥ 30 y σ conocida) son razonables en este caso.

3. COMPARACIÓN CON EL ESTUDIANTE: Compara la interpretación del estudiante con la decisión automática. ¿Coinciden? ¿La interpretación es correcta y usa terminología estadística adecuada? Señala aciertos y corrige con amabilidad si hay errores.

4. CONCLUSIÓN FINAL: Resume qué se puede inferir de estos resultados en términos estadísticos y prácticos.

Usa un tono profesional y educativo. No uses emojis. Responde en español."""

        client = google_genai.Client(api_key=key)
        response = client.models.generate_content(
            model=MODELO_GEMINI,
            contents=prompt_text,
            config=genai_types.GenerateContentConfig(
                temperature=0.3,
                max_output_tokens=4096,
            )
        )
        return response.text

    except Exception as e:
        msg = str(e)
        if "429" in msg:
            return "Error 429: Cuota agotada. Crea una nueva API Key en aistudio.google.com/app/apikey → 'Create API key in new project'."
        if "403" in msg or "API_KEY" in msg.upper() or "invalid" in msg.lower():
            return "Error de autenticación: La API Key no es válida o no tiene permisos."
        if "404" in msg or "not found" in msg.lower():
            return "Error 404: Modelo no encontrado. Verifica que tu API Key tenga acceso a Gemini."
        return f"Error inesperado: {msg}"


def seccion_ia():
    st.markdown('<div class="section-title">🤖 4. Asistente IA — Gemini Lab Bot</div>', unsafe_allow_html=True)

    st.info(
        "💡 **¿Cómo funciona?** Ingresa tu API Key de Google Gemini en la barra lateral "
        "(gratuita en [aistudio.google.com](https://aistudio.google.com/app/apikey)) "
        "y el bot analizará tus resultados. Tu key **nunca se comparte**.",
        icon="🔑"
    )

    if st.session_state.resultados_z is None:
        st.warning("⚠️ Ejecuta primero la Prueba Z para habilitar el asistente.")
        return

    resumen = st.session_state.resultados_z

    st.markdown("#### Validación y Conclusiones")
    col_ia1, col_ia2 = st.columns([1, 1], gap="large")

    with col_ia1:
        st.markdown("**Tu interpretación (escribe tu conclusión):**")
        decision_estudiante = st.text_area(
            "Conclusión del estudiante:",
            key="decision_estudiante",
            height=150,
            label_visibility="collapsed",
            placeholder="Basándome en el p-value y el estadístico Z, concluyo que..."
        )

    with col_ia2:
        st.markdown("**Resumen que se enviará a Gemini:**")
        st.markdown(f'''
        <div class="result-card" style="font-size:13px;">
            <strong>Variable:</strong> {resumen['variable_nombre']} · n = {resumen['n']}<br>
            <strong>H₀:</strong> μ = {resumen['h0_media']} &nbsp;|&nbsp; <strong>H₁:</strong> {resumen['h1_texto']}<br>
            <strong>Z =</strong> {resumen['estadistico_z']:.4f} · <strong>p =</strong> {resumen['p_value']:.4e}<br>
            <strong>Región crítica:</strong> {resumen['region_critica']}<br>
            <strong>Decisión:</strong> {resumen['decision_automatica']}
        </div>
        ''', unsafe_allow_html=True)

        st.caption(f"🤖 Modelo: {MODELO_GEMINI}")

        if st.button("🧠 Consultar a Gemini Lab Bot"):
            if not st.session_state.api_key:
                st.error("❌ Primero guarda tu API Key en la barra lateral.")
            else:
                resumen_completo = {**resumen, "interpretacion_estudiante": decision_estudiante}
                with st.spinner("Analizando resultados con Gemini..."):
                    respuesta = llamar_gemini_api(st.session_state.api_key, resumen_completo)

                if respuesta and not respuesta.startswith("Error"):
                    st.markdown("#### 💬 Respuesta del Asistente:")
                    st.markdown(f'<div class="ia-response">{respuesta}</div>', unsafe_allow_html=True)

                    # ── Comparación automática de decisiones ──
                    st.markdown("#### 🔍 Comparación de Decisiones")
                    decision_auto = resumen['decision_automatica']

                    if decision_estudiante.strip():
                        palabras_rechazo    = ["rechaz", "sí se rechaza", "si se rechaza", "reject"]
                        palabras_no_rechazo = ["no se rechaza", "no rechaz", "no hay evidencia", "fail to reject"]
                        est_lower           = decision_estudiante.lower()
                        auto_es_rechazo     = "Rechazar" in decision_auto

                        estudiante_dice_rechazo    = any(p in est_lower for p in palabras_rechazo)
                        estudiante_dice_no_rechazo = any(p in est_lower for p in palabras_no_rechazo)

                        if   estudiante_dice_rechazo and auto_es_rechazo:         match = True
                        elif estudiante_dice_no_rechazo and not auto_es_rechazo:  match = True
                        elif estudiante_dice_rechazo and not auto_es_rechazo:     match = False
                        elif estudiante_dice_no_rechazo and auto_es_rechazo:      match = False
                        else:                                                      match = None

                        if match is True:
                            st.markdown('''
                            <div class="comparacion-box coincide">
                                ✅ Tu conclusión <strong>coincide</strong> con la decisión automática del sistema.
                            </div>''', unsafe_allow_html=True)
                        elif match is False:
                            st.markdown(f'''
                            <div class="comparacion-box no-coincide">
                                ⚠️ Tu conclusión <strong>difiere</strong> de la decisión automática ({decision_auto}).
                                Revisa la interpretación del asistente para identificar el error.
                            </div>''', unsafe_allow_html=True)
                        else:
                            st.info("ℹ️ No se pudo determinar automáticamente. Compara manualmente con la decisión del sistema.")
                    else:
                        st.info("ℹ️ Escribe tu interpretación para habilitar la comparación automática.")
                else:
                    st.error(f"❌ {respuesta}")
                    st.markdown("""
                    **Verifica:**
                    - Que tu API Key sea válida (cópiala directamente de aistudio.google.com)
                    - Que no tenga espacios al inicio o al final
                    - Que tengas conexión a internet
                    """)


# ═══════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════
def mostrar_footer():
    st.markdown("""
    <div class="footer">
        Verde Analytics Lab · Módulo de Distribuciones y Pruebas de Hipótesis<br>
        Desarrollado con Streamlit · Python · Plotly · SciPy · Google Gemini API (gemini-2.5-flash-preview-04-17)
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# FLUJO PRINCIPAL
# ═══════════════════════════════════════════════════════
def main():
    aplicar_estilos_visuales()
    inicializar_estado()
    seccion_carga_datos()
    seccion_visualizacion()
    seccion_inferencia()
    mostrar_footer()


if __name__ == "__main__":
    main()
