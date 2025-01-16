import arcade

# Configuración básica de la ventana
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 670
SCREEN_TITLE = "Simulación de Central Nuclear"

# Variables de estado del sistema
water_level = 50  # Nivel de agua (0 a 100)
temperature = 100  # Temperatura del reactor en °C
energy_level = 10  # Nivel de energía generada en MWe
MAX_TEMPERATURE = 400
MIN_WATER_LEVEL = 10
GAME_TIME_LIMIT = 30  # Límite de tiempo en segundos

class NuclearControlPanel(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.DARK_SLATE_BLUE)
        # Cargar la imagen de fondo
        self.start_background = arcade.load_texture("imagenes/fondoInicio.jpg")
        self.background = arcade.load_texture("imagenes/Panel2.jpg")
        
        self.game_state = "start"  # Estados: "running", "game_over", "success"
        self.time_elapsed = 0
        self.current_step = 0
        self.countdown_timer = 5  # Temporizador para la cuenta regresiva

        # Cargar la fuente personalizada
        arcade.load_font("Fuente/Minecraft.ttf")
        self.font = "Minecraft"  # Nombre del archivo sin la extensión

        self.instructions = [
            "1. Detener turbinas",
            "2. Ventilar contenido radioactivo",
            "3. Inyectar agua fría",
            "4. Evacuar agua caliente",
            "5. Apagar el reactor",
            "6. Presionar el botón de emergencia"
        ]
        self.current_instruction = self.instructions[self.current_step]
        self.action_counters = [0] * len(self.instructions)  # Contadores para cada acción
        self.reactor_active = True  # Indica si el reactor sigue activo
        self.temperature_decreasing = False  # Indica si la temperatura está disminuyendo
        self.alert_message = ""
        self.alert_timer = 0  # Temporizador para el mensaje de error

    def setup(self):
        """Configura el estado inicial del sistema."""
        self.water_level = water_level
        self.temperature = temperature
        self.energy_level = energy_level
        self.alert_message = ""
        self.alert_timer = 0
        self.time_elapsed = 0
        #self.game_state = "running"
        self.current_step = 0
        self.current_instruction = self.instructions[self.current_step]
        self.action_counters = [0] * len(self.instructions)
        self.reactor_active = True
        self.temperature_decreasing = False

    def get_required_clicks(self, step):
        """Devuelve el número de clics necesarios para completar el paso actual."""
        required_clicks = [3, 2, 5, 10, 1, 1]  # Clics necesarios por instrucción
        return required_clicks[step]

    def on_draw(self):
        """Dibuja la interfaz gráfica."""
        arcade.start_render()

        if self.game_state == "start":
        # Pantalla de inicio
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.start_background)

            # Dibuja el rectángulo de difuminado
            arcade.draw_rectangle_filled(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                SCREEN_WIDTH,
                SCREEN_HEIGHT,
                (0, 0, 0, 200)  # Negro con 150 de transparencia
            )
            
            story_text_lines = [
                "El personal de limpieza se ha quedado encerrado dentro de la sala de control",
                "de una central nuclear, oculta en unas remotas estepas siberianas, a causa de",
                "una peligrosa invasión zombie.", 
                 "",
                "Un valiente barrendero es el único que puede",
                "detener la peligrosa reacción del núcleo de la central, desencadenada debido",
                "al caos que reina en la instalación.",
                "",
                "El intrépido personal de limpieza se acerca al panel de control de la central",
                "y debe entender claramente lo que debe hacer para apagar el sistema de reacción",
                "y generación de energía de la central; de lo contrario, la inminente explosión",
                "empeorará el ataque zombie, produciendo criaturas radioactivas."
            ]

            # Dibuja cada línea del texto, con un espaciado vertical entre ellas
            y_position = SCREEN_HEIGHT - 100
            for line in story_text_lines:
                arcade.draw_text(
                    line,
                    start_x=0,
                    start_y=y_position,
                    color=arcade.color.WHITE,
                    font_size=13,
                    font_name=self.font,
                    width=SCREEN_WIDTH,  # Ajusta el texto al ancho de la ventana
                    align="center"
                )
                y_position -= 25  # Espaciado entre líneas

            # Añadir texto grande debajo de la historia
            arcade.draw_text(
                "¡ESTÁ EN TUS MANOS SALVAR A TODOS!",
                start_x=0,  # Inicia en 0
                start_y=y_position - 50,  # Colocar debajo de la última línea de la historia
                color=arcade.color.YELLOW,
                font_size=20,  # Tamaño de fuente mayor
                font_name=self.font,
                width=SCREEN_WIDTH,  # Ajusta el texto al ancho de la ventana
                align="center"  # Centra el texto horizontalmente
            )

            # Botones de "Empezar" y "Salir"
            arcade.draw_rectangle_filled(300, 120, 120, 40, arcade.color.GRAY)
            arcade.draw_text("Empezar", 265, 110, arcade.color.BLACK, 14, font_name=self.font)
            arcade.draw_rectangle_filled(500, 120, 120, 40, arcade.color.GRAY)
            arcade.draw_text("Salir", 475, 110, arcade.color.BLACK, 14, font_name=self.font)

        elif self.game_state == "countdown":
                # Pantalla de cuenta regresiva
                arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.start_background)

                # Dibuja el rectángulo de difuminado
                arcade.draw_rectangle_filled(
                    SCREEN_WIDTH // 2,
                    SCREEN_HEIGHT // 2,
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT,
                    (0, 0, 0, 150)  # Negro con 150 de transparencia
                )

                
                # Texto del temporizador
                arcade.draw_text(
                    f"Comenzando en: {int(self.countdown_timer)}",
                    start_x=0,
                    start_y=SCREEN_HEIGHT // 2,
                    color=arcade.color.YELLOW,
                    font_size=40,
                    font_name=self.font,
                    width=SCREEN_WIDTH,
                    align="center"
                )
                
                 # Dividir el texto en dos líneas y centrarlas
                instruction_line_1 = "Sigue las instrucciones del panel pequeño de arriba para salir de aquí."
                instruction_line_2 = "¡Buena suerte!"

                # Primera línea centrada
                arcade.draw_text(
                    instruction_line_1,
                    start_x=0,
                    start_y=SCREEN_HEIGHT // 2 - 30,  # Posicionar debajo del temporizador
                    color=arcade.color.WHITE,
                    font_size=14,
                    font_name=self.font,
                    width=SCREEN_WIDTH,  # Centrar en el ancho de la pantalla
                    align="center"
                )

                # Segunda línea centrada
                arcade.draw_text(
                    instruction_line_2,
                    start_x=0,
                    start_y=SCREEN_HEIGHT // 2 - 60,  # Posicionar debajo de la primera línea
                    color=arcade.color.WHITE,
                    font_size=14,
                    font_name=self.font,
                    width=SCREEN_WIDTH,  # Centrar en el ancho de la pantalla
                    align="center"
                )

        else:   

            # Dibujar la imagen de fondo ajustada al tamaño de la ventana
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

            if self.game_state == "running":
                # Dibujar marcadores con salto de línea
                arcade.draw_text("Nivel de agua:", 290, 560, arcade.color.WHITE, 11, font_name=self.font)
                arcade.draw_text(f"{self.water_level}%", 315, 525, arcade.color.WHITE, 19, font_name=self.font)

                arcade.draw_text("Temperatura:", 450,  560, arcade.color.WHITE, 12, font_name=self.font)
                arcade.draw_text(f"{self.temperature} °C", 465, 525, arcade.color.WHITE, 19, font_name=self.font)

                arcade.draw_text("Energía (MWe):", 285, 460, arcade.color.WHITE, 11, font_name=self.font)
                arcade.draw_text(f"{self.energy_level} MWe", 295, 425, arcade.color.WHITE, 18, font_name=self.font)

                arcade.draw_text("Tiempo restante:", 625, 195, arcade.color.BLACK, 14, font_name=self.font)
                arcade.draw_text(f"{max(0, GAME_TIME_LIMIT - self.time_elapsed):.1f} s", 665, 155, arcade.color.BLACK, 24, font_name=self.font)

                # Mostrar instrucción actual con el contador de clics
                progress = f"{self.action_counters[self.current_step]}/{self.get_required_clicks(self.current_step)}"
                arcade.draw_text(f"Instrucción: {self.current_instruction} ({progress})", 50, 612, arcade.color.YELLOW, 13, font_name=self.font)

                arcade.draw_rectangle_filled(405, 72, 615, 30, arcade.color.ORANGE)

                # Dibujar alertas de error si hay alguna
                if self.alert_message:
                    arcade.draw_text(self.alert_message, 105, 60, arcade.color.RED, 12, font_name=self.font) 

                # Dibujar botones para la secuencia correcta
                arcade.draw_rectangle_filled(130, 355, 180, 70, arcade.color.GRAY)
                arcade.draw_text("Detener Turbinas", 50, 345, arcade.color.BLACK, 14, font_name=self.font)

                arcade.draw_rectangle_filled(365, 355, 180, 70, arcade.color.GRAY)
                arcade.draw_text("Ventilar", 310, 335, arcade.color.BLACK, 22, font_name=self.font)

                arcade.draw_rectangle_filled(130, 270, 185, 65, arcade.color.GRAY)
                arcade.draw_text("Inyectar Agua", 55, 253, arcade.color.BLACK, 16, font_name=self.font)

                arcade.draw_rectangle_filled(365, 268, 183, 67, arcade.color.GRAY)
                arcade.draw_text("Evacuar Agua", 287, 250, arcade.color.BLACK, 17, font_name=self.font)

                arcade.draw_rectangle_filled(130, 183, 184, 72, arcade.color.GRAY)
                arcade.draw_text("Apagar Reactor", 55, 170, arcade.color.BLACK, 14, font_name=self.font)

                arcade.draw_rectangle_filled(363, 183, 184, 70, arcade.color.RED)
                arcade.draw_text("Emergencia", 290, 166, arcade.color.WHITE, 19, font_name=self.font)

            elif self.game_state in ["game_over", "success"]:
            # Dibujar capa de difuminado
                arcade.draw_rectangle_filled(
                    SCREEN_WIDTH // 2,
                    SCREEN_HEIGHT // 2,
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT,
                    (0, 0, 0, 150)  # Color negro con alfa 150 (transparencia)
                )

            if self.game_state == "game_over":
                # Dibujar la pantalla de Game Over
                arcade.draw_text(
                    "¡Game Over!", 230, 400,
                    arcade.color.RED, 40, font_name=self.font
                )
                arcade.draw_rectangle_filled(300, 280, 120, 40, arcade.color.GRAY)
                arcade.draw_text("Reiniciar", 260, 270, arcade.color.BLACK, 14, font_name=self.font)

                arcade.draw_rectangle_filled(500, 280, 120, 40, arcade.color.GRAY)
                arcade.draw_text("Salir", 475, 270, arcade.color.BLACK, 14, font_name=self.font)

            elif self.game_state == "success":
                # Dibujar la pantalla de éxito
                arcade.draw_text(
                    "¡Lograste desactivar el reactor!", 90, 400,
                    arcade.color.GREEN, 30, font_name=self.font
                )
                arcade.draw_rectangle_filled(300, 280, 120, 40, arcade.color.GRAY)
                arcade.draw_text("Reiniciar", 260, 270, arcade.color.BLACK, 14, font_name=self.font)
                arcade.draw_rectangle_filled(500, 280, 120, 40, arcade.color.GRAY)
                arcade.draw_text("Salir", 475, 270, arcade.color.BLACK, 14, font_name=self.font)
            
            super().on_draw()


    def on_mouse_press(self, x, y, button, modifiers):
        """Detecta clics en los botones."""


        if self.game_state == "start":
            # Botón "Empezar"
            if 240 < x < 360 and 100 < y < 140:
                self.game_state = "countdown"
            # Botón "Salir"
            elif 440 < x < 560 and 100 < y < 140:
                arcade.close_window()

        if self.game_state == "running":
            if 40 < x < 220 and 320 < y < 390:  # Detener Turbinas
                if self.current_step == 0:
                    self.action_counters[0] += 1
                    if self.action_counters[0] >= self.get_required_clicks(0):
                        self.current_step += 1
                        self.current_instruction = self.instructions[self.current_step]
                else:
                    self.alert_message = "Error: Paso incorrecto, sigue la instrucción."
                    self.alert_timer = 4  # Reiniciar temporizador a 4 segundos

            elif 275 < x < 455 and 320 < y < 390:  # Ventilar contenido radioactivo
                if self.current_step == 1:
                    self.action_counters[1] += 1
                    if self.action_counters[1] >= self.get_required_clicks(1):
                        self.current_step += 1
                        self.current_instruction = self.instructions[self.current_step]
                else:
                    self.alert_message = "Error: Paso incorrecto, sigue la instrucción."
                    self.alert_timer = 4

            elif 40 < x < 225 and 235 < y < 300:  # Inyectar agua fría
                if self.current_step == 2:
                    self.water_level = min(100, self.water_level + 10)
                    self.temperature = max(50, self.temperature - 5)
                    self.action_counters[2] += 1
                    if self.water_level >= 100:
                        self.current_step += 1
                        self.current_instruction = self.instructions[self.current_step]
                else:
                    self.alert_message = "Error: Paso incorrecto, sigue la instrucción."
                    self.alert_timer = 4

            elif 275 < x < 458 and 230 < y < 295:  # Evacuar agua caliente
                if self.current_step == 3:
                    self.water_level = max(0, self.water_level - 10)
                    self.action_counters[3] += 1
                    if self.water_level <= 0:
                        self.current_step += 1
                        self.current_instruction = self.instructions[self.current_step]
                        self.temperature_decreasing = True  # Iniciar la disminución de temperatura
                else:
                    self.alert_message = "Error: Paso incorrecto, sigue la instrucción."
                    self.alert_timer = 4

            elif 40 < x < 224 and 145 < y < 215:  # Apagar reactor
                if self.current_step == 4:
                    self.action_counters[4] += 1
                    if self.action_counters[4] >= 1:
                        self.energy_level = 0  # Detener generación de energía
                        self.current_step += 1
                        self.current_instruction = self.instructions[self.current_step]
                        self.reactor_active = False  # Desactivar el reactor
                        self.temperature_decreasing = True  # Continuar disminuyendo la temperatura
                else:
                    self.alert_message = "Error: Paso incorrecto, sigue la instrucción."
                    self.alert_timer = 4

            elif 275 < x < 458 and 145 < y < 215:  # Botón de emergencia
                if self.current_step == 5 and self.temperature == 0:
                    self.game_state = "success"
                else:
                    self.alert_message = "Error: La temperatura debe ser 0 antes de presionar el botón de emergencia."
                    self.alert_timer = 4

        elif self.game_state in ["game_over", "success"]:
            if 240 < x < 360 and 260 < y < 300:  # Reiniciar
                self.setup()
                self.game_state = "running"  # Cambia el estado del juego a "running"
            elif 440 < x < 560 and 260 < y < 300:  # Salir
                arcade.close_window()

    def update(self, delta_time):
        """Actualiza el estado del sistema."""

        if self.game_state == "countdown":
            self.countdown_timer -= delta_time
            if self.countdown_timer <= 0:
                self.countdown_timer = 0
                self.game_state = "running"
                self.setup()

        if self.game_state == "running":
            self.time_elapsed += delta_time

            if self.alert_timer > 0:
                self.alert_timer -= delta_time
                if self.alert_timer <= 0:
                    self.alert_message = ""

            if self.time_elapsed >= GAME_TIME_LIMIT:
                self.game_state = "game_over"

            if self.reactor_active:
                if self.water_level > MIN_WATER_LEVEL:
                    self.temperature += 1
                else:
                    self.temperature += 5

            if not self.reactor_active:
                self.energy_level = 0

            if self.temperature_decreasing and self.temperature > 0:
                self.temperature -= 1  # Reducir temperatura gradualmente
                if self.temperature <= 0:
                    self.temperature = 0
                    self.temperature_decreasing = False  # Detener la disminución de temperatura cuando llegue a 0

# Ejecutar la aplicación
if __name__ == "__main__":
    window = NuclearControlPanel()
    window.setup()
    arcade.run()
