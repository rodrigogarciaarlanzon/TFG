import numpy as np
from scipy.stats import multivariate_normal


class AffiliatedObject:
    """
    Representa un objeto subastado en un entorno con afiliación entre valoraciones.

    Además del estado interno habitual de una subasta eBay reserve_price, min_increment,
    highest_bid, second_highest_bid, current_price, highest_bidder y buyers_count),
    este objeto incorpora atributos adicionales que permiten modelizar correlación entre
    valoraciones y señales públicas:

        - feature_vector: vector de características latentes asociado al objeto.
        - correlation_group: etiqueta que permite agrupar objetos con
          características correlacionadas.
        - latent_quality: calidad latente del objeto, generada como una
          combinación lineal del feature_vector más un término gaussiano.

    El objeto también registra información pública observable por los
    compradores durante la subasta:

        - observed_bids: historial de pujas observadas (ID del pujador,
              cantidad y orden temporal).
        - bidding_intensity: medida agregada de intensidad de puja basada
              en las pujas más recientes.

    Esta clase permite extender el mecanismo multiobjeto para estudiar
    entornos con afiliación.
    """

    def __init__(self, ID, reserve_price, min_increment,
                 feature_vector=None, correlation_group=0):
        """
        Inicializa un objeto con afiliación, extendiendo la lógica del
        objeto estándar de eBay Proxy Bidding.

        Args:
            ID (int)
            reserve_price (float)
            min_increment (float)
            feature_vector (np.ndarray | None): Vector de características latentes que generan
                    correlación entre objetos. Si es None, se genera aleatoriamente.
            correlation_group (int): Grupo de correlación al que pertenece el objeto
                    (permite modelizar clusters de afiliación).

        Se generan además:
            - latent_quality: calidad latente del objeto, como combinación
                    lineal del feature_vector más ruido gaussiano.
            - observed_bids: lista vacía para registrar pujas observadas.
            - bidding_intensity: intensidad inicial de puja (= 0).
    """
        self.ID = ID
        self.reserve_price = reserve_price
        self.min_increment = min_increment
        # Para afiliación
        self.feature_vector = feature_vector if feature_vector is not None else np.random.rand(3)
        self.correlation_group = correlation_group
        self.latent_quality = np.dot(self.feature_vector, [0.3, 0.34, 0.33]) + np.random.normal(0, 0.05) #parámetros random para determinar objetos similares: mayor correlación en calidad latente y menos ruido
        # Estado de subasta
        self.current_price = 0.0
        self.highest_bid = 0.0
        self.second_highest_bid = 0.0
        self.highest_bidder = None
        self.buyers_count = 0
        # Información pública para afiliación
        self.observed_bids = []
        self.bidding_intensity = 0.0

    def enter_price(self):

        if self.highest_bidder is None:
            return self.reserve_price
        else:
            return self.current_price + self.min_increment

    def registrar_puja(self, buyer, bid_max):
        """
        Registra una puja proxy en el objeto, extendiendo la lógica estándar
        del mecanismo eBay Proxy Bidding para incluir información pública relevante en entornos con afiliación.

        La puja se interpreta como la valoración máxima del comprador(bid_max). El mét0do:
            1. Comprueba si la puja alcanza el precio de entrada.Si no lo hace, se ignora.

            2. Registra información pública observable:
                    - ID del pujador
                    - cantidad ofertada
                    - orden temporal de la puja

            3. Actualiza la intensidad de puja (`bidding_intensity`) como la diferencia entre
               la media de las dos últimas pujas observadas y el current_price.

            4. Actualiza el estado interno del objeto siguiendo la lógica estándar del proxy bidding:
                    - actualización de highest_bid y second_highest_bid
                    - actualización del highest_bidder
                    - actualización del current_price

        Args:
            buyer (Buyer): comprador que realiza la puja.
            bid_max (float): valoración máxima declarada por el comprador.

        Returns:
            bool: True si la puja fue aceptada, False si fue ignorada.
        """
        enter_price = self.enter_price()
        if bid_max < enter_price:
            return False
        self.buyers_count += 1
        # Registrar información pública (para afiliación)
        self.observed_bids.append({'bidder': buyer.ID,'amount': bid_max,'time': len(self.observed_bids)})
        # Actualizar intensidad de puja
        if len(self.observed_bids) >= 2:
            recent = [b['amount'] for b in self.observed_bids[-2:]]
            self.bidding_intensity = np.mean(recent) - self.current_price
        # Actualización de pujas
        if self.highest_bidder is None:
            self.highest_bid = bid_max
            self.highest_bidder = buyer
            self.current_price = self.reserve_price
        else:
            if bid_max > self.highest_bid:
                self.second_highest_bid = self.highest_bid
                self.highest_bid = bid_max
                self.highest_bidder = buyer
            else:
                self.second_highest_bid = max(self.second_highest_bid, bid_max)
            self.current_price = min(self.highest_bid,
                                     self.second_highest_bid + self.min_increment)

        return True

    def get_public_info(self):
        """
        Devuelve la información pública observable por todos los compradores
        durante la subasta, relevante en entornos con afiliación.

        Returns:
            dict: Diccionario con:
                    - 'observed_bids': número total de pujas observadas.
                    - 'bidding_intensity': intensidad agregada de puja.
                    - 'current_price': precio visible actual.
                    - 'has_bids': True si el objeto tiene al menos una puja válida.
        """

        return {'observed_bids': len(self.observed_bids),'bidding_intensity': self.bidding_intensity,
            'current_price': self.current_price,'has_bids': self.highest_bidder is not None}


class AffiliatedBuyer:
    """
    Representa un comprador en un entorno con valoraciones afiliadas,
    Cada comprador posee un vector de valoraciones para los distintos
    objetos, cuya estructura depende del modelo de afiliación elegido:

            - common_value:
                Modelo de valor común V con señales privadas "ruidosas".
                Las valoraciones se generan como V + ε_i, truncadas a [0,1].

            - correlated_private:
                Valoraciones privadas correlacionadas entre objetos, generadas
                mediante una distribución normal multivariante con matriz de
                covarianzas decreciente en función de la distancia entre objetos.

            - independent:
                Valoraciones independientes ~ U(0,1), equivalente al modelo
                original sin afiliación.

    El comprador puede actualizar sus valoraciones durante la subasta utilizando información
    pública observable (pujas, intensidad de puja, precios de objetos similares), lo que permite
    modelizar aprendizaje y retroalimentación estratégica en entornos con afiliación.

    Atributos principales:
        - valuations: vector de valoraciones actuales.
        - original_valuations: copia de las valoraciones iniciales.
        - adjustment_history: historial de ajustes aplicados.
        - active_object: identificador del objeto en el que está compitiendo
            actualmente (None si no participa en ninguno).

    Esta clase permite estudiar cómo la afiliación entre valoraciones afecta al comportamiento
    estratégico y a los resultados del mecanismo multiobjeto.
    """

    def __init__(self, ID, n_objects,affiliation_strength=0.5, #fuerte afiliación
                 learning_rate=0.15,valuation_method = "common_value"): #por defecto
        """
        Inicializa un comprador con valoraciones afiliadas.

        Args:
            ID (str | int)
            n_objects (int)
            affiliation_strength (float): Intensidad con la que la información
                        pública afecta a las valoraciones del comprador.
            learning_rate (float): Velocidad de ajuste de las valoraciones.
            valuation_method (str): Mét0do de generación de valoraciones:
                    "common_value", "correlated_private" o "independent".

        Se generan las valoraciones iniciales mediante el mét0do especificado y se inicializa
        el estado interno del comprador.
        """
        self.ID = ID
        self.n_objects = n_objects
        self.affiliation_strength = affiliation_strength
        self.learning_rate = learning_rate
        self.valuation_method = valuation_method
        # Generar señales/valoraciones base
        self._generate_base_valuations()
        # Estado
        self.active_object = None
        # Para tracking
        self.original_valuations = self.valuations.copy()
        self.adjustment_history = []

    def _generate_base_valuations(self):
        """
        Genera las valoraciones iniciales del comprador según el modelo de afiliación seleccionado.
                - common_value:
                    Valor común V ~ N(0.5, 0.2) y señales privadas ε_i ~ N(0, 0.15).
                    Las valoraciones se truncan al intervalo [0,1].

                - correlated_private:
                    Valoraciones privadas correlacionadas generadas mediante una
                    distribución normal multivariante con matriz de covarianzas
                    decreciente en función de la distancia entre objetos.

                - independent:
                    Valoraciones independientes ~ U(0,1), equivalente al modelo
                    original sin afiliación.

        Las valoraciones generadas se almacenan en self.valuations.
        """
        if self.valuation_method == "common_value":
            # Modelo: Valor común V + señal privada
            V = np.random.normal(0.5, 0.15)  # Valor común
            self.common_value = V
            epsilon = np.random.normal(0, 0.1, self.n_objects)
            self.valuations = np.clip(V + epsilon, 0, 1)

        elif self.valuation_method == "correlated_private":
            # Valoraciones privadas correlacionadas
            corr = 0.8  # Correlación base
            cov_matrix = np.eye(self.n_objects) * 0.08
            for i in range(self.n_objects):
                for j in range(self.n_objects):
                    if i != j:
                        # Objetos cercanos más correlacionados
                        distance = abs(i - j)
                        cov_matrix[i, j] = 0.1 * corr * np.exp(-distance / 3) #mayor efecto de cercanía
            mean = np.full(self.n_objects, 0.5)
            self.valuations = np.clip(multivariate_normal.rvs(mean=mean, cov=cov_matrix),0, 1)

        elif self.valuation_method == "independent":
            self.valuations = np.random.uniform(0, 1, self.n_objects)

    def update_valuations(self, objects, market_info=None):
        """
        Actualiza las valoraciones del comprador utilizando información
        pública observable durante la subasta.

        Args:
            objects (list[AffiliatedObject]): Lista de objetos subastados.
            market_info (dict | None): Información adicional del mercado

        Comportamiento según el modelo de afiliación:

            - common_value:
                Si un objeto recibe pujas, la valoración aumenta en función
                de la intensidad de puja observada:
                        adjustment = learning_rate * bidding_intensity * affiliation_strength

            - correlated_private:
                La valoración de un objeto se ajusta hacia el precio medio de objetos similares
                (mismo correlation_group):
                        adjustment = learning_rate * (avg_price - current_price) * affiliation_strength

            - independent:
                No se realizan ajustes.

        Los ajustes se registran en adjustment_history y las nuevas
        valoraciones se truncan al intervalo [0,1].

        """
        if self.valuation_method == "independent":
            return  # No actualiza en modelo independiente

        new_valuations = self.valuations.copy()

        for obj_idx, obj in enumerate(objects):
            if obj.highest_bidder is not None:
                public_info = obj.get_public_info()
                if self.valuation_method == "common_value":
                    # Ajuste basado en pujas observadas
                    if public_info['observed_bids'] > 0:
                        # Si hay mucha actividad, incrementar valoración
                        adjustment = (self.learning_rate *public_info['bidding_intensity'] *self.affiliation_strength)
                        new_valuations[obj_idx] += adjustment
                elif self.valuation_method == "correlated_private":
                    # Ajuste basado en objetos similares
                    similar_objects = [o for o in objects if o.correlation_group == obj.correlation_group and o.ID != obj.ID]

                    if similar_objects:
                        similar_prices = [o.current_price for o in similar_objects if o.highest_bidder is not None]
                        if similar_prices:
                            avg_price = np.mean(similar_prices)
                            # Ajustar hacia el precio de objetos similares
                            price_diff = avg_price - obj.current_price
                            adjustment = (self.learning_rate * price_diff * self.affiliation_strength * 1.2)
                            new_valuations[obj_idx] += adjustment
        # Guardar historial y actualizar
        self.adjustment_history.append(new_valuations - self.valuations)
        self.valuations = np.clip(new_valuations, 0, 1)

    def puede_pujar(self, objeto):
        """
        Mismo mét0do utiliszado para el caso eBay multiple.
        """
        if objeto.highest_bidder is None:
            # Usar valoración para este objeto específico
            obj_idx = objeto.ID - 1 if hasattr(objeto, 'ID') else 0
            return self.valuations[obj_idx] >= objeto.reserve_price

        return self.valuations[objeto.ID - 1] >= objeto.current_price + objeto.min_increment

    def get_valuation_for_object(self, obj_id):
        """
        Devuelve la valoración actual del comprador para un objeto específico.

        Args:
            obj_id (int): Identificador del objeto (1-indexado).

        Returns:
            float: Valoración del comprador para ese objeto, o 0.0 si el identificador está fuera de rango.
        """

        idx = obj_id - 1 if isinstance(obj_id, int) else 0
        return self.valuations[idx] if idx < len(self.valuations) else 0.0