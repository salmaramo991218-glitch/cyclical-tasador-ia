import streamlit as st
import pandas as pd
import random

# ──────────────────────────────────────────────
# 1. PAGE CONFIG & CUSTOM CSS
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Cyclical | Motor de Tasación Predictiva",
    page_icon="♻️",
    layout="centered",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #000000;
    }
    .stApp { background-color: #FFFFFF; }

    .main-title {
        font-size: 2.2rem; font-weight: 700; letter-spacing: -0.5px;
        color: #000000; margin-bottom: 0; line-height: 1.2;
    }
    .sub-title {
        font-size: 1rem; font-weight: 300; color: #666666;
        margin-top: 4px; margin-bottom: 32px; letter-spacing: 0.3px;
    }

    .stSelectbox > label, .stTextInput > label {
        font-weight: 500 !important; font-size: 0.85rem !important;
        text-transform: uppercase !important; letter-spacing: 1px !important;
        color: #333333 !important;
    }

    .stButton > button {
        background-color: #000000 !important; color: #FFFFFF !important;
        border: none !important; border-radius: 6px !important;
        padding: 14px 32px !important; font-weight: 600 !important;
        font-size: 0.95rem !important; letter-spacing: 0.5px !important;
        width: 100% !important;
        transition: background-color 0.25s ease, transform 0.15s ease !important;
    }
    .stButton > button:hover {
        background-color: #333333 !important; transform: translateY(-1px) !important;
    }

    [data-testid="stMetric"] {
        background: #FAFAFA; border: 1px solid #E8E8E8;
        border-radius: 10px; padding: 20px 16px; text-align: center;
    }
    [data-testid="stMetricLabel"] {
        font-weight: 500 !important; font-size: 0.78rem !important;
        text-transform: uppercase !important; letter-spacing: 1.2px !important;
        color: #888888 !important;
    }
    [data-testid="stMetricValue"] {
        font-weight: 700 !important; color: #000000 !important;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #E8E8E8; border-radius: 8px; overflow: hidden;
    }

    .section-header {
        font-size: 1.1rem; font-weight: 600; color: #000000;
        margin-top: 28px; margin-bottom: 12px; letter-spacing: -0.2px;
    }

    .footer-text {
        text-align: center; font-size: 0.75rem; color: #AAAAAA;
        margin-top: 48px; letter-spacing: 0.5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ──────────────────────────────────────────────
# 2. HEADER
# ──────────────────────────────────────────────
st.markdown(
    '<p class="main-title">♻️ Cyclical | Motor de Tasación Predictiva</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="sub-title">Modelo predictivo basado en datos históricos de mercado para moda circular.</p>',
    unsafe_allow_html=True,
)
st.markdown("---")


# ──────────────────────────────────────────────
# 3. DATASET INTERNO DE PRECIOS
# ──────────────────────────────────────────────

# Precios base por categoría (COP)
PRECIOS_BASE = {
    "Chaquetas": 150_000,
    "Zapatos": 180_000,
    "Vestidos": 120_000,
    "Tops": 60_000,
    "Pantalones": 100_000,
    "Bolsos": 200_000,
}

# Marcas organizadas por segmento con sus multiplicadores
MARCAS_POR_SEGMENTO = {
    "Fast Fashion (x1.0)": {
        "marcas": ["Zara", "H&M", "Mango", "Pull&Bear", "Bershka",
                    "Stradivarius", "Shein", "Forever 21", "Primark", "C&A"],
        "multiplicador": 1.0,
    },
    "Gama Media (x1.5)": {
        "marcas": ["Nike", "Adidas", "Studio F", "Arturo Calle", "Tennis",
                    "Ela", "Koaj", "Chevignon", "Levi's", "Tommy Hilfiger",
                    "Lacoste", "Guess", "Calvin Klein", "Michael Kors"],
        "multiplicador": 1.5,
    },
    "Lujo (x3.5)": {
        "marcas": ["Gucci", "Prada", "Carolina Herrera", "Louis Vuitton",
                    "Chanel", "Dior", "Balenciaga", "Burberry", "Versace",
                    "Fendi", "Saint Laurent", "Valentino"],
        "multiplicador": 3.5,
    },
}

# Lista plana de todas las marcas para el selectbox
TODAS_LAS_MARCAS = []
MULTIPLICADOR_MARCA = {}
SEGMENTO_MARCA = {}
for segmento, data in MARCAS_POR_SEGMENTO.items():
    for m in data["marcas"]:
        TODAS_LAS_MARCAS.append(m)
        MULTIPLICADOR_MARCA[m] = data["multiplicador"]
        SEGMENTO_MARCA[m] = segmento

# Factor de depreciación según estado
FACTORES_ESTADO = {
    "Nuevo con etiqueta (10/10)": 1.20,
    "Excelente estado (9/10)": 1.00,
    "Buen estado (7-8/10)": 0.85,
    "Vintage / Desgaste visible (5-6/10)": 0.70,
}

ESTADO_CORTO = {
    "Nuevo con etiqueta (10/10)": "Nuevo",
    "Excelente estado (9/10)": "Excelente",
    "Buen estado (7-8/10)": "Bueno",
    "Vintage / Desgaste visible (5-6/10)": "Vintage",
}


# ──────────────────────────────────────────────
# 4. INPUTS
# ──────────────────────────────────────────────
col_left, col_right = st.columns(2, gap="large")

with col_left:
    categoria = st.selectbox("Categoría", list(PRECIOS_BASE.keys()))
    marca = st.selectbox("Marca", TODAS_LAS_MARCAS)

with col_right:
    estado = st.selectbox("Estado de la prenda", list(FACTORES_ESTADO.keys()))

st.markdown("")
ejecutar = st.button("🔍 Ejecutar Motor de Tasación")


# ──────────────────────────────────────────────
# 5. MOTOR DE TASACIÓN
# ──────────────────────────────────────────────
def calcular_tasacion(categoria, marca, estado):
    """
    1. Precio base de la categoría
    2. × multiplicador de marca (segmento)
    3. × factor de estado (depreciación)
    4. Rango dinámico: Piso (-15%), Óptimo, Techo (+15%)
    """
    precio_base = PRECIOS_BASE[categoria]
    mult = MULTIPLICADOR_MARCA[marca]
    factor = FACTORES_ESTADO[estado]

    optimo = round(precio_base * mult * factor)
    piso = round(optimo * 0.85)
    techo = round(optimo * 1.15)

    return piso, optimo, techo


def generar_testigos(categoria, marca, estado, precio_optimo, n=8):
    """
    Genera n testigos de mercado simulados con variación ±10%
    para dar contexto realista de rango de precios.
    """
    estado_label = ESTADO_CORTO[estado]
    singular = categoria[:-1] if categoria.endswith("s") else categoria

    estados_variados = ["Nuevo", "Excelente", "Bueno", "Vintage"]
    testigos = []

    for i in range(n):
        variacion = random.uniform(0.90, 1.10)
        precio = round(precio_optimo * variacion, -3)
        est = random.choice(estados_variados)
        testigos.append({
            "Artículo": f"{singular} {marca} – {est}",
            "Precio (COP)": precio,
            "Confianza": f"{random.randint(85, 99)}%",
        })

    return pd.DataFrame(testigos)


# ──────────────────────────────────────────────
# 6. RESULTADOS
# ──────────────────────────────────────────────
def fmt(v):
    return f"${v:,.0f} COP".replace(",", ".")


if ejecutar:
    piso, optimo, techo = calcular_tasacion(categoria, marca, estado)
    segmento = SEGMENTO_MARCA[marca]
    mult = MULTIPLICADOR_MARCA[marca]

    st.markdown("---")

    # Info del modelo
    st.success(
        f"✅ **{marca}** → Segmento **{segmento}** · "
        f"Base {fmt(PRECIOS_BASE[categoria])} × {mult} × {FACTORES_ESTADO[estado]}"
    )

    # Metric cards
    st.markdown(
        '<p class="section-header">📊 Resultado de Tasación</p>',
        unsafe_allow_html=True,
    )
    m1, m2, m3 = st.columns(3)
    m1.metric("Piso de Venta", fmt(piso), "-15%")
    m2.metric("💎 Precio Óptimo", fmt(optimo))
    m3.metric("Techo de Mercado", fmt(techo), "+15%")

    # Gráfico de barras
    st.markdown(
        '<p class="section-header">📈 Rango de Precios</p>',
        unsafe_allow_html=True,
    )
    chart_data = pd.DataFrame(
        {"Precio (COP)": [piso, optimo, techo]},
        index=["Piso", "Óptimo", "Techo"],
    )
    st.bar_chart(chart_data, color="#000000")

    # Testigos
    st.markdown(
        '<p class="section-header">🗂️ Testigos de Mercado</p>',
        unsafe_allow_html=True,
    )
    df_testigos = generar_testigos(categoria, marca, estado, optimo)
    st.dataframe(
        df_testigos,
        column_config={
            "Artículo": st.column_config.TextColumn("Artículo", width="large"),
            "Precio (COP)": st.column_config.NumberColumn(
                "Precio (COP)", format="$ %,.0f"
            ),
            "Confianza": st.column_config.TextColumn("Confianza"),
        },
        hide_index=True,
        use_container_width=True,
    )

    # Detalle técnico
    with st.expander("🔬 Detalle del Modelo"):
        st.markdown(f"""
| Parámetro | Valor |
|---|---|
| **Categoría** | {categoria} |
| **Precio Base** | {fmt(PRECIOS_BASE[categoria])} |
| **Marca** | {marca} |
| **Segmento** | {segmento} |
| **Multiplicador** | ×{mult} |
| **Estado** | {estado} |
| **Factor Estado** | ×{FACTORES_ESTADO[estado]} |
| **Precio Óptimo** | {fmt(optimo)} |
| **Rango** | {fmt(piso)} → {fmt(techo)} |
        """)


# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<p class="footer-text">CYCLICAL © 2026 — Moda circular, tasada con inteligencia artificial.</p>',
    unsafe_allow_html=True,
)
