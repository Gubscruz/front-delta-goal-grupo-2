# Import your page modules
from .. import Jogos
from . import Dashboard_Cruzamentos, Dashboard_Quebra_de_Linha

pages = {
    "Jogos": Jogos,
    "Dashboard Cruzamentos": Dashboard_Cruzamentos,
    "Dashboard Quebra de Linha": Dashboard_Quebra_de_Linha
}
