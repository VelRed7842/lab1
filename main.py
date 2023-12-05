# pong.py
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty, StringProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout


class PongPaddle(Widget):
    score = NumericProperty(0)
    color = ListProperty([1, 1, 1, 1])  # Додано атрибут color

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    game_paused = False

    def update_score_labels(self):
        self.ids.player1_score.text = str(self.player1.score)
        self.ids.player2_score.text = str(self.player2.score)

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = Vector(vel[0], vel[1]).rotate(randint(0, 360))

    def update(self, dt):
        if not self.game_paused:
            self.ball.move()
            self.player1.bounce_ball(self.ball)
            self.player2.bounce_ball(self.ball)

            if (self.ball.y < 0) or (self.ball.top > self.height):
                self.ball.velocity_y *= -1

            if self.ball.x < self.x:
                self.player2.score += 1
                self.serve_ball(vel=(4, 0))

            if self.ball.x > self.width:
                self.player1.score += 1
                self.serve_ball(vel=(-4, 0))

    def on_size(self, *args):
        self.update_score_labels()

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y

        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y

    def start_game(self):
        if self.game_paused:
            self.game_paused = False
        else:
            self.ids.player1_score.text = '0'
            self.ids.player2_score.text = '0'
            self.player1.score = 0
            self.player2.score = 0
            self.serve_ball()
            self.game_paused = False

    def toggle_pause(self):
        self.game_paused = not self.game_paused

    def restart_game(self):
        self.start_game()

    def exit_game(self):
        App.get_running_app().stop()


class PongApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10)
        menu = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)

        start_button = Button(text='Restart', on_press=self.start_game, background_color=(0.1, 0.6, 0.1, 1))
        exit_button = Button(text='Exit', on_press=self.exit_game, background_color=(0.1, 0.6, 0.1, 1))

        menu.add_widget(start_button)
        menu.add_widget(exit_button)

        layout.add_widget(menu)

        self.game = PongGame()
        self.game.serve_ball()
        Clock.schedule_interval(self.game.update, 1.0 / 60)
        self.game.update_score_labels()
        layout.add_widget(self.game)

        return layout

    def start_game(self, instance):
        self.game.start_game()

    def exit_game(self, instance):
        App.get_running_app().stop()


if __name__ == '__main__':
    PongApp().run()
