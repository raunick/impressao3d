import streamlit as st

def calcular_preco_venda(preco_custo, comissao, taxa_fixa, nota_fiscal, embalagem, margem_lucro, outras_taxas=0):
    # Calcula o lucro desejado (percentual do preço de custo)
    lucro_desejado = preco_custo * (margem_lucro / 100)
    
    # Soma dos percentuais que incidem sobre o preço de venda
    total_percentual = comissao + nota_fiscal + outras_taxas
    
    # Evitar divisão por zero ou porcentagens inválidas
    if total_percentual >= 100:
        return 0, 0, 0, 0, 0, 0, 0
    
    # Calcula o preço de venda usando a equação:
    # Preço de Venda = (Custo + Lucro Desejado + Taxa Fixa + Embalagem) / (1 - (Comissão + Nota Fiscal + Outras Taxas)/100)
    preco_venda = (preco_custo + lucro_desejado + taxa_fixa + embalagem) / (1 - (total_percentual / 100))
    
    # Cálculo dos valores individuais com base no preço de venda
    comissao_valor = preco_venda * (comissao / 100)
    nota_fiscal_valor = preco_venda * (nota_fiscal / 100)
    outras_taxas_valor = preco_venda * (outras_taxas / 100)
    
    # O lucro efetivo é o lucro desejado (definido como percentual sobre o custo)
    lucro = lucro_desejado
    
    # Valor líquido que o vendedor recebe
    recebe = preco_venda - comissao_valor - taxa_fixa - nota_fiscal_valor - embalagem - outras_taxas_valor
    
    return preco_venda, comissao_valor, taxa_fixa, nota_fiscal_valor, embalagem, outras_taxas_valor, lucro, recebe

st.set_page_config(page_title="Calculadora de Preços para Marketplaces", layout="wide")

st.title("Calculadora de Preços para Marketplaces")

tab1, tab2, tab3, tab4 = st.tabs(["Shopee", "Mercado Livre", "TikTok Shop", "Kawaii"])

with tab1:
    st.header("Calculadora Shopee")
    
    # Entradas do usuário para Shopee
    preco_custo_shopee = st.number_input("Preço de Custo (R$):", min_value=0.0, value=10.0, step=0.1, key="custo_shopee")
    margem_lucro_shopee = st.number_input("Margem de Lucro Desejada (%):", min_value=0.0, max_value=100.0, value=50.0, step=0.1, key="margem_shopee")
    comissao_shopee = st.number_input("Comissão da Shopee (%):", min_value=0.0, max_value=100.0, value=20.0, step=0.1, key="comissao_shopee")
    taxa_fixa_shopee = st.number_input("Taxa Fixa (Frete) (R$):", min_value=0.0, value=4.0, step=0.1, key="taxa_shopee")
    nota_fiscal_shopee = st.number_input("Nota Fiscal (%):", min_value=0.0, max_value=100.0, value=5.0, step=0.1, key="nf_shopee")
    embalagem_shopee = st.number_input("Custo de Embalagem (R$):", min_value=0.0, value=1.0, step=0.1, key="embalagem_shopee")
    
    # Chamando a função para Shopee
    if st.button("Calcular Preço Shopee"):
        preco_venda, comissao_valor, taxa_fixa, nota_fiscal_valor, embalagem, outras_taxas_valor, lucro, recebe = calcular_preco_venda(
            preco_custo_shopee, comissao_shopee, taxa_fixa_shopee, nota_fiscal_shopee, embalagem_shopee, margem_lucro_shopee
        )
        
        # Exibição dos resultados Shopee
        st.subheader("Resultados Shopee")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Preço de Venda", f"R$ {preco_venda:.2f}")
            st.metric(f"Comissão ({comissao_shopee}%)", f"R$ {comissao_valor:.2f}")
            st.metric("Taxa Fixa", f"R$ {taxa_fixa:.2f}")
            st.metric("Embalagem", f"R$ {embalagem:.2f}")
        
        with col2:
            st.metric(f"Nota Fiscal ({nota_fiscal_shopee}%)", f"R$ {nota_fiscal_valor:.2f}")
            st.metric("Lucro Desejado", f"R$ {lucro:.2f}")
            st.metric("Valor Líquido Recebido", f"R$ {recebe:.2f}")
            st.info("O valor líquido é o que você recebe após descontar todas as taxas e custos.")

with tab2:
    st.header("Calculadora Mercado Livre")
    
    # Entradas do usuário para Mercado Livre
    preco_custo_ml = st.number_input("Preço de Custo (R$):", min_value=0.0, value=10.0, step=0.1, key="custo_ml")
    margem_lucro_ml = st.number_input("Margem de Lucro Desejada (%):", min_value=0.0, max_value=100.0, value=50.0, step=0.1, key="margem_ml")
    comissao_ml = st.number_input("Comissão do Mercado Livre (%):", min_value=0.0, max_value=100.0, value=17.0, step=0.1, key="comissao_ml")
    taxa_fixa_ml = st.number_input("Taxa Fixa (Frete) (R$):", min_value=0.0, value=5.0, step=0.1, key="taxa_ml")
    nota_fiscal_ml = st.number_input("Nota Fiscal (%):", min_value=0.0, max_value=100.0, value=5.0, step=0.1, key="nf_ml")
    embalagem_ml = st.number_input("Custo de Embalagem (R$):", min_value=0.0, value=1.5, step=0.1, key="embalagem_ml")
    taxa_anuncio_ml = st.number_input("Taxa de Anúncio (%):", min_value=0.0, max_value=100.0, value=2.0, step=0.1, key="anuncio_ml")
    
    # Chamando a função para Mercado Livre
    if st.button("Calcular Preço Mercado Livre"):
        preco_venda, comissao_valor, taxa_fixa, nota_fiscal_valor, embalagem, outras_taxas_valor, lucro, recebe = calcular_preco_venda(
            preco_custo_ml, comissao_ml, taxa_fixa_ml, nota_fiscal_ml, embalagem_ml, margem_lucro_ml, taxa_anuncio_ml
        )
        
        # Exibição dos resultados Mercado Livre
        st.subheader("Resultados Mercado Livre")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Preço de Venda", f"R$ {preco_venda:.2f}")
            st.metric(f"Comissão ({comissao_ml}%)", f"R$ {comissao_valor:.2f}")
            st.metric("Taxa Fixa", f"R$ {taxa_fixa:.2f}")
            st.metric("Embalagem", f"R$ {embalagem:.2f}")
        
        with col2:
            st.metric(f"Nota Fiscal ({nota_fiscal_ml}%)", f"R$ {nota_fiscal_valor:.2f}")
            st.metric(f"Taxa de Anúncio ({taxa_anuncio_ml}%)", f"R$ {outras_taxas_valor:.2f}")
            st.metric("Lucro Desejado", f"R$ {lucro:.2f}")
            st.metric("Valor Líquido Recebido", f"R$ {recebe:.2f}")
            st.info("O valor líquido é o que você recebe após descontar todas as taxas e custos.")

with tab3:
    st.header("Calculadora TikTok Shop")
    
    # Entradas do usuário para TikTok Shop
    preco_custo_tiktok = st.number_input("Preço de Custo (R$):", min_value=0.0, value=10.0, step=0.1, key="custo_tiktok")
    margem_lucro_tiktok = st.number_input("Margem de Lucro Desejada (%):", min_value=0.0, max_value=100.0, value=50.0, step=0.1, key="margem_tiktok")
    comissao_tiktok = st.number_input("Comissão do TikTok Shop (%):", min_value=0.0, max_value=100.0, value=8.0, step=0.1, key="comissao_tiktok")
    taxa_fixa_tiktok = st.number_input("Taxa Fixa (Frete) (R$):", min_value=0.0, value=3.5, step=0.1, key="taxa_tiktok")
    nota_fiscal_tiktok = st.number_input("Nota Fiscal (%):", min_value=0.0, max_value=100.0, value=5.0, step=0.1, key="nf_tiktok")
    embalagem_tiktok = st.number_input("Custo de Embalagem (R$):", min_value=0.0, value=1.0, step=0.1, key="embalagem_tiktok")
    taxa_promocao_tiktok = st.number_input("Taxa de Promoção (%):", min_value=0.0, max_value=100.0, value=3.0, step=0.1, key="promocao_tiktok")
    
    # Chamando a função para TikTok Shop
    if st.button("Calcular Preço TikTok Shop"):
        preco_venda, comissao_valor, taxa_fixa, nota_fiscal_valor, embalagem, outras_taxas_valor, lucro, recebe = calcular_preco_venda(
            preco_custo_tiktok, comissao_tiktok, taxa_fixa_tiktok, nota_fiscal_tiktok, embalagem_tiktok, margem_lucro_tiktok, taxa_promocao_tiktok
        )
        
        # Exibição dos resultados TikTok Shop
        st.subheader("Resultados TikTok Shop")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Preço de Venda", f"R$ {preco_venda:.2f}")
            st.metric(f"Comissão ({comissao_tiktok}%)", f"R$ {comissao_valor:.2f}")
            st.metric("Taxa Fixa", f"R$ {taxa_fixa:.2f}")
            st.metric("Embalagem", f"R$ {embalagem:.2f}")
        
        with col2:
            st.metric(f"Nota Fiscal ({nota_fiscal_tiktok}%)", f"R$ {nota_fiscal_valor:.2f}")
            st.metric(f"Taxa de Promoção ({taxa_promocao_tiktok}%)", f"R$ {outras_taxas_valor:.2f}")
            st.metric("Lucro Desejado", f"R$ {lucro:.2f}")
            st.metric("Valor Líquido Recebido", f"R$ {recebe:.2f}")
            st.info("O valor líquido é o que você recebe após descontar todas as taxas e custos.")

with tab4:
    st.header("Calculadora Kawaii")
    
    # Entradas do usuário para Kawaii
    preco_custo_kawaii = st.number_input("Preço de Custo (R$):", min_value=0.0, value=10.0, step=0.1, key="custo_kawaii")
    margem_lucro_kawaii = st.number_input("Margem de Lucro Desejada (%):", min_value=0.0, max_value=100.0, value=50.0, step=0.1, key="margem_kawaii")
    comissao_kawaii = st.number_input("Comissão da Kawaii (%):", min_value=0.0, max_value=100.0, value=15.0, step=0.1, key="comissao_kawaii")
    taxa_fixa_kawaii = st.number_input("Taxa Fixa (Frete) (R$):", min_value=0.0, value=3.0, step=0.1, key="taxa_kawaii")
    nota_fiscal_kawaii = st.number_input("Nota Fiscal (%):", min_value=0.0, max_value=100.0, value=5.0, step=0.1, key="nf_kawaii")
    embalagem_kawaii = st.number_input("Custo de Embalagem (R$):", min_value=0.0, value=0.8, step=0.1, key="embalagem_kawaii")
    taxa_plataforma_kawaii = st.number_input("Taxa da Plataforma (%):", min_value=0.0, max_value=100.0, value=2.5, step=0.1, key="plataforma_kawaii")
    
    # Chamando a função para Kawaii
    if st.button("Calcular Preço Kawaii"):
        preco_venda, comissao_valor, taxa_fixa, nota_fiscal_valor, embalagem, outras_taxas_valor, lucro, recebe = calcular_preco_venda(
            preco_custo_kawaii, comissao_kawaii, taxa_fixa_kawaii, nota_fiscal_kawaii, embalagem_kawaii, margem_lucro_kawaii, taxa_plataforma_kawaii
        )
        
        # Exibição dos resultados Kawaii
        st.subheader("Resultados Kawaii")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Preço de Venda", f"R$ {preco_venda:.2f}")
            st.metric(f"Comissão ({comissao_kawaii}%)", f"R$ {comissao_valor:.2f}")
            st.metric("Taxa Fixa", f"R$ {taxa_fixa:.2f}")
            st.metric("Embalagem", f"R$ {embalagem:.2f}")
        
        with col2:
            st.metric(f"Nota Fiscal ({nota_fiscal_kawaii}%)", f"R$ {nota_fiscal_valor:.2f}")
            st.metric(f"Taxa da Plataforma ({taxa_plataforma_kawaii}%)", f"R$ {outras_taxas_valor:.2f}")
            st.metric("Lucro Desejado", f"R$ {lucro:.2f}")
            st.metric("Valor Líquido Recebido", f"R$ {recebe:.2f}")
            st.info("O valor líquido é o que você recebe após descontar todas as taxas e custos.")

# Adicionar uma seção de comparação
st.header("Comparação entre Plataformas")
st.write("Compare os resultados entre todas as plataformas simultaneamente:")

with st.expander("Comparação Automática de Preços", expanded=True):
    # Campos unificados para a comparação
    st.subheader("Insira os dados para comparação")
    
    col1, col2 = st.columns(2)
    
    with col1:
        preco_custo_comp = st.number_input("Preço de Custo (R$):", min_value=0.0, value=10.0, step=0.1, key="custo_comp")
        margem_lucro_comp = st.number_input("Margem de Lucro Desejada (%):", min_value=0.0, max_value=100.0, value=50.0, step=0.1, key="margem_comp")
        embalagem_comp = st.number_input("Custo de Embalagem (R$):", min_value=0.0, value=1.0, step=0.1, key="embalagem_comp")
    
    with col2:
        nota_fiscal_comp = st.number_input("Nota Fiscal (%):", min_value=0.0, max_value=100.0, value=5.0, step=0.1, key="nf_comp")
        incluir_frete = st.checkbox("Incluir taxas de frete", value=True)
    
    # Taxas predefinidas para cada marketplace
    if incluir_frete:
        taxa_fixa_shopee_comp = 4.0
        taxa_fixa_ml_comp = 5.0
        taxa_fixa_tiktok_comp = 3.5
        taxa_fixa_kawaii_comp = 3.0
    else:
        taxa_fixa_shopee_comp = 0.0
        taxa_fixa_ml_comp = 0.0
        taxa_fixa_tiktok_comp = 0.0
        taxa_fixa_kawaii_comp = 0.0
    
    # Calcular para todas as plataformas quando o botão for pressionado
    if st.button("Calcular e Comparar Todas as Plataformas"):
        # Shopee
        preco_venda_shopee, comissao_valor_shopee, _, nota_fiscal_valor_shopee, _, _, lucro_shopee, recebe_shopee = calcular_preco_venda(
            preco_custo_comp, 20.0, taxa_fixa_shopee_comp, nota_fiscal_comp, embalagem_comp, margem_lucro_comp
        )
        
        # Mercado Livre
        preco_venda_ml, comissao_valor_ml, _, nota_fiscal_valor_ml, _, outras_taxas_valor_ml, lucro_ml, recebe_ml = calcular_preco_venda(
            preco_custo_comp, 17.0, taxa_fixa_ml_comp, nota_fiscal_comp, embalagem_comp, margem_lucro_comp, 2.0
        )
        
        # TikTok Shop
        preco_venda_tiktok, comissao_valor_tiktok, _, nota_fiscal_valor_tiktok, _, outras_taxas_valor_tiktok, lucro_tiktok, recebe_tiktok = calcular_preco_venda(
            preco_custo_comp, 8.0, taxa_fixa_tiktok_comp, nota_fiscal_comp, embalagem_comp, margem_lucro_comp, 3.0
        )
        
        # Kawaii
        preco_venda_kawaii, comissao_valor_kawaii, _, nota_fiscal_valor_kawaii, _, outras_taxas_valor_kawaii, lucro_kawaii, recebe_kawaii = calcular_preco_venda(
            preco_custo_comp, 15.0, taxa_fixa_kawaii_comp, nota_fiscal_comp, embalagem_comp, margem_lucro_comp, 2.5
        )
        
        # Criar dataframe para visualização
        import pandas as pd
        
        data = {
            'Plataforma': ['Shopee', 'Mercado Livre', 'TikTok Shop', 'Kawaii'],
            'Preço de Venda (R$)': [preco_venda_shopee, preco_venda_ml, preco_venda_tiktok, preco_venda_kawaii],
            'Comissão (R$)': [comissao_valor_shopee, comissao_valor_ml, comissao_valor_tiktok, comissao_valor_kawaii],
            'Nota Fiscal (R$)': [nota_fiscal_valor_shopee, nota_fiscal_valor_ml, nota_fiscal_valor_tiktok, nota_fiscal_valor_kawaii],
            'Taxas Adicionais (R$)': [0, outras_taxas_valor_ml, outras_taxas_valor_tiktok, outras_taxas_valor_kawaii],
            'Frete (R$)': [taxa_fixa_shopee_comp, taxa_fixa_ml_comp, taxa_fixa_tiktok_comp, taxa_fixa_kawaii_comp],
            'Embalagem (R$)': [embalagem_comp, embalagem_comp, embalagem_comp, embalagem_comp],
            'Lucro (R$)': [lucro_shopee, lucro_ml, lucro_tiktok, lucro_kawaii],
            'Valor Líquido (R$)': [recebe_shopee, recebe_ml, recebe_tiktok, recebe_kawaii]
        }
        
        df = pd.DataFrame(data)
        
        # Exibir tabela comparativa
        st.subheader("Tabela Comparativa")
        st.dataframe(df.style.format({
            'Preço de Venda (R$)': '{:.2f}',
            'Comissão (R$)': '{:.2f}',
            'Nota Fiscal (R$)': '{:.2f}',
            'Taxas Adicionais (R$)': '{:.2f}',
            'Frete (R$)': '{:.2f}',
            'Embalagem (R$)': '{:.2f}',
            'Lucro (R$)': '{:.2f}',
            'Valor Líquido (R$)': '{:.2f}'
        }))
        
        # Gráfico comparativo de preços de venda
        st.subheader("Comparação de Preços de Venda")
        chart_data = pd.DataFrame({
            'Plataforma': ['Shopee', 'Mercado Livre', 'TikTok Shop', 'Kawaii'],
            'Preço de Venda': [preco_venda_shopee, preco_venda_ml, preco_venda_tiktok, preco_venda_kawaii]
        })
        st.bar_chart(chart_data.set_index('Plataforma'))
        
        # Gráfico comparativo de lucro
        st.subheader("Comparação de Valor Líquido Recebido")
        chart_data = pd.DataFrame({
            'Plataforma': ['Shopee', 'Mercado Livre', 'TikTok Shop', 'Kawaii'],
            'Valor Líquido': [recebe_shopee, recebe_ml, recebe_tiktok, recebe_kawaii]
        })
        st.bar_chart(chart_data.set_index('Plataforma'))
        
        # Mostrar a plataforma mais vantajosa
        melhor_plataforma = df.loc[df['Valor Líquido (R$)'].idxmax()]['Plataforma']
        maior_valor_liquido = df['Valor Líquido (R$)'].max()
        
        st.success(f"A plataforma mais vantajosa para este produto é: **{melhor_plataforma}** com valor líquido de R$ {maior_valor_liquido:.2f}")
        
        # Resumo da rentabilidade
        st.subheader("Resumo da Rentabilidade")
        for index, row in df.iterrows():
            plataforma = row['Plataforma']
            percentual_lucro = (row['Valor Líquido (R$)'] / preco_custo_comp - 1) * 100
            st.write(f"**{plataforma}**: Rentabilidade de **{percentual_lucro:.2f}%** sobre o preço de custo")

# Adicionar informações úteis
st.sidebar.title("Informações Úteis")
st.sidebar.info("""
### Sobre as taxas:
- **Shopee**: Comissão entre 15-20% dependendo da categoria
- **Mercado Livre**: Comissão entre 12-22% dependendo da categoria, plus taxa de anúncio 
- **TikTok Shop**: Comissão entre 5-10% dependendo da categoria, plus taxas promocionais
- **Kawaii**: Comissão entre 13-18% dependendo da categoria
""")

st.sidebar.warning("""
### Dicas:
- Sempre verifique as taxas atuais das plataformas, pois elas podem mudar
- Considere os custos de logística ao definir seu preço
- Avalie o custo-benefício de cada plataforma para seu produto
""")