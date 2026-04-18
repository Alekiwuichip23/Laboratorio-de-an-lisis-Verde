import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import scipy.stats as stats
 
st.set_page_config(
    page_title="Laboratorio de Análisis Verde",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
COLOR_DARK  = "#003d2e"
COLOR_VERDE = "#00b87a"
 
# ═══════════════════════════════════════════════════════
# ESTILOS
# ═══════════════════════════════════════════════════════
def aplicar_estilos_visuales():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
    html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }
 
    .header-wrap {
        background: linear-gradient(135deg, #002418 0%, #004d35 50%, #007a55 100%);
        border-radius: 20px; padding: 44px 52px 40px; margin-bottom: 36px;
        position: relative; overflow: hidden;
        box-shadow: 0 20px 60px rgba(0,77,53,0.35);
    }
    .header-badge {
        display: inline-block; background: rgba(255,255,255,0.1); color: #7fffd4;
        border: 1px solid rgba(127,255,212,0.3); border-radius: 20px;
        padding: 5px 16px; font-size: 11px; font-weight: 600;
        letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 16px;
    }
    .header-title { color:#fff; font-size:42px; font-weight:700; letter-spacing:-1px; margin:0 0 8px; }
    .header-title span { color: #7fffd4; }
    .header-sub { color: rgba(255,255,255,0.6); font-size:15px; margin:0; }
 
    .section-title {
        background: linear-gradient(90deg, #e8f8f0 0%, #f5fffe 100%);
        color: #004d35; font-size: 17px; font-weight: 700;
        padding: 14px 22px; border-radius: 12px;
        border-left: 5px solid #00b87a; margin: 28px 0 20px;
    }
    .result-card {
        background: #f5fffe; padding: 20px 24px; border-radius: 14px;
        border: 1px solid #b2eed8; border-left: 5px solid #00b87a;
        margin-bottom: 16px; line-height: 1.8;
    }
    .error-card {
        background: #fff5f5; padding: 20px 24px; border-radius: 14px;
        border: 1px solid #fecaca; border-left: 5px solid #ef4444;
        margin-bottom: 16px; line-height: 1.8;
    }
 
    /* BARRA RESUMEN GRANDE */
    .barra-resumen {
        background: linear-gradient(135deg, #002418 0%, #004d35 100%);
        border-radius: 18px; padding: 30px 36px; margin: 24px 0 28px;
        box-shadow: 0 8px 32px rgba(0,77,53,0.3);
        display: flex; gap: 0; align-items: stretch;
    }
    .barra-item {
        flex: 1; text-align: center; padding: 0 20px;
        border-right: 1px solid rgba(127,255,212,0.2);
    }
    .barra-item:last-child { border-right: none; }
    .barra-item-label {
        color: #7fffd4; font-size: 11px; font-weight: 600;
        letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 12px;
    }
    .barra-item-valor {
        color: #ffffff; font-size: 32px; font-weight: 700;
        font-family: 'JetBrains Mono', monospace; line-height: 1;
    }
    .barra-item-valor.rojo  { color: #fca5a5; }
    .barra-item-valor.verde { color: #6ee7b7; }
    .barra-item-sub { color: rgba(255,255,255,0.45); font-size: 12px; margin-top: 8px; }
 
    /* Métricas */
    .metric-card {
        background: #ffffff; border: 1px solid #d6f5e8; border-radius: 16px;
        padding: 18px 14px; text-align: center; margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,180,120,0.07);
    }
    .metric-label {
        color: #6b7280; font-size: 10px; font-weight: 600;
        text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px;
    }
    .metric-value {
        color: #002418; font-size: 22px; font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }
    .metric-value.red   { color: #be123c; }
    .metric-value.green { color: #15803d; }
 
    .hipotesis-box {
        background: #ffffff; border: 1.5px solid #b2eed8; border-radius: 14px;
        padding: 18px 22px; margin-bottom: 16px; font-family: 'JetBrains Mono', monospace;
    }
    .hipotesis-title {
        color: #6b7280; font-size: 11px; font-weight: 600;
        letter-spacing: 1px; text-transform: uppercase; margin-bottom: 10px;
        font-family: 'Space Grotesk', sans-serif;
    }
    .hipotesis-h0 { color: #15803d; font-size: 20px; font-weight: 600; margin-bottom: 6px; }
    .hipotesis-h1 { color: #b91c1c; font-size: 20px; font-weight: 600; }
 
    .decision-h0 {
        font-weight: 700; font-size: 24px; padding: 22px; border-radius: 14px;
        text-align: center; margin-top: 12px;
    }
    .rechazo    { background: #fff1f2; color: #be123c; border: 2px solid #fda4af; }
    .no-rechazo { background: #f0fdf4; color: #166534; border: 2px solid #86efac; }
 
    .interpretacion-box {
        background: linear-gradient(135deg, #f0fdf8, #e8faf2);
        border: 1px solid #b2eed8; border-radius: 14px; padding: 20px 24px;
        margin-top: 14px; font-size: 14px; line-height: 1.7; color: #1f2937;
    }
    .interpretacion-box strong { color: #004d35; }
 
    .sigma-warning {
        background: #fffbeb; border: 1px solid #fcd34d;
        border-left: 4px solid #f59e0b; border-radius: 10px;
        padding: 12px 16px; font-size: 13px; color: #78350f; margin-top: 8px;
    }
    .sidebar-header {
        background: linear-gradient(135deg, #002418, #004d35); color: white;
        padding: 18px 22px; border-radius: 14px; font-size: 17px; font-weight: 700;
        margin-bottom: 22px; text-align: center;
    }
    div.stButton > button {
        background-color: #d1fae5 !important; color: #065f46 !important;
        border: 1.5px solid #6ee7b7 !important; border-radius: 10px !important;
        font-weight: 600 !important; padding: 8px 20px !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        background-color: #a7f3d0 !important; border-color: #34d399 !important;
        transform: translateY(-1px) !important;
    }
    .ia-response {
        background: #f8fffc; border: 1px solid #6ee7b7; border-left: 5px solid #00b87a;
        border-radius: 14px; padding: 22px 26px; font-size: 14px;
        line-height: 1.8; color: #1f2937; white-space: pre-wrap;
    }
    .comparacion-box {
        border-radius: 14px; padding: 16px 20px; margin-top: 12px;
        font-size: 14px; font-weight: 600; text-align: center;
    }
    .coincide    { background: #f0fdf4; color: #166534; border: 2px solid #86efac; }
    .no-coincide { background: #fff1f2; color: #be123c; border: 2px solid #fda4af; }
    .footer {
        text-align: center; color: #9ca3af; font-size: 12px;
        padding: 36px 0 14px; border-top: 1px solid #e5e7eb; margin-top: 48px;
    }
    </style>
 
    <div class="header-wrap">
        <div class="header-badge">🔬 Laboratorio Estadístico</div>
        <div class="header-title">Verde <span>Analytics</span> Lab</div>
        <p class="header-sub">Distribuciones de Probabilidad · Pruebas de Hipótesis · Asistente IA (Gemini)</p>
    </div>
    """, unsafe_allow_html=True)
 
 
# ═══════════════════════════════════════════════════════
# INICIALIZACIÓN
# ═══════════════════════════════════════════════════════
def inicializar_estado():
    clave_por_defecto = ""
    try:
        clave_por_defecto = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        pass
    defaults = {'df': None, 'api_key': clave_por_defecto, 'resultados_z': None}
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
 
 
# ═══════════════════════════════════════════════════════
# VALIDACIÓN CSV
# ═══════════════════════════════════════════════════════
def validar_y_cargar_csv(archivo):
    try:
        df = pd.read_csv(archivo)
    except Exception as e:
        return None, f"No se pudo leer el archivo: {e}"
    if df.empty:
        return None, "El archivo CSV está vacío."
 
    cols_texto = [c for c in df.columns if df[c].dtype == object]
    if cols_texto:
        lista = " · ".join([f"**{c}**" for c in cols_texto[:6]])
        msg = (
            f"❌ **Columnas con texto detectadas:** {lista}\n\n"
            f"**¿Por qué solo se aceptan números?** La Prueba Z necesita calcular "
            f"medias y desviaciones — imposible con texto.\n\n"
            f"**Solución:** Elimina esas columnas o usa la Generación Sintética."
        )
        return None, msg
 
    cols_num = df.select_dtypes(include=[np.number]).columns.tolist()
    if not cols_num:
        return None, "No hay columnas numéricas en el archivo."
    df = df[cols_num].dropna(axis=1, how='all')
    return df, None
 
 
# ═══════════════════════════════════════════════════════
# SECCIÓN 1: CARGA DE DATOS
# ═══════════════════════════════════════════════════════
def seccion_carga_datos():
    st.markdown('<div class="section-title">☘️ 1. Adquisición de Datos</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2], gap="large")
 
    with col1:
        st.markdown("#### Configuración")
        origen = st.radio("Origen:", ("📂 Subir Archivo CSV", "🧪 Generación Sintética"),
                          label_visibility="collapsed")
 
        if origen == "📂 Subir Archivo CSV":
            st.info("⚠️ El CSV debe tener **solo columnas numéricas**.", icon="📋")
            archivo = st.file_uploader("Cargar CSV", type=["csv"])
            if archivo:
                df_ok, err = validar_y_cargar_csv(archivo)
                if err:
                    st.markdown(f'<div class="error-card">{err}</div>', unsafe_allow_html=True)
                    st.session_state.df = None
                else:
                    st.session_state.df = df_ok
                    st.success(f"✅ {len(df_ok)} filas · {len(df_ok.columns)} columnas")
        else:
            st.markdown("**Datos de ejemplo (distribución normal)**")
            n     = st.number_input("Tamaño de muestra (n ≥ 30)", min_value=30, value=100)
            media = st.number_input("Media real (μ)", value=75.0)
            desv  = st.number_input("Desviación estándar (σ)", min_value=0.1, value=10.0)
            if st.button("⚙️ Generar Muestra"):
                datos = np.random.normal(loc=media, scale=desv, size=int(n))
                st.session_state.df = pd.DataFrame({"Calificaciones": datos})
                st.session_state.resultados_z = None
                st.success("✅ Datos generados correctamente.")
 
    with col2:
        st.markdown("#### Vista Previa")
        if st.session_state.df is not None:
            df = st.session_state.df
            st.dataframe(df.head(8), use_container_width=True)
            st.caption(f"📋 {len(df)} registros · {len(df.columns)} columnas numéricas")
        else:
            st.info("⏳ Esperando datos...")
 
 
# ═══════════════════════════════════════════════════════
# SECCIÓN 2: VISUALIZACIÓN
# ═══════════════════════════════════════════════════════
def seccion_visualizacion():
    st.markdown('<div class="section-title">📊 2. Análisis Exploratorio de Distribuciones</div>',
                unsafe_allow_html=True)
 
    if st.session_state.df is None:
        st.warning("⚠️ Primero carga datos en la sección 1.")
        return
 
    df = st.session_state.df
    cols_num = df.select_dtypes(include=[np.number]).columns.tolist()
    if not cols_num:
        st.error("❌ No hay columnas numéricas.")
        return
 
    col_izq, col_der = st.columns([1, 2], gap="large")
 
    with col_izq:
        st.markdown("#### Variable a analizar")
        variable = st.selectbox("Selecciona:", cols_num)
        datos = df[variable].dropna()
 
        media     = datos.mean()
        mediana   = datos.median()
        desv_std  = datos.std()
        asimetria = datos.skew()
        q1, q3    = datos.quantile(0.25), datos.quantile(0.75)
        iqr       = q3 - q1
        outliers  = int(((datos < q1 - 1.5*iqr) | (datos > q3 + 1.5*iqr)).sum())
 
        st.markdown(f"""
        <div class="result-card">
            <strong style="color:#004d35;">📊 Estadísticas descriptivas</strong><br><br>
            📐 Media: <strong>{media:.3f}</strong><br>
            📍 Mediana: <strong>{mediana:.3f}</strong><br>
            📏 Desv. Std: <strong>{desv_std:.3f}</strong><br>
            〰️ Asimetría: <strong>{asimetria:.3f}</strong><br>
            ⚠️ Outliers: <strong>{outliers}</strong><br>
            🔢 N: <strong>{len(datos)}</strong>
        </div>
        """, unsafe_allow_html=True)
 
        # ── Autoevaluación con expanders ──
        st.markdown("#### 🤔 Autoevaluación")
        st.caption("Observa las gráficas y responde:")
 
        pista_normal   = "Sí parece normal"    if abs(asimetria) < 0.5 else "Presenta sesgo"
        pista_outliers = f"Sí, {outliers} detectado(s)" if outliers > 0 else "No hay outliers"
 
        with st.expander("❓ 1. ¿La distribución parece normal?", expanded=True):
            st.caption(f"💡 Pista: asimetría = {asimetria:.3f} → {pista_normal}")
            resp_normal = st.radio("rn", label_visibility="collapsed", key="q1_radio",
                options=[
                    "Sí, tiene forma de campana simétrica",
                    "Más o menos, tiene un ligero sesgo",
                    "No, tiene sesgo marcado o forma irregular",
                    "No estoy seguro/a",
                ])
 
        with st.expander("❓ 2. ¿Hay sesgo evidente u outliers?", expanded=True):
            st.caption(f"💡 Pista: {pista_outliers} | Media={media:.2f} vs Mediana={mediana:.2f}")
            resp_sesgo = st.radio("rs", label_visibility="collapsed", key="q2_radio",
                options=[
                    "No hay sesgo ni outliers importantes",
                    "Hay un sesgo leve pero sin outliers",
                    "Sí hay outliers visibles en el boxplot",
                    "Sí hay sesgo marcado (media y mediana muy alejadas)",
                    "No estoy seguro/a",
                ])
 
        with st.expander("3. ¿El tamaño de muestra es suficiente para la Prueba Z?", expanded=True):
            pista_n = f"Sí, n = {len(datos)} ≥ 30" if len(datos) >= 30 else f"No, n = {len(datos)} < 30"
            st.caption(f"Pista: {pista_n}")
            resp_n = st.radio("rn2", label_visibility="collapsed", key="q3_radio",
                options=[
                    f"Sí, n = {len(datos)} ≥ 30, cumple el requisito de la Prueba Z",
                    f"No, n = {len(datos)} < 30, se debería usar Prueba T",
                    "No sé cuál es el requisito mínimo",
                ])
 
        st.session_state['resp_normal'] = resp_normal
        st.session_state['resp_sesgo']  = resp_sesgo
        st.session_state['resp_n']      = resp_n
 
    with col_der:
        tab1, tab2, tab3 = st.tabs(["📈 Histograma + KDE", "📦 Boxplot", "📉 Q-Q Plot"])
 
        with tab1:
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=datos, name="Frecuencia observada",
                histnorm="probability density", nbinsx=20,
                marker=dict(color=COLOR_VERDE, opacity=0.75,
                            line=dict(color=COLOR_DARK, width=0.8)),
            ))
            kde = stats.gaussian_kde(datos)
            xr  = np.linspace(datos.min(), datos.max(), 300)
            fig.add_trace(go.Scatter(
                x=xr, y=kde(xr), mode="lines", name="Curva KDE (suavizado)",
                line=dict(color=COLOR_DARK, width=3)
            ))
            fig.add_vline(x=media, line_dash="dash", line_color="#f59e0b", line_width=2,
                          annotation_text=f"Media = {media:.2f}",
                          annotation_font_size=12, annotation_font_color="#f59e0b")
            fig.add_vline(x=mediana, line_dash="dot", line_color="#6366f1", line_width=2,
                          annotation_text=f"Mediana = {mediana:.2f}",
                          annotation_font_size=12, annotation_font_color="#6366f1",
                          annotation_position="top left")
            fig.update_layout(
                title=dict(text=f"Distribución de <b>{variable}</b>", font_size=16),
                xaxis_title=variable, yaxis_title="Densidad",
                template="plotly_white", bargap=0.05, height=390,
                legend=dict(orientation="h", y=1.12),
                font=dict(family="Space Grotesk"),
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption("🟡 Línea amarilla = Media  |  🟣 Línea morada = Mediana  |  "
                       "Si están muy juntas y la curva es simétrica → distribución normal.")
 
        with tab2:
            fig_box = go.Figure()
            fig_box.add_trace(go.Box(
                y=datos, name=variable,
                marker_color=COLOR_VERDE,
                boxmean="sd",
                boxpoints="outliers",
                line_color=COLOR_DARK,
                fillcolor="rgba(0,184,122,0.18)",
                line_width=2,
                marker_size=6,
            ))
            fig_box.update_layout(
                title=dict(text=f"Boxplot de <b>{variable}</b>", font_size=16),
                yaxis_title=variable,
                template="plotly_white", height=390,
                font=dict(family="Space Grotesk"),
            )
            st.plotly_chart(fig_box, use_container_width=True)
            st.caption("Los puntos fuera de los bigotes son outliers. "
                       "La línea central = mediana. La caja = 50% central de los datos.")
 
        with tab3:
            (osm, osr), (slope, intercept, r) = stats.probplot(datos, dist="norm")
            fig_qq = go.Figure()
            x_line = np.array([osm[0], osm[-1]])
            fig_qq.add_trace(go.Scatter(
                x=x_line, y=slope * x_line + intercept,
                mode="lines", name="Línea ideal (normal perfecta)",
                line=dict(color="#ef4444", dash="dash", width=2.5)
            ))
            fig_qq.add_trace(go.Scatter(
                x=osm, y=osr, mode="markers", name="Datos observados",
                marker=dict(color=COLOR_VERDE, size=7, opacity=0.85,
                            line=dict(color=COLOR_DARK, width=0.5))
            ))
            fig_qq.update_layout(
                title=dict(text=f"Q-Q Plot — Normalidad (R² = {r**2:.3f})", font_size=16),
                xaxis_title="Cuantiles teóricos (si fuera normal perfecta)",
                yaxis_title="Cuantiles observados en tus datos",
                template="plotly_white", height=390,
                font=dict(family="Space Grotesk"),
            )
            st.plotly_chart(fig_qq, use_container_width=True)
            interp_r = (
                "✅ Excelente — muy normal" if r**2 > 0.98 else
                "✅ Bueno — bastante normal" if r**2 > 0.95 else
                "⚠️ Regular — algo de desviación" if r**2 > 0.90 else
                "❌ Bajo — no sigue distribución normal"
            )
            st.caption(f"R² = {r**2:.4f} → {interp_r}. "
                       "Si los puntos verdes siguen la línea roja → tus datos son normales.")
 
 
# ═══════════════════════════════════════════════════════
# SECCIÓN 3: PRUEBA Z
# ═══════════════════════════════════════════════════════
def seccion_inferencia():
    st.markdown('<div class="section-title">🔬 3. Prueba de Hipótesis — Prueba Z</div>',
                unsafe_allow_html=True)
 
    if st.session_state.df is None:
        st.warning("⚠️ Carga datos primero.")
        return
 
    df = st.session_state.df
    cols_num = df.select_dtypes(include=[np.number]).columns.tolist()
    if not cols_num:
        return
 
    # ── Sidebar ──
    with st.sidebar:
        st.markdown('<div class="sidebar-header">🔬 Verde Analytics Lab</div>', unsafe_allow_html=True)
 
        with st.expander("🔑 API Key de Gemini", expanded=(st.session_state.api_key == "")):
            api_input = st.text_input("API Key:", type="password",
                                      value=st.session_state.api_key,
                                      placeholder="AIza...", key="api_key_input")
            if st.button("💾 Guardar Key", key="guardar_key"):
                st.session_state.api_key = api_input.strip()
                st.success("✅ Key guardada.")
 
        st.divider()
        st.markdown("### ⚙️ Parámetros Prueba Z")
 
        variable_z     = st.selectbox("Variable:", cols_num, key="sb_varz")
        datos_z        = df[variable_z].dropna()
        n_z            = len(datos_z)
        media_muestral = datos_z.mean()
        desv_muestral  = datos_z.std()
 
        if n_z < 30:
            st.error(f"❌ n = {n_z} < 30. La Prueba Z no es válida.")
            st.stop()
 
        st.metric("n (tamaño muestra)", n_z)
        st.metric("x̄ (media muestral)", f"{media_muestral:.4f}")
        st.divider()
 
        st.markdown("**Define tu hipótesis:**")
        # H0 por defecto diferente a la media para que Z no sea 0
        h0_sugerido = float(round(media_muestral - 5, 1))
        h0_val = st.number_input(
            "H₀: μ =", value=h0_sugerido,
            help="⚠️ Si pones el mismo valor que la media muestral, Z = 0. Pon un valor diferente."
        )
 
        # Aviso si H0 == media
        if abs(h0_val - media_muestral) < 0.001:
            st.warning("⚠️ H₀ es igual a la media muestral → Z = 0. Cambia H₀ para obtener un resultado significativo.")
 
        tipo_h1 = st.selectbox("Hipótesis alternativa H₁:", (
            "Bilateral (μ ≠ H₀)  — dos colas",
            "Cola Derecha (μ > H₀)  — una cola derecha",
            "Cola Izquierda (μ < H₀)  — una cola izquierda",
        ))
        alpha = st.selectbox("Nivel de significancia (α)", (0.01, 0.05, 0.10), index=1)
        st.divider()
 
        sigma_conocida = st.number_input(
            "σ poblacional conocida:", min_value=0.01,
            value=float(round(desv_muestral, 2)), step=0.5,
            help="Desviación estándar de la POBLACIÓN (no de la muestra)"
        )
 
        dif_pct = abs(sigma_conocida - desv_muestral) / desv_muestral * 100
        if dif_pct > 30:
            st.markdown(f"""
            <div class="sigma-warning">
                ⚠️ σ ingresada ({sigma_conocida:.2f}) difiere {dif_pct:.0f}%
                de la desv. muestral ({desv_muestral:.2f}).
            </div>""", unsafe_allow_html=True)
 
        ejecutar = st.button("🚀 Ejecutar Prueba Z", use_container_width=True)
 
    # ── Cálculos ──
    if ejecutar:
        error_est  = sigma_conocida / np.sqrt(n_z)
        z_score    = (media_muestral - h0_val) / error_est
        z_ci = z_cs = None
 
        if "Bilateral" in tipo_h1:
            p_value  = 2 * (1 - stats.norm.cdf(abs(z_score)))
            z_cs     = stats.norm.ppf(1 - alpha / 2)
            z_ci     = -z_cs
            rechazo  = abs(z_score) > z_cs
            h1_texto = f"μ ≠ {h0_val}"
            reg_txt  = f"|Z| > ±{z_cs:.4f}"
            tipo_cola = "Bilateral (dos colas)"
        elif "Derecha" in tipo_h1:
            p_value  = 1 - stats.norm.cdf(z_score)
            z_cs     = stats.norm.ppf(1 - alpha)
            rechazo  = z_score > z_cs
            h1_texto = f"μ > {h0_val}"
            reg_txt  = f"Z > {z_cs:.4f}"
            tipo_cola = "Cola derecha"
        else:
            p_value  = stats.norm.cdf(z_score)
            z_ci     = stats.norm.ppf(alpha)
            rechazo  = z_score < z_ci
            h1_texto = f"μ < {h0_val}"
            reg_txt  = f"Z < {z_ci:.4f}"
            tipo_cola = "Cola izquierda"
 
        decision_txt = "⛔ Rechazar H₀" if rechazo else "✅ No Rechazar H₀"
        clase_dec    = "rechazo"         if rechazo else "no-rechazo"
 
        if rechazo:
            interp = (
                f"Con α = {alpha}, existe evidencia estadística suficiente para "
                f"<strong>rechazar H₀</strong>. El estadístico Z = {z_score:.4f} cae en "
                f"la región crítica ({reg_txt}) y p-value = {p_value:.4e} < α = {alpha}. "
                f"Se concluye que {h1_texto}."
            )
        else:
            interp = (
                f"Con α = {alpha}, <strong>no hay evidencia suficiente para rechazar H₀</strong>. "
                f"Z = {z_score:.4f} no cae en la región crítica ({reg_txt}) y "
                f"p-value = {p_value:.4e} ≥ α = {alpha}. "
                f"Los datos son consistentes con μ = {h0_val}."
            )
 
        st.session_state.resultados_z = {
            "variable_nombre":            variable_z,
            "n":                          n_z,
            "media_muestral":             media_muestral,
            "h0_media":                   h0_val,
            "h1_texto":                   h1_texto,
            "sigma_poblacional_supuesta": sigma_conocida,
            "tipo_prueba":                tipo_h1,
            "tipo_cola":                  tipo_cola,
            "alpha":                      alpha,
            "estadistico_z":              z_score,
            "p_value":                    p_value,
            "z_critico_sup":              z_cs,
            "z_critico_inf":              z_ci,
            "region_critica":             reg_txt,
            "decision_automatica":        decision_txt,
            "clase_decision":             clase_dec,
            "interpretacion_auto":        interp,
        }
 
    # ── Mostrar resultados ──
    if st.session_state.resultados_z is not None:
        r = st.session_state.resultados_z
 
        # ══ BARRA RESUMEN GRANDE ══
        z_col  = "rojo"  if "Rechazar" in r["decision_automatica"] else "verde"
        p_col  = "rojo"  if "Rechazar" in r["decision_automatica"] else "verde"
        dec_c  = "⛔ RECHAZAR H₀" if "Rechazar" in r["decision_automatica"] else "✅ NO RECHAZAR H₀"
 
        st.markdown(f"""
        <div class="barra-resumen">
            <div class="barra-item">
                <div class="barra-item-label">📐 Media muestral (x̄)</div>
                <div class="barra-item-valor">{r['media_muestral']:.3f}</div>
                <div class="barra-item-sub">H₀: μ = {r['h0_media']}</div>
            </div>
            <div class="barra-item">
                <div class="barra-item-label">⚡ Estadístico Z</div>
                <div class="barra-item-valor {z_col}">{r['estadistico_z']:.4f}</div>
                <div class="barra-item-sub">Región: {r['region_critica']}</div>
            </div>
            <div class="barra-item">
                <div class="barra-item-label">🎯 Tipo de prueba</div>
                <div class="barra-item-valor" style="font-size:18px;">{r['tipo_cola']}</div>
                <div class="barra-item-sub">α = {r['alpha']}</div>
            </div>
            <div class="barra-item">
                <div class="barra-item-label">📊 p-value</div>
                <div class="barra-item-valor {p_col}">{r['p_value']:.4e}</div>
                <div class="barra-item-sub">α = {r['alpha']}</div>
            </div>
            <div class="barra-item">
                <div class="barra-item-label">🏁 Decisión</div>
                <div class="barra-item-valor {z_col}" style="font-size:17px;">{dec_c}</div>
                <div class="barra-item-sub">&nbsp;</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
 
        # ── Resultados detallados ──
        c1, c2 = st.columns([1, 2], gap="large")
 
        with c1:
            st.markdown("#### Hipótesis planteadas")
            st.markdown(f"""
            <div class="hipotesis-box">
                <div class="hipotesis-title">📐 Hipótesis Estadísticas</div>
                <div class="hipotesis-h0">H₀: μ = {r['h0_media']}</div>
                <div class="hipotesis-h1">H₁: {r['h1_texto']}</div>
            </div>
            """, unsafe_allow_html=True)
 
            z_cs = r['z_critico_sup']
            z_ci = r['z_critico_inf']
            z_crit_display = (
                f"±{z_cs:.4f}" if z_cs is not None and z_ci is not None
                else f"{z_cs:.4f}" if z_cs is not None
                else f"{z_ci:.4f}"
            )
            clase_p = "green" if r['p_value'] > r['alpha'] else "red"
 
            st.markdown("#### Resultados numéricos")
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Estadístico Z calculado</div>
                <div class="metric-value">{r['estadistico_z']:.4f}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">p-value</div>
                <div class="metric-value {clase_p}">{r['p_value']:.4e}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Valor crítico Zc (α = {r['alpha']})</div>
                <div class="metric-value">{z_crit_display}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Región de rechazo</div>
                <div class="metric-value" style="font-size:15px;">{r['region_critica']}</div>
            </div>
            """, unsafe_allow_html=True)
 
            st.markdown(f"#### Decisión estadística (α = {r['alpha']})")
            st.markdown(
                f"<div class='decision-h0 {r['clase_decision']}'>{r['decision_automatica']}</div>",
                unsafe_allow_html=True
            )
            st.markdown("#### Interpretación automática")
            st.markdown(
                f'<div class="interpretacion-box">{r["interpretacion_auto"]}</div>',
                unsafe_allow_html=True
            )
 
        with c2:
            st.markdown("#### Curva Normal — Región Crítica")
 
            x     = np.linspace(-4, 4, 600)
            y_pdf = stats.norm.pdf(x)
 
            fig_z = go.Figure()
            fig_z.add_trace(go.Scatter(
                x=x, y=y_pdf, mode="lines", name="Distribución N(0,1)",
                line=dict(color=COLOR_DARK, width=3)
            ))
 
            COLOR_ROJO  = "rgba(190,18,60,0.30)"
            COLOR_VERDE_T = "rgba(0,180,120,0.12)"
 
            x_nrec = np.linspace(
                z_ci if z_ci is not None else -4,
                z_cs if z_cs is not None else 4, 400
            )
            fig_z.add_trace(go.Scatter(
                x=x_nrec, y=stats.norm.pdf(x_nrec),
                fill="tozeroy", fillcolor=COLOR_VERDE_T,
                mode="none", name="No se rechaza H₀"
            ))
            if z_cs is not None:
                xd = np.linspace(z_cs, 4, 200)
                fig_z.add_trace(go.Scatter(
                    x=xd, y=stats.norm.pdf(xd),
                    fill="tozeroy", fillcolor=COLOR_ROJO,
                    mode="none", name="Zona de rechazo H₀"
                ))
            if z_ci is not None:
                xi = np.linspace(-4, z_ci, 200)
                fig_z.add_trace(go.Scatter(
                    x=xi, y=stats.norm.pdf(xi),
                    fill="tozeroy", fillcolor=COLOR_ROJO,
                    mode="none", name="Zona rechazo (izq)", showlegend=False
                ))
 
            z_val = r['estadistico_z']
            # Clamp Z para que se vea aunque sea muy grande
            z_vis = max(-3.9, min(3.9, z_val))
            fig_z.add_vline(
                x=z_vis, line_width=3, line_dash="dash", line_color="#f59e0b",
                annotation_text=f"Z = {z_val:.3f}",
                annotation_font_color="#f59e0b", annotation_font_size=14,
                annotation_position="top"
            )
            if z_cs is not None:
                fig_z.add_vline(x=z_cs, line_width=2, line_dash="dot", line_color="#be123c",
                                annotation_text=f"Zc = {z_cs:.3f}",
                                annotation_font_color="#be123c", annotation_font_size=12)
            if z_ci is not None:
                fig_z.add_vline(x=z_ci, line_width=2, line_dash="dot", line_color="#be123c",
                                annotation_text=f"Zc = {z_ci:.3f}",
                                annotation_font_color="#be123c", annotation_font_size=12,
                                annotation_position="top left")
 
            fig_z.update_layout(
                title=dict(
                    text=f"Distribución N(0,1) — {r['tipo_cola']} — α = {r['alpha']}",
                    font_size=15
                ),
                xaxis_title="Valor Z",
                yaxis_title="Densidad de probabilidad",
                template="plotly_white", height=430,
                font=dict(family="Space Grotesk"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            )
            st.plotly_chart(fig_z, use_container_width=True)
            st.caption(
                "🟩 Verde = No se rechaza H₀  |  🟥 Rojo = Zona de rechazo  |  "
                "🟡 Línea amarilla = tu Z calculado  |  🔴 Líneas punteadas = valores críticos Zc"
            )
 
        seccion_ia()
 
 
# ═══════════════════════════════════════════════════════
# SECCIÓN 4: ASISTENTE IA
# ═══════════════════════════════════════════════════════
MODELO_GEMINI = "gemini-2.5-flash"
 
def llamar_gemini_api(key: str, resumen: dict) -> str:
    try:
        from google import genai as google_genai
        from google.genai import types as genai_types
    except ImportError:
        return "Error: Instala el SDK con: pip install google-genai"
    try:
        prompt_text = f"""Eres un asistente de laboratorio estadístico profesional, serio y didáctico.
 
Se realizó una Prueba Z para la media con los siguientes parámetros:
 
DATOS:
- Variable: {resumen['variable_nombre']}
- n = {resumen['n']}
- Media muestral (x̄) = {resumen['media_muestral']:.4f}
- H₀: μ = {resumen['h0_media']}
- H₁: {resumen['h1_texto']}
- σ = {resumen['sigma_poblacional_supuesta']}
- α = {resumen['alpha']}
- Tipo: {resumen['tipo_prueba']}
 
RESULTADOS:
- Z calculado = {resumen['estadistico_z']:.4f}
- p-value = {resumen['p_value']:.4e}
- Región crítica: {resumen['region_critica']}
- Decisión del sistema: {resumen['decision_automatica']}
 
AUTOEVALUACIÓN DEL ESTUDIANTE:
- ¿Distribución normal?: {resumen.get('resp_normal','(no respondida)')}
- ¿Sesgo u outliers?: {resumen.get('resp_sesgo','(no respondida)')}
- ¿Tamaño muestra suficiente?: {resumen.get('resp_n','(no respondida)')}
 
INTERPRETACIÓN DEL ESTUDIANTE:
"{resumen.get('interpretacion_estudiante','(sin interpretación)')}"
 
Por favor realiza:
1. VERIFICACIÓN: ¿Es correcta la decisión {resumen['decision_automatica']}? Explica con p-value y región crítica.
2. SUPUESTOS: Evalúa si n ≥ 30 y σ conocida son razonables.
3. AUTOEVALUACIÓN: ¿Las respuestas del estudiante son correctas?
4. COMPARACIÓN: ¿La interpretación del estudiante coincide con la decisión?
5. CONCLUSIÓN: Qué se puede inferir estadística y prácticamente.
 
Tono profesional y educativo. Sin emojis. En español."""
 
        client   = google_genai.Client(api_key=key)
        response = client.models.generate_content(
            model=MODELO_GEMINI,
            contents=prompt_text,
            config=genai_types.GenerateContentConfig(temperature=0.3, max_output_tokens=4096)
        )
        return response.text
    except Exception as e:
        msg = str(e)
        if "429" in msg: return "Error 429: Cuota agotada. Genera nueva key en aistudio.google.com."
        if "403" in msg: return "Error 403: API Key inválida o sin permisos."
        if "404" in msg: return "Error 404: Modelo no encontrado."
        return f"Error inesperado: {msg}"
 
 
def seccion_ia():
    st.markdown('<div class="section-title">🤖 4. Asistente IA — Gemini Lab Bot</div>',
                unsafe_allow_html=True)
    st.info(
        "💡 Ingresa tu API Key de Gemini en la barra lateral "
        "(gratuita en [aistudio.google.com](https://aistudio.google.com/app/apikey)).",
        icon="🔑"
    )
    if st.session_state.resultados_z is None:
        st.warning("⚠️ Ejecuta primero la Prueba Z.")
        return
 
    resumen = st.session_state.resultados_z
    col_ia1, col_ia2 = st.columns([1, 1], gap="large")
 
    with col_ia1:
        st.markdown("**✍️ Escribe tu conclusión personal:**")
        decision_estudiante = st.text_area(
            "conclusion", height=140, label_visibility="collapsed",
            key="decision_estudiante",
            placeholder="Basándome en el estadístico Z y el p-value, concluyo que..."
        )
 
    with col_ia2:
        st.markdown("**📋 Resumen que se enviará a Gemini:**")
        st.markdown(f"""
        <div class="result-card" style="font-size:13px;">
            <strong>Variable:</strong> {resumen['variable_nombre']} · n = {resumen['n']}<br>
            <strong>H₀:</strong> μ = {resumen['h0_media']} · <strong>H₁:</strong> {resumen['h1_texto']}<br>
            <strong>Z =</strong> {resumen['estadistico_z']:.4f} · <strong>p =</strong> {resumen['p_value']:.4e}<br>
            <strong>Región:</strong> {resumen['region_critica']} · <strong>α =</strong> {resumen['alpha']}<br>
            <strong>Decisión:</strong> {resumen['decision_automatica']}
        </div>
        """, unsafe_allow_html=True)
        st.caption(f"🤖 Modelo: {MODELO_GEMINI}")
 
        if st.button("🧠 Consultar a Gemini Lab Bot"):
            if not st.session_state.api_key:
                st.error("❌ Guarda tu API Key primero en la barra lateral.")
            else:
                resumen_completo = {
                    **resumen,
                    "interpretacion_estudiante": decision_estudiante,
                    "resp_normal": st.session_state.get('resp_normal', '(no respondida)'),
                    "resp_sesgo":  st.session_state.get('resp_sesgo',  '(no respondida)'),
                    "resp_n":      st.session_state.get('resp_n',      '(no respondida)'),
                }
                with st.spinner("Analizando con Gemini..."):
                    respuesta = llamar_gemini_api(st.session_state.api_key, resumen_completo)
 
                if respuesta and not respuesta.startswith("Error"):
                    st.markdown("#### 💬 Respuesta del Asistente:")
                    st.markdown(f'<div class="ia-response">{respuesta}</div>', unsafe_allow_html=True)
 
                    st.markdown("#### 🔍 ¿Tu conclusión coincide con el sistema?")
                    if decision_estudiante.strip():
                        est = decision_estudiante.lower()
                        auto_rechaza    = "Rechazar" in resumen['decision_automatica']
                        dice_rechaza    = any(p in est for p in ["rechaz","reject","sí se rechaza","si se rechaza"])
                        dice_no_rechaza = any(p in est for p in ["no se rechaza","no rechaz","no hay evidencia"])
 
                        match = (
                            True  if dice_rechaza    and auto_rechaza     else
                            True  if dice_no_rechaza and not auto_rechaza else
                            False if dice_rechaza    and not auto_rechaza  else
                            False if dice_no_rechaza and auto_rechaza      else
                            None
                        )
                        if match is True:
                            st.markdown('<div class="comparacion-box coincide">✅ Tu conclusión <strong>coincide</strong> con la decisión del sistema.</div>', unsafe_allow_html=True)
                        elif match is False:
                            st.markdown(f'<div class="comparacion-box no-coincide">⚠️ Tu conclusión <strong>difiere</strong> de la decisión ({resumen["decision_automatica"]}). Revisa la respuesta de Gemini.</div>', unsafe_allow_html=True)
                        else:
                            st.info("ℹ️ No se pudo comparar automáticamente. Revisa manualmente.")
                    else:
                        st.info("ℹ️ Escribe tu conclusión para habilitar la comparación.")
                else:
                    st.error(f"❌ {respuesta}")
                    st.markdown("**Verifica:** API Key válida · Sin espacios · Conexión a internet")
 
 
# ═══════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════
def mostrar_footer():
    st.markdown("""
    <div class="footer">
        Laboratorio de análisis · Distribuciones y Pruebas de Hipótesis<br>
        Desarrollado con Streamlit · Python · Plotly · SciPy · Google Gemini API (gemini-2.5-flash)
    </div>
    """, unsafe_allow_html=True)
 
 
def main():
    aplicar_estilos_visuales()
    inicializar_estado()
    seccion_carga_datos()
    seccion_visualizacion()
    seccion_inferencia()
    mostrar_footer()
 
if __name__ == "__main__":
    main()