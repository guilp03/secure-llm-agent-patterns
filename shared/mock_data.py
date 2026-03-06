# Dados fictícios da Livraria Page Turner

# Pedidos: order_id -> detalhes do pedido
ORDERS = {
    "1001": {"order_id": "1001", "status": "entregue", "title": "Dom Casmurro", "customer": "Ana Souza"},
    "1002": {"order_id": "1002", "status": "em trânsito", "title": "O Senhor dos Anéis", "customer": "Bruno Lima"},
    "1003": {"order_id": "1003", "status": "processando", "title": "1984", "customer": "Carla Mendes"},
    "1004": {"order_id": "1004", "status": "cancelado", "title": "Duna", "customer": "Diego Rocha"},
    "1005": {"order_id": "1005", "status": "em trânsito", "title": "Harry Potter e a Pedra Filosofal", "customer": "Elena Costa"},
}

# Livros: titulo -> detalhes do livro
BOOKS = {
    "Dom Casmurro": {"title": "Dom Casmurro", "category": "classicos", "price": 29.90, "available": True},
    "O Senhor dos Anéis": {"title": "O Senhor dos Anéis", "category": "fantasia", "price": 89.90, "available": True},
    "1984": {"title": "1984", "category": "ficcao_cientifica", "price": 39.90, "available": False},
    "Duna": {"title": "Duna", "category": "ficcao_cientifica", "price": 59.90, "available": True},
    "Harry Potter e a Pedra Filosofal": {"title": "Harry Potter e a Pedra Filosofal", "category": "fantasia", "price": 49.90, "available": True},
    "O Alquimista": {"title": "O Alquimista", "category": "autoajuda", "price": 34.90, "available": True},
    "Sapiens": {"title": "Sapiens", "category": "historia", "price": 54.90, "available": False},
}

# Categorias disponíveis na livraria
CATEGORIES = {
    "classicos": ["Dom Casmurro"],
    "fantasia": ["O Senhor dos Anéis", "Harry Potter e a Pedra Filosofal"],
    "ficcao_cientifica": ["1984", "Duna"],
    "autoajuda": ["O Alquimista"],
    "historia": ["Sapiens"],
}

# Frete por região (baseado no prefixo do CEP)
SHIPPING_BY_REGION = {
    "Sul": {"prefixes": ["80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "90", "91", "92", "93", "94", "95", "96", "97", "98", "99"], "rate": 15.00, "delivery_time": "3-5 dias"},
    "Sudeste": {"prefixes": ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49"], "rate": 12.00, "delivery_time": "2-4 dias"},
    "Norte": {"prefixes": ["66", "67", "68", "69", "76", "77", "78", "79"], "rate": 25.00, "delivery_time": "7-10 dias"},
    "Nordeste": {"prefixes": ["40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65"], "rate": 22.00, "delivery_time": "5-8 dias"},
    "Centro-Oeste": {"prefixes": ["70", "71", "72", "73", "74", "75", "76", "77", "78", "79"], "rate": 18.00, "delivery_time": "4-6 dias"},
}


def calculate_shipping(zip_code: str) -> dict:
    """Calcula o frete com base nos dois primeiros dígitos do CEP."""
    prefix = zip_code[:2]
    for region, data in SHIPPING_BY_REGION.items():
        if prefix in data["prefixes"]:
            return {"region": region, "rate": data["rate"], "delivery_time": data["delivery_time"]}
    # Região não mapeada — valor padrão
    return {"region": "Não identificada", "rate": 30.00, "delivery_time": "10-15 dias"}
