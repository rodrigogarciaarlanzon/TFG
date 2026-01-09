import numpy as np
from Class.Class_Multiple_Affiliated import AffiliatedObject, AffiliatedBuyer
from scipy.stats import multivariate_normal

def generate_correlated_features(m: int, correlation=0.85):
    """
    Genera vectores de características correlacionadas para los m objetos de una subasta con afiliación,
    destinados a capturar similitudes estructurales entre ellos.

    La función construye una matriz de covarianzas que induce distintos
    niveles de correlación entre objetos:

        - Objetos pertenecientes al mismo grupo (bloques de 3) presentan
            alta correlación: cov = 0.1 * correlation.

        - Objetos adyacentes presentan correlación media:
              cov = 0.1 * correlation * 0.5.

        - El resto de pares mantiene únicamente la varianza base (0.1).

    A partir de esta matriz de covarianzas, se generan 3 vectores de características
    mediante una distribución normal multivariante, que posteriormente se normalizan individualmente
    al intervalo [0,1].

    Args:
        m (int): Número total de objetos.
        correlation (float): Nivel de correlación base entre objetos
                pertenecientes al mismo grupo.

    Returns:
        np.ndarray:
            Matriz de dimensión (m, 3), donde cada fila corresponde al
            vector de características normalizado de un objeto.

    """
    # Crear matriz base diagonal. LA MATRIZ HA DE SER SIMÉTRICA DEFINIDA POSITIVA (scipy.stats.multivariate_normal.rvs())
    cov_matrix = np.eye(m) * 0.08
    # Primero construir una matriz simétrica
    for i in range(m):
        for j in range(i + 1, m):  # Solo la mitad superior
            # Objetos en el mismo grupo tienen alta correlación
            if i // 3 == j // 3:
                cov_value = 0.08 * correlation
            # Objetos adyacentes tienen correlación media
            elif abs(i - j) == 1:
                cov_value = 0.08 * correlation * 0.8
            else:
                cov_value = 0  # Sin correlación directa

            # Asignar a ambas posiciones para mantener simetría
            cov_matrix[i, j] = cov_value
            cov_matrix[j, i] = cov_value

    # Asegurar que la matriz sea semidefinida positiva
    # Mét0do: añadir una pequeña constante a la diagonal
    min_eig = np.min(np.real(np.linalg.eigvals(cov_matrix)))
    if min_eig < 0:
        cov_matrix += np.eye(m) * (-min_eig + 1e-8)

    mean = np.full(m, 0.5)

    # Generar características
    try:
        features = multivariate_normal.rvs(mean=mean, cov=cov_matrix, size=3).T
    except ValueError as e:
        print(f"Error con matriz de covarianza: {e}")
        print(f"m={m}, correlation={correlation}")
        print(f"min_eig={min_eig}")
        # Fallback: usar características independientes
        features = np.random.rand(m, 3)

    # Normalizar cada vector de características
    for i in range(m):
        min_val = features[i].min()
        max_val = features[i].max()
        features[i] = (features[i] - min_val) / (max_val - min_val + 1e-8)

    return features


def multiple_affiliated_arrival_order(n: int, m: int,valuation_method,affiliation_params=None):
    """
    Genera un conjunto de compradores afiliados y devuelve un orden de llegada
    aleatorio para ser utilizado en el mecanismo de subasta múltiple con afiliación.

    Para cada comprador i:
        - Se asigna un identificador único "ID{i}".
        - Se generan valoraciones para los m objetos según el modelo especificado en `valuation_method`:
                * "common_value": valor común + señales privadas ruidosas.
                * "correlated_private": valoraciones privadas correlacionadas.
                * "independent": valoraciones independientes ~ U(0,1).
        - Se inicializa un objeto `AffiliatedBuyer` con los parámetros adicionales
             proporcionados en `affiliation_params`.

    Los compradores se almacenan en un array de objetos y posteriormente se devuelve una
    permutación aleatoria del mismo, representando el orden de llegada efectivo en la subasta.

    Args:
        n (int): Número total de compradores a generar.
        m (int): Número total de objetos en subasta.
        valuation_method (str): Mét0do de generación de valoraciones.
        affiliation_params (dict | None): Parámetros adicionales para configurar el comportamiento
             afiliado del comprador (p. ej., affiliation_strength, learning_rate).

    Returns:
        np.ndarray:
            Array unidimensional de objetos `AffiliatedBuyer` permutado aleatoriamente,
            representando el orden de llegada.
    """
    if affiliation_params is None:
        affiliation_params = {}

    buyers_array = np.empty((0,), dtype=object)

    for i in range(n):
        buyer = AffiliatedBuyer(ID=f"ID{i + 1}",n_objects=m,valuation_method=valuation_method,**affiliation_params)
        buyers_array = np.append(buyers_array, buyer)
    return np.random.permutation(buyers_array)


def create_affiliated_objects(m, reserve_prices, min_increments,feature_correlation=0.85):
    """
    Crea una colección de objetos con características correlacionadas para ser utilizados
    en un mecanismo de subasta múltiple con afiliación.

    La función genera primero un conjunto de vectores de características correlacionadas mediante
    `generate_correlated_features`, donde la correlación entre objetos depende del parámetro
    `feature_correlation` y de la estructura de grupos (bloques de 3 objetos altamente
    correlacionados).

    Para cada objeto j:
        - Se asigna un identificador único ID = j + 1.
        - Se asignan su precio de reserva y su incremento mínimo.
        - Se asigna un vector de características correlacionadas.
        - Se determina su grupo de correlación como j // 3, de modo que
            cada grupo contiene 3 objetos con características similares.

    Cada objeto se instancia como `AffiliatedObject`, manteniendo la misma interfaz que los objetos estándar
    del mecanismo eBay Proxy Bidding, pero incorporando atributos adicionales para modelizar afiliación
        (feature_vector, correlation_group, latent_quality, etc.).

    Args:
        m (int)
        reserve_prices (list[float]): Lista de precios de reserva para
                cada objeto.
        min_increments (list[float]): Lista de incrementos mínimos de puja
                para cada objeto.
        feature_correlation (float): Nivel de correlación base entre
                características de objetos pertenecientes al mismo grupo.

    Returns:
        list[AffiliatedObject]: Lista de objetos con características correlacionadas y estado
            inicial listo para ser utilizado en el mecanismo de subasta múltiple con afiliación.
    """
    features = generate_correlated_features(m, feature_correlation)

    objetos = []
    for i in range(m):
        # Asignar grupo de correlación (cada 3 objetos en mismo grupo)
        correlation_group = i // 3
        obj = AffiliatedObject(ID=i + 1,reserve_price=reserve_prices[i],min_increment=min_increments[i],
            feature_vector=features[i],correlation_group=correlation_group)
        objetos.append(obj)
    return objetos


def ebay_affiliated_bidding_multiple(n: int, m: int,reserve_prices: list,min_increments: list,biders=None,
                                     valuation_method = "common_value",learning_rate=0.15,affiliation_strength=0.3,
                                     max_iter: int = 10000):
    """
    Implementa un mecanismo de Proxy Bidding para múltiples objetos en un
    entorno con valoraciones afiliadas, extendiendo la lógica del mecanismo
    eBay Proxy Bidding estándar.

    El algoritmo combina tres elementos clave:
        1. Compradores con valoraciones afiliadas (AffiliatedBuyer)
        2. Objetos con características correlacionadas (AffiliatedObject)
        3. Dinámica iterativa de entrada, salida y actualización de pujas

    Dinámica del mecanismo:
        - Cada comprador posee un vector de valoraciones para los m objetos, generado según
          el modelo de afiliación especificado:
                * "common_value": valor común + señales privadas ruidosas.
                * "correlated_private": valoraciones privadas correlacionadas.
                * "independent": valoraciones independientes ~ U(0,1).

        - En cada iteración:
            (Fase 1) Los compradores actualizan sus valoraciones utilizando información pública
                     observable (pujas, intensidad,precios de objetos similares).

            (Fase 2) Los compradores toman decisiones de puja:
                * Si están compitiendo en un objeto, verifican si su valoración actualizada sigue
                  superando el precio visible.
                * Si no están en ningún objeto, evalúan todos los objetos donde pueden pujar y
                  seleccionan aquel con mayor beneficio esperado (valoración − enter_price).

        - El proceso continúa hasta alcanzar un punto fijo (ningún comprador cambia de objeto) o hasta alcanzar `max_iter`.

    Args:
        n (int)
        m (int)
        reserve_prices (list[float])
        min_increments (list[float])
        biders (list | None): Orden de llegada opcional. Si es None, se generan compradores afiliados
          mediante `multiple_affiliated_arrival_order`.
        valuation_method (str): Mét0do de generación de valoraciones
        learning_rate (float): Tasa de aprendizaje en la actualización de valoraciones.
        affiliation_strength (float): Intensidad del efecto de afiliación.
        max_iter (int): Máximo número de iteraciones permitidas.

    Returns:
        list[AffiliatedObject]: Lista de objetos con su estado final tras la subasta, incluyendo
                ganador, precio final, historial de pujas e intensidad de puja.
    """
    # 1. Generar compradores afiliados
    if biders is None:
        biders = multiple_affiliated_arrival_order(n, m,valuation_method=valuation_method,affiliation_params={
                'learning_rate': learning_rate,'affiliation_strength': affiliation_strength})

    # 2. Crear objetos con características correlacionadas
    objetos = create_affiliated_objects(m, reserve_prices, min_increments)
    objetos_by_id = {obj.ID: obj for obj in objetos}

    # 3. Dinámica iterativa (similar a eBay Proxy Bidding Multiple)
    changed = True
    it = 0
    while changed and it < max_iter:
        changed = False
        it += 1

        # Fase 1: Actualizar valoraciones basadas en información pública
        for buyer in biders:
            buyer.update_valuations(objetos)

        # Fase 2: Tomar decisiones de puja
        for buyer in biders:
            # 2.1) Si está en un objeto, verificar si sigue siendo viable
            if buyer.active_object is not None:
                obj = objetos_by_id[buyer.active_object]
                # Usar valoración actualizada
                valuation = buyer.get_valuation_for_object(obj.ID)
                if valuation < obj.current_price:
                    # print(f"Buyer {buyer.ID} abandona Objeto {obj.ID}")
                    buyer.active_object = None
                    changed = True
            # 2.2) Si no está en ningún objeto, intentar entrar
            if buyer.active_object is None:
                # Buscar objetos donde puede pujar
                candidates = []
                for obj in objetos:
                    # Verificar con valoración actualizada
                    if buyer.puede_pujar(obj):
                        enter_price = obj.enter_price()
                        valuation = buyer.get_valuation_for_object(obj.ID)
                        expected_profit = valuation - enter_price

                        if expected_profit > 0:
                            candidates.append((obj, expected_profit))

                if candidates:
                    # Elegir objeto con mayor beneficio esperado
                    best_obj, _ = max(candidates, key=lambda x: x[1])
                    # Obtener valoración actual para este objeto
                    bid_amount = buyer.get_valuation_for_object(best_obj.ID)
                    # Registrar puja
                    success = best_obj.registrar_puja(buyer, bid_amount)
                    if success:
                        buyer.active_object = best_obj.ID
                        changed = True
    return objetos





# Función de conveniencia para mantener compatibilidad
def ebay_proxy_bidding_multiple_affiliated(*args, **kwargs):
    """
    Alias para mantener compatibilidad con el código de simulación.
    """
    return ebay_affiliated_bidding_multiple(*args, **kwargs)