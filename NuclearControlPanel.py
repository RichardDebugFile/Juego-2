import arcade

# Configuración básica de la ventana
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
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
        self.game_state = "running"  # Estados: "running", "game_over", "success"
        self.time_elapsed = 0
        self.current_step = 0  # Paso actual en la secuencia de apagado
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
        self.game_state = "running"
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

        if self.game_state == "running":
            # Dibujar marcadores
            arcade.draw_text(f"Nivel de agua: {self.water_level}%", 50, 500, arcade.color.WHITE, 16)
            arcade.draw_text(f"Temperatura: {self.temperature} °C", 50, 460, arcade.color.WHITE, 16)
            arcade.draw_text(f"Energía generada: {self.energy_level} MWe", 50, 420, arcade.color.WHITE, 16)
            arcade.draw_text(f"Tiempo restante: {max(0, GAME_TIME_LIMIT - self.time_elapsed):.1f} s", 50, 380, arcade.color.WHITE, 16)

            # Mostrar instrucción actual con el contador de clics
            progress = f"{self.action_counters[self.current_step]}/{self.get_required_clicks(self.current_step)}"
            arcade.draw_text(f"Instrucción: {self.current_instruction} ({progress})", 50, 340, arcade.color.YELLOW, 16)

            # Dibujar alertas de error si hay alguna
            if self.alert_message:
                arcade.draw_text(self.alert_message, 50, 300, arcade.color.RED, 16)

            # Dibujar botones para la secuencia correcta
            arcade.draw_rectangle_filled(200, 100, 120, 40, arcade.color.GRAY)
            arcade.draw_text("Detener Turbinas", 160, 90, arcade.color.BLACK, 12)

            arcade.draw_rectangle_filled(400, 100, 120, 40, arcade.color.GRAY)
            arcade.draw_text("Ventilar", 380, 90, arcade.color.BLACK, 12)

            arcade.draw_rectangle_filled(600, 100, 120, 40, arcade.color.GRAY)
            arcade.draw_text("Inyectar Agua", 560, 90, arcade.color.BLACK, 12)

            arcade.draw_rectangle_filled(200, 50, 120, 40, arcade.color.GRAY)
            arcade.draw_text("Evacuar Agua", 160, 40, arcade.color.BLACK, 12)

            arcade.draw_rectangle_filled(400, 50, 120, 40, arcade.color.GRAY)
            arcade.draw_text("Apagar Reactor", 360, 40, arcade.color.BLACK, 12)

            arcade.draw_rectangle_filled(600, 50, 120, 40, arcade.color.GRAY)
            arcade.draw_text("Emergencia", 570, 40, arcade.color.BLACK, 12)

        elif self.game_state == "game_over":
            # Dibujar la pantalla de Game Over
            arcade.draw_text("¡Game Over!", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, arcade.color.RED, 40)
            arcade.draw_rectangle_filled(300, 200, 120, 40, arcade.color.GRAY)
            arcade.draw_text("Reiniciar", 270, 190, arcade.color.BLACK, 14)

            arcade.draw_rectangle_filled(500, 200, 120, 40, arcade.color.GRAY)
            arcade.draw_text("Salir", 475, 190, arcade.color.BLACK, 14)

        elif self.game_state == "success":
            # Dibujar la pantalla de éxito
            arcade.draw_text("¡Lograste desactivar el reactor!", SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 50, arcade.color.GREEN, 30)
            arcade.draw_rectangle_filled(300, 200, 120, 40, arcade.color.GRAY)
            arcade.draw_text("Reiniciar", 270, 190, arcade.color.BLACK, 14)

            arcade.draw_rectangle_filled(500, 200, 120, 40, arcade.color.GRAY)
            arcade.draw_text("Salir", 475, 190, arcade.color.BLACK, 14)

    def on_mouse_press(self, x, y, button, modifiers):
        """Detecta clics en los botones."""
        if self.game_state == "running":
            if 140 < x < 260 and 80 < y < 120:  # Detener Turbinas
                if self.current_step == 0:
                    self.action_counters[0] += 1
                    if self.action_counters[0] >= self.get_required_clicks(0):
                        self.current_step += 1
                        self.current_instruction = self.instructions[self.current_step]
                else:
                    self.alert_message = "Error: Paso incorrecto, sigue la instrucción."
                    self.alert_timer = 4  # Reiniciar temporizador a 4 segundos

            elif 340 < x < 460 and 80 < y < 120:  # Ventilar contenido radioactivo
                if self.current_step == 1:
                    self.action_counters[1] += 1
                    if self.action_counters[1] >= self.get_required_clicks(1):
                        self.current_step += 1
                        self.current_instruction = self.instructions[self.current_step]
                else:
                    self.alert_message = "Error: Paso incorrecto, sigue la instrucción."
                    self.alert_timer = 4

            elif 540 < x < 660 and 80 < y < 120:  # Inyectar agua fría
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

            elif 140 < x < 260 and 30 < y < 70:  # Evacuar agua caliente
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

            elif 340 < x < 460 and 30 < y < 70:  # Apagar reactor
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

            elif 540 < x < 660 and 30 < y < 70:  # Botón de emergencia
                if self.current_step == 5 and self.temperature == 0:
                    self.game_state = "success"
                else:
                    self.alert_message = "Error: La temperatura debe ser 0 antes de presionar el botón de emergencia."
                    self.alert_timer = 4

        elif self.game_state in ["game_over", "success"]:
            if 240 < x < 360 and 180 < y < 220:  # Reiniciar
                self.setup()
            elif 440 < x < 560 and 180 < y < 220:  # Salir
                arcade.close_window()

    def update(self, delta_time):
        """Actualiza el estado del sistema."""
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