# 🎖️ Marechal Deodoro da Fonseca — Chat Histórico

Uma aplicação interativa desenvolvida para estudantes que desejam aprender sobre
o fim do Segundo Reinado e a Proclamação da República do Brasil de forma dinâmica
— conversando diretamente com um dos protagonistas da época.

🌐 **Acesse:** [marechaldeodoro.streamlit.app](https://marechaldeodoro.streamlit.app)

## 💡 Motivação

O conteúdo ensinado nas escolas sobre o Segundo Reinado e a Proclamação da
República muitas vezes não consegue transmitir a complexidade humana e política
dos eventos. Quais eram as tensões reais entre o Exército e a Coroa? O que levou
Deodoro a agir no dia 15 de novembro de 1889? Como ele via Dom Pedro II como
pessoa, e não apenas como imperador?

Esta aplicação permite explorar essas perguntas em conversa direta com o próprio
Marechal Deodoro da Fonseca — reconstruído com base na historiografia brasileira
consolidada, de José Murilo de Carvalho a Lilia Schwarcz.

## 🗺️ O que você pode perguntar

- A Guerra do Paraguai e seus impactos no Exército brasileiro
- As tensões entre militares e o governo imperial (a chamada Questão Militar)
- Os bastidores da Proclamação da República em 15 de novembro de 1889
- A relação pessoal de Deodoro com Dom Pedro II
- Seu governo provisório e constitucional (1889–1891)
- O fechamento do Congresso e a renúncia
- O início do governo de Floriano Peixoto
- O que se falava sobre a transição para o primeiro governo civil, de Prudente de Morais

## ⚠️ Limites do personagem

O Marechal Deodoro faleceu em 23 de agosto de 1892. Sobre eventos posteriores
a essa data — como a Revolta da Armada, a Guerra de Canudos e a presidência de
Prudente de Morais — ele só pode falar com base no que "chegou aos seus ouvidos"
nos meses finais de vida. Esse limite é intencional e faz parte da proposta
histórica da aplicação.

## 📚 Aviso educacional

Esta aplicação foi desenvolvida **exclusivamente para fins educacionais**, como
um ponto de partida para o estudo do Segundo Reinado e da Proclamação da
República.

**O personagem é gerado por inteligência artificial e está sujeito a erros.**
Modelos de linguagem podem cometer imprecisões históricas, confundir datas,
atribuir falas incorretamente ou apresentar interpretações parciais — mesmo
quando instruídos a seguir fontes confiáveis. Por isso:

- Trate as respostas como um ponto de partida, não como fonte definitiva
- Verifique informações importantes em livros didáticos e fontes acadêmicas
- Em caso de dúvida, consulte obras de historiadores como José Murilo de
  Carvalho, Boris Fausto e Lilia Schwarcz

A inteligência artificial não substitui o estudo — ela pode torná-lo mais
curioso e envolvente.

## 🛠️ Tecnologias utilizadas

- [Streamlit](https://streamlit.io/) — interface do chat
- [Groq API](https://console.groq.com/) — inferência do modelo de linguagem
- [Llama 3.3 70B](https://groq.com/) — modelo de linguagem utilizado
- Python 3.11+

## 🚀 Como rodar localmente

**1. Clone o repositório**
```bash
git clone https://github.com/felipe-roch/Marechal_Deodoro.git
cd Marechal_Deodoro
```

**2. Instale as dependências**
```bash
pip install -r requirements.txt
```

**3. Configure sua chave da Groq**

Crie o arquivo `.streamlit/secrets.toml` na raiz do projeto:
```toml
GROQ_API_KEY = "sua_chave_aqui"
```

**4. Rode a aplicação**
```bash
streamlit run Chat_Marechal.py
```

## 🔑 Deploy no Streamlit Cloud

Na tela de configuração do app, acesse **Advanced settings → Secrets** e adicione:
```toml
GROQ_API_KEY = "sua_chave_aqui"
```

## Autor

Felipe da Rocha
[Linkedin](https://www.linkedin.com/in/felipedarochaferreira/) · [GitHub](http://github.com/felipe-roch)