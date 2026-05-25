import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

st.set_page_config(
    page_title="Perceptrón Interactivo",
    page_icon="🌸",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #fce4ec 0%, #f3e5f5 50%, #ede7f6 100%);
    }
    .titulo-principal {
        text-align: center;
        font-size: 2.8em;
        font-weight: bold;
        color: #6a1b9a;
        text-shadow: 2px 2px 4px #ce93d8;
        padding: 10px;
        margin-bottom: 5px;
    }
    .subtitulo {
        text-align: center;
        font-size: 1.1em;
        color: #ad1457;
        margin-bottom: 25px;
    }
    .patron-card {
        background: rgba(255,255,255,0.7);
        border-radius: 15px;
        padding: 12px;
        margin: 6px 0;
        border-left: 5px solid #ce93d8;
        box-shadow: 2px 2px 8px rgba(174,114,202,0.2);
    }
    .metrica-box {
        background: rgba(255,255,255,0.8);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        border: 2px solid #ce93d8;
        margin: 5px;
    }
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
    .separador {
        border: none;
        height: 2px;
        background: linear-gradient(to right, #f48fb1, #ce93d8, #9fa8da);
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="titulo-principal">🌸 Simulador de Perceptrón 💜</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">Ajusta las perillas manualmente y descubre cómo aprenden las máquinas</div>', unsafe_allow_html=True)
st.markdown('<hr class="separador">', unsafe_allow_html=True)

col_izq, col_der = st.columns([1, 1.2])

with col_izq:
    st.markdown("### Perillas de Pesos")
    st.markdown("Mueve los sliders para ajustar los pesos manualmente")

    w1 = st.slider("Peso w1 (entrada 1)", min_value=-5.0, max_value=5.0, value=0.0, step=0.1)
    w2 = st.slider("Peso w2 (entrada 2)", min_value=-5.0, max_value=5.0, value=0.0, step=0.1)
    bias = st.slider("Bias (b)", min_value=-5.0, max_value=5.0, value=0.0, step=0.1)

    st.markdown('<hr class="separador">', unsafe_allow_html=True)
    st.markdown("### Definir Problema")

    problema = st.selectbox(
        "Elige un problema o personaliza:",
        ["Personalizado", "OR logico", "AND logico", "XOR (imposible)"]
    )

    if problema == "OR logico":
        etiquetas = [-1, 1, 1, 1]
    elif problema == "AND logico":
        etiquetas = [-1, -1, -1, 1]
    elif problema == "XOR (imposible)":
        etiquetas = [-1, 1, 1, -1]
    else:
        st.markdown("Asigna la etiqueta deseada a cada patron:")
        etiquetas = []
        nombres_patron = ["(-1, -1)", "(-1, +1)", "(+1, -1)", "(+1, +1)"]
        for i, nombre in enumerate(nombres_patron):
            e = st.radio(
                "Patron " + nombre,
                options=[1, -1],
                format_func=lambda x: "Positivo (+1)" if x == 1 else "Negativo (-1)",
                horizontal=True,
                key="etiqueta_" + str(i)
            )
            etiquetas.append(e)

patrones = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

def calcular(x1, x2, w1, w2, b):
    suma = w1 * x1 + w2 * x2 + b
    salida = 1 if suma > 0 else -1
    return round(suma, 3), salida

resultados = []
for (x1, x2) in patrones:
    suma, salida = calcular(x1, x2, w1, w2, bias)
    resultados.append((suma, salida))

aciertos = sum(1 for i, (_, sal) in enumerate(resultados) if sal == etiquetas[i])

with col_der:
    st.markdown("### Tabla de Clasificacion")
    nombres_patron = ["(-1, -1)", "(-1, +1)", "(+1, -1)", "(+1, +1)"]
    for i, (x1, x2) in enumerate(patrones):
        suma, salida = resultados[i]
        esperado = etiquetas[i]
        correcto = salida == esperado
        icono_switch1 = "arriba" if x1 == 1 else "abajo"
        icono_switch2 = "arriba" if x2 == 1 else "abajo"
        icono_result = "CORRECTO" if correcto else "INCORRECTO"
        etiqueta_str = "Positivo (+1)" if esperado == 1 else "Negativo (-1)"
        salida_str = "Positivo (+1)" if salida == 1 else "Negativo (-1)"

        st.markdown(
            '<div class="patron-card">'
            '<b>Patron ' + str(i+1) + ':</b> Entrada 1 (' + icono_switch1 + ') <b>' + str(x1) + '</b> | '
            'Entrada 2 (' + icono_switch2 + ') <b>' + str(x2) + '</b><br>'
            'Deseado: ' + etiqueta_str + ' | '
            'Suma ponderada: ' + str(suma) + '<br>'
            'Salida: ' + salida_str + ' --- ' + icono_result +
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown('<hr class="separador">', unsafe_allow_html=True)

    color_contador = "#7b1fa2" if aciertos == 4 else "#e91e63"
    mensaje = "Problema resuelto!" if aciertos == 4 else "Sigue ajustando las perillas..."
    icono = "Excelente!" if aciertos == 4 else "Sigue intentando"

    st.markdown(
        '<div class="metrica-box">'
        '<span style="font-size:2em;">' + icono + '</span><br>'
        '<span style="font-size:1.5em; font-weight:bold; color:' + color_contador + ';">'
        + str(aciertos) + ' / 4 patrones correctos'
        '</span><br>'
        '<span style="color:#9c27b0;">' + mensaje + '</span>'
        '</div>',
        unsafe_allow_html=True
    )

st.markdown('<hr class="separador">', unsafe_allow_html=True)
st.markdown(
    '<div class="formula-box">'
    'Formula del Perceptron:<br><br>'
    'salida = w1*x1 + w2*x2 + b = '
    '(' + str(w1) + ') * x1 + (' + str(w2) + ') * x2 + (' + str(bias) + ')<br><br>'
    'Si salida > 0 entonces Positivo (+1) | Si salida menor o igual a 0 entonces Negativo (-1)'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("### Fronter")
