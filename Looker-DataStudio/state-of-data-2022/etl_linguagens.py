import pandas as pd

class ETLLinguagens:
    def __init__(self, url):
        self.url = url
        
    def extract(self):
        #Carrega os dados do arquivo CSV a partir da URL
        df = pd.read_csv(self.url, low_memory=False)
        return df
    
    def transform(self,df):
        #Seleciona as colunas relevantes para análise
        df = df.loc[:,["('P1_i_1 ', 'uf onde mora')",
                                     "('P2_f ', 'Cargo Atual')",
                                     "('P4_f ', 'Entre as linguagens listadas abaixo, qual é a sua preferida?')"]]
        
        #Renomeia as colunas para facilitar a manipulação
        df.columns = ['uf', 'cargo_atual', 'linguagem_preferida']
        
        #Substitui valores ausentes por 'Não informado'
        df = df.fillna('Não informado')
        
        #Modifica o padrão do tamanho de cada letra das linguagens preferidas
        df['linguagem_preferida'] = df['linguagem_preferida'].str.upper()
        
        # Adiciona o prefixo "BR-"
        df['uf'] = df['uf'].apply(lambda x: 'BR-' + x)
        
        return df
    
    def load(self, df_selected, file_path):
        # Salva o dataframe selecionado em um arquivo CSV
        df_selected.to_csv(file_path, index=False)
        print('Dados salvos em:', file_path)
        
        
#ETL LINGUAGENS

url = 'https://github.com/FranciscoFoz/data-viz-training/blob/main/Datasets/State_of_data_2022.csv?raw=true'
file_path = '/home/franciscofoz/Documents/GitHub/data-viz-training/Datasets/etl_linguagens.csv'

# Instancia a classe
etl = ETLLinguagens(url)

# Extract
df_extract = etl.extract()
# Transform
df_transform = etl.transform(df_extract)
# Load
etl.load(df_transform, file_path)


#ETL percentual por estado

# Ler os dados 
dados_linguagem = pd.read_csv('Datasets/etl_linguagens.csv')[['uf','linguagem_preferida']]

# Remover as entradas que não informam a linguagem preferida e as linhas com valores faltantes
dados_linguagem = dados_linguagem[dados_linguagem['linguagem_preferida'] != 'NÃO INFORMADO'].dropna()

# Calcular o percentual de uso de cada linguagem preferida em cada UF
percentual_estado = (pd.crosstab(dados_linguagem['linguagem_preferida'], dados_linguagem['uf'], normalize='columns') * 100).round(1).reset_index()

# Fazer um melt na tabela para facilitar visualização.
percentual_estado = percentual_estado.melt( id_vars=["linguagem_preferida"], var_name="uf", value_name="percentual")

# Mostrar o resultado final
percentual_estado.to_csv('/home/franciscofoz/Documents/GitHub/data-viz-training/Datasets/percentual_estado.csv',index=False)