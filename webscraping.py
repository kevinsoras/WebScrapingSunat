from selenium import webdriver
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import datetime
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

class DatosTabla:
  def __init__(self,Tipo, FechaEvento, FechaActualizacion,Afectacion,Carretera,Departamento,Provincia,Distrito,Latitud,Longitud,Evento,Fuente):
    self.Tipo = Tipo
    self.FechaEvento = FechaEvento
    self.FechaActualizacion = FechaActualizacion
    self.Afectacion = Afectacion
    self.Carretera = Carretera
    self.Departamento = Departamento
    self.Provincia = Provincia
    self.Distrito = Distrito
    self.Latitud = Latitud
    self.Longitud = Longitud
    self.Evento = Evento
    self.Fuente = Fuente
    
try:
    
    driver.set_page_load_timeout(4000)
    #driver.get("https://sweetalert2.github.io/")
    driver.get("http://gis.sutran.gob.pe/alerta_sutran/")
    time.sleep(60)
    #driver.maximize_window()
    ListElements = driver.find_element(By.CSS_SELECTOR, ".leaflet-marker-pane")
    if ListElements:
        print("")
    else :
        driver.refresh()
        time.sleep(60)
    
    #Click en elemento modal
    elements = ListElements.find_elements(By.CSS_SELECTOR, '.leaflet-marker-icon.leaflet-zoom-animated.leaflet-interactive')
    time.sleep(30)
    num=0
    numError=0
    dataExcel=[]
    for e in elements:
        #Se intenta dar click al div ,para cambiar el valor de la tabla
        try:
            if(e): 
                driver.execute_script ("arguments[0].click();",e)
                time.sleep(0.2) 
        except:
            numError=numError+1
        #div = driver.find_element(By.CSS_SELECTOR, ".leaflet-popup-content-wrapper")
        div = driver.find_element(By.CSS_SELECTOR, ".leaflet-pane.leaflet-popup-pane")
        textoTable=div.get_attribute('innerHTML')
        if len(textoTable) != 0:
            num=num+1
            #Obtención de la tabla
            table = driver.find_element(By.CSS_SELECTOR, ".leaflet-popup-content-wrapper")
            tr = table.find_elements(By.TAG_NAME, "tr")
            #Titulo de la tabla
            #Se elimina y asigna el primer elemento
            title=(tr.pop(0)).text
            #Se eliminan los últimos 2 elementos de la lista,
            #que representan 2 filas de datos no necesarios
            tr.pop()
            tr.pop()
            dataPart=[]
            dataPart.append(title)
            try:
                for i in tr:
                    td = i.find_elements(By.TAG_NAME, "td")
                    time.sleep(0.05) 
                    #Por que en un tr ,solo hay 2 td ,el primero es el titulo y el segundo su descripción
                    if len(td) >1 :
                        validarEntrada=0
                        nombreColumna=(td[0].text).replace(':', '')
                        datoColumna=td[1].text
                        if(nombreColumna == "Ubigeo"):
                            try :
                                arrUbigeo= datoColumna.split("/")
                                dataPart.append(arrUbigeo[0]) #Departamento
                                dataPart.append(arrUbigeo[1]) #Provincia 
                                dataPart.append(arrUbigeo[2]) #Distrito
                            except:
                                #En caso salga error la división de ubigeo ,se pondra igual en todos
                                dataPart.append(datoColumna)
                                dataPart.append(datoColumna)
                                dataPart.append(datoColumna)

                            validarEntrada=validarEntrada+1
                        if(nombreColumna == "Coordenada"):
                            try :
                                arrCoordenada= datoColumna.split(",")
                                dataPart.append(arrCoordenada[0]) #Latitud
                                dataPart.append(arrCoordenada[1]) #Longitud
                            except:
                                #En caso salga error la división de coordenada ,se pondra igual en todos
                                dataPart.append(datoColumna)
                                dataPart.append(datoColumna)

                            validarEntrada=validarEntrada+1
                        #En caso no haya entrado a ninguna condición se guarda el dato ,tal como esta    
                        if(validarEntrada==0):
                            dataPart.append(datoColumna)

                dataExcel.append(dataPart)
            except:

                print("Error en lectura de Tr de la tabla")        
               
    print(dataExcel)
    # Create the pandas DataFrame
    df = pd.DataFrame(dataExcel, columns=['Tipo', 'Fecha del evento','Fecha de actualización','Afectación','Carretera','Departamento','Provincia','Distrito','Latitud','Longitud','Evento','Fuente'])
    # print dataframe.
    print(df)
    print("succes:"+str(num))
    print("error:"+str(numError))
    print("elementRecolected:"+str(len(elements)))
    #Guardar en un excel el dataFrame
    fecha_actual = datetime.datetime.now()
    fecha_actual=fecha_actual.strftime('-Fecha-%d-%m-%Y-Hora-%H-%M')
    saveExcel= df.to_excel("SutranDatos"+fecha_actual+".xlsx")

except TimeoutException as ex:
    isrunning = 0
    print("Exception has been thrown. " + str(ex))
    driver.close()

driver.quit()