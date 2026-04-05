import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
app = doc.Application

# --- CONFIGURACIÓN ---
ruta_txt = r"C:\Users\DELL\Documents\ALCABAMA\GENERAL\PARÁMETROS\PARAMETROS COMPARTIDOS.txt"
nombres_parametros = [
    "MATERIAL INTEGRADO", 
    "NIVEL INTEGRADO", 
    "SUBPROYECTOS INTEGRADO", 
    "AREA INTEGRADO", 
    "LONGITUD INTEGRADO", 
    "NOMBRE INTEGRADO", 
    "VOLUMEN INTEGRADO"
]

# 1. Cargar archivo de parámetros
app.SharedParametersFilename = ruta_txt
def_file = app.OpenSharedParameterFile()

if not def_file:
    OUT = "Error: No se pudo abrir el archivo de parámetros en la ruta especificada."
else:
    # 2. Preparar categorías
    cat_set = app.Create.NewCategorySet()
    for cat in doc.Settings.Categories:
        if cat.AllowsBoundParameters:
            cat_set.Insert(cat)

    # 3. Iniciar Transacción
    TransactionManager.Instance.EnsureInTransaction(doc)
    
    resultados = []
    
    try:
        for nombre in nombres_parametros:
            param_def = None
            # Buscar el parámetro en cualquier grupo del archivo TXT
            for group in def_file.Groups:
                # CAMBIO CLAVE: Se usa get_Item(nombre) para CPython3
                param_def = group.Definitions.get_Item(nombre)
                if param_def: break
            
            if param_def:
                binding = app.Create.NewInstanceBinding(cat_set)
                # Agrupado en Datos de Identidad (PG_IDENTITY_DATA)
                doc.ParameterBindings.Insert(param_def, binding, BuiltInParameterGroup.PG_IDENTITY_DATA)
                resultados.append("Éxito: " + nombre)
            else:
                resultados.append("No encontrado en TXT: " + nombre)
        
        out_msg = "\n".join(resultados)
    except Exception as e:
        out_msg = "Error: " + str(e)

    TransactionManager.Instance.TransactionTaskDone()
    OUT = out_msg
