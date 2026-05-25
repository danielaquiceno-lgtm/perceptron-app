import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ─── Configuración de página ───────────────────────────────────────────────
st.set_page_config(
    page_title="Perceptrón Interactivo",
    page_icon="🌸",
    layout="wide"
)

# ─── Estilos personalizados ────────────────────────────────────────────────
st.markdown("""
<style>
    /* Fondo general */
    .stApp {
        background: linear-gradient(135deg, #fce4ec 0%, #f3e5f5 50%, #ede7f6 100%);
    }
    /* Título principal */
    .titulo-principal {
        text-align: center;
        font-size: 2.8em;
        font-weight: bold;
        color: #6a1b9a;
        text-shadow: 2px 2px 4px #ce93d8;
        padding: 10px;
        margin-bottom: 5px;
    }
    /* Subtítulo */
    .subtitulo {
        text-align: center;
        font-size: 1.1em;
        color: #ad1457;
        margin-bottom: 25px;
    }
    /* Tarjetas de patrones */
    .patron-card {
        background: rgba(255,255,255,0.7);
        border-radius: 15px;
        padding: 12px;
        margin: 6px 0;
        border-left: 5px solid #ce93d8;
        box-shadow: 2px 2px 8px rgba(174,114,202,0.2);
    }
    /* Resultado correcto */
    .correcto {
        color: #7b1fa2;
        font-weight: bold;
        font-size: 1.3em;
    }
    /* Resultado incorrecto */
    .incorrecto {
        color: #e91e63;
        font-weight: bold;
        font-size: 1.3em;
    }
    /* Caja de métricas */
    .metrica-box {
        background: rgba(255,255,255,0.8);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        border: 2px solid #ce93d8;
        margin: 5px;
    }
    /* Sección de fórmula */
    .formula-box {
        background: rgba(243,229,245,0.9);
        border-radius: 12px;
        padding: 15px;
        border: 2px solid #ab47bc;
        margin: 10px 0;
        text-align: center;
        font-size: 1.1em;
        color: #4a148c;
    }
    /* Separador decorativo */
    .separador {
        border: none;
        height: 2px;
        background: linear-gradient(to right, #f48fb1, #ce93d8, #9fa8da);
        margin: 15px 0;
    }
    div[data-testid="stSlider"] > div > div > div > div {
        background: linear-gradient(to right, #f48fb1, #ab47bc) !important;
    }
</style>
""", unsafe_allow_html=True)

# ─── Título ────────────────────────────────────────────────────────────────
st.markdown('<div class="titulo-principal">🌸 Simulador de Perceptrón 💜</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">Ajusta las perillas manualmente y descubre cómo aprenden las máquinas ✨</div>', unsafe_allow_html=True)
st.markdown('<hr class="separador">', unsafe_allow_html=True)

# ─── Layout principal ──────────────────────────────────────────────────────
col_izq, col_der = st.columns([1, 1.2])

with col_izq:
    st.markdown("### 🎛️ Perillas de Pesos")
    st.markdown("*Mueve los sliders para ajustar los pesos manualmente*")

    w1 = st.slider("⚙️ Peso w₁ (entrada 1)", min_value=-5.0, max_value=5.0, value=0.0, step=0.1)
    w2 = st.slider("⚙️ Peso w₂ (entrada 2)", min_value=-5.0, max_value=5.0, value=0.0, step=0.1)
    bias = st.slider("⚖️ Bias (b)", min_value=-5.0, max_value=5.0, value=0.0, step=0.1)

    st.markdown('<hr class="separador">', unsafe_allow_html=True)
    st.markdown("### 🎯 Definir Problema")

    problema = st.selectbox(
        "Elige un problema o personaliza:",
        ["Personalizado", "OR lógico", "AND lógico", "XOR (¡imposible!) 🔥"]
    )

    # Etiquetas según problema
    if problema == "OR lógico":
        etiquetas = [-1, 1, 1, 1]
    elif problema == "AND lógico":
        etiquetas = [-1, -1, -1, 1]
    elif problema == "XOR (¡imposible!) 🔥":
        etiquetas = [-1, 1, 1, -1]
    else:
        st.markdown("*Asigna la etiqueta deseada a cada patrón:*")
        etiquetas = []
        nombres_patron = ["(-1, -1)", "(-1, +1)", "(+1, -1)", "(+1, +1)"]
        for i, nombre in enumerate(nombres_patron):
            e = st.radio(
                f"Patrón {nombre}",
                options=[1, -1],
                format_func=lambda x: "✅ Positivo (+1)" if x == 1 else "❌ Negativo (-1)",
                horizontal=True,
                key=f"etiqueta_{i}"
            )
            etiquetas.append(e)

# ─── Patrones de entrada ───────────────────────────────────────────────────
patrones = [
    (-1, -1),
    (-1,  1),
    ( 1, -1),
    ( 1,  1)
]

# ─── Cálculo del perceptrón ────────────────────────────────────────────────
def calcular(x1, x2, w1, w2, b):
    suma = w1 * x1 + w2 * x2 + b
    salida = 1 if suma > 0 else -1
    return round(suma, 3), salida

resultados = []
for (x1, x2) in patrones:
    suma, salida = calcular(x1, x2, w1, w2, bias)
    resultados.append((suma, salida))

aciertos = sum(1 for i, (_, sal) in enumerate(resultados) if sal == etiquetas[i])

# ─── Panel derecho: tabla de patrones ─────────────────────────────────────
with col_der:
    st.markdown("### 📊 Tabla de Clasificación")

    nombres_patron = ["(-1, -1)", "(-1, +1)", "(+1, -1)", "(+1, +1)"]
    for i, (x1, x2) in enumerate(patrones):
        suma, salida = resultados[i]
        esperado = etiquetas[i]
        correcto = salida == esperado
        icono_switch1 = "🔼" if x1 == 1 else "🔽"
        icono_switch2 = "🔼" if x2 == 1 else "🔽"
        icono_result = "✅" if correcto else "❌"
        etiqueta_str = "Positivo (+1)" if esperado == 1 else "Negativo (-1)"
        salida_str = "Positivo (+1)" if salida == 1 else "Negativo (-1)"

        st.markdown(f"""
        <div class="patron-card">
            <b>Patrón {i+1}:</b> Entrada 1 {icono_switch1} <b>{x1}</b> &nbsp;|&nbsp; Entrada 2 {icono_switch2} <b>{x2}</b><br>
            🎯 <b>Deseado:</b> {etiqueta_str} &nbsp;&nbsp;
            🧮 <b>Suma ponderada:</b> {suma}<br>
            🤖 <b>Salida:</b> {salida_str} &nbsp;&nbsp; {icono_result}
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr class="separador">', unsafe_allow_html=True)

    # Contador de aciertos
    color_contador = "#7b1fa2" if aciertos == 4 else "#e91e63"
    st.markdown(f"""
    <div class="metrica-bo
