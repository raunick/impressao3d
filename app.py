import streamlit as st
import pandas as pd
from dataclasses import dataclass
from typing import Dict

@dataclass
class Filamento:
    nome: str
    marca: str
    material: str
    diametro: float
    comprimento_total: int  # metros por kg
    peso_total: float      # em kg
    preco: float          # preço por kg

    def calcular_peso_por_metro(self) -> float:
        return (self.peso_total * 1000) / self.comprimento_total  # retorna peso em gramas por metro

    def calcular_preco_por_metro(self) -> float:
        return self.preco / self.comprimento_total

# Catálogo de filamentos
CATALOGO_FILAMENTOS = {
    "Creality Hyper PLA": Filamento(
        nome="Hyper PLA",
        marca="Creality",
        material="PLA",
        diametro=1.75,
        comprimento_total=330,
        peso_total=1.0,
        preco=120.00
    ),
    "3D Lab PLA+": Filamento(
        nome="PLA+",
        marca="3D Lab",
        material="PLA+",
        diametro=1.75,
        comprimento_total=330,
        peso_total=1.0,
        preco=130.00
    ),
    "3D Fila PETG": Filamento(
        nome="PETG Premium",
        marca="3D Fila",
        material="PETG",
        diametro=1.75,
        comprimento_total=335,
        peso_total=1.0,
        preco=140.00
    ),
    "3DX ABS Premium": Filamento(
        nome="ABS Premium",
        marca="3DX",
        material="ABS",
        diametro=1.75,
        comprimento_total=340,
        peso_total=1.0,
        preco=110.00
    ),
    "Flexível TPU": Filamento(
        nome="TPU Flex",
        marca="3D Prime",
        material="TPU",
        diametro=1.75,
        comprimento_total=320,
        peso_total=1.0,
        preco=180.00
    )
}

def calcular_preco_impressao(filamento: Filamento, metros_usados: float, 
                           tempo_impressao: float, custo_energia_hora: float,
                           custo_manutencao_hora: float, margem_lucro: float):
    # Calcula o custo do material por metro
    peso_usado = metros_usados * filamento.calcular_peso_por_metro()  # em gramas
    custo_material = (metros_usados * filamento.calcular_preco_por_metro())
    
    # Calcula o custo da energia e manutenção
    tempo_impressao_horas = tempo_impressao / 60  # Converte minutos para horas
    custo_energia = tempo_impressao_horas * custo_energia_hora
    custo_manutencao = tempo_impressao_horas * custo_manutencao_hora
    
    # Calcula o custo total
    custo_total = custo_material + custo_energia + custo_manutencao
    
    # Aplica a margem de lucro
    preco_final = custo_total * (1 + (margem_lucro / 100))
    
    return {
        'Peso Usado (g)': peso_usado,
        'Metros Usados': metros_usados,
        'Custo do Material': custo_material,
        'Custo de Energia': custo_energia,
        'Custo de Manutenção': custo_manutencao,
        'Custo Total': custo_total,
        'Preço Final': preco_final
    }

# Configuração da página
st.set_page_config(page_title='Calculadora de Impressão 3D 🖨️', layout='wide')

# Título
st.title('🖨️ Calculadora de Preço para Impressão 3D')

# Sidebar com os inputs
with st.sidebar:
    st.header('⚙️ Configurações')
    
    # Seleção do filamento
    st.subheader('🧱 Filamento')
    filamento_selecionado = st.selectbox(
        'Selecione o Filamento:',
        options=list(CATALOGO_FILAMENTOS.keys())
    )
    
    filamento = CATALOGO_FILAMENTOS[filamento_selecionado]
    
    # Exibe informações do filamento
    st.write(f"""
    ℹ️ **Informações do Filamento:**
    - Marca: {filamento.marca}
    - Material: {filamento.material}
    - Diâmetro: {filamento.diametro}mm
    - Comprimento: {filamento.comprimento_total}m/kg
    - Preço: R$ {filamento.preco:.2f}/kg
    """)

    # Inputs principais
    metros_usados = st.number_input('📏 Metros de Filamento:', 
                                  min_value=0.0, value=10.0, step=1.0)
    
    tempo_impressao = st.number_input('⏱️ Tempo de Impressão (minutos):', 
                                    min_value=0, value=180, step=30)
    
    # Custos operacionais
    st.subheader('💼 Custos Operacionais')
    custo_energia_hora = st.number_input('⚡ Custo de Energia por Hora (R$):', 
                                       min_value=0.0, value=0.5, step=0.1)
    
    custo_manutencao_hora = st.number_input('🔧 Custo de Manutenção por Hora (R$):', 
                                          min_value=0.0, value=2.0, step=0.5)
    
    # Margem de lucro
    st.subheader('📈 Margem de Lucro')
    margem_lucro = st.slider('Margem de Lucro (%)', 
                            min_value=0, max_value=200, value=50)

# Botão para calcular
if st.button('🧮 Calcular Preço'):
    resultados = calcular_preco_impressao(
        filamento, metros_usados, tempo_impressao,
        custo_energia_hora, custo_manutencao_hora, margem_lucro
    )
    
    # Exibe os resultados
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader('📊 Detalhamento dos Custos')
        st.write(f"📏 Metros Usados: {resultados['Metros Usados']:.1f}m")
        st.write(f"⚖️ Peso Usado: {resultados['Peso Usado (g)']:.1f}g")
        for item, valor in resultados.items():
            if item not in ['Preço Final', 'Metros Usados', 'Peso Usado (g)']:
                st.write(f'{item}: R$ {valor:.2f}')
    
    with col2:
        st.subheader('💵 Preço Final Sugerido')
        st.write(f'R$ {resultados["Preço Final"]:.2f}')
        
        # Calcula o lucro
        lucro = resultados['Preço Final'] - resultados['Custo Total']
        st.write(f'📈 Lucro: R$ {lucro:.2f}')

# Adiciona informações de ajuda
with st.expander('❓ Como usar a calculadora'):
    st.write("""
    1. 🧱 Selecione o filamento que será usado na impressão
    2. 📏 Digite a quantidade de metros de filamento necessária
    3. ⏱️ Insira o tempo estimado de impressão em minutos
    4. 💼 Ajuste os custos operacionais se necessário
    5. 📈 Define a margem de lucro desejada
    6. 🧮 Clique em 'Calcular Preço' para ver os resultados
    
    Os custos operacionais incluem:
    - ⚡ Energia: consumo da impressora e equipamentos
    - 🔧 Manutenção: desgaste da máquina, troca de peças, etc.
    
    O preço final é calculado somando todos os custos e aplicando a margem de lucro.
    """)

# Adiciona tabela comparativa de filamentos
with st.expander('📋 Catálogo de Filamentos'):
    # Criar DataFrame com informações dos filamentos
    df_filamentos = pd.DataFrame([
        {
            'Marca': f.marca,
            'Material': f.material,
            'Diâmetro (mm)': f.diametro,
            'Metros/kg': f.comprimento_total,
            'Preço/kg (R$)': f.preco,
            'Preço/metro (R$)': f.calcular_preco_por_metro()
        }
        for f in CATALOGO_FILAMENTOS.values()
    ])
    
    st.dataframe(df_filamentos)