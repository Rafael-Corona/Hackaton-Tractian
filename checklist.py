from openai import OpenAI
import openai
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def generate_checklist(transcribed_text):
    # Define the prompt in Portuguese to ask for a checklist based on the transcribed text
    prompt = f"""
    A partir do texto a seguir, gere uma lista de verificação para o técnico de manutenção com as ações necessárias:
    
    Texto transcrito:
    {transcribed_text}
    
    Por favor, organize as ações em uma checklist com pontos claros e específicos. Gere o texto em markdown.
    
    Além disso, gere uma checklist com os equipamentos necessarios para cada etapa.
    Use a seguinte lista de equipamentos com os seus respectivos codigos
    ```markdown
    | Categoria                  | Descrição do Material/Equipamento                  | Código SAP |
|----------------------------|---------------------------------------------------|------------|
| **Ferramentas de Corte**   | Serra Circular                                    | MAT001     |
|                            | Disco de Corte                                    | MAT002     |
|                            | Serra de Fita                                      | MAT003     |
|                            | Disco de Desbaste                                  | MAT004     |
|                            | Broca de Aço Rápido 10mm                           | MAT005     |
|                            | Conjunto de Fresas para Usinagem                   | MAT006     |
|                            | Lâmina de Serra Sabre                              | MAT007     |
|                            | Lixadeira Angular                                  | EQP001     |
| **Ferramentas de Medição** | Paquímetro Digital                                | MAT101     |
|                            | Micrômetro                                        | MAT102     |
|                            | Relógio Comparador                                | MAT103     |
|                            | Trena de Aço 5m                                   | MAT104     |
|                            | Nível de Bolha                                    | MAT105     |
|                            | Goniômetro Digital                                | MAT106     |
|                            | Manômetro para Pressão                            | MAT107     |
|                            | Calibrador de Roscas                              | MAT108     |
| **Equipamentos de Solda**  | Máquina de Solda MIG                              | EQP201     |
|                            | Eletrodo de Solda Inox                            | MAT201     |
|                            | Máscara de Solda Automática                       | MAT202     |
|                            | Maçarico de Corte Oxiacetilênico                  | EQP202     |
|                            | Tocha de Solda TIG                                | MAT203     |
|                            | Fio de Solda MIG ER70S-6                          | MAT204     |
|                            | Regulador de Pressão para Gás                     | MAT205     |
|                            | Tubo de Gás Acetileno                             | MAT206     |
| **Lubrificação e Manutenção** | Graxa Industrial                          | MAT301     |
|                            | Óleo Lubrificante 10W30                           | MAT302     |
|                            | Bomba de Graxa Pneumática                         | EQP301     |
|                            | Limpa Contatos Elétricos                          | MAT303     |
|                            | Spray Desengripante                               | MAT304     |
|                            | Veda Rosca em Fita                                | MAT305     |
| **Equipamentos de Segurança** | Capacete de Segurança com Aba                 | MAT401     |
|                            | Luvas Térmicas de Alta Resistência                | MAT402     |
|                            | Óculos de Proteção Antirrespingos                 | MAT403     |
|                            | Protetor Auricular Tipo Plug                      | MAT404     |
|                            | Máscara Respiratória com Filtro P3                | MAT405     |
|                            | Cinto de Segurança para Trabalho em Altura        | MAT406     |
|                            | Sapato de Segurança com Biqueira de Aço           | MAT407     |
|                            | Protetor Facial de Policarbonato                  | MAT408     |
| **Equipamentos de Elevação** | Talha Elétrica de Corrente                    | EQP501     |
|                            | Corrente de Elevação de 10m                       | MAT501     |
|                            | Gancho Giratório com Trava de Segurança           | MAT502     |
|                            | Cinta de Elevação com Olhal                       | MAT503     |
|                            | Carrinho de Transporte de Bobinas                 | EQP502     |
|                            | Macaco Hidráulico 10 Toneladas                    | EQP503     |
| **Componentes Mecânicos**  | Rolamento Esférico de Precisão                    | MAT601     |
|                            | Parafuso de Alta Resistência M12                  | MAT602     |
|                            | Correia de Transmissão Industrial                 | MAT603     |
|                            | Junta de Vedação em Borracha                      | MAT604     |
|                            | Engrenagem Cilíndrica de Aço                      | MAT605     |
|                            | Bucha de Bronze Autolubrificante                  | MAT606     |
|                            | Eixo de Transmissão                               | MAT607     |
|                            | Polia de Alumínio                                 | MAT608     |
| **Equipamentos Hidráulicos** | Válvula Solenoide Hidráulica                  | EQP601     |
|                            | Bomba Hidráulica de Pistão                        | EQP602     |
|                            | Mangueira Hidráulica de Alta Pressão              | MAT701     |
|                            | Conector Hidráulico Rápido                        | MAT702     |
| **Equipamentos Elétricos** | Motor Elétrico Trifásico 5HP                      | EQP701     |
|                            | Cabo Elétrico 10mm²                               | MAT801     |
|                            | Disjuntor de 100A                                 | MAT802     |
|                            | Quadro de Comando Elétrico com Inversor de Frequência | EQP702 |
|                            | Chave Seccionadora                                | MAT803     |
|                            | Fusível NH 100A                                   | MAT804     |
|                            | Tomada Industrial 380V                            | MAT805     |
| **Ferramentas Manuais**    | Chave de Fenda Phillips 6mm                      | MAT901     |
|                            | Alicate de Corte                                 | MAT902     |
|                            | Martelo de Borracha                              | MAT903     |
|                            | Torquímetro 40-200Nm                             | MAT904     |
|                            | Conjunto de Chaves Allen                         | MAT905     |
|                            | Chave Estrela 12mm                               | MAT906     |
|                            | Serra Manual                                     | MAT907     |
    ```
    """

    # Call ChatGPT to generate the checklist
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "system", "content": "Você é um assistente que ajuda a criar listas de verificação para manutenção com base em textos transcritos."},
                  {"role": "user", "content": prompt}],
    )
    
    # Extract and return the checklist text
    checklist = completion.choices[0].message.content
    return checklist