import pandas as pd


MODEL_COLUMNS = [
    "number_of_items",
    "number_of_products",
    "number_of_sellers",
    "total_price",
    "total_freight",
    "total_product_weight",
    "total_product_volume",
    "total_payment_value",
    "max_payment_installments",
    "number_of_payments",
    "order_purchase_hour",
    "order_purchase_day_of_week",
    "order_purchase_month",
    "order_purchase_year",
    "order_approval_delay_hours",
    "estimated_delivery_days",
    "customer_state",
    "seller_state",
    "payment_type",
    "product_category_name"
]
category_mapping = {
    # Home & Furniture
    "moveis_decoracao": "Home & Furniture",
    "cama_mesa_banho": "Home & Furniture",
    "utilidades_domesticas": "Home & Furniture",
    "moveis_escritorio": "Home & Furniture",
    "moveis_cozinha_area_de_servico_jantar_e_jardim": "Home & Furniture",
    "casa_conforto": "Home & Furniture",
    "moveis_sala": "Home & Furniture",
    "moveis_quarto": "Home & Furniture",
    "casa_conforto_2": "Home & Furniture",
    "moveis_colchao_e_estofado": "Home & Furniture",

    # Home Appliances
    "eletrodomesticos": "Home Appliances",
    "portateis_casa_forno_e_cafe": "Home Appliances",
    "eletroportateis": "Home Appliances",
    "eletrodomesticos_2": "Home Appliances",
    "portateis_cozinha_e_preparadores_de_alimentos": "Home Appliances",
    "climatizacao": "Home Appliances",

    # Electronics & Computers
    "eletronicos": "Electronics & Computers",
    "informatica_acessorios": "Electronics & Computers",
    "audio": "Electronics & Computers",
    "pcs": "Electronics & Computers",
    "pc_gamer": "Electronics & Computers",
    "tablets_impressao_imagem": "Electronics & Computers",

    # Telephony
    "telefonia": "Telephony",
    "telefonia_fixa": "Telephony",

    # Fashion
    "fashion_bolsas_e_acessorios": "Fashion",
    "fashion_underwear_e_moda_praia": "Fashion",
    "fashion_roupa_masculina": "Fashion",
    "fashion_calcados": "Fashion",
    "fashion_roupa_feminina": "Fashion",
    "fashion_esporte": "Fashion",
    "fashion_roupa_infanto_juvenil": "Fashion",
    "malas_acessorios": "Fashion",

    # Beauty & Personal Care
    "perfumaria": "Beauty & Personal Care",
    "beleza_saude": "Beauty & Personal Care",
    "fraldas_higiene": "Beauty & Personal Care",

    # Sports & Leisure
    "esporte_lazer": "Sports & Leisure",
    "consoles_games": "Sports & Leisure",
    "instrumentos_musicais": "Sports & Leisure",
    "cool_stuff": "Sports & Leisure",

    # Books & Media
    "livros_tecnicos": "Books & Media",
    "livros_interesse_geral": "Books & Media",
    "livros_importados": "Books & Media",
    "musica": "Books & Media",
    "cds_dvds_musicais": "Books & Media",
    "dvds_blu_ray": "Books & Media",

    # Baby & Kids
    "bebes": "Baby & Kids",
    "brinquedos": "Baby & Kids",

    # Tools & Construction
    "ferramentas_jardim": "Tools & Construction",
    "construcao_ferramentas_construcao": "Tools & Construction",
    "construcao_ferramentas_iluminacao": "Tools & Construction",
    "construcao_ferramentas_jardim": "Tools & Construction",
    "construcao_ferramentas_seguranca": "Tools & Construction",
    "construcao_ferramentas_ferramentas": "Tools & Construction",
    "casa_construcao": "Tools & Construction",

    # Food & Beverages
    "alimentos": "Food & Beverages",
    "alimentos_bebidas": "Food & Beverages",
    "bebidas": "Food & Beverages",

    # Automotive
    "automotivo": "Automotive",

    # Pets
    "pet_shop": "Pets",

    # Agriculture & Garden
    "agro_industria_e_comercio": "Agriculture & Garden",
    "flores": "Agriculture & Garden",

    # Office, Arts & Services
    "papelaria": "Office, Arts & Services",
    "industria_comercio_e_negocios": "Office, Arts & Services",
    "artigos_de_festas": "Office, Arts & Services",
    "artes": "Office, Arts & Services",
    "cine_foto": "Office, Arts & Services",
    "artes_e_artesanato": "Office, Arts & Services",
    "relogios_presentes": "Office, Arts & Services",
    "market_place": "Office, Arts & Services",
    "seguros_e_servicos": "Office, Arts & Services",
    "artigos_de_natal": "Office, Arts & Services",
    "la_cuisine": "Office, Arts & Services",
}

def create_prediction_features(data: dict) -> pd.DataFrame:

    df = pd.DataFrame([data])

    # Convert timestamps
    df["order_purchase_timestamp"] = pd.to_datetime(
        df["order_purchase_timestamp"]
    )

    df["order_approved_at"] = pd.to_datetime(
        df["order_approved_at"]
    )

    df["order_estimated_delivery_date"] = pd.to_datetime(
        df["order_estimated_delivery_date"]
    )

    # Timestamp features
    
    df["order_purchase_hour"] = (
        df["order_purchase_timestamp"].dt.hour
    )

    df["order_purchase_day_of_week"] = (
        df["order_purchase_timestamp"].dt.dayofweek
    )

    df["order_purchase_month"] = (
        df["order_purchase_timestamp"].dt.month
    )

    df["order_purchase_year"] = (
        df["order_purchase_timestamp"].dt.year
    )

    # Approval delay
   
    df["order_approval_delay_hours"] = (
        (
            df["order_approved_at"]
            - df["order_purchase_timestamp"]
        )
        .dt.total_seconds()
        / 3600
    )

    # Estimated delivery duration
    
    df["estimated_delivery_days"] = (
        (
            df["order_estimated_delivery_date"]
            - df["order_purchase_timestamp"]
        )
        .dt.total_seconds()
        / 86400
    )
    df["product_category_name"] = df["product_category_name"].map(
    category_mapping
    )

    # Return only model features
    return df[MODEL_COLUMNS]