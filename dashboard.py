import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
from datetime import datetime
import time
import numpy as np
import pytz

# Atualiza automaticamente os dados a cada 60 segundos sem recarregar a página do navegador
if 'last_update' not in st.session_state:
    st.session_state['last_update'] = time.time()

if time.time() - st.session_state['last_update'] > 60:
    st.session_state['last_update'] = time.time()
    st.experimental_rerun()

fuso_brasil = pytz.timezone('America/Sao_Paulo')
agora_brasil = datetime.now(fuso_brasil)

print(f"Dashboard atualizado em: {agora_brasil.strftime('%d/%m/%Y, %H:%M:%S')}")

# CSS para cards super compactos e sem margens extras
st.markdown('''
    <style>
    .main, .block-container { padding-top: 0.1rem !important; padding-left: 0.5vw !important; padding-right: 0.5vw !important; }
    h1 { margin-top: 0.05em !important; margin-bottom: 0.05em !important; }
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', Arial, sans-serif !important;
        background-color: #f7f9fa !important;
    }
    .stMetric { text-align: center !important; }
    .export-btn { display: flex; align-items: center; height: 100px; }
    .export-btn a {
        text-decoration: none !important;
    }
    .export-btn button {
        display: flex;
        align-items: center;
        gap: 0.6em;
        background: linear-gradient(90deg, #f7fafd 60%, #e3ecf7 100%) !important;
        color: #2A5C8C !important;
        border-radius: 12px !important;
        font-family: 'Segoe UI', Arial, sans-serif !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 0.5em 1.3em !important;
        border: 1.5px solid #2A5C8C !important;
        box-shadow: 0 3px 14px #2A5C8C18, 0 1px 4px #2A5C8C11;
        margin-left: 1em !important;
        margin-top: 0.2em !important;
        transition: all 0.22s cubic-bezier(.4,2,.6,1);
        cursor: pointer;
    }
    .export-btn button:hover {
        background: #2A5C8C !important;
        color: #fff !important;
        border: 2px solid #2A5C8C !important;
        box-shadow: 0 8px 32px #2A5C8C33, 0 2px 8px #2A5C8C22;
        transform: translateY(-2px) scale(1.04);
    }
    .export-btn svg {
        width: 1.3em;
        height: 1.3em;
        vertical-align: middle;
        fill: currentColor;
    }
    .card-spaced {
        background:#fff;
        border-radius:18px;
        box-shadow:0 2px 12px #4058bd18;
        padding:1.5em 1.2em 1.2em 1.2em;
        min-height:140px;min-width:210px;max-width:220px;width:100%;
        display:flex;flex-direction:column;align-items:flex-start;
        margin-right:18px;margin-bottom:18px;
    }
    .card-label {
        color: #4058BD;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.2em;
    }
    .card-value {
        font-size: 2.1rem;
        font-weight: 800;
        color: #222;
        margin-bottom: 0.2em;
    }
    .card-icon {
        font-size: 2rem;
        margin-bottom: 0.3em;
    }
    </style>
''', unsafe_allow_html=True)

# Top bar com título e botão exportar
col_top1, col_top2 = st.columns([6,1])
with col_top1:
    st.markdown("<h1 style='color:#4058BD;font-size:1.5rem;font-family:Segoe UI;margin-bottom:0.1em;'>Dashboard - Atendimento Personalizado</h1>", unsafe_allow_html=True)
    st.markdown(f"<span style='color:#888;font-size:0.95rem;'>Última atualização: {agora_brasil.strftime('%d/%m/%Y, %H:%M:%S')}</span>", unsafe_allow_html=True)
with col_top2:
    # Carregar o CSV normalmente para definir df
    csv_url = "https://docs.google.com/spreadsheets/d/16wN44BGetQZYs2BxEJRq-BbdLtTPdYCzlMgoBQEHNbA/export?format=csv"
    try:
        df = pd.read_csv(csv_url)
    except Exception:
        df = pd.DataFrame()
    # Botão de exportação Excel
    excel_url = "https://docs.google.com/spreadsheets/d/16wN44BGetQZYs2BxEJRq-BbdLtTPdYCzlMgoBQEHNbA/export?format=xlsx"
    st.markdown(f"""
<div class='export-btn'>
  <a href='{excel_url}' target='_blank'>
    <button>
      <svg viewBox='0 0 20 20'><path d='M13 10V3H7v7H4l6 7 6-7h-3zM4 18v-2h12v2H4z'></path></svg>
      Exportar
    </button>
  </a>
</div>
""", unsafe_allow_html=True)

# Forçar colunas a string para evitar erro do .str
for col in ['Nome', 'Gênero', 'Cesta', 'Aceita Cursos', 'Escolaridade']:
    if col in df.columns:
        df[col] = df[col].astype(str)

def contar_escolaridade(df, nivel):
    if 'Escolaridade' in df.columns:
        return df[df['Escolaridade'] == nivel].shape[0]
    return 0

if 'Nome' in df.columns:
    # Remove linhas onde todas as colunas estão vazias ou só espaços
    df = df.replace(r'^\s*$', np.nan, regex=True)
    df = df.dropna(how='all')
    # Filtra linhas onde 'Nome' não é nulo, não é vazio, não é só espaço
    valid_df = df[df['Nome'].notna() & df['Nome'].astype(str).str.strip().ne('')]
else:
    valid_df = pd.DataFrame()

total_atendidos = valid_df.shape[0]
qtd_masculinos = valid_df[valid_df['Gênero'].str.lower() == 'masculino'].shape[0] if 'Gênero' in valid_df.columns and not valid_df.empty else 0
qtd_femininos = valid_df[valid_df['Gênero'].str.lower() == 'feminino'].shape[0] if 'Gênero' in valid_df.columns and not valid_df.empty else 0
analfabeto = contar_escolaridade(valid_df, 'Analfabeto')
fund_incompleto = contar_escolaridade(valid_df, 'Ensino Fundamental Incompleto')
fund_completo = contar_escolaridade(valid_df, 'Ensino Fundamental Completo')
medio_incompleto = contar_escolaridade(valid_df, 'Ensino Médio Incompleto')
medio_completo = contar_escolaridade(valid_df, 'Ensino Médio Completo')
sup_incompleto = contar_escolaridade(valid_df, 'Ensino Superior Incompleto')
sup_completo = contar_escolaridade(valid_df, 'Ensino Superior Completo')
total_encaminhamentos = valid_df['QTD Encaminhentos'].fillna(0).astype(int).sum() if 'QTD Encaminhentos' in valid_df.columns and not valid_df.empty else 0
ocup_cols = [col for col in valid_df.columns if 'Ocupação N. Vaga' in col] if not valid_df.empty else []
total_contratados = valid_df[ocup_cols].notnull().any(axis=1).sum() if ocup_cols else 0
aproveitamento = (total_contratados / total_encaminhamentos * 100) if total_encaminhamentos else 0
if 'Cesta' in valid_df.columns and not valid_df.empty:
    trabalhadores_com_cesta = valid_df[valid_df['Cesta'].str.lower() == 'sim'].shape[0]
    qtd_cestas_entregues = valid_df['Cesta'].str.lower().value_counts().get('sim', 0)
else:
    trabalhadores_com_cesta = 0
    qtd_cestas_entregues = 0
if 'Aceita Cursos' in valid_df.columns and not valid_df.empty:
    trabalhadores_fizeram_curso = valid_df[valid_df['Aceita Cursos'].str.lower() == 'sim'].shape[0]
    total_participacoes_cursos = valid_df['Aceita Cursos'].str.lower().value_counts().get('sim', 0)
else:
    trabalhadores_fizeram_curso = 0
    total_participacoes_cursos = 0

# Função para renderizar cards em grid super compacto
def render_cards_grid(cards, columns=6):
    for i in range(0, len(cards), columns):
        cols = st.columns(columns)
        row = cards[i:i+columns]
        for j in range(columns):
            with cols[j]:
                if j < len(row):
                    card = row[j]
                    st.markdown(f"""
                        <div style='background:#fff;border-radius:12px;box-shadow:0 1px 4px #4058bd10;
                        padding:0.4em 0.4em 0.4em 0.4em;min-height:48px;display:flex;flex-direction:column;align-items:flex-start;'>
                            <div style='font-size:1.1rem;margin-bottom:0.05em;'>{card['icon']}</div>
                            <div style='color:#4058BD;font-size:0.85rem;font-weight:600;margin-bottom:0.01em;'>{card['label']}</div>
                            <div style='font-size:1.1rem;font-weight:800;color:#222;margin-bottom:0.01em;'>{card['value']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("<div style='visibility:hidden;min-height:48px;'></div>", unsafe_allow_html=True)

# Adicionar antes de '## Perfil Educacional'
st.markdown("<h2 style='color:#4058BD;font-size:1.1rem;font-family:Segoe UI;margin-top:0.2em;margin-bottom:0.2em;'>Atendimentos</h2>", unsafe_allow_html=True)
cards_demograficos = [
    {"icon": "👥", "label": "Total de Atendidos", "value": total_atendidos},
    {"icon": "🧑‍🦱", "label": "Quantidade Masculinos", "value": qtd_masculinos},
    {"icon": "👩", "label": "Quantidade Feminino", "value": qtd_femininos},
    {"icon": "📈", "label": "Total de Encaminhamentos", "value": total_encaminhamentos},
]
render_cards_grid(cards_demograficos, columns=4)

# --- Perfil Educacional ---
st.markdown("<h2 style='color:#2A5C8C;font-size:1.1rem;font-family:Segoe UI;margin-top:0.2em;margin-bottom:0.2em;'>Perfil Educacional</h2>", unsafe_allow_html=True)
labels_educ = ["Analfabeto", "Ensino Fundamental Incompleto", "Ensino Fundamental Completo", "Ensino Médio Incompleto", "Ensino Médio Completo", "Ensino Superior Incompleto", "Ensino Superior Completo"]
values_educ = [contar_escolaridade(valid_df, nivel) for nivel in labels_educ]
educ_df = pd.DataFrame({"Escolaridade": labels_educ, "Quantidade": values_educ})
fig_educ = px.bar(
    educ_df,
    x="Escolaridade",
    y="Quantidade",
    color_discrete_sequence=["#4058BD"],
)
fig_educ.update_layout(
    yaxis_range=[0, max(values_educ + [1])],
    xaxis_title=None,
    yaxis_title=None,
    plot_bgcolor="#fff",
    paper_bgcolor="#fff",
    font=dict(size=15),
    showlegend=False,
    margin=dict(l=10, r=10, t=10, b=10),
    height=260,
    yaxis=dict(dtick=1)
)
fig_educ.update_traces(marker_line_width=0)
st.plotly_chart(fig_educ, use_container_width=True)

# --- Resultados e Benefícios ---
st.markdown("<h2 style='color:#2A5C8C;font-size:1.1rem;font-family:Segoe UI;margin-top:0.2em;margin-bottom:0.2em;'>Resultados e Benefícios</h2>", unsafe_allow_html=True)
cards_resultados = [
    {"icon": "✅", "label": "Total de Contratados", "value": total_contratados},
    {"icon": "📊", "label": "Aproveitamento", "value": f"{aproveitamento:.1f}%"},
    {"icon": "🧺", "label": "Pessoas com Cesta", "value": trabalhadores_com_cesta},
    {"icon": "📦", "label": "Total de Cestas Entregues", "value": qtd_cestas_entregues},
    {"icon": "🎓", "label": "Pessoas que Fizeram Curso", "value": trabalhadores_fizeram_curso},
    {"icon": "📚", "label": "Total de Participações em Cursos", "value": total_participacoes_cursos},
]
render_cards_grid(cards_resultados, columns=6)

# --- OCUPAÇÕES MAIS CONTRATADAS (Gráfico de barras azul, agora VERTICAL) ---
st.markdown("<h2 style='color:#2A5C8C;font-size:1.1rem;font-family:Segoe UI;margin-top:0.2em;margin-bottom:0.2em;'>Ocupações que mais foram contratados</h2>", unsafe_allow_html=True)
if ocup_cols and total_contratados > 0:
    ocupacoes = pd.Series(dtype=str)
    for col in ocup_cols:
        ocupacoes = ocupacoes.append(valid_df[col].dropna().astype(str))
    ocupacoes = ocupacoes[ocupacoes.str.strip() != '']
    ocupacoes_count = ocupacoes.value_counts().reset_index()
    ocupacoes_count.columns = ['Ocupação', 'Contratações']
    top_ocup = ocupacoes_count.head(8)
else:
    top_ocup = pd.DataFrame({"Ocupação": ["-"]*4, "Contratações": [0]*4})
fig_ocup = px.bar(top_ocup, y='Contratações', x='Ocupação', color_discrete_sequence=['#4058BD'])
fig_ocup.update_layout(xaxis_title=None, yaxis_title=None, plot_bgcolor='#fff', paper_bgcolor='#fff', font=dict(size=15), showlegend=False, yaxis_range=[0, max(top_ocup['Contratações'].max(), 1)], yaxis=dict(dtick=1))
st.plotly_chart(fig_ocup, use_container_width=True)

# --- Gráfico de Gantt: Linha do tempo Atendimento até Contratação ---
if 'Data Primeiro Atendimento' in valid_df.columns and 'Data de Contração' in valid_df.columns:
    gantt_df = valid_df[['Nome', 'Data Primeiro Atendimento', 'Data de Contração']].copy()
    # Filtrar apenas registros com ambas as datas preenchidas
    gantt_df = gantt_df.dropna(subset=['Data Primeiro Atendimento', 'Data de Contração'])
    # Converter para datetime
    gantt_df['Data Primeiro Atendimento'] = pd.to_datetime(gantt_df['Data Primeiro Atendimento'], errors='coerce', dayfirst=True)
    gantt_df['Data de Contração'] = pd.to_datetime(gantt_df['Data de Contração'], errors='coerce', dayfirst=True)
    gantt_df = gantt_df.dropna(subset=['Data Primeiro Atendimento', 'Data de Contração'])
    # Ordenar por data de atendimento
    gantt_df = gantt_df.sort_values('Data Primeiro Atendimento')
    if not gantt_df.empty:
        fig_gantt = px.timeline(
            gantt_df,
            x_start='Data Primeiro Atendimento',
            x_end='Data de Contração',
            y='Nome',
            color_discrete_sequence=['#4058BD'],
        )
        fig_gantt.update_yaxes(autorange="reversed")
        fig_gantt.update_layout(
            title_text='Linha do Tempo: Atendimento até Contratação',
            xaxis_title=None,
            yaxis_title=None,
            plot_bgcolor='#fff',
            paper_bgcolor='#fff',
            font=dict(size=14),
            showlegend=False,
            margin=dict(l=10, r=10, t=40, b=10),
            height=350
        )
        st.plotly_chart(fig_gantt, use_container_width=True)

        # --- Média de dias e meses até contratação ---
        gantt_df['Dias até Contratação'] = (gantt_df['Data de Contração'] - gantt_df['Data Primeiro Atendimento']).dt.days
        media_dias_contratacao = gantt_df['Dias até Contratação'].mean()
        media_meses_contratacao = media_dias_contratacao / 30.44 if media_dias_contratacao is not None and not np.isnan(media_dias_contratacao) else None

        if media_dias_contratacao is not None and not np.isnan(media_dias_contratacao):
            st.markdown(
                f"""<div style='color:#4058BD;font-size:1.1rem;font-weight:600;margin-top:0.5em;'>
                Média de dias até contratação: <b>{media_dias_contratacao:.1f} dias</b><br>
                Média de meses até contratação: <b>{media_meses_contratacao:.2f} meses</b>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown(
                "<div style='color:#4058BD;font-size:1.1rem;font-weight:600;margin-top:0.5em;'>Média de dias/meses até contratação: <b>Não disponível</b></div>",
                unsafe_allow_html=True)

st.markdown(
    "<div style='text-align:center; color:#888; font-size:0.85rem; margin-top:2em;'>Desenvolvido por Paulo Gramacho</div>",
    unsafe_allow_html=True
) 