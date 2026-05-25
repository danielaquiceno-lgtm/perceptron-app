import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

st.set_page_config(
    page_title="Máquina Perceptrón Interactiva",
    page_icon="🌸",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #fce4ec 0%, #f3e5f5 50%, #ede7f6 100%);
    }
    .titulo-principal {
        font-size: 2.2em;
        font-weight: bold;
        color: #6a1b9a;
        margin-bottom: 2px;
    }
    .subtitulo {
        font-size: 1em;
        color: #ad1457;
        margin-bottom: 10px;
    }
    .paso-header {
        background: linear-gradient(90deg, #f3e5f5, #fce4ec);
        border-radius: 12px;
        padding: 10px 18px;
        border-left: 6px solid #ab47bc;
        margin: 18px 0 8px 0;
        font-size: 1.2em;
        font-weight: bold;
        color: #6a1b9a;
    }
    .patron-card {
        background: rgba(255,255,255,0.75);
        border-radius: 12px;
        padding: 12px 16px;
        margin: 7px 0;
        border-left: 5px solid #ce93d8;
        box-shadow: 2px 2px 8px rgba(174,114,202,0.15);
        color: #4a148c;
    }
    .marcador-box {
        background: rgba(255,255,255,0.85);
        border-radius: 14px;
        padding: 18px;
        text-align: center;
        border: 2px solid #ce93d8;
        margin-bottom: 12px;
    }
    .pesos-box {
        background: rgba(243,229,245,0.9);
        border-radius: 12px;
        padding: 14px 18px;
        border: 2px solid #ab47bc;
        color: #4a148c;
        font-size: 0.97em;
    }
    .separador {
        border: none;
        height: 2px;
        background: linear-gradient(to right, #f48fb1, #ce93d8, #9fa8da);
        margin: 18px 0;
    }
    .instrucciones {
        background: rgba(255,255,255,0.6);
        border-radius: 10px;
        padding: 10px 16px;
        color: #6a1b9a;
        font-size: 0.95em;
        margin-bottom: 8px;
    }
    .correcto { color: #7b1fa2; font-weight: bold; }
    .incorrecto { color: #e91e63; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ── Título ──────────────────────────────────────────────────────────────────
st.markdown('<div class="titulo-principal">🌸 Máquina Perceptrón Interactiva</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">Inspirada en la máquina física de Rosenblatt (1957)</div>', unsafe_allow_html=True)
st.markdown('<hr class="separador">', unsafe_allow_html=True)

# ── Instrucciones ───────────────────────────────────────────────────────────
st.markdown("""
<div class="instrucciones">
<b>¿Cómo funciona?</b><br>
1. Selecciona el problema que quieres resolver (OR, AND o XOR)<br>
2. Activa o desactiva las entradas con los botones ON/OFF de cada patrón<br>
3. Ajusta las perillas (sliders) de los pesos w₁, w₂ y el Bias<br>
4. Observa en tiempo real cómo cambia la frontera de decisión<br>
5. ¡Tu objetivo es clasificar correctamente los 4 patrones!
</div>
""", unsafe_allow_html=True)

# ── PASO 1 ──────────────────────────────────────────────────────────────────
st.markdown('<div class="paso-header">🎯 Paso 1: Selecciona el problema</div>', unsafe_allow_html=True)
st.markdown("Elige el problema lógico que quieres que el perceptrón aprenda a clasificar:")

problema = st.selectbox(
    "Problema:",
    ["OR lógico", "AND lógico", "XOR (¡imposible!) 🔥"],
    label_visibility="collapsed"
)

if problema == "OR lógico":
    etiquetas = [-1, 1, 1, 1]
    desc_problema = "OR: Positivo si AL MENOS UNA entrada está activa"
elif problema == "AND lógico":
    etiquetas = [-1, -1, -1, 1]
    desc_problema = "AND: Positivo solo si AMBAS entradas están activas"
else:
    etiquetas = [-1, 1, 1, -1]
    desc_problema = "XOR: Positivo si UNA SOLA entrada está activa (no separable linealmente)"

st.info(desc_problema)

# ── PASO 2 ──────────────────────────────────────────────────────────────────
st.markdown('<div class="paso-header">🎛️ Paso 2: Configura los 4 patrones de entrada</div>', unsafe_allow_html=True)
st.markdown("Cada fila es una combinación posible de las dos entradas. Observa la etiqueta deseada según el problema elegido.")

patrones = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
nombres_x1 = ["OFF (-1)", "OFF (-1)", "ON (+1)", "ON (+1)"]
nombres_x2 = ["OFF (-1)", "ON (+1)", "OFF (-1)", "ON (+1)"]

col_p1, col_p2, col_p3, col_p4 = st.columns(4)
cols_patrones = [col_p1, col_p2, col_p3, col_p4]

for i, col in enumerate(cols_patrones):
    with col:
        etiqueta_str = "✅ Positivo (+1)" if etiquetas[i] == 1 else "❌ Negativo (-1)"
        color_etq = "#7b1fa2" if etiquetas[i] == 1 else "#e91e63"
        st.markdown(
            '<div class="patron-card">'
            '<b>Patrón ' + str(i+1) + '</b><br>'
            'Entrada 1: <b>' + nombres_x1[i] + '</b><br>'
            'Entrada 2: <b>' + nombres_x2[i] + '</b><br>'
            'Etiqueta deseada:<br>'
            '<span style="color:' + color_etq + '; font-weight:bold;">' + etiqueta_str + '</span>'
            '</div>',
            unsafe_allow_html=True
        )

# ── PASO 3 ──────────────────────────────────────────────────────────────────
st.markdown('<div class="paso-header">⚙️ Paso 3: Ajusta las perillas manualmente</div>', unsafe_allow_html=True)
st.markdown("Mueve los sliders para cambiar los pesos. ¡Tú eres el algoritmo de aprendizaje!")

col_w1, col_w2, col_bias = st.columns(3)
with col_w1:
    w1 = st.slider("⚙️ Peso w₁", min_value=-5.0, max_value=5.0, value=0.0, step=0.1)
with col_w2:
    w2 = st.slider("⚙️ Peso w₂", min_value=-5.0, max_value=5.0, value=0.0, step=0.1)
with col_bias:
    bias = st.slider("⚖️ Bias (b)", min_value=-5.0, max_value=5.0, value=0.0, step=0.1)

# ── Cálculo ─────────────────────────────────────────────────────────────────
def calcular(x1, x2, w1, w2, b):
    suma = w1 * x1 + w2 * x2 + b
    salida = 1 if suma > 0 else -1
    return round(suma, 3), salida

resultados = []
for (x1, x2) in patrones:
    suma, salida = calcular(x1, x2, w1, w2, bias)
    resultados.append((suma, salida))

aciertos = sum(1 for i, (_, sal) in enumerate(resultados) if sal == etiquetas[i])

# ── PASO 4 ──────────────────────────────────────────────────────────────────
st.markdown('<div class="paso-header">📊 Paso 4: Resultados en tiempo real</div>', unsafe_allow_html=True)

col_tabla, col_marcador = st.columns([1.5, 1])

with col_tabla:
    st.markdown("##### 📋 Tabla de resultados")
    for i, (x1, x2) in enumerate(patrones):
        suma, salida = resultados[i]
        esperado = etiquetas[i]
        correcto = salida == esperado
        icono = "✅" if correcto else "❌"
        salida_str = "POSITIVO (+1)" if salida == 1 else "NEGATIVO (-1)"
        esperado_str = "POSITIVO (+1)" if esperado == 1 else "NEGATIVO (-1)"
        color_salida = "#7b1fa2" if correcto else "#e91e63"

        st.markdown(
            '<div class="patron-card">'
            '<b>Patrón ' + str(i+1) + ' ' + icono + '</b><br>'
            'x₁ = ' + str(x1) + ', x₂ = ' + str(x2) + '<br>'
            'Suma ponderada: <b>' + str(suma) + '</b><br>'
            'Salida del perceptrón: <b style="color:' + color_salida + ';">' + salida_str + '</b><br>'
            'Etiqueta deseada: <b>' + esperado_str + '</b>'
            '</div>',
            unsafe_allow_html=True
        )

with col_marcador:
    st.markdown("##### 🏅 Marcador")
    color_contador = "#7b1fa2" if aciertos == 4 else "#e91e63"
    mensaje = "¡Felicidades! ¡Clasificaste todos los patrones correctamente! 🎉" if aciertos == 4 else "Sigue ajustando las perillas... 💪"
    st.markdown(
        '<div class="marcador-box">'
        '<div style="color:#9c27b0; font-size:0.9em;">Patrones correctos</div>'
        '<div style="font-size:3em; font-weight:bold; color:' + color_contador + ';">'
        + str(aciertos) + ' / 4</div>'
        '</div>',
        unsafe_allow_html=True
    )
    if aciertos == 4:
        st.success(mensaje)
    else:
        st.warning(mensaje)

    st.markdown("##### 📐 Pesos actuales")
    st.markdown(
        '<div class="pesos-box">'
        'w₁ = <b>' + str(w1) + '</b><br>'
        'w₂ = <b>' + str(w2) + '</b><br>'
        'Bias = <b>' + str(bias) + '</b><br>'
        'Fórmula: salida = ' + str(w1) + '·x₁ + ' + str(w2) + '·x₂ + ' + str(bias) +
        '</div>',
        unsafe_allow_html=True
    )

# ── GRÁFICA ─────────────────────────────────────────────────────────────────
st.markdown('<hr class="separador">', unsafe_allow_html=True)
st.markdown('<div class="paso-header">🗺️ Frontera de Decisión en el Plano 2D</div>', unsafe_allow_html=True)

fig, ax = plt.subplots(figsize=(7, 6))
fig.patch.set_facecolor('#fce4ec')
ax.set_facecolor('#fdf2f8')

x_vals = np.linspace(-2, 2, 300)
if abs(w2) > 1e-6:
    y_vals = -(w1 * x_vals + bias) / w2
    ax.plot(x_vals, y_vals, color='#7b1fa2', linewidth=2.5, linestyle='--', label='Frontera de decisión')
    ax.fill_between(x_vals, y_vals, 2.5, alpha=0.12, color='#ce93d8')
    ax.fill_between(x_vals, y_vals, -2.5, alpha=0.12, color='#f48fb1')
elif abs(w1) > 1e-6:
    x_frontera = -bias / w1
    ax.axvline(x=x_frontera, color='#7b1fa2', linewidth=2.5, linestyle='--', label='Frontera de decisión')

for i, (x1, x2) in enumerate(patrones):
    esperado = etiquetas[i]
    _, salida = resultados[i]
    correcto = salida == esperado
    color = '#7b1fa2' if esperado == 1 else '#e91e63'
    marker = 'o' if esperado == 1 else 's'
    borde = '#2e7d32' if correcto else '#b71c1c'
    ax.scatter(x1, x2, c=color, s=220, marker=marker, edgecolors=borde, linewidths=3, zorder=5)
    ax.annotate("P" + str(i+1), (x1, x2), textcoords="offset points",
                xytext=(12, 8), fontsize=10, color='#4a148c', fontweight='bold')

patch_pos = mpatches.Patch(color='#7b1fa2', label='Clase Positiva (+1) ●')
patch_neg = mpatches.Patch(color='#e91e63', label='Clase Negativa (-1) ■')
ax.legend(handles=[patch_pos, patch_neg], loc='upper right',
          facecolor='#f3e5f5', edgecolor='#ce93d8', fontsize=9)

ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_xlabel("Entrada x₁", color='#6a1b9a', fontsize=12)
ax.set_ylabel("Entrada x₂", color='#6a1b9a', fontsize=12)
ax.set_title("Plano de Clasificación del Perceptrón 🌸", color='#6a1b9a', fontsize=14, fontweight='bold')
ax.axhline(0, color='#ce93d8', linewidth=0.8, linestyle=':')
ax.axvline(0, color='#ce93d8', linewidth=0.8, linestyle=':')
ax.tick_params(colors='#6a1b9a')
ax.grid(True, color='#f0d6f5', linewidth=0.8)
for spine in ax.spines.values():
    spine.set_edgecolor('#ce93d8')

st.pyplot(fig)

# ── Nota XOR ────────────────────────────────────────────────────────────────
if problema == "XOR (¡imposible!) 🔥":
    st.markdown(
        '<div style="background:rgba(255,255,255,0.85); border-radius:12px; padding:15px;'
        'border-left:5px solid #e91e63; margin-top:15px;">'
        '<b style="color:#ad1457;">🔥 ¿Por qué XOR es imposible?</b><br><br>'
        'El perceptrón solo puede trazar <b>una línea recta</b> para separar los patrones. '
        'En el problema XOR, los puntos positivos están en esquinas diagonales opuestas '
        'y <b>ninguna línea recta puede separarlos</b> de los negativos.<br><br>'
        'Esto se llama <b>no separabilidad lineal</b> y fue la gran limitación del perceptrón '
        'descubierta por Minsky y Papert en 1969. ¡Se necesitan redes neuronales multicapa para resolverlo! 🧠'
        '</div>',
        unsafe_allow_html=True
    )

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown('<hr class="separador">', unsafe_allow_html=True)
st.markdown(
    '<div style="text-align:center; color:#9c27b0; font-size:0.9em; padding:10px;">'
    '💜 Simulador de Perceptrón · Autómatas, Gramáticas y Lenguaje · Hecho con Streamlit 🌸'
    '</div>',
    unsafe_allow_html=True
)
