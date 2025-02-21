"""
Robotic Process Automation (RPA) Script

Author: [LUCAS BRANDAO DOS SANTOS]
Date: [09/05/2024]

Description:
This Python script automates the creation of exam schedules.
It utilizes various libraries and frameworks for web and GUI automation.

Libraries Used:
- Selenium
- Pandas
- SqlAlchemy
- cls_bot (custom)
- Smtp [not implemented yet]


Note: Before running this script, ensure that the necessary tools and libraries are installed.
"""
from database import update_table
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime, time
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
frame = ['default', 'socframe']
timeout = [0,3]
filename = 'SOC - [cad192m] - [675 - Guia de Encaminhamento de Exames ].pdf'


async def update_database(data,db):
        await update_table(data=data, db=db)
        return


def criar_guia(guia_data: dict, user_data: dict, execution_id: str, db: AsyncSession):
    try:
        s = sydle_bot()
        tmp_dir = s.temp_path(execution_id)
        
        
        while True:
            if s.clear_temp_folder(path=s.tmp_dir) == True:
                break
        
        options = s.soc_driver_options(path_download=s.tmp_dir)
        driver = webdriver.Chrome(options=s.driver_options)
        driver.set_window_rect(x=-1,y=-1,width=1200,height=800)
            
        funct = 'site_soc'
        site_soc = s.acessarSoc(driver=driver)
        if site_soc == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')
            
        funct = 'login_soc'
        login_soc = s.loginSoc(driver=driver,username=user_data['SOC_USER'],password=user_data['SOC_PASSWORD'],id=user_data['SOC_ID'])
        if login_soc == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')

        funct = 'verificar_aviso'
        verificar_aviso = s.verificar_aviso(driver=driver, timeout=timeout[0])
        if verificar_aviso == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')
        
        funct = 'tela_inicial'
        tela_inicial = s.tela_inicial_soc(driver=driver)
        if tela_inicial == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')
        
        funct = 'script_busca_avancada'
        script = str("javascript:MainJava('pesqRapida!browser.action','1','088');hideall();hidemenus('');menu_close();")
        script_busca_avancada = s.execute_script(driver=driver,frame=frame[0],script=script)
        if script_busca_avancada == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')
        
        funct = 'await_tela_busca_avancada'
        data_list = ['buscaFuncionario_3']
        type = 'id'
        await_tela_busca_avancada = s.await_element(driver=driver,frame=frame[1], id=data_list[0], type=type)
        if await_tela_busca_avancada == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')
        
        funct = 'selecionar_radio_funcionario'
        page_vars = ['buscaFuncionario_0','id']
        selecionar_radio_funcionario = s.selecionar_radio(driver=driver,frame=frame[1], id=page_vars[0], type=page_vars[1])
        if selecionar_radio_funcionario == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')
        
        funct = 'selecionar_checkbox_status'
        page_vars = ['ativo','inativo','pendente','afastado','ferias']
        type = 'id'
        selecionar_checkbox_status = s.selecionar_multi_checkbox(driver=driver,frame=frame[1], type=type, id_list=page_vars)
        if selecionar_checkbox_status == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')
        
        funct = 'selecionar_checkbox_socnet'
        page_vars = [guia_data['empresa_socnet'],'acessoSocnet','id'] #s.df['socnet'][0]
        selecionar_checkbox_socnet = s.selecionar_checkbox_socnet(driver=driver,frame=frame[1], id=page_vars[1], type=page_vars[2], socnet=page_vars[0])
        if selecionar_checkbox_socnet == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')
        
        funct = 'insere_dados_funcionario'
        page_ids = ['nomeEmpresaFuncionario','nomeFuncionario']
        data_list =[guia_data['codigo_empresa_cliente'],guia_data['codigo_funcionario'], guia_data['empresa_socnet']]
        type = 'id'
        insere_dados_funcionario = s.insere_dados_funcionario(driver=driver,frame=frame[1], id_list=page_ids, data_list=data_list, type=type)
        if insere_dados_funcionario == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')
        
        funct = 'selecionar_combo_pequisa'
        data_list = ['tipoPesquisaFuncionario','1','Código']
        type = 'id'
        selecionar_combo_pequisa = s.selecionar_combo_pequisa(driver=driver,frame=frame[1], data_list=data_list, type=type)
        if selecionar_combo_pequisa == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')
        
        funct = 'browse_funcionario'
        browse_funcionario = s.execute_pesquisa(driver=driver,frame=frame[1])
        if browse_funcionario == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')
        
        funct = 'await_lista_funcionario'
        data_list = str(guia_data['codigo_funcionario'])
        type = 'partial_link'
        await_lista_funcionario = s.await_element(driver=driver,frame=frame[1], id=data_list[0], type=type, timeout=30)
        if await_lista_funcionario == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')
        
        while True:
            funct = 'funcionario_link_text'
            data_list = str(guia_data['codigo_funcionario'])
            type = 'partial_link'
            funcionario_link_text = s.funcionario_link_text(driver=driver,frame=frame[1], data_list=data_list, type=type)
            if funcionario_link_text == True:
                print(f'{funct} passed at {datetime.datetime.now()}')
                break
            else:
                print(f'error')
        
        funct = 'script_funcionario'
        script = str(s.funcionario_link)
        script_funcionario = s.execute_script(driver=driver,frame=frame[1],script=script)
        if script_funcionario == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')
        
        funct = 'await_tela_funcionario'
        data_list = ['codigoGenerico']
        type = 'id'
        await_tela_funcionario = s.await_element(driver=driver,frame=frame[1], id=data_list[0], type=type)
        if await_tela_funcionario == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')
            
        funct = 'script_guia'
        script = str("doAcao('guia');")
        script_guia = s.execute_script(driver=driver,frame=frame[1],script=script)
        if script_guia == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')
        
        funct = 'await_tela_guia'
        data_list = ['cad192_ac']
        type = 'id'
        await_tela_guia = s.await_element(driver=driver,frame=frame[1], id=data_list[0], type=type)
        if await_tela_guia == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')
        
        funct = 'script_incluir_guia'
        script = str("javascript:doAcao('inc');")
        script_incluir_guia = s.execute_script(driver=driver,frame=frame[1],script=script)
        if script_incluir_guia == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')
        
        funct = 'await_tela_incluir_guia'
        data_list = ['pedirExamesNaoConvocados']
        type = 'id'
        await_tela_guia = s.await_element(driver=driver,frame=frame[1], id=data_list[0], type=type)
        if await_tela_guia == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')
        
        funct = 'selecionar_combo_tipo_exame'
        data_list = ['tipoExame', guia_data['tipo_exame']]
        type = 'id'
        selecionar_combo_tipo_exame = s.selecionar_combo_tipo_exame(driver=driver,frame=frame[1], data_list=data_list, type=type)
        if selecionar_combo_tipo_exame == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')
        
        funct = 'await_combo_exames'
        data_list = ['btnTipoExameAtras']
        type = 'id'
        await_combo_exames = s.await_element(driver=driver,frame=frame[1], id=data_list[0], type=type)
        if await_combo_exames == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')

        funct = 'script_gravar_guia'
        script = str("javascript:doAcao('save');")
        script_gravar_guia = s.execute_script(driver=driver,frame=frame[1],script=script)
        if script_gravar_guia == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')
        
        funct = 'alert_check'
        alert_check = s.alert_accept(driver=driver, frame=frame[1], timeout=10)
        if alert_check == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            print(s.alert_text)
            pass
        else:
            print(f'error')
        
        driver.switch_to.default_content()
        driver.switch_to.frame(frame[1])
        
        codigo_guia = s.await_element(driver=driver,frame=frame[1],id='codGuia',type='id', timeout=10)
        codigo_guia = str(driver.find_element(By.ID,'codGuia').get_attribute('value'))
        
        
        funct = 'script_data_hora'
        script = str('javascript:selecionaDataHora();')
        script_data_hora = s.execute_script(driver=driver,frame=frame[1],script=script)
        if script_data_hora == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')
            
        funct = 'await_data_hora'
        data_list = ['data_0_0']
        type = 'id'
        await_combo_exames = s.await_element(driver=driver,frame=frame[1], id=data_list[0], type=type)
        if await_combo_exames == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')    
        
        funct = 'insere_data'
        page_ids = ['data_0_0',guia_data['data_exame']]
        type = 'id'
        insere_data = s.insere_data(driver=driver,frame=frame[1], id_list=page_ids, data_list=page_ids, type=type)
        if insere_data == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')
        
        funct = 'insere_hora'
        page_ids = ['hora_inicio_0_0',guia_data['hora_inicio']]
        type = 'id'
        insere_hora = s.insere_hora(driver=driver,frame=frame[1], id_list=page_ids, data_list=page_ids, type=type)
        if insere_hora == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')
        
        funct = 'script_gravar_datahora'
        script = str("javascript:salvarDataHora();")
        script_gravar_datahora = s.execute_script(driver=driver,frame=frame[1],script=script)
        if script_gravar_datahora == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')
        
        funct = 'script_selecionar_prestador'
        script = str("javascript:selecionaPrestador();")
        script_selecionar_prestador = s.execute_script(driver=driver,frame=frame[1],script=script)
        if script_selecionar_prestador == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')
        
        funct = 'captura_id_dinamico_prestador'
        id_list = ['a','type', 'hidden', 'class', 'prestador']
        captura_id_dinamico_prestador = s.recebe_id_prestador(driver=driver,frame=frame[1],id_list=id_list)
        if captura_id_dinamico_prestador == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')
        
        
        funct = 'insere_prestador'
        id_list = [s.variable_id_split[1], guia_data['codigo_prestador']]
        insere_prestador = s.insere_prestador(driver=driver,frame=frame[1],id_list=id_list, type='id')
        if insere_prestador == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')
        
        funct = 'script_gravar_prestador'
        script = str("javascript:salvarPrestador();")
        script_gravar_prestador = s.execute_script(driver=driver,frame=frame[1],script=script)
        if script_gravar_prestador == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')

        
        funct = 'script_impressao_multipla'
        script = str("javascript:doAcao('impressao_multipla');")
        script_impressao_multipla = s.execute_script(driver=driver,frame=frame[1],script=script)
        if script_impressao_multipla == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')

        
        funct = 'selecionar_janela_impressao'
        selecionar_janela_impressao = s.select_window(driver=driver)
        if selecionar_janela_impressao == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')

        
        while True:
            if s.wait_for_file(filename=filename) == True:        
                break
            else:
                script = str("window.print();")
                s.execute_script(driver=driver,frame=None,script=script)            
                
        funct = 'rename_file'
        id_list = [guia_data['codigo_empresa_cliente'], guia_data['codigo_funcionario'], guia_data['codigo_prestador']]
        rename_file = s.rename_file(file_path=s.file_path,name_data=id_list)
        if rename_file == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')

        funct = 'file_b64'
        rename_file = s.file_b64(filepath=s.new_file_path)
        if rename_file == True:
            print(f'{funct} passed at {datetime.datetime.now()}')
            pass
        else:
            print(f'error')
        
        funct = 'update_SQL_table'
        id_solicitacao = guia_data['id']
        extensao_arquivo= s.file_extension
        nome_arquivo = s.new_filename_noext
        conteudo_arquivo = s.base64_encoded
        status = 200
        
        data_retorno={
                "extensao_arquivo":extensao_arquivo,
                "nome_arquivo": nome_arquivo,
                "codigo_guia":   codigo_guia,
                "status":  status,
                "conteudo_arquivo": conteudo_arquivo,
                "id_solicitacao":id_solicitacao
        }
        

        loop = asyncio.get_event_loop()
        loop.create_task(update_database(data=data_retorno, db=db))

        driver.quit()

        return {"status": "success",
                "data": data_retorno}
    

    except Exception as e:
        driver.quit()
        return {
            "status": "error",
            "message": e
        }

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import json, io, os, datetime, time, shutil, urllib, base64
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text, bindparam
from sqlalchemy.orm import sessionmaker

from sqlalchemy.exc import SQLAlchemyError


class sydle_bot():
    def __init__(self):
        load_dotenv()
        self.soc_username = os.getenv('SOC_USER')
        self.soc_password = os.getenv('SOC_USER_PASS')
        self.soc_id = os.getenv('USER_ID')
        self.headless = os.getenv('HEADLESS')
        pass
    
    def db_engine(self, env):
        try:
            if env == 'prod':
                self.db_host = os.getenv('PROD_DB_HOST')
                self.db_port = os.getenv('PROD_DB_PORT')
                self.db_user = os.getenv('PROD_DB_USER')
                self.db_pass = os.getenv('PROD_DB_PASS')
                self.db_name = os.getenv('PROD_DB_NAME')
                self.db_table = os.getenv('PROD_DB_TABLE')
                self.db_driver = os.getenv('DB_DRIVER')
                
            elif env == 'dev':
                self.db_host = os.getenv('DEV_DB_HOST')
                self.db_port = os.getenv('DEV_DB_PORT')
                self.db_user = os.getenv('DEV_DB_USER')
                self.db_pass = os.getenv('DEV_DB_PASS')
                self.db_name = os.getenv('DEV_DB_NAME')
                self.db_table = os.getenv('DEV_DB_TABLE')
                self.db_driver = os.getenv('DB_DRIVER')
            
            self.db_params = urllib.parse.quote_plus(f"DRIVER={self.db_driver};SERVER={self.db_host};PORT={self.db_port};DATABASE={self.db_name};UID={self.db_user};PWD={self.db_pass}")
            self.engine = create_engine(f"mssql+pyodbc:///?odbc_connect={self.db_params}")
            
            return True
        
        except Exception as e:
            print(e)
            return False 
       
    def pending_list(self,engine):
        try:
            self.df = pd.read_sql_query("SELECT TOP 1 * FROM suporte_db.dbo.dev_Guias WHERE STATUS = 0 ORDER BY created_at asc;", con=engine) #['IDARQUIVO'].tolist()    
        except:
            return False
        finally:
            return True

    def temp_path(self, execution_id: str) -> str:
        """Generates a temporary directory in the root project folder for the execution ID."""
        execution_dir = os.path.join(os.getcwd(), "temp", execution_id)
        self.tmp_dir = execution_dir
        # ✅ Create directory if it doesn't exist
        os.makedirs(execution_dir, exist_ok=True)

        return execution_dir

    def clear_temp_folder(self, path=''):
        if not os.path.exists(self.tmp_dir):
            print(f"The folder '{self.tmp_dir}' does not exist.")
            return False
        if not os.path.isdir(self.tmp_dir):
            print(f"The path '{self.tmp_dir}' is not a directory.")
            return False
        for filename in os.listdir(self.tmp_dir):
            file_path = os.path.join(self.tmp_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete '{file_path}'. Reason: {e}")
                return False
        if len(os.listdir(self.tmp_dir)) == 0:
            print(f"All files successfully deleted from '{self.tmp_dir}'.")
            return True
        else:
            print(f"Failed to delete all files from '{self.tmp_dir}'.")
            return False
    
    def wait_for_file(self, filename, timeout=15, interval=3):
        end_time = time.time() + timeout
        self.file_path = os.path.join(self.tmp_dir, filename)
        
        while time.time() < end_time:
            if os.path.isfile(self.file_path):
                return True
            time.sleep(interval)
            
        print(f"File '{filename}' not found in '{self.tmp_dir}' within {timeout} seconds.")
        return False

    def rename_file(self, file_path, name_data):
        if not os.path.isfile(file_path):
            print(f"The file '{file_path}' does not exist.")
            return None

        # Extract directory and original file extension
        directory, original_filename = os.path.split(file_path)
        _, self.file_extension = os.path.splitext(original_filename)

        # Get current date in the desired format (YYYY-MM-DD)
        current_date = datetime.datetime.now().strftime('%d%m%Y')

        # Create the new file name
        self.new_filename = f"{name_data[0]}_{name_data[1]}_{name_data[2]}_{current_date}{self.file_extension}"
        self.new_filename_noext = f"{name_data[0]}_{name_data[1]}_{name_data[2]}_{current_date}"
        self.new_file_path = os.path.join(directory, self.new_filename)

        try:
            # Rename the file
            os.rename(file_path, self.new_file_path)
            print(f"File renamed to '{self.new_file_path}'.")
            return True
        except Exception as e:
            print(f"Failed to rename file. Reason: {e}")
            return False

    def file_b64(self, filepath):
        try:
            with open(filepath, "rb") as file:
                file_content = file.read()
                self.base64_encoded = base64.b64encode(file_content).decode('utf-8')
                return True
        except FileNotFoundError:
            print(f"The file '{filepath}' does not exist.")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def presenceWait(self, driver, element, type, timeout=10):
        wait = WebDriverWait(driver,timeout)
        try:
            if type == "name":
                waitReturn = wait.until(
                    EC.presence_of_element_located((By.Name, element))
                )
            elif type == 'id':
                waitReturn = wait.until(
                    EC.presence_of_element_located((By.ID, element))
                )
            elif type == 'xpath':
                waitReturn = wait.until(
                    EC.presence_of_element_located((By.XPATH, element))
                )
            return True
        except:
            return False

    def elementWait(self, driver, element, type, timeout=10):
        wait = WebDriverWait(driver,timeout)
        try:
            if type == "name":
                waitReturn = wait.until(
                    EC.visibility_of_element_located((By.Name, element))
                )
            elif type == 'id':
                waitReturn = wait.until(
                    EC.visibility_of_element_located((By.ID, element))
                )
            elif type == 'xpath':
                waitReturn = wait.until(
                    EC.visibility_of_element_located((By.XPATH, element))
                )
            return True
        except:
            return False
     
    def soc_driver_options(self, path_download, headless=False):
        self.driver_options = Options()
        appState = {
        "recentDestinations": [
            {
                "id": "Save as PDF",
                "origin": "local",
                "account": ""
            }
        ],
        "selectedDestinationId": "Save as PDF",
        "version": 2
        }

        profile = {'printing.print_preview_sticky_settings.appState': json.dumps(appState),
                'savefile.default_directory': self.tmp_dir}
        self.driver_options.add_experimental_option('prefs', profile)
        self.driver_options.add_argument('--kiosk-printing')
        self.driver_options.add_argument('--disable-features=InsecureDownloadWarnings')
        self.driver_options.page_load_strategy = 'normal'        
        self.driver_options.add_argument('--disable-gpu')
        self.driver_options.add_argument('--disable-dev-shm-usage')
        self.driver_options.add_argument('--no-sandbox')
        self.driver_options.add_argument('--disable-extensions')
        self.driver_options.add_argument('--disable-infobars')
        self.driver_options.add_argument('--disable-popup-blocking')
        self.driver_options.add_argument('--disable-notifications')
        
        if headless == True:
            self.driver_options.add_argument('--headless')
        else:
            pass
        
        return self.driver_options
    
    def acessarSoc(self, driver):
        try:
            driver.get("https://sistema.soc.com.br")
            loginEntry = driver.find_element(By.ID,"usu")
            wait = WebDriverWait(driver,timeout=5)
            wait.until(lambda d : loginEntry.is_displayed())
            return True
        except Exception as e:
            print(e)
            return False
            
    def loginSoc(self,driver,username,password,id):
        try:
            login_script = f'''
            document.getElementById("usu").value = "{username}";
            document.getElementById("senha").value = "{password}";
            document.getElementById("empsoc").value = "{id}";

            setTimeout(function(){{
                document.getElementById("bt_entrar").click();
            }}, 1000);
            '''
            driver.execute_script(login_script)
            wait = WebDriverWait(driver,timeout=7)
            wait.until(
                EC.visibility_of_element_located((By.ID, 'infoPrograma'))
            )
            return True
        except Exception as e:
            return e
        
    def verificar_aviso(self,driver,timeout=5):
        vars_aviso = ['avisoAdmAge','id','naoMostrarAvisoAdministrador','botaoOk']
        try:
            driver.switch_to.default_content()
            if self.elementWait(driver=driver,element=vars_aviso[0],type=vars_aviso[1], timeout=timeout) == True:
                while True:
                    if driver.find_element(By.ID,vars_aviso[0]).is_displayed() == True:
                        element = driver.find_element(By.ID,vars_aviso[2])
                        while element.is_selected() != True:
                            element.click()
                        element_button = driver.find_element(By.ID,vars_aviso[3])
                        driver.execute_script("arguments[0].click();",element_button)
                    else:
                        break
                print('Aviso fechado')
            else:
                print('Sem avisos')
            return True
        except Exception as e:
            print(f'erro {e}')
            return False
    
    def tela_inicial_soc(self,driver):
        driver.switch_to.default_content()
        try:
            driver.execute_script('javascript:Empresas(); hideall();hidemenus('');menu_close();avisoLogin();')
            return True
        except:
            return False
    
    def selecionar_radio(self,frame,driver,id,type):
        self.frame_switch(driver,'socframe')
        try:
            element = self.return_element(driver=driver, frame=frame, id=id, type=type)
            if element != False:
                while element.is_selected() != True:
                    element.click()
                return True
            else:
                raise 'return_element: Error while fetching element identifier = {id}, type = {type}'
        except Exception as e:
            print(f'erro {e}')
            return False
    
    def selecionar_multi_checkbox(self,frame,driver,type,id_list):
        try:
            self.frame_switch(driver,frame)
            for id in id_list:
                element = self.return_element(driver=driver,frame=frame,id=id,type=type)
                while element.is_selected() != True:
                    element.click()
            return True
        except Exception as e:
            print(f'erro {e}')
            return False
    
    def selecionar_checkbox_socnet(self,frame,driver,id,type, socnet):
        self.frame_switch(driver,'socframe')
        try:
            if socnet == True:
                element = self.return_element(driver=driver, frame=frame, id=id, type=type)
                if element != False:
                    while element.is_selected() != True:
                        element.click()
                    return True
                else:
                    raise 'return_element: Error while fetching element identifier = {id}, type = {type}'
            elif socnet == False:
                return True
        except Exception as e:
            print(f'erro {e}')
            return False
    
    def selecionar_combo_pequisa(self,frame,driver,data_list,type):
        try:
            self.frame_switch(driver,frame)
            while True:
                element = self.return_element(driver=driver,frame=frame,id=data_list[0],type=type)
                select = Select(element)
                if select.first_selected_option.text != str(data_list[2]):
                    print('selecionando novamente')
                    select.select_by_value(data_list[1])
                elif select.first_selected_option.text == str(data_list[2]):
                    break
            return True
        except Exception as e:
            print(f'erro {e}')
            return False

    def insere_dados_funcionario(self,driver,frame,id_list,data_list,type):
        try:
            self.frame_switch(driver,frame)
            for i in range(0,2):
                element = self.return_element(driver=driver,frame=frame,id=id_list[i],type=type)
                while str(element.get_attribute('value')) != str(data_list[i]):
                    element.clear()
                    element.send_keys(f'{data_list[i]}')
            return True
        except Exception as e:
            print(f'erro {e}')
            return False
    
    def execute_pesquisa(self, driver, frame):
        self.frame_switch(driver,frame)        
        try:
            driver.execute_script("javascript:doAcao('browse');")
            return True
        except Exception as e:
            return False
    
    def funcionario_link_text(self,driver,frame,data_list,type):
        self.frame_switch(driver=driver,frame=frame)
        try:
            element = self.return_element(driver=driver,frame=frame,id=data_list,type=type)
            if element != False:
                self.funcionario_link = element.get_attribute('href')
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False        
    
    def execute_script(self,driver,frame,script):
        self.frame_switch(driver=driver, frame=frame) if frame is not None else None
        try:
            driver.execute_script(script)
            return True
        except Exception as e:
            print(e)
            return False        

    def await_element(self,driver,frame,id,type, timeout=10):
        self.frame_switch(driver=driver,frame=frame)
        try:
            element_presence = self.presenceWait(driver=driver,element=id,type=type,timeout=timeout)
            if element_presence != True:
                return False
            element = self.return_element(driver=driver,frame=frame,id=id,type=type)
            if element != False:
                return True
            else:
                return False
            
        except Exception as e:
            print(e)
            return False  
    
    def selecionar_combo_tipo_exame(self,frame,driver,data_list,type):
        try:
            #self.frame_switch(driver,frame)
            while True:
                driver.switch_to.default_content()
                driver.switch_to.frame('socframe')
                time.sleep(5)
                element = driver.find_element(By.ID, 'tipoExame')
                #driver.execute_script(f"document.getElementById('tipoExame').value = '{data_list[1]}'")
                select = Select(element)
                element = driver.find_element(By.ID, 'tipoExame')
                element_value = driver.execute_script('return arguments[0].value', element)
                element_value = int(element_value)
                if int(element_value) != int(data_list[1]):
                    print('selecionando novamente')
                    select.select_by_value(str(data_list[1]))
                elif element_value == data_list[1]:
                    break
            return True
        except Exception as e:
            print(f'erro {e}')
            return False
    
    def insere_data(self,driver,frame,id_list,data_list,type):
        try:
            self.frame_switch(driver,frame)
            element = self.return_element(driver=driver,frame=frame,id=id_list[0],type=type)
            while str(element.get_attribute('value')) != str(data_list[1]):
                element.clear()
                element.send_keys(f'{data_list[1]}')
            return True
        except Exception as e:
            print(f'erro {e}')
            return False

    def insere_hora(self,driver,frame,id_list,data_list,type):
        try:
            self.frame_switch(driver,frame)
            element = self.return_element(driver=driver,frame=frame,id=id_list[0],type=type)
            while str(element.get_attribute('value')) != str(data_list[1]):
                element.clear()
                element.send_keys(f'{data_list[1]}')
            return True
        except Exception as e:
            print(f'erro {e}')
            return False
    
    def recebe_id_prestador(self, driver, frame,id_list):
        try:
            self.frame_switch(driver,frame)
            elements = driver.find_elements(By.TAG_NAME, id_list[0])
            for item in elements:
                if str(item.get_attribute('href')).__contains__('limpaCamposPrestador') == True and str(item.get_attribute('href')).__contains__('Socnet') == False:
                    variable_id = str(item.get_attribute('href'))
            self.variable_id_split = variable_id.split("'")
        except Exception as e:
            print(e)
            return False
        
    def insere_prestador(self, driver, frame,id_list,type):
        try:
            self.frame_switch(driver,frame)
            id_prestador = str(id_list[1])
            element = self.return_element(driver=driver,frame=frame,id=id_list[0],type=type)
            while element.get_attribute('value') != id_prestador:
                driver.execute_script(f"arguments[0].setAttribute('value','{id_prestador}')", element)
                if element.get_attribute('value') == id_prestador:
                    break
        except Exception as e:
            print(f'erro {e}')
    
    def select_window(self, driver):
        try:
            self.windows = driver.window_handles
            if len(self.windows) < 2:
                return False
            else:
                driver.switch_to.window(self.windows[1])
                return True
        except Exception as e:
            print(e)
            return False
    
    #def salva o arquivo temporário no socged [realiza o upload do arquivo temporário no socged].
    #def atualiza o banco de dados com as informações do arquivo no scoged.
    
    def alert_accept(self, driver, frame, timeout=10):
        try:
            alert = WebDriverWait(driver, timeout).until(EC.alert_is_present())
            if alert:
                self.alert_text = alert.text
                alert.accept()
            return True
        except Exception as e:
            print(e)
            return False
     
    def return_element(self, driver, frame, id, type):
        self.frame_switch(driver,frame)
        try:
            if type == 'tag':
                element = driver.find_element(By.TAG_NAME, id)
            elif type == 'id':
                element = driver.find_element(By.ID, id)
            elif type == 'xpath':
                element = driver.find_element(By.XPATH, id)
            elif type == 'css':
                element = driver.find_element(By.CSS_SELECTOR, id)
            elif type == 'partial_link':
                element = driver.find_element(By.PARTIAL_LINK_TEXT, id)
            return element
        
        except Exception as e:
            print(e)
            return False
        
    def frame_switch(self, driver, frame):
        if frame == 'default':        
            driver.switch_to.default_content()
        else:
            driver.switch_to.default_content()
            driver.switch_to.frame(frame)
        return
    