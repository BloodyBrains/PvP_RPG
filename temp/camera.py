class Camera:
    pos = (0, 0)
    x_speed = 0
    y_speed = 0

    @classmethod
    def update(cls):
        """Moves the camera.
        """
        cls.pos = (cls.pos[0] + cls.x_speed, cls.pos[1] + cls.y_speed)