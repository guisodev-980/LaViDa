from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QTextEdit
from PySide6.QtCore import Qt
from data.models import Const_Vars as Vars

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sobre")
        self.setMinimumSize(500, 400)

        layout = QVBoxLayout()

        self.text_box = QTextEdit()
        self.text_box.setReadOnly(True)
        self.text_box.setHtml(self.get_about_text())
        layout.addWidget(self.text_box)

        close_btn = QPushButton("Fechar")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn, alignment=Qt.AlignRight)

        self.setLayout(layout)

    def get_about_text(self):
        return f"""\

<b>Nome do Software: LaViDa - Análise de Vídeos e Dados Laboratoriais</b><br>
Versão: {Vars.VERSION}<br>
<br>
Autor: Guilherme S. Oliveira<br>
<br>
<b>Descrição:</b><br>
Este software realiza a leitura e análise de vídeos, extraindo informações como trajetórias e resultados analíticos, além de exportar imagens e tabelas.<br>
<br>
<b>Instruções:</b><br>
<br>

<b>1. Cadastro e manutenção de usuários:</b><br>
1.1 Na tela <b><i>Usuários</i></b>, clique em <b><i>Novo</i></b> e digite o e-mail do usuário a ser cadastrado. Após inserir um e-mail válido, serão liberados os demais campos para preenchimento, como cargo, telefone e nome completo. Caso deseje que o usuário tenha permissões de administrador, marque a caixa de seleção “Adm?” no canto superior do frame de cadastro. Você também poderá selecionar a foto ou avatar do usuário, tanto no cadastro quanto na edição, clicando na imagem à esquerda do frame.<br>
1.2 O usuário administrador possui permissão para remover ou editar qualquer outro usuário, bem como cadastrar novos.<br>
1.3 Os usuários cadastrados definirão sua senha na primeira tentativa de login.<br>
1.4 Para editar um usuário diferente de si mesmo, é necessário possuir permissão de administrador. Na edição, é possível alterar os dados do usuário ou resetar sua senha, o que o obrigará a cadastrar uma nova senha ao tentar fazer login novamente.<br>
1.5 Para editar outro usuário, após clicar em <b><i>Editar</i></b>, digite o e-mail do usuário desejado. Caso o usuário seja encontrado, todos os demais campos e a foto serão preenchidos automaticamente com os dados correspondentes.<br>
1.6 Excluir a si mesmo ou resetar a própria senha provocará logout imediato, forçando nova autenticação ou removendo o acesso.<br>
1.7 Para resetar a senha de um usuário, clique em <b><i>Editar</i></b>, digite o e-mail do usuário e clique em <b><i>Limpar Senha</i></b>. É necessário ter permissão de administrador.<br>
1.8 Para realizar logout, clique no ícone (avatar) do usuário localizado no canto superior do cabeçalho e selecione a opção <b><i>Logout</i></b>.<br>
<br>

<b>2. Cadastro e preparação dos vídeos:</b><br>
2.1 Coloque os vídeos que serão analisados na pasta <b><i>LV_Videos</i></b>, localizada na pasta de instalação do software.<br>
2.2 Ao abrir o software, ele fará a leitura dos vídeos nessa pasta e salvará os dados necessários para o cadastro.<br>
2.3 Após o login, clique em <b><i>Leitor</i></b> e depois em <b><i>Cadastrar Vídeos</i></b>. Será exibida uma tabela com todos os vídeos encontrados. Selecione um vídeo, insira as informações pertinentes (Sujeito, Grupo, Tipo de Teste, etc.) e clique em <b><i>Salvar</i></b>.<br>
2.4 Na tela <b><i>Leitor</i></b>, clique no botão <b><i>Máscara</i></b> para criar a máscara do campo de leitura. Siga as instruções na tela para clicar no centro e na borda do tanque. A máscara será ajustada automaticamente e salva junto aos dados do vídeo. Caso o resultado não seja satisfatório, repita o processo.<br>
2.5 Na tela <b><i>Leitor</i></b>, é possível copiar máscaras da seguinte forma:<br>
<i><b>1.</b></i> Selecione na tabela o vídeo de origem.<br>
<i><b>2.</b></i> Clique no botão <b><i>Copiar máscara</i></b>.<br>
<i><b>3.</b></i> Selecione o(s) vídeo(s) de destino.<br>
<i><b>4.</b></i> Clique em <b>Colar máscara</b>.<br>
2.6 As análises podem ser realizadas manualmente ou em lote, selecionando um ou diversos vídeos ao mesmo tempo.<br>
2.7 <i><b>Importante:</b></i> Executar a análise de um vídeo que já possui resultados sobrescreverá todos os resultados previamente existentes.<br>
2.8 O botão <b><i>Descartar</i></b> apagará todos os dados de análise do(s) vídeo(s) selecionado(s). Os dados cadastrados manualmente e a máscara permanecerão intactos.<br>
<br>

<b>3. Análise dos vídeos:</b><br>
3.1 As análises podem ser feitas individualmente ou em lote.<br>
3.2 Para leitura manual, acesse a tela <b><i>Leitor</i></b>, selecione um ou mais vídeos já cadastrados e com máscara e clique em <b><i>Analisar</i></b>. O processo será feito em tempo real (frame a frame), e os resultados aparecerão na tabela analítica inferior. Após gerados, os resultados poderão ser consultados sem necessidade de nova análise.<br>
3.3 Para análise em lote ou agendada, acesse a tela <b><i>Agendamento</i></b>. Nela há duas tabelas: à esquerda, os vídeos disponíveis (já cadastrados e com máscara); à direita, os vídeos selecionados para análise em lote.<br>
3.4 Para agendar análises, clique em <b><i>Editar</i></b> no canto superior esquerdo do frame, defina o horário (horas e minutos) e, se desejar, marque a opção para desligar o computador automaticamente após a finalização das tarefas (somente Windows). Clique novamente em <b><i>Salvar</i></b> para confirmar.<br>
3.5 Utilize os botões entre as tabelas para mover os vídeos desejados para a tabela da direita. Clique em <b><i>Salvar</i></b> no frame inferior para confirmar as tarefas.<br>
3.6 É possível reanalisar vídeos, lembrando que os <b>RESULTADOS SERÃO SUBSTITUÍDOS</b>. Para ocultar vídeos já analisados, marque a caixa <b><i>Pendentes</i></b>.<br>
3.7 Os botões no frame inferior executam as seguintes funções:<br>
a) <b>Salvar:</b> confirma todas as alterações feitas. Sem clicar neste botão, as modificações serão descartadas ao fechar a janela.<br>
b) <b>Cancelar/Sair:</b> descarta alterações feitas desde o último salvamento e/ou fecha a tela de Agendamentos.<br>
c) <b>Limpar:</b> remove todas as configurações de agendamento e limpa a lista de vídeos.<br>
<br>

<b>4. Análise comparativa:</b><br>
4.1 A tela de análise permite comparações, cálculos de média, mínima e máxima por grupo, além da exportação dos resultados em PDF.<br>
4.2 No canto superior do frame da tabela de vídeos analisados há um botão para alternar entre os testes de nado e probatórios, filtrando os grupos de vídeos disponíveis.<br>
4.3 Para realizar a análise comparativa, selecione os vídeos desejados. Na tabela inferior aparecerão os resultados obtidos, bem como suas médias, mínimas e máximas. O gráfico será atualizado automaticamente com esses valores.<br>
4.4 Para exportar as análises, selecione o grupo desejado e clique em <b><i>Exportar</i></b>. Será gerado um arquivo PDF com todos os dados e cálculos (média, mínima, máxima e margens de erro), além das informações do usuário que realizou a análise e demais anotações necessárias para documentação.<br>
<br>

<i><b>Importante:</b></i> Não foram encontrados valores diferenciados em análises repetidas do mesmo vídeo, sendo observados resultados idênticos com precisão superior a cinco casas decimais.<br>
A qualidade da produção das <b><i>máscaras</i></b> pode produzir diferenças substanciais, principalmente nos valores referentes ao comportamento <i>"Wall Hugging"</i>.<br>
<br>

<b>Licença:</b><br>
Este software é de uso pessoal e não possui distribuição comercial.<br>
<br>
<b>(c) 2025 - LaViDa - {Vars.VERSION}</b><br>
<b>Desenvolvido por: Guilherme S. Oliveira</b><br>
<b>Contato: </b> guisomtc@gmail.com<br>

"""