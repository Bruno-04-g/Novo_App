import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# -----------------------------------------------------------------------------
# Configuração da Página e Estilo CSS Personalizado
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Sistema de Calibração Estática | Célula de Carga",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilização CSS para visual acadêmico e técnico
st.markdown(
    """
    <style>
    .main {
        background-color: #f8f9fa;
    }
    h1 {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 700;
        color: #1a252f;
        margin-bottom: 0px;
    }
    .subtitle {
        font-size: 0.95rem;
        color: #6c757d;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }
    
    /* Cartões de Métricas */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e9ecef;
        border-radius: 6px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        text-align: center;
    }
    .metric-title {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #6c757d;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #111827;
    }
    .metric-unit {
        font-size: 0.85rem;
        color: #4b5563;
        font-weight: 400;
    }

    /* Formatação de Abas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        white-space: pre-wrap;
        border-radius: 4px;
        font-weight: 500;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Cabeçalho Principal
# -----------------------------------------------------------------------------
st.markdown(
    "<h1>Análise da Calibração Estática — Célula de Carga</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p class='subtitle'>Laboratório de Medições e Instrumentação Industrial"
    " — Engenharia Mecânica</p>",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Módulo 1: Entrada de Dados (Painel Lateral)
# -----------------------------------------------------------------------------
st.sidebar.markdown("### Parâmetros de Operação")

y_lido = st.sidebar.number_input(
    "Sinal de Saída Lido y (mV)", value=1220.0, step=5.0, format="%.2f"
)
T_medida = st.sidebar.number_input(
    "Temp. de Operação Top (°C)", value=28.0, step=0.5, format="%.1f"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Condições de Calibração")
T_nom = st.sidebar.number_input("Temp. Nominal T₀ (°C)", value=20.0, step=1.0)
T_calib = st.sidebar.number_input(
    "Temp. de Ensaio T₁ (°C)", value=35.0, step=1.0
)

# Matrizes de Dados do Ensaio
cargas = np.array([0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500])
y20 = np.array(
    [0.0, 130.0, 161.0, 189.0, 1122.0, 1148.0, 1180.0, 1211.0, 1241.0, 1269.0, 1300.0]
)
y35 = np.array(
    [15.0, 149.0, 177.0, 208.0, 1137.0, 1178.0, 1197.0, 1228.0, 1259.0, 1288.0, 1345.0]
)

# -----------------------------------------------------------------------------
# Módulo 2: Processamento Numérico
# -----------------------------------------------------------------------------
delta_T_calib = T_calib - T_nom
K0 = y20[-1] / cargas[-1]  # mV/kgf
Ki = (y35[0] - y20[0]) / delta_T_calib  # mV/°C
K35 = (y35[-1] - y35[0]) / cargas[-1]
Km = (K35 - K0) / delta_T_calib  # (mV/kgf)/°C

delta_T_op = T_medida - T_nom
P_real = (y_lido - Ki * delta_T_op) / (K0 + Km * delta_T_op)
P_indicado = y_lido / K0

E_int = (Ki * delta_T_op) / K0
E_mod = (Km * delta_T_op * P_real) / K0
E_total = P_indicado - P_real

# -----------------------------------------------------------------------------
# Módulo 3: Apresentação dos Resultados
# -----------------------------------------------------------------------------
tab_dash, tab_dados, tab_arch = st.tabs(
    ["Painel de Resultados", "Dados Experimentais", "Estrutura do Sistema"]
)

with tab_dash:
  # Indicadores Chave
  c1, c2, c3, c4 = st.columns(4)

  with c1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Massa Real Corrigida</div>
            <div class="metric-value">{P_real:.2f} <span class="metric-unit">kgf</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

  with c2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Massa Indicada Direta</div>
            <div class="metric-value">{P_indicado:.2f} <span class="metric-unit">kgf</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

  with c3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Erro Global Acumulado</div>
            <div class="metric-value">{E_total:.2f} <span class="metric-unit">kgf</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

  with c4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Sensibilidade Nominal (K₀)</div>
            <div class="metric-value">{K0:.3f} <span class="metric-unit">mV/kgf</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

  st.markdown("<br>", unsafe_allow_html=True)

  col_left, col_right = st.columns([0.45, 0.55])

  with col_left:
    st.subheader("Modelagem Matemática e Componentes do Erro")
    st.markdown(
        "A determinação da massa real considera a compensação térmica dos"
        " efeitos interferentes e modificantes:"
    )

    st.latex(
        r"P_{\text{real}} = \frac{y_{\text{lido}} - K_i \cdot \Delta T}{K_0 +"
        r" K_m \cdot \Delta T}"
    )

    st.markdown("#### Parâmetros do Sensor")
    st.write(f"• **Ganho Interferente ($K_i$):** `{Ki:.4f} mV/°C`")
    st.write(f"• **Ganho Modificante ($K_m$):** `{Km:.6f} (mV/kgf)/°C`")

    st.markdown("#### Decomposição das Parcelas de Erro")
    st.write(
        f"• **Erro de Zero (Interferente):** `{E_int:.3f} kgf`"
        f" ({(E_int/E_total)*100:.1f}% do total)"
    )
    st.write(
        f"• **Erro de Ganho (Modificante):** `{E_mod:.3f} kgf`"
        f" ({(E_mod/E_total)*100:.1f}% do total)"
    )

  with col_right:
    st.subheader("Curvas Características de Resposta Estática")

    # Gráfico Estilizado
    fig, ax = plt.subplots(figsize=(6, 4), dpi=120)

    ax.plot(
        cargas,
        y20,
        marker="o",
        color="#1e3d59",
        linewidth=1.8,
        markersize=5,
        label=f"Ensaio Nominal ({T_nom:.0f} °C)",
    )
    ax.plot(
        cargas,
        y35,
        marker="s",
        color="#ff6e40",
        linestyle="--",
        linewidth=1.8,
        markersize=5,
        label=f"Ensaio Térmico ({T_calib:.0f} °C)",
    )

    ax.axhline(
        y=y_lido,
        color="#d9534f",
        linestyle=":",
        linewidth=1.5,
        label=f"Leitura Operacional ({y_lido} mV)",
    )

    ax.set_xlabel(
        "Carga Aplicada (kgf)", fontsize=9, fontweight="bold", color="#2b2b2b"
    )
    ax.set_ylabel(
        "Sinal de Saída (mV)", fontsize=9, fontweight="bold", color="#2b2b2b"
    )
    ax.tick_params(axis="both", which="major", labelsize=8)

    ax.grid(True, linestyle="--", alpha=0.4, color="#b0bec5")
    ax.legend(
        frameon=True, facecolor="#ffffff", edgecolor="#e0e0e0", fontsize=8
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#888888")
    ax.spines["bottom"].set_color("#888888")

    st.pyplot(fig)

with tab_dados:
  st.subheader("Matriz de Calibração do Ensaio de Célula de Carga")
  st.markdown(
      "Valores medidos durante o ensaio de calibração em duas condições de"
      " temperatura controlada:"
  )

  df_dados = pd.DataFrame({
      "Carga Aplicada (kgf)": cargas,
      "Saída Térmica a 20°C (mV)": y20,
      "Saída Térmica a 35°C (mV)": y35,
  })

  st.dataframe(
      df_dados.style.format({
          "Carga Aplicada (kgf)": "{:.0f}",
          "Saída Térmica a 20°C (mV)": "{:.1f}",
          "Saída Térmica a 35°C (mV)": "{:.1f}",
      }),
      use_container_width=True,
      hide_index=True,
  )

with tab_arch:
  st.subheader("Arquitetura e Fluxo de Dados do Sistema Computacional")
  st.markdown(
      "Estrutura modular desenvolvida para aquisição, processamento e exibição"
      " gráfica:"
  )

  st.markdown("""
    ```text
    ┌────────────────────────────────────────────────────────────────────────┐
    │                           MÓDULO PRINCIPAL                             │
    └──────────────────────────────────┬─────────────────────────────────────┘
                                       │
        ┌──────────────────────────────┼──────────────────────────────┐
        ▼                              ▼                              ▼
  ┌───────────┐                  ┌───────────┐                  ┌───────────┐
  │ ENTRADA DE│                  │ PROCESSA- │                  │ SAÍDA DE  │
  │   DADOS   │                  │  MENTO    │                  │   DADOS   │
  └─────┬─────┘                  └─────┬─────┘                  └─────┬─────┘
        │                              │                              │
        ├─ Leitura do Sinal (mV)       ├─ Sensibilidade K₀            ├─ Dashboard KPIs
        ├─ Temperatura Operacional     ├─ Ganhos Kᵢ e Kₘ              ├─ Curvas Térmicas
        └─ Tabelas de Calibração       └─ Compensação de Erros        └─ Matriz de Dados
    ```
    """)
