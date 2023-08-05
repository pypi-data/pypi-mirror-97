from ftsa.cli.utils.files import get_project_properties


""" Project Properties File """
project = get_project_properties()


""" Autenticacao Usuario Page Locators """
alt1 = "xpath://html[@id='index-page']//div[@id='content']//a[@href='/cas2/login']"
alt2 = "//html[@id='authorize-page']//div[@id='content']//a[@href='/cas2/login']"
botao_login_novamente = "xpath://*[@id='content']/div/div/p[3]/a"
campo_usuario = "name:username"
campo_senha = "name:password"
botao_entrar = "name:submit"
