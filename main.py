import flet as ft
import time
import threading

def main(page: ft.Page):
    page.title = "ProtegeAí"
    page.window_width = 400
    page.window_height = 700
    page.theme = ft.Theme(
        page_transitions=ft.PageTransitionsTheme(windows=ft.PageTransitionTheme.FADE_UPWARDS),
        color_scheme_seed="blue"
    )

    IMG_FUNDO = "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=400&auto=format&fit=crop"

    estado_jogo = {
        "hp": 100,
        "modulos_liberados": 1,
        "usuario": ""
    }

    # --- BANCO DE DADOS: 4 MÓDULOS COM 3 FASES ---
    modulos = [
        {
            "id": 1, "nome": "Módulo 1: Phishing", "icone": ft.icons.PHISHING,
            "teoria_titulo": "A Engenharia Social",
            "teoria_desc": "O Phishing usa gatilhos mentais (urgência, medo, curiosidade) para enganar você. Golpes começam genéricos e ficam mais sofisticados, mirando até sua profissão.",
            "desafios": [
                {
                    "contexto": "FASE 1 (FÁCIL): Você recebe um SMS genérico.",
                    "msg": "'BANCO: Conta bloqueada. Acesse: http://banco-alerta.com'",
                    "opcoes": [
                        {"texto": "Clico para checar a tela.", "dano": 30},
                        {"texto": "Respondo o SMS com dúvidas.", "dano": 15},
                        {"texto": "Ignoro e abro o app oficial.", "dano": 0, "certo": True},
                        {"texto": "Ligo de volta para o número.", "dano": 15}
                    ],
                    "msg_acerto": "Perfeito! Bancos não mandam links encurtados por SMS.",
                    "msg_erro": "Erro! Clicar ou interagir valida seu número para os criminosos."
                },
                {
                    "contexto": "FASE 2 (MÉDIO): E-mail com visual da Netflix.",
                    "msg": "'Seu pagamento falhou. Atualize seu cartão em 24h.'",
                    "opcoes": [
                        {"texto": "Clico no link do e-mail para atualizar.", "dano": 30},
                        {"texto": "Abro o site oficial no navegador para checar.", "dano": 0, "certo": True},
                        {"texto": "Baixo o anexo 'fatura.pdf' para ler.", "dano": 50},
                        {"texto": "Clico em 'Cancelar Assinatura' no e-mail.", "dano": 30}
                    ],
                    "msg_acerto": "Excelente! O e-mail era falso. Sempre acesse pelo navegador.",
                    "msg_erro": "Erro! E-mails falsos copiam o design oficial. Nunca clique neles."
                },
                {
                    "contexto": "FASE 3 (DIFÍCIL): Mensagem de recrutador no LinkedIn.",
                    "msg": "'Adorei seu perfil! Baixe os detalhes da vaga (10k) no arquivo VAGA.ZIP'",
                    "opcoes": [
                        {"texto": "Baixo e extraio o ZIP na hora.", "dano": 50},
                        {"texto": "Peço para mandar o formato em PDF.", "dano": 15},
                        {"texto": "Ignoro, vagas não vêm em ZIP.", "dano": 0, "certo": True},
                        {"texto": "Abro o arquivo pelo celular para segurança.", "dano": 30}
                    ],
                    "msg_acerto": "Defesa Impecável! Arquivos ZIP em chats costumam ser malwares.",
                    "msg_erro": "Sistema Comprometido! O arquivo instalou um Cavalo de Tróia."
                }
            ]
        },
        {
            "id": 2, "nome": "Módulo 2: Senhas", "icone": ft.icons.PASSWORD,
            "teoria_titulo": "O Mito da Senha Forte",
            "teoria_desc": "Hackers usam máquinas que testam bilhões de senhas por segundo. O tamanho da senha importa muito mais do que usar caracteres especiais no lugar das letras.",
            "desafios": [
                {
                    "contexto": "FASE 1 (FÁCIL): Criando senha do e-mail.",
                    "msg": "Selecione a senha mais resistente contra ataques:",
                    "opcoes": [
                        {"texto": "Mudar@123", "dano": 30},
                        {"texto": "data_nasc_nome", "dano": 50},
                        {"texto": "O_Gato_Azul_Bebe_Cafe!", "dano": 0, "certo": True},
                        {"texto": "P@ssw0rd!", "dano": 30}
                    ],
                    "msg_acerto": "Correto! Frases longas são matematicamente imbatíveis.",
                    "msg_erro": "Vulnerável! Senhas curtas e comuns são quebradas em segundos."
                },
                {
                    "contexto": "FASE 2 (MÉDIO): Onde guardar suas 15 senhas?",
                    "msg": "Você precisa gerenciar várias senhas seguras. O que faz?",
                    "opcoes": [
                        {"texto": "Anoto no bloco de notas do celular.", "dano": 30},
                        {"texto": "Uso um Gerenciador de Senhas oficial (ex: Bitwarden).", "dano": 0, "certo": True},
                        {"texto": "Uso a mesma senha complexa para tudo.", "dano": 50},
                        {"texto": "Mando para mim mesmo no WhatsApp.", "dano": 30}
                    ],
                    "msg_acerto": "Ótimo! Gerenciadores criptografam suas senhas.",
                    "msg_erro": "Erro! Usar a mesma senha ou guardar sem criptografia é fatal."
                },
                {
                    "contexto": "FASE 3 (DIFÍCIL): Alerta de Vazamento",
                    "msg": "'O Google avisa: Sua senha vazou num ataque ao site de compras X.'",
                    "opcoes": [
                        {"texto": "Não faço nada, o antivírus bloqueia.", "dano": 50},
                        {"texto": "Troco a senha SÓ no site X.", "dano": 30},
                        {"texto": "Mudo uma letra no final da senha.", "dano": 30},
                        {"texto": "Troco no site X e em todos onde repeti essa senha.", "dano": 0, "certo": True}
                    ],
                    "msg_acerto": "Exato! Senhas vazadas são testadas em e-mails e bancos imediatamente.",
                    "msg_erro": "Risco Crítico! Mudar só uma letra ou ignorar não protege suas outras contas."
                }
            ]
        },
        {
            "id": 3, "nome": "Módulo 3: Clonagem", "icone": ft.icons.PEOPLE_ALT,
            "teoria_titulo": "Golpes de Perfil Falso",
            "teoria_desc": "Com uma simples foto sua da internet, golpistas chamam seus parentes usando um chip novo. Hoje, a IA já permite até clonar áudios perfeitamente usando vídeos antigos.",
            "desafios": [
                {
                    "contexto": "FASE 1 (FÁCIL): Número novo com foto do seu filho.",
                    "msg": "'Oi! Meu celular quebrou. Consegue me fazer um Pix de R$ 300?'",
                    "opcoes": [
                        {"texto": "Faço um Pix de R$ 1 para checar o nome.", "dano": 30},
                        {"texto": "Ligo para o número antigo (original) dele.", "dano": 0, "certo": True},
                        {"texto": "Peço para mandar um áudio.", "dano": 30},
                        {"texto": "Faço o Pix pedido na hora.", "dano": 50}
                    ],
                    "msg_acerto": "Perfeito! Ligar para o número antigo expõe a mentira.",
                    "msg_erro": "Erro! Golpistas usam laranjas, desculpas prontas ou IA para áudios."
                },
                {
                    "contexto": "FASE 2 (MÉDIO): A mensagem de segurança do WhatsApp.",
                    "msg": "'Atendimento WhatsApp: Seu app será bloqueado. Informe o código de 6 dígitos recebido por SMS.'",
                    "opcoes": [
                        {"texto": "Incorreto: Passo o código para evitar bloqueio.", "dano": 50},
                        {"texto": "Incorreto: Mando um print da tela.", "dano": 50},
                        {"texto": "Seguro: Nunca compartilho códigos SMS com ninguém.", "dano": 0, "certo": True},
                        {"texto": "Incorreto: Ligo para o atendente para passar o código.", "dano": 30}
                    ],
                    "msg_acerto": "Exato! O código do SMS é a chave mestre da sua conta.",
                    "msg_erro": "Conta Roubada! Você deu a chave para o hacker acessar seu WhatsApp."
                },
                {
                    "contexto": "FASE 3 (DIFÍCIL): A IA e a Urgência Extrema.",
                    "msg": "Áudio (voz do seu chefe, perfeita): 'Transfira os 5 mil pra conta X, urgente!'",
                    "opcoes": [
                        {"texto": "Faço a transferência pela urgência.", "dano": 50},
                        {"texto": "Questiono via texto pelo WhatsApp.", "dano": 30},
                        {"texto": "Ligo por chamada de vídeo para confirmar.", "dano": 0, "certo": True},
                        {"texto": "Transfiro, mas com comprovante.", "dano": 50}
                    ],
                    "msg_acerto": "Estratégia brilhante. A IA clona voz, mas a interação ao vivo derruba o golpe.",
                    "msg_erro": "Prejuízo financeiro! A IA clonou a voz perfeitamente, o áudio era falso."
                }
            ]
        },
        {
            "id": 4, "nome": "Módulo 4: Pirataria", "icone": ft.icons.DOWNLOAD,
            "teoria_titulo": "A Ilusão do Grátis",
            "teoria_desc": "O produto não é de graça; o produto é o acesso aos seus dados. Sites piratas e cracks de jogos sobrevivem infectando máquinas com malwares silenciosos.",
            "desafios": [
                {
                    "contexto": "FASE 1 (FÁCIL): Assistir a um filme de graça.",
                    "msg": "[ SITE: SUPERFILMES BR ] Baixar Filme HD (5 MB).",
                    "opcoes": [
                        {"texto": "Baixo o arquivo, pois é leve.", "dano": 50},
                        {"texto": "Clico com antivírus ligado.", "dano": 30},
                        {"texto": "Fecho o site e fujo.", "dano": 0, "certo": True},
                        {"texto": "Baixo pelo celular (mais seguro).", "dano": 30}
                    ],
                    "msg_acerto": "Decisão segura! Um filme nunca terá 5MB, é um executável de vírus.",
                    "msg_erro": "Infectado! O arquivo instalou um espião, antivírus nem sempre bloqueiam ameaças novas."
                },
                {
                    "contexto": "FASE 2 (MÉDIO): Instalando jogo pirata.",
                    "msg": "O instalador do jogo pede: 'Desative o antivírus para o crack funcionar'.",
                    "opcoes": [
                        {"texto": "Desativo temporariamente, é normal.", "dano": 50},
                        {"texto": "Adiciono o arquivo na exceção do antivírus.", "dano": 50},
                        {"texto": "Apago o jogo pirata da máquina.", "dano": 0, "certo": True},
                        {"texto": "Desconecto a internet e desativo.", "dano": 30}
                    ],
                    "msg_acerto": "Sensato. 'Cracks' desativam defesas para instalar sequestradores de dados (Ransomware).",
                    "msg_erro": "Máquina comprometida! Você abriu as portas voluntariamente para o malware."
                },
                {
                    "contexto": "FASE 3 (DIFÍCIL): A Falsa Plataforma Oficial.",
                    "msg": "Anúncio no Google: 'App do WhatsApp Oficial para PC. Baixe o .EXE aqui'.",
                    "opcoes": [
                        {"texto": "Clico no anúncio e baixo.", "dano": 50},
                        {"texto": "Ignoro anúncios e baixo pela Microsoft Store oficial.", "dano": 0, "certo": True},
                        {"texto": "Baixo pelo anúncio, mas rodo escaneamento antes.", "dano": 30},
                        {"texto": "Uso o link encurtado que um amigo mandou.", "dano": 30}
                    ],
                    "msg_acerto": "Excelente. Hackers pagam anúncios no Google para espalhar apps falsificados.",
                    "msg_erro": "Hackeado. Anúncios falsos lideram o topo das pesquisas entregando instaladores falsos."
                }
            ]
        }
    ]

    def criar_barra_hp():
        cor_hp = "green" if estado_jogo["hp"] > 50 else ("orange" if estado_jogo["hp"] > 25 else "red")
        return ft.Row([
            ft.Icon(ft.icons.FAVORITE, color=cor_hp),
            ft.ProgressBar(value=estado_jogo["hp"]/100, color=cor_hp, bgcolor="white24", expand=True, height=10),
            ft.Text(f"{estado_jogo['hp']}%", color="white", weight="bold")
        ])

    def abrir_login(e=None):
        page.views.clear()
        logo_container = ft.Container(
            content=ft.Column([ft.Icon(ft.icons.SHIELD_OUTLINED, size=90, color="blue"), ft.Text("ProtegeAí", size=45, weight="bold", color="white")], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            margin=ft.margin.only(top=200), animate=ft.animation.Animation(1000, ft.AnimationCurve.EASE_OUT)
        )
        login_form = ft.Container(
            opacity=0, animate_opacity=1000, padding=30,
            content=ft.Column([
                ft.Text("Acesse sua central de defesa", size=16, color="white70", text_align="center"), ft.Container(height=20),
                ft.TextField(label="Nome de Usuário", prefix_icon=ft.icons.PERSON, bgcolor="white10", color="white"),
                ft.TextField(label="Senha de Acesso", prefix_icon=ft.icons.LOCK, password=True, can_reveal_password=True, bgcolor="white10", color="white"),
                ft.Container(height=20),
                ft.ElevatedButton("ENTRAR NO SISTEMA", width=300, height=50, style=ft.ButtonStyle(color="white", bgcolor="blue700"), on_click=lambda e: (estado_jogo.update({"usuario": e.control.parent.controls[2].value or "Agente"}), abrir_menu()))
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        page.views.append(ft.View(route="/login", padding=0, controls=[ft.Container(image_src=IMG_FUNDO, image_fit=ft.ImageFit.COVER, expand=True, content=ft.Container(bgcolor=ft.colors.with_opacity(0.9, "black"), expand=True, content=ft.Column([logo_container, login_form], horizontal_alignment=ft.CrossAxisAlignment.CENTER)))]))
        page.update()
        def iniciar_animacao():
            time.sleep(1.5)
            logo_container.margin = ft.margin.only(top=50)
            login_form.opacity = 1
            page.update()
        threading.Thread(target=iniciar_animacao, daemon=True).start()

    def abrir_menu(e=None):
        page.views.clear()
        page.views.append(
            ft.View(
                route="/menu", padding=0,
                controls=[
                    ft.Container(
                        image_src=IMG_FUNDO, image_fit=ft.ImageFit.COVER, expand=True,
                        content=ft.Container(
                            bgcolor=ft.colors.with_opacity(0.85, "black"), expand=True, padding=30,
                            content=ft.Column(
                                [
                                    ft.Row([ft.Icon(ft.icons.SHIELD_OUTLINED, size=40, color="blue"), ft.Text("ProtegeAí", size=28, weight="bold", color="white")], alignment=ft.MainAxisAlignment.CENTER),
                                    ft.Text(f"Bem-vindo(a), {estado_jogo['usuario']}", size=16, color="white70"),
                                    ft.Container(height=40),
                                    ft.ElevatedButton("Biblioteca de Aprendizado", icon=ft.icons.MENU_BOOK, width=320, height=60, on_click=abrir_menu_teoria),
                                    ft.Container(height=10),
                                    ft.ElevatedButton("Área de Desafios (Prática)", icon=ft.icons.GAMES, width=320, height=60, color="red", on_click=abrir_menu_desafios),
                                    ft.Container(height=10),
                                    ft.ElevatedButton("Meu Perfil & Status", icon=ft.icons.PERSON, width=320, height=60, color="green", on_click=abrir_perfil),
                                    ft.Container(height=50),
                                    ft.TextButton("Desconectar", icon=ft.icons.LOGOUT, on_click=abrir_login)
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER
                            )
                        )
                    )
                ]
            )
        )
        page.update()

    def abrir_menu_teoria(e):
        lista_botoes = []
        for mod in modulos:
            lista_botoes.append(ft.ElevatedButton(mod["nome"], icon=mod["icone"], width=320, height=50, on_click=lambda e, m=mod: abrir_teoria(m)))
            lista_botoes.append(ft.Container(height=5))

        secao_futuro = ft.Container(
            bgcolor=ft.colors.with_opacity(0.2, "blue"), border=ft.border.all(1, "blue"), border_radius=10, padding=15,
            content=ft.Column([
                ft.Row([ft.Icon(ft.icons.NEW_RELEASES, color="blue"), ft.Text("Futuras Atualizações", color="blue", weight="bold")], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=10),
                ft.ElevatedButton("🎥 Videoaulas Explicativas", disabled=True, width=320, height=50, style=ft.ButtonStyle(color="grey400")),
                ft.Text("Módulos em vídeo serão lançados na versão 2.0!", size=12, color="white54", text_align="center")
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

        page.views.append(
            ft.View(
                route="/aprendizado", padding=0,
                controls=[
                    ft.Container(
                        bgcolor="black", expand=True, padding=30,
                        content=ft.ListView(
                            controls=[
                                ft.Icon(ft.icons.MENU_BOOK, size=50, color="blue"),
                                ft.Text("Biblioteca Teórica", size=26, weight="bold", color="white", text_align="center"),
                                ft.Text("Estude os módulos com atenção para ter chances nos Desafios.", size=14, color="white70", text_align="center"),
                                ft.Container(height=20),
                            ] + lista_botoes + [
                                ft.Container(height=20), secao_futuro, ft.Container(height=20),
                                ft.TextButton("Voltar ao Menu", icon=ft.icons.ARROW_BACK, on_click=abrir_menu)
                            ]
                        )
                    )
                ]
            )
        )
        page.update()

    def abrir_menu_desafios(e):
        lista_botoes = []
        for mod in modulos:
            ta_liberado = mod["id"] <= estado_jogo["modulos_liberados"]
            icone_status = mod["icone"] if ta_liberado else ft.icons.LOCK
            cor_btn = "red" if ta_liberado else "grey"
            lista_botoes.append(ft.ElevatedButton(mod["nome"] + " (3 Fases)", icon=icone_status, color=cor_btn, disabled=not ta_liberado, width=320, height=60, on_click=lambda e, m=mod: abrir_simulacao(m, 0)))
            lista_botoes.append(ft.Container(height=10))

        page.views.append(
            ft.View(
                route="/desafios", padding=0,
                controls=[
                    ft.Container(
                        bgcolor="black", expand=True, padding=30,
                        content=ft.Column(
                            [
                                ft.Icon(ft.icons.WARNING, size=50, color="red"),
                                ft.Text("Área de Desafios", size=26, weight="bold", color="white"),
                                criar_barra_hp(), ft.Container(height=20),
                            ] + lista_botoes + [
                                ft.Container(height=20), ft.TextButton("Voltar ao Menu", icon=ft.icons.ARROW_BACK, on_click=abrir_menu)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    )
                ]
            )
        )
        page.update()

    def abrir_teoria(dados):
        page.views.append(ft.View(route="/leitura", padding=0, controls=[ft.Container(bgcolor="black", expand=True, padding=30, content=ft.Column([ft.Icon(dados["icone"], size=50, color="blue"), ft.Text(dados["teoria_titulo"], size=26, weight="bold", color="white", text_align="center"), ft.Container(height=15), ft.Text(dados["teoria_desc"], size=16, color="white", text_align="justify"), ft.Container(height=30), ft.TextButton("Voltar à Biblioteca", icon=ft.icons.ARROW_BACK, on_click=abrir_menu_teoria)], horizontal_alignment=ft.CrossAxisAlignment.CENTER))]))
        page.update()

    def abrir_perfil(e):
        page.views.append(ft.View(route="/perfil", padding=0, controls=[ft.Container(bgcolor="black", expand=True, padding=30, content=ft.Column([ft.Icon(ft.icons.PERSON_PIN, size=70, color="green"), ft.Text("Perfil do Agente", size=26, weight="bold", color="white"), ft.Text(f"Nome: {estado_jogo['usuario']}", size=18, color="white70"), ft.Container(height=30), ft.Text("Saúde do Dispositivo:", size=16, color="white"), criar_barra_hp(), ft.Container(height=20), ft.Text(f"Módulos Liberados: {estado_jogo['modulos_liberados']} / 4", size=16, color="white", weight="bold"), ft.Container(height=40), ft.TextButton("Voltar ao Menu", icon=ft.icons.ARROW_BACK, on_click=abrir_menu)], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER))]))
        page.update()

    # --- TELA EDUCATIVA DE GAME OVER ---
    def abrir_game_over(e=None):
        page.views.clear()
        page.views.append(
            ft.View(
                route="/gameover",
                padding=0,
                controls=[
                    ft.Container(
                        bgcolor="red900",
                        expand=True,
                        alignment=ft.alignment.center,
                        padding=30,
                        content=ft.Column(
                            [
                                ft.Icon(ft.icons.ERROR_OUTLINE, size=80, color="white"),
                                ft.Text("VOCÊ FOI HACKEADO!", size=32, weight="bold", color="white", text_align="center"),
                                ft.Container(height=15),
                                ft.Text("Sua Saúde Digital chegou a 0%.", size=18, color="white", weight="bold"),
                                ft.Container(height=20),
                                ft.Text(
                                    "Na vida real, não há botão de reiniciar. Um ataque bem-sucedido pode resultar em roubo de identidade, perdas financeiras e exposição de dados íntimos.\n\nA pressa é a maior arma dos cibercriminosos. Aprenda com os erros desta simulação, respire fundo e mantenha suas defesas sempre ativas.",
                                    size=16, color="white70", text_align="center"
                                ),
                                ft.Container(height=40),
                                ft.ElevatedButton("Formatar Sistema e Recomeçar", icon=ft.icons.RESTART_ALT, on_click=reiniciar_jogo, style=ft.ButtonStyle(color="red", bgcolor="white"))
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        )
                    )
                ]
            )
        )
        page.update()

    def reiniciar_jogo(e):
        estado_jogo["hp"] = 100
        estado_jogo["modulos_liberados"] = 1
        abrir_menu() # Volta pro menu sem precisar digitar o login de novo

    def abrir_simulacao(dados_modulo, fase_atual=0):
        fase_dados = dados_modulo["desafios"][fase_atual]
        controle_timer = {"rodando": True} 
        
        limites_tempo = [25, 20, 15]
        tempo_maximo = limites_tempo[fase_atual]
        
        texto_timer = ft.Text(f"⏳ TEMPO: {tempo_maximo}s", size=20, weight="bold", color="red")
        
        container_botoes = ft.Column(spacing=10)
        container_feedback = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        def ir_proxima_fase(e):
            if fase_atual + 1 < len(dados_modulo["desafios"]):
                abrir_simulacao(dados_modulo, fase_atual + 1)
            else:
                if estado_jogo["modulos_liberados"] == dados_modulo["id"]:
                    estado_jogo["modulos_liberados"] += 1
                abrir_menu_desafios(None)

        def verificar(dano, certo, motivo_esgotado=False):
            controle_timer["rodando"] = False
            container_botoes.controls.clear() 
            
            estado_jogo["hp"] = max(0, estado_jogo["hp"] - dano)
            barra_atualizada.content = criar_barra_hp()
            
            # ATIVA A TELA DE GAME OVER SE A VIDA ZERAR
            if estado_jogo["hp"] == 0:
                container_feedback.controls.append(ft.Text("SISTEMA CORROMPIDO!", size=18, color="red", weight="bold"))
                camada_animada.bgcolor = ft.colors.with_opacity(0.95, "red")
                page.update()
                time.sleep(1.5)
                abrir_game_over()
                return

            if certo:
                msg = fase_dados['msg_acerto']
                camada_animada.bgcolor = ft.colors.with_opacity(0.95, "green")
                btn_proximo = ft.ElevatedButton("Próxima Fase" if fase_atual < 2 else "Concluir Módulo", on_click=ir_proxima_fase)
            else:
                msg = "TEMPO ESGOTADO!" if motivo_esgotado else fase_dados['msg_erro']
                camada_animada.bgcolor = ft.colors.with_opacity(0.95, "red")
                btn_proximo = ft.ElevatedButton("Avançar Ferido" if fase_atual < 2 else "Sobreviveu ao Módulo", on_click=ir_proxima_fase, color="red")

            container_feedback.controls.append(ft.Text(f"{msg}\n\n[ DANO: -{dano}% HP ]", size=16, weight="bold", color="white", text_align="center"))
            container_feedback.controls.append(ft.Container(height=10))
            container_feedback.controls.append(btn_proximo)
            page.update()

        for opcao in fase_dados["opcoes"]:
            is_correct = opcao.get("certo", False)
            container_botoes.controls.append(
                ft.ElevatedButton(text=opcao["texto"], width=350, on_click=lambda e, d=opcao["dano"], c=is_correct: verificar(d, c), style=ft.ButtonStyle(padding=15))
            )

        barra_atualizada = ft.Container(padding=10, content=criar_barra_hp())

        coluna_elementos = [
            texto_timer,
            ft.Text(f"DESAFIO - FASE {fase_atual + 1}/3", size=20, weight="bold", color="white", text_align="center"),
            ft.Text(fase_dados["contexto"], size=14, color="white70", text_align="center"),
            ft.Container(bgcolor=ft.colors.with_opacity(0.3, "white"), padding=15, border_radius=10, content=ft.Text(fase_dados["msg"], size=15, color="white", text_align="center")),
            ft.Container(height=10),
            container_botoes,
            container_feedback,
            ft.Container(height=10),
            ft.TextButton("Abandonar Missão", icon=ft.icons.EXIT_TO_APP, on_click=lambda e: (controle_timer.update({"rodando": False}), abrir_menu_desafios(e)))
        ]

        camada_animada = ft.Container(bgcolor=ft.colors.with_opacity(0.85, "black"), expand=True, padding=20, content=ft.ListView(controls=coluna_elementos, spacing=10))

        page.views.append(ft.View(route="/modulo", padding=0, controls=[ft.Container(image_src=IMG_FUNDO, image_fit=ft.ImageFit.COVER, expand=True, content=ft.Column([barra_atualizada, ft.Container(content=camada_animada, expand=True)]))]))
        page.update()

        def rodar_timer():
            for i in range(tempo_maximo, -1, -1):
                if not controle_timer["rodando"]: break
                texto_timer.value = f"⏳ TEMPO: {i}s"
                if i <= 5: texto_timer.color = "orange" if i % 2 == 0 else "red"
                page.update()
                time.sleep(1)
            if controle_timer["rodando"] and i == 0:
                verificar(30, False, motivo_esgotado=True)

        threading.Thread(target=rodar_timer, daemon=True).start()

    abrir_login()

ft.app(target=main)