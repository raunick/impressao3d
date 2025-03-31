import streamlit as st
import pandas as pd
from dataclasses import dataclass
from typing import Dict, List, Tuple
import json
import os
from datetime import datetime

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
        """Calcula o peso em gramas por metro de filamento."""
        return (self.peso_total * 1000) / self.comprimento_total
    
    def calcular_preco_por_metro(self) -> float:
        """Calcula o preço por metro de filamento."""
        return self.preco / self.comprimento_total
    
    def calcular_preco_por_grama(self) -> float:
        """Calcula o preço por grama de filamento."""
        return self.preco / (self.peso_total * 1000)

# Catálogo de filamentos padrão
DEFAULT_FILAMENTOS = {
    "Creality Hyper PLA": Filamento("Hyper PLA", "Creality", "PLA", 1.75, 330, 1.0, 120.00),
    "3D Lab PLA+": Filamento("PLA+", "3D Lab", "PLA+", 1.75, 330, 1.0, 130.00),
    "3D Fila PETG": Filamento("PETG Premium", "3D Fila", "PETG", 1.75, 335, 1.0, 140.00),
    "3DX ABS Premium": Filamento("ABS Premium", "3DX", "ABS", 1.75, 340, 1.0, 110.00),
    "Flexível TPU": Filamento("TPU Flex", "3D Prime", "TPU", 1.75, 320, 1.0, 180.00)
}

def salvar_catalogo(catalogo: Dict[str, Filamento], arquivo: str = "catalogo_filamentos.json") -> None:
    """Salva o catálogo de filamentos em um arquivo JSON."""
    # Convertendo objetos Filamento para dicionários
    catalogo_dict = {
        nome: {
            "nome": f.nome,
            "marca": f.marca,
            "material": f.material,
            "diametro": f.diametro,
            "comprimento_total": f.comprimento_total,
            "peso_total": f.peso_total,
            "preco": f.preco
        }
        for nome, f in catalogo.items()
    }
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(catalogo_dict, f, ensure_ascii=False, indent=4)
    
    return True

def carregar_catalogo(arquivo: str = "catalogo_filamentos.json") -> Dict[str, Filamento]:
    """Carrega o catálogo de filamentos de um arquivo JSON."""
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            catalogo_dict = json.load(f)
        
        # Convertendo dicionários para objetos Filamento
        return {
            nome: Filamento(
                nome=dados["nome"],
                marca=dados["marca"],
                material=dados["material"],
                diametro=dados["diametro"],
                comprimento_total=dados["comprimento_total"],
                peso_total=dados["peso_total"],
                preco=dados["preco"]
            )
            for nome, dados in catalogo_dict.items()
        }
    except (FileNotFoundError, json.JSONDecodeError):
        # Se o arquivo não existir ou estiver corrompido, retorna o catálogo padrão
        return DEFAULT_FILAMENTOS

def calcular_preco_impressao(filamento: Filamento, 
                             metros_usados: float, 
                             tempo_impressao: float, 
                             custo_energia_hora: float,
                             custo_manutencao_hora: float, 
                             margem_lucro: float,
                             custo_falha: float = 0.0):
    """
    Calcula o preço de uma impressão 3D.
    
    Args:
        filamento: Objeto Filamento usado na impressão
        metros_usados: Quantidade de metros de filamento usados
        tempo_impressao: Tempo de impressão em minutos
        custo_energia_hora: Custo da energia elétrica por hora em R$
        custo_manutencao_hora: Custo de manutenção por hora em R$
        margem_lucro: Margem de lucro em porcentagem
        custo_falha: Custo adicional para cobrir potenciais falhas (%)
    
    Returns:
        Dict com os detalhes do cálculo
    """
    peso_usado = metros_usados * filamento.calcular_peso_por_metro()
    custo_material = metros_usados * filamento.calcular_preco_por_metro()
    tempo_impressao_horas = tempo_impressao / 60
    custo_energia = tempo_impressao_horas * custo_energia_hora
    custo_manutencao = tempo_impressao_horas * custo_manutencao_hora
    
    # Adicionar custo de falha como porcentagem do custo material
    valor_custo_falha = custo_material * (custo_falha / 100)
    
    custo_total = custo_material + custo_energia + custo_manutencao + valor_custo_falha
    preco_final = custo_total * (1 + (margem_lucro / 100))
    
    return {
        'Peso Usado (g)': peso_usado,
        'Metros Usados': metros_usados,
        'Custo do Material': custo_material,
        'Custo de Energia': custo_energia,
        'Custo de Manutenção': custo_manutencao,
        'Custo para Falhas': valor_custo_falha,
        'Custo Total': custo_total,
        'Preço Final': preco_final
    }

def salvar_orcamento(dados_impressao: Dict, nome_projeto: str):
    """Salva os dados de um orçamento em um arquivo CSV."""
    hoje = datetime.now().strftime("%Y-%m-%d")
    
    # Verificar se o arquivo existe
    arquivo = "historico_orcamentos.csv"
    arquivo_existe = os.path.isfile(arquivo)
    
    # Criar um DataFrame e salvar
    df = pd.DataFrame([{
        'Data': hoje,
        'Projeto': nome_projeto,
        'Filamento': dados_impressao.get('Filamento', 'Não especificado'),
        'Metros': dados_impressao.get('Metros Usados', 0),
        'Peso (g)': dados_impressao.get('Peso Usado (g)', 0),
        'Tempo (min)': dados_impressao.get('Tempo (min)', 0),
        'Custo Material': dados_impressao.get('Custo do Material', 0),
        'Custo Energia': dados_impressao.get('Custo de Energia', 0),
        'Custo Manutenção': dados_impressao.get('Custo de Manutenção', 0),
        'Custo Falhas': dados_impressao.get('Custo para Falhas', 0),
        'Custo Total': dados_impressao.get('Custo Total', 0),
        'Preço Final': dados_impressao.get('Preço Final', 0),
    }])
    
    df.to_csv(arquivo, mode='a', header=not arquivo_existe, index=False)
    return True

def carregar_historico():
    """Carrega o histórico de orçamentos salvos."""
    try:
        return pd.read_csv("historico_orcamentos.csv")
    except FileNotFoundError:
        return pd.DataFrame()

def criar_novo_filamento():
    """Interface para criar um novo filamento."""
    st.subheader("Adicionar Novo Filamento")
    
    with st.form("novo_filamento"):
        col1, col2 = st.columns(2)
        
        with col1:
            nome_completo = st.text_input("Nome Completo (como aparecerá na lista)")
            nome = st.text_input("Nome do Filamento")
            marca = st.text_input("Marca")
            material = st.text_input("Material")
        
        with col2:
            diametro = st.number_input("Diâmetro (mm)", value=1.75, step=0.05)
            comprimento = st.number_input("Comprimento (m/kg)", value=330, step=5)
            peso = st.number_input("Peso (kg)", value=1.0, step=0.1)
            preco = st.number_input("Preço (R$)", value=100.0, step=10.0)
        
        submitted = st.form_submit_button("Adicionar Filamento")
        
        if submitted:
            if not nome_completo or not nome or not marca or not material:
                st.error("Todos os campos de texto são obrigatórios.")
                return None
            
            return {
                "nome_completo": nome_completo,
                "filamento": Filamento(
                    nome=nome,
                    marca=marca,
                    material=material,
                    diametro=diametro,
                    comprimento_total=comprimento,
                    peso_total=peso,
                    preco=preco
                )
            }
    
    return None

def main():
    # Configuração da página
    st.set_page_config(
        page_title='Calculadora de Impressão 3D 🖨️', 
        layout='wide',
        initial_sidebar_state='expanded'
    )
    
    # Inicialização da sessão
    if 'catalogo' not in st.session_state:
        st.session_state.catalogo = carregar_catalogo()
    
    if 'historico' not in st.session_state:
        st.session_state.historico = []
    
    if 'modo' not in st.session_state:
        st.session_state.modo = 'calculadora'
    
    # Barra lateral de navegação
    with st.sidebar:
        st.title('🖨️ Calculadora 3D')
        
        # Menu de navegação
        menu = st.radio(
            "Menu",
            ["Calculadora", "Gerenciar Filamentos", "Histórico", "Sobre"]
        )
        
        if menu == "Calculadora":
            st.session_state.modo = 'calculadora'
        elif menu == "Gerenciar Filamentos":
            st.session_state.modo = 'filamentos'
        elif menu == "Histórico":
            st.session_state.modo = 'historico'
        elif menu == "Sobre":
            st.session_state.modo = 'sobre'
    
    # Conteúdo principal
    if st.session_state.modo == 'calculadora':
        mostrar_calculadora()
    elif st.session_state.modo == 'filamentos':
        mostrar_gerenciador_filamentos()
    elif st.session_state.modo == 'historico':
        mostrar_historico()
    elif st.session_state.modo == 'sobre':
        mostrar_sobre()

def mostrar_calculadora():
    st.title('🧮 Calculadora de Preço para Impressão 3D')
    
    # Layout em colunas
    col_config, col_resultado = st.columns([3, 2])
    
    with col_config:
        st.subheader('⚙️ Configurações da Impressão')
        
        # Detalhes do projeto
        nome_projeto = st.text_input("📋 Nome do Produto", "Minha Impressão 3D")
        
        # Seleção de filamento
        st.subheader('🧱 Filamento')
        filamento_selecionado = st.selectbox(
            'Selecione o Filamento:', 
            options=sorted(list(st.session_state.catalogo.keys()))
        )
        filamento = st.session_state.catalogo[filamento_selecionado]
        
        # Informações do filamento selecionado
        st.info(f"""
        ℹ️ **Informações do Filamento:**
        - Marca: {filamento.marca}
        - Material: {filamento.material}
        - Diâmetro: {filamento.diametro}mm
        - Comprimento: {filamento.comprimento_total}m/kg
        - Preço: R$ {filamento.preco:.2f}/kg
        - Preço por metro: R$ {filamento.calcular_preco_por_metro():.3f}/m
        - Peso por metro: {filamento.calcular_peso_por_metro():.2f}g/m
        """)
        
        # Parâmetros da impressão
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader('📦 Custos do Produto')
            metros_usados = st.number_input('📏 Metros de Filamento:', 
                                         min_value=0.1, value=10.0, step=1.0,
                                         help="Quantidade de metros de filamento usados na impressão")
            st.caption(f"Peso estimado: {metros_usados * filamento.calcular_peso_por_metro():.1f}g")
            
            tempo_impressao = st.number_input('⏱️ Tempo de Impressão (minutos):', 
                                           min_value=1, value=180, step=30,
                                           help="Tempo estimado de impressão em minutos")
            st.caption(f"Equivalente a {tempo_impressao/60:.1f} horas")
        
        with col2:
            st.subheader('💼 Custos Operacionais')
            custo_energia_hora = st.number_input('⚡ Custo de Energia por Hora (R$):', 
                                              min_value=0.1, value=0.5, step=0.1,help="Custo da energia elétrica por hora")
            
            custo_manutencao_hora = st.number_input('🔧 Custo de Manutenção por Hora (R$):', 
                                                 min_value=0.0, value=2.0, step=0.5,help="Custo de manutenção da impressora por hora")
            
            custo_falha = st.number_input('🚨 Margem para Falhas (%):', 
                                      min_value=0, value=5, step=1,
                                      help="Percentual adicional para cobrir potenciais falhas de impressão")
        
        # Margem de lucro
        st.subheader('📈 Margem de Lucro')
        margem_lucro = st.slider('Margem de Lucro (%)', 
                              min_value=0, max_value=200, value=100,help="Margem de lucro desejada em porcentagem")
        
        # Botão de cálculo
        if st.button('🧮 Calcular Preço', type="primary"):
            resultados = calcular_preco_impressao(
                filamento, 
                metros_usados, 
                tempo_impressao, 
                custo_energia_hora, 
                custo_manutencao_hora, 
                margem_lucro,
                custo_falha
            )
            
            # Adicionar informações extras para salvar
            resultados['Filamento'] = filamento_selecionado
            resultados['Tempo (min)'] = tempo_impressao
            
            # Guardar na sessão
            st.session_state.ultimo_resultado = resultados
            st.session_state.ultimo_projeto = nome_projeto
            
            # Forçar atualização da coluna de resultados
            st.rerun()
    
    # Coluna de resultados
    with col_resultado:
        if 'ultimo_resultado' in st.session_state:
            resultados = st.session_state.ultimo_resultado
            nome_projeto = st.session_state.ultimo_projeto
            
            st.subheader(f'💵 Resultado: {nome_projeto}')
            
            # Preço final destacado
            st.metric(
                label="Preço Final Sugerido", 
                value=f"R$ {resultados['Preço Final']:.2f}",
                delta=f"Lucro: R$ {resultados['Preço Final'] - resultados['Custo Total']:.2f}"
            )
            
            # Card com detalhes
            with st.expander('📊 Detalhamento dos Custos', expanded=True):
                st.write(f"📏 **Filamento:** {resultados['Metros Usados']:.1f}m ({resultados['Peso Usado (g)']:.1f}g)")
                st.write(f"⏱️ **Tempo:** {resultados['Tempo (min)']} minutos ({resultados['Tempo (min)']/60:.1f}h)")
                
                # Tabela de custos
                custos_df = pd.DataFrame({
                    'Item': [
                        'Material', 
                        'Energia', 
                        'Manutenção', 
                        'Reserva para Falhas',
                        'Custo Total',
                        'Lucro',
                        'Preço Final'
                    ],
                    'Valor (R$)': [
                        f"{resultados['Custo do Material']:.2f}",
                        f"{resultados['Custo de Energia']:.2f}",
                        f"{resultados['Custo de Manutenção']:.2f}",
                        f"{resultados['Custo para Falhas']:.2f}",
                        f"{resultados['Custo Total']:.2f}",
                        f"{resultados['Preço Final'] - resultados['Custo Total']:.2f}",
                        f"{resultados['Preço Final']:.2f}"
                    ]
                })
                
                st.dataframe(custos_df, hide_index=True, use_container_width=True)
            
            # Opção para salvar
            if st.button("💾 Salvar Orçamento"):
                if salvar_orcamento(resultados, nome_projeto):
                    st.success("Orçamento salvo com sucesso!")
                else:
                    st.error("Erro ao salvar o orçamento.")

def mostrar_gerenciador_filamentos():
    st.title('🧱 Gerenciador de Filamentos')
    
    # Tabela com filamentos existentes
    st.subheader("Catálogo Atual")
    catalogo = st.session_state.catalogo
    
    if catalogo:
        df_filamentos = pd.DataFrame([
            {
                'Nome': nome,
                'Marca': f.marca, 
                'Material': f.material, 
                'Diâmetro (mm)': f.diametro, 
                'Metros/kg': f.comprimento_total, 
                'Preço/kg (R$)': f.preco, 
                'Preço/m (R$)': round(f.calcular_preco_por_metro(), 3),
                'Preço/g (R$)': round(f.calcular_preco_por_grama(), 3)
            } 
            for nome, f in catalogo.items()
        ])
        
        st.dataframe(df_filamentos, use_container_width=True)
    else:
        st.warning("Nenhum filamento cadastrado.")
    
    # Adicionar novo filamento
    st.divider()
    novo_filamento = criar_novo_filamento()
    
    if novo_filamento:
        # Adicionar ao catálogo
        catalogo[novo_filamento["nome_completo"]] = novo_filamento["filamento"]
        st.session_state.catalogo = catalogo
        
        # Salvar no arquivo
        if salvar_catalogo(catalogo):
            st.success(f"Filamento '{novo_filamento['nome_completo']}' adicionado com sucesso!")
        else:
            st.error("Erro ao salvar o catálogo de filamentos.")
    
    # Opção para remover filamento
    st.divider()
    with st.expander("🗑️ Remover Filamento"):
        filamento_para_remover = st.selectbox(
            "Selecione o filamento que deseja remover:",
            options=list(catalogo.keys())
        )
        
        if st.button("Remover", type="primary"):
            del catalogo[filamento_para_remover]
            st.session_state.catalogo = catalogo
            
            if salvar_catalogo(catalogo):
                st.success(f"Filamento '{filamento_para_remover}' removido com sucesso!")
            else:
                st.error("Erro ao salvar o catálogo atualizado.")

def mostrar_historico():
    st.title('📜 Histórico de Orçamentos')
    
    # Carregar histórico
    df = carregar_historico()
    
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        
        # Opção para exportar
        if st.button("📊 Exportar para Excel"):
            df.to_excel("historico_orcamentos.xlsx", index=False)
            st.success("Arquivo exportado como 'historico_orcamentos.xlsx'")
    else:
        st.info("Nenhum orçamento salvo até o momento.")

def mostrar_sobre():
    st.title('ℹ️ Sobre a Calculadora')
    
    st.markdown("""
    ## Calculadora de Preço para Impressão 3D
    
    Esta ferramenta foi desenvolvida para ajudar profissionais e entusiastas de impressão 3D a 
    calcularem preços justos para seus serviços, levando em consideração:
    
    - 🧱 Custo do filamento
    - ⚡ Gastos com energia elétrica
    - 🔧 Custos de manutenção
    - 🚨 Margem para falhas de impressão
    - 💰 Margem de lucro desejada
    
    ### Como calcular
    
    1. Selecione o tipo de filamento
    2. Informe a quantidade de metros usados (obtido do slicer)
    3. Insira o tempo de impressão estimado
    4. Ajuste os custos operacionais conforme necessário
    5. Defina sua margem de lucro
    6. Clique em "Calcular Preço"
    
    ### Recursos adicionais
    
    - Gerenciamento de catálogo de filamentos
    - Salvamento de histórico de orçamentos
    - Exportação de dados para análise
    
    ### Dicas para um orçamento preciso
    
    - Sempre configure os custos operacionais conforme a realidade da sua impressora
    - Considere incluir uma margem para falhas de impressão (5-10%)
    - Atualize regularmente os preços dos filamentos
    - Para objetos complexos, considere aumentar a margem de lucro
    """)

if __name__ == "__main__":
    main()