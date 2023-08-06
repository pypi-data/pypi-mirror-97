PACS = {
    "PRUEBA": 0,
    "PRODIGIA": 1,
    "FINKOK": 2,
    "STOCONSULTING": 3,
    "DFACTURE": 4,
}

CHOICES_PACS = []
for nombre,valor in PACS.items():
	CHOICES_PACS.append((valor, nombre))

CLAVES_COMBUSTIBLE = ["15101506", "15101505", "15101509", "15101514", "15101515"]


ADDENDAS = (
    ("", "-------"),
    ("agnico", "Agnico Eagle"),
    ("ahmsa", "AHMSA"),
    ("coppel", "Coppel"),
    ("loreal", "Loreal"),
    ("multiasistencia", "Multiasistencia"),
    ("pemex", "Pemex"),
    ("lacomer", "Comercial Mexicana"),
)