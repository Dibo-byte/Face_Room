# Sistema de Controle de Presença com Reconhecimento Facial

📌 Visão Geral

Este projeto visa automatizar o controle de presença em salas de aula utilizando reconhecimento facial (OpenCV e Haar Cascade) e notificação via SMS (Twilio). O sistema identifica alunos por meio de uma câmera (Raspberry Pi), registra sua presença em um banco de dados (JSON) e envia notificações para professores ou responsáveis.
⚙️ Funcionalidades

✔ Detecção Facial em Tempo Real (OpenCV + Haar Cascade)
✔ Registro Automático de Presença (Armazenamento em JSON)
✔ Notificação via SMS (Twilio API)
✔ Interface Web Simples (HTML + Flask)

📂 Estrutura do Projeto

projeto_final/
│
├── 📁 dataset/                     # Fotos dos alunos para treinamento
│   ├── aluno1/                     # Pasta por aluno (ex: aluno1_1.jpg, aluno1_2.jpg)
│   └── aluno2/
│
├── 📜 coleta_rosto.py              # Captura rostos e armazena em dataset/
├── 📜 haarcascade_frontalface_default.xml  # Modelo Haar Cascade para detecção facial
├── 📜 labels.txt                   # Mapeamento ID-Nome dos alunos
├── 📜 modelo_lbph.yml              # Modelo treinado (LBPH)
├── 📜 presenca.html                # Relatório HTML de presenças
├── 📜 presenca.json                # Registro de presenças (JSON)
├── 📜 presenca_sala.py             # Script principal (detecta rostos e registra presença)
├── 📜 teste_janela.py              # Teste de exibição de janela de captura
├── 📜 teste_reconhecimento.py      # Teste de reconhecimento facial
└── 📜 treina_reconhecimento.py     # Treina o modelo LBPH com as imagens do dataset


⚙️ Funcionalidades

✔ Coleta de Rostos (coleta_rosto.py) → Captura imagens e armazena em dataset/.
✔ Treinamento do Modelo (treina_reconhecimento.py) → Gera modelo_lbph.yml e labels.txt.
✔ Reconhecimento em Tempo Real (presenca_sala.py) → Detecta alunos e registra em presenca.json.
✔ Relatório de Presença (presenca.html) → Exibe dados consolidados.


🔧 Pré-requisitos

    Hardware:

        Raspberry Pi + Câmera 5MP OV5647

    Software:

        Python 3.x

        OpenCV (pip install opencv-python opencv-contrib-python)

🚀 Como Usar?
1. Coletar Rostos (Cadastro de Alunos)

Execute e siga as instruções no terminal:
bash

python3 coleta_rosto.py

    As imagens serão salvas em dataset/nome_do_aluno/.

2. Treinar o Modelo
bash

python3 treina_reconhecimento.py

    Gera modelo_lbph.yml (modelo treinado) e labels.txt (IDs dos alunos).

3. Executar Sistema de Presença
bash

python3 presenca_sala.py

    O que acontece?

        Abre a câmera e detecta rostos.

        Se reconhecer um aluno, registra em presenca.json.

        Atualiza presenca.html com os dados mais recentes.

4. Visualizar Relatório

Abra presenca.html em um navegador:
bash

xdg-open presenca.html  # Linux

📝 Formatos dos Arquivos
labels.txt
plaintext

0:Joao
1:Maria

(Mapeia IDs do modelo para nomes reais.)
presenca.json
json

{
  "2024-06-15": {
    "Joao": ["10:00", "10:15"],
    "Maria": ["10:05"]
  }
}

🔍 Testes

    Testar reconhecimento:
    bash

python3 teste_reconhecimento.py

Testar janela de captura:
bash

python3 teste_janela.py
