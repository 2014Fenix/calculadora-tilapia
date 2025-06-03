
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import base64
import os

st.set_page_config(page_title="Calculadora de Tilapias", layout="centered")

st.title("🐟 Calculadora Agroeducativa de Tilapias")
st.write("Simulador educativo para el seguimiento del crecimiento, alimentación y condiciones de cultivo de tilapias.")

# Entradas del usuario
fecha = st.date_input("📅 Fecha de la semana:", value=datetime.today())

volumen = st.number_input("💧 Volumen de agua (litros):", min_value=1)
n_tilapias = st.number_input("🐟 Número de tilapias al inicio de la semana:", min_value=1)
tilapias_muertas = st.number_input("☠️ Tilapias muertas esta semana:", min_value=0, max_value=n_tilapias)
alimento_por_tilapia = st.number_input("🍽️ Alimento por tilapia por día (gramos):", min_value=0.0)
dias_alimentacion = st.number_input("📆 Días de alimentación en la semana:", min_value=1, max_value=7)
peso_inicial = st.number_input("⚖️ Peso promedio inicial por tilapia (gramos):", min_value=0.0)
peso_final = st.number_input("📈 Peso promedio final por tilapia (gramos):", min_value=0.0)
T_actual = st.number_input("🌡️ Temperatura actual del agua (°C):", min_value=0.0)
T_optima = st.number_input("🎯 Temperatura óptima (°C):", min_value=0.0)
tipo_energia = st.selectbox("⚡ Tipo de energía utilizada:", ["Eléctrica", "Solar", "Otra"])

if st.button("Calcular resultados"):
    st.subheader("📊 Resultados semanales")

    alimento_total = alimento_por_tilapia * n_tilapias * dias_alimentacion
    ganancia_peso = peso_final - peso_inicial

    if ganancia_peso > 0:
        ica = alimento_total / (ganancia_peso * n_tilapias)
        ica_texto = f"{ica:.2f}"
    else:
        ica = None
        ica_texto = "No calculable"

    mortalidad = (tilapias_muertas / n_tilapias) * 100
    tilapias_vivas = n_tilapias - tilapias_muertas
    biomasa_kg = (peso_final * tilapias_vivas) / 1000

    st.write(f"🍽️ Alimento total consumido por semana: **{alimento_total:.2f} g**")
    st.write(f"⚖️ Ganancia de peso semanal por tilapia: **{ganancia_peso:.1f} g**")
    st.write(f"📈 Índice de conversión alimenticia (ICA): **{ica_texto}**")
    st.write(f"☠️ Mortalidad semanal: **{mortalidad:.1f}%**")
    st.write(f"🐟 Biomasa total en el estanque: **{biomasa_kg:.2f} kg**")

    if mortalidad > 5:
        st.error("🚨 Mortalidad alta. Revisa calidad del agua o densidad.")
    elif mortalidad > 0:
        st.warning("⚠️ Mortalidad registrada. Hacer seguimiento.")
    else:
        st.success("✅ Sin mortalidad esta semana.")

    if T_actual < T_optima - 2:
        st.error("🌡️ La temperatura está por debajo del rango óptimo.")
    elif T_actual > T_optima + 2:
        st.warning("🌡️ La temperatura está por encima del ideal.")
    else:
        st.success("🌡️ Temperatura adecuada para crecimiento.")

    st.info(f"⚡ Energía utilizada: **{tipo_energia}**")

    fig, ax = plt.subplots()
    ax.plot([0, 1], [peso_inicial, peso_final], marker='o')
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Semana anterior", "Semana actual"])
    ax.set_ylabel("Peso (g)")
    ax.set_title("Crecimiento semanal de tilapias")
    st.pyplot(fig)

    fila = {
        "fecha": fecha,
        "volumen_litros": volumen,
        "n_tilapias": n_tilapias,
        "tilapias_muertas": tilapias_muertas,
        "alimento_por_tilapia": alimento_por_tilapia,
        "dias_alimentacion": dias_alimentacion,
        "alimento_total": alimento_total,
        "peso_inicial": peso_inicial,
        "peso_final": peso_final,
        "ganancia_peso_semanal": ganancia_peso,
        "ICA": ica_texto,
        "T_actual": T_actual,
        "T_optima": T_optima,
        "tipo_energia": tipo_energia,
        "biomasa_kg": biomasa_kg,
        "mortalidad": mortalidad
    }

    archivo = "registro_tilapia.csv"
    try:
        df = pd.read_csv(archivo)
        df = pd.concat([df, pd.DataFrame([fila])], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame([fila])
    df.to_csv(archivo, index=False)
    st.success("✅ Datos guardados correctamente.")

    st.subheader("📋 Historial de semanas registradas")
    st.dataframe(df)

    # Botón de descarga CSV
    with open(archivo, "rb") as file:
        btn = st.download_button(
            label="⬇️ Descargar historial en Excel (.csv)",
            data=file,
            file_name="registro_tilapia.csv",
            mime="text/csv"
        )
