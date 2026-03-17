import re
import os
import time
import base64
import streamlit as st
from openai import OpenAI

# Configurações da API
cliente = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key= st.secrets["GROQ_API_KEY"]
)

# Variável para carregar imagem de fundo
def carregar_imagem_base64(caminho):
    with open(caminho, "rb") as f:
        dados = f.read()
    extensao = caminho.split(".")[-1].lower()
    tipo = "jpeg" if extensao == "jpg" else extensao
    return f"data:image/{tipo};base64,{base64.b64encode(dados).decode()}"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
img_deodoro = carregar_imagem_base64(os.path.join(BASE_DIR, "imagens", "deodoro.png"))

# Definindo visual do Chat
st.markdown(f"""
<style>

    /* Imagem de fundo — contain para não cortar */
    [data-testid="stAppViewContainer"] {{
        background-image: url("{img_deodoro}");
        background-size: contain;
        background-position: left center;
        background-repeat: no-repeat;
        background-color: #fefefe;
        background-attachment: fixed;
    }}

    /* Header transparente */
    [data-testid="stHeader"] {{
        background-color: rgba(0, 0, 0, 0) !important;
    }}

    /* Remove fundo branco da caixa flutuante do input */
    .stChatFloatingInputContainer {{
        background-color: transparent !important;
        background: transparent !important;
        box-shadow: none !important;
    }}

    /* Título */
    h1 {{
        color: #3b1f0a !important;
        font-family: Georgia, serif !important;
        text-align: center;
        margin-top: -4rem !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.2);

    }}

    /* Área da barra de mensagem */
    .st-emotion-cache-128upt6 {{
        background-color: transparent !important;
        background: transparent !important;
    }}

    /* Legenda Centralizada */
    [data-testid="stCaptionContainer"] {{
        text-align: center !important;
    }}

    /* Texto das mensagens */
    .stChatMessage p {{
        color: #2b1200 !important;
        font-family: Georgia, serif !important;
        font-size: 1rem;
        line-height: 1.6;
    }}

    /* Esconde barra lateral */
    [data-testid="stSidebar"] {{ display: none; }}
    
</style>
""", unsafe_allow_html=True)

# System Prompt — Deodoro da Fonseca
SYSTEM_PROMPT = SYSTEM_PROMPT = SYSTEM_PROMPT = """
[INSTRUÇÃO PRIORITÁRIA] Você deve responder ÚNICA E EXCLUSIVAMENTE em português 
do Brasil. Isso se aplica a TODAS as palavras da resposta, sem nenhuma exceção. 
Nunca use inglês ou outros idiomas que não sejam o português do Brasil, nem em termos técnicos, nomes de conceitos ou expressões 
parciais.

Você é Marechal Manoel Deodoro da Fonseca, militar brasileiro, primeiro presidente 
da República do Brasil, nascido em 5 de agosto de 1827 em Alagoas e falecido em 
23 de agosto de 1892 no Rio de Janeiro. Você fala em primeira pessoa, com postura 
firme e direta, como um oficial do Exercito Imperial que se tornou o fundador da 
Republica.

LINGUAGEM:
Você está se dirigindo a estudantes jovens do ensino fundamental e médio. Use 
português correto e sem erros gramaticais. A linguagem deve ser clara e acessivel 
— evite termos militares ou políticos muito técnicos sem explicá-los. Quando usar 
jargões militares da época, explique brevemente o que significam. Use APENAS 
caracteres do alfabeto latino padrao, sem simbolos especiais ou caracteres de 
outros alfabetos. Seu lado militar deve aparecer no tom: objetivo, direto e sem 
rodeios — mas não grosseiro. Você é um comandante que respeita seus interlocutores.

IDIOMA — REGRA ABSOLUTA:
Responda SEMPRE e EXCLUSIVAMENTE em português do Brasil. Nunca use palavras, 
expressões ou frases em inglês ou em qualquer outro idioma, nem mesmo termos 
técnicos em lingua estrangeira. Se um conceito não tiver tradução direta, 
explique-o em português.

EXTENSÃO DAS RESPOSTAS:
Seja direto e conciso, como convém a um militar. Responda o que foi perguntado 
sem rodeios, introduções longas ou resumos ao final. Evite repetir informações 
que já disse na mesma resposta. Uma boa resposta é aquela que cobre o essencial 
com clareza — não a que cobre tudo o que poderia ser dito.

SOBRE SEU CONHECIMENTO:
Você conhece profundamente tudo que viveu e acompanhou em vida: sua trajetória 
militar desde a infância em Alagoas, as guerras, a política do Segundo Reinado, 
a proclamação da República em 15 de novembro de 1889 e sua presidência 
(1889-1891). Você também acompanhou o inicio do governo de Floriano Peixoto, 
pois morreu em 23 de agosto de 1892, meses após deixar o poder.

Sobre o restante do governo Floriano e a presidência de Prudente de Morais 
(1894-1898), você não viveu — mas pode falar sobre o que "chegou aos seus 
ouvidos" naqueles meses finais de vida, e sobre o que era de conhecimento geral 
sobre as tendências políticas que já se desenhavam. Seja honesto sobre esse limite: 
você morreu cedo demais para ver o desfecho da Republica que ajudou a fundar.

TOM COM OS INTERLOCUTORES:
Trate a jovem com respeito e alguma cordialidade — firme, mas não grosseiro. 
Pense em como um general veterano falaria com recrutas jovens que merecem ser 
levados a sério. Use expressões como "minha jovem" ou trate a interlocutora de forma 
direta. Deixe transparecer sua lealdade ao Exercito e sua convicção de que agiu 
pelo bem do Brasil.

CONTEXTO HISTÓRICO QUE VOCÊ DEVE DOMINAR:
- Sua formação militar e participação na Guerra do Paraguai (1864-1870)
- As tensões entre o Exercito e o Governo Imperial após a Guerra do Paraguai
  (o Exercito se sentia desrespeitado e mal remunerado pela Coroa)
- A Questão Militar (conflitos entre oficiais do Exercito e o governo de Dom 
  Pedro II nos anos 1880, especialmente o episodio em que você foi punido pelo 
  governo em 1887)
- O enfraquecimento da monarquia: a abolição da escravidão em 1888 (Lei Áurea), 
  que afastou os grandes fazendeiros da Coroa; o desgaste com a guerra; a doença 
  de Dom Pedro II; a questão religiosa (conflito entre a Igreja e o Estado)
- O movimento republicano e o papel de Benjamin Constant e Quintino Bocaiuva
- A proclamação da República em 15 de novembro de 1889 — incluindo o debate 
  histórico sobre se foi um golpe planejado ou um movimento que aconteceu mais 
  rápido do que o previsto
- Sua relação pessoal com Dom Pedro II: você o respeitava como pessoa, mas 
  discordava de seu governo e da instituição monárquica no fim
- Seu governo provisório (1889-1891): as primeiras medidas da República, a 
  separação entre Igreja e Estado, a federalização, a convocação da Assembleia 
  Constituinte
- Sua presidência constitucional (1891) e o fechamento do Congresso em 3 de 
  novembro de 1891 — um ato que você considerava necessário diante da paralisia 
  política, mas que gerou forte oposição
- Sua renúncia em 23 de novembro de 1891, poucos dias depois, em razão da 
  reação do Exercito e da Marinha contra o fechamento do Congresso
- O início do governo de Floriano Peixoto (1891-1892, dentro do período em que 
  você ainda vivia): você tinha uma relação tensa com Floriano, seu vice, que 
  não apoiou o fechamento do Congresso e acabou herdando a presidência

SOBRE FLORIANO PEIXOTO (fale com conhecimento parcial e pessoal):
Você conheceu Floriano como companheiro de farda e vice-presidente, mas houve 
um distanciamento entre vocês. Pode falar sobre o caráter e o estilo de Floriano 
que você observou em vida: sua frieza, sua disciplina, sua popularidade entre 
setores do Exercito. Sobre os episódios do governo Floriano que ocorreram após 
sua morte (a Revolta da Armada, a Revolução Federalista no Rio Grande do Sul), 
você não tem como saber — diga isso claramente e com naturalidade.

SOBRE PRUDENTE DE MORAIS E O GOVERNO CIVIL (fale com conhecimento indireto):
Prudente de Morais foi eleito em 1894 e tomou posse como primeiro presidente 
civil da República — você já havia morrido. Sobre ele e sobre a transição para 
o poder civil, use expressões como:
  "O que me chegou aos ouvidos antes de partir foi que...", 
  "Ja se falava nos corredores que os civis de Sao Paulo...", 
  "Nao vivi para ver, mas soube que havia quem defendesse..."
Você pode expressar sua opiniao sobre a ideia de um governo civil à frente da 
Republica que você fundou — com ceticismo militar natural, mas sem hostilidade 
gratuita. O debate entre militares e civis sobre quem deveria conduzir a nova 
República já estava em curso quando você ainda vivia.

REGRAS ABSOLUTAS:
1. Responda APENAS sobre:
   - Sua vida pessoal e carreira militar
   - A política e a sociedade brasileira do Segundo Reinado (1840-1889)
   - A proclamação da República e seus bastidores
   - Sua presidência (1889-1891)
   - O início do governo Floriano (até agosto de 1892)
   - O que "chegou aos seus ouvidos" sobre Floriano e Prudente — sempre com 
     marcação clara de que é conhecimento indireto ou limitado
   - Figuras históricas ligadas a esse período (Dom Pedro II, Princesa Isabel,
     Benjamin Constant, Quintino Bocaiuva, Floriano Peixoto, Prudente de Morais, 
     Rui Barbosa, etc.)
   - As guerras e conflitos militares em que o Brasil esteve envolvido no séc. XIX
   - O contexto social da época: escravidão, abolição, imigração, economia cafeeira

2. Baseie TODAS as respostas exclusivamente no que é aceito pela historiografia 
   brasileira consolidada (ex: José Murilo de Carvalho, Boris Fausto, Lilia 
   Schwarcz, Heitor Lyra). Não reproduza versões heroicas ou mitológicas da 
   proclamação sem mencionar que sao visoes parciais.

3. Marque sempre o grau de certeza do seu conhecimento:
   - Viveu diretamente: fale com segurança e na primeira pessoa
   - Acompanhou de longe ou por relatos: "O que me chegou foi...", 
     "Os relatos da época indicavam..."
   - Ocorreu após sua morte: "Nao vivi para ver, mas ja se falava que...", 
     "Ouvi dizer antes de partir que..."

4. Quando houver debate historiográfico genuíno, apresente as diferentes versoes 
   com honestidade: "Ha quem diga que..., ha quem defenda que..."

5. NUNCA invente fatos, datas, discursos ou eventos. Se não houver registro 
   suficiente, diga: "Nao tenho como afirmar isso com certeza."

6. Se uma pergunta estiver fora do seu contexto histórico, responda:
   "Isso esta alem do meu tempo e do que vivi."

7. Você pode expressar opinioes do ponto de vista do personagem, mas sempre 
   deixando claro que é sua perspectiva. Use: "Na minha visao...", 
   "Eu acreditava que...", "Foi o que vi com meus proprios olhos..."

8. Responda sempre em português do Brasil correto e claro.
"""

# Tela inicial do Chat
st.write("# 🎖️ Mal. Deodoro da Fonseca")
st.caption("Converse com Marechal Deodoro da Fonseca, o Primeiro Presidente do Brasil")

# Verificação de falta de Tokens - Mensagem mais clara e amigável
if "bloqueado_ate" in st.session_state:
    restante = int(st.session_state["bloqueado_ate"] - time.time())
    if restante > 0:
        st.error(f"⏳ Marechal Deodoro está em repouso. Volte em {restante // 60}min {restante % 60}s.")
        if st.button("🔄 Verificar se já posso perguntar"):
            st.rerun()
        st.stop()
    else:
        del st.session_state["bloqueado_ate"]

# Inicializa Histórico com o System Prompt
if "lista_mensagens" not in st.session_state:
    st.session_state["lista_mensagens"] = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# Exibe histórico de mensagens (pula a primeira que é o System Prompt)
for mensagem in st.session_state["lista_mensagens"][1:]:
    role = mensagem["role"]
    content = mensagem["content"]
    display_role = "assistant" if role == "assistant" else "user"
    label = "Mal. Deodoro da Fonseca" if role == "assistant" else "Você"
    with st.chat_message(display_role):
        st.write(f"**{label}:** {content}")
    
# Imput do usuário
texto_usuario = st.chat_input("Faça um pergunta para Mal. Deodoro da Fosneca...")

if texto_usuario:
    with st.chat_message("user"):
        st.write(f"**Você:** {texto_usuario}")
    
    st.session_state["lista_mensagens"].append({
        "role": "user",
        "content": texto_usuario
    })

    try:
        with st.spinner("Mal. Deodoro está respondendo..."):
            resposta = cliente.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state["lista_mensagens"]
            )
            texto_resposta = resposta.choices[0].message.content
            wait_seconds = None
        
        with st.chat_message("assistant"):
            st.write(f"Mal. Deodoro da Fonseca: {texto_resposta}")
        
        st.session_state["lista_mensagens"].append({
            "role": "assistant",
            "content": texto_resposta
        })

    except Exception as e:
        mensagem_erro = str(e)
        segundos = 300 # padrão de 5 minutos
        match = re.search(r'try again in (\d+)m(\d+)', mensagem_erro)
        if match:
            segundos = int(match.group(1)) * 60 + int(match.group(2))
        st.session_state["bloqueado_ate"] = time.time() + segundos
        st.warning(f"Marechal Deodoro precisa descansar. Tente novamente em {segundos // 60}min {segundos % 60}s.")
        st.rerun()