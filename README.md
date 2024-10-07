# ASTRO·SHAPE

**Descripción**  
*ASTRO·SHAPE* es un juego similar a *Hole in the Wall*, diseñado para ambientes de microgravedad, como estaciones espaciales, utilizando algoritmos de estimación de poses humanas. En el juego, se crea una silueta a partir de coordenadas predefinidas y el objetivo es que los jugadores ajusten su pose para coincidir con la silueta proyectada. El sistema detecta si los jugadores están dentro de los límites de la silueta usando la cámara y algoritmos de visión por computadora.

**Beneficios en Microgravedad**  
El ambiente de microgravedad permite una mayor flexibilidad en la cantidad de poses que los astronautas pueden realizar, lo que potencia la interacción y la diversión del juego. Además, ayuda a mantener la actividad física, ya que los jugadores deben moverse para ajustar sus poses. Esto es crucial para contrarrestar los efectos de la microgravedad, como la pérdida de masa muscular y densidad ósea.

**Objetivo del Juego**  
El objetivo principal es promover la actividad física y la salud mental de los astronautas, mejorando la cohesión del equipo y proporcionando entretenimiento en misiones prolongadas. La naturaleza interactiva y físicamente exigente del juego contribuye a la resiliencia y adaptabilidad de los jugadores en entornos extraterrestres.

**Tecnologías Utilizadas**  
- *OpenCV*: Para procesamiento de video y manejo de la cámara.
- *Mediapipe*: Para la detección de poses humanas.
- *PySide6*: Para la interfaz gráfica.
- *Numpy*: Para operaciones de procesamiento numérico y visualización.
- *Pygame*: Para música de fondo y efectos visuales adicionales.

**Instrucciones de Instalación**  
1. Clona este repositorio:
    ```bash
    git clone https://github.com/tuusuario/astro-shape.git
    cd astro-shape
    ```

2. Instala las dependencias utilizando el archivo `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

3. Ejecuta la aplicación:
    ```bash
    python tracking.py
    ```
