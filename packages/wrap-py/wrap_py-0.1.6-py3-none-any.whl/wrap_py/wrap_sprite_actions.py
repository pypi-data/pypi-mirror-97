import time
import wrap_py

sprite = wrap_py.sprite


def _reset_global_interfaces():
    global sprite
    sprite = wrap_py.sprite


class wrap_sprite_actions():
    mult_fps = 100

    @staticmethod
    def _make_calls_with_delay(func, fixed_kwargs: dict, changing_kwargs: dict, time_ms: int, fps: int):
        """changing_kwargs:{
            "argname1":{
                start: int,
                stop: int
            }
        }
        """

        start_time = time.time()
        time_length = time_ms / 1000
        end_time = start_time + time_length

        step_delay = 1 / fps

        now = time.time()
        while now < end_time:

            # percent of time length passed
            passed_percent = (time.time() - start_time) / time_length

            # if all time passed - nothing to do here
            if passed_percent >= 1:
                break

            # change all values proportionally to passed time
            for arg_dict in changing_kwargs.values():
                arg_dict['val'] = arg_dict['start'] + (arg_dict['stop'] - arg_dict['start']) * passed_percent

            ch_kw = {name: int(d['val']) for (name, d) in changing_kwargs.items()}
            func(**fixed_kwargs, **ch_kw)

            # wait for next step
            if now + step_delay > time.time():
                time.sleep(now + step_delay - time.time())

            now = time.time()

        # final call with final values
        ch_kw = {name: int(d['stop']) for (name, d) in changing_kwargs.items()}
        func(**fixed_kwargs, **ch_kw)

    @staticmethod
    def change_sprite_size(id, time_ms, width, height):
        start_width, start_height = sprite.get_sprite_size(id)

        f = sprite.change_sprite_size
        fixkw = {"id": id}
        chkw = {
            "width": {"start": start_width, "stop": width},
            "height": {"start": start_height, "stop": height}
        }
        cls._make_calls_with_delay(f, fixkw, chkw, time_ms, cls.mult_fps)

    @staticmethod
    def change_sprite_width(id, time_ms, width):
        start_width = sprite.get_sprite_width(id)

        f = sprite.change_sprite_width
        fixkw = {"id": id}
        chkw = {
            "width": {"start": start_width, "stop": width}
        }
        cls._make_calls_with_delay(f, fixkw, chkw, time_ms, cls.mult_fps)

    @staticmethod
    def change_sprite_height(id, time_ms, height):
        start_height = sprite.get_sprite_height(id)

        f = sprite.change_sprite_height
        fixkw = {"id": id}
        chkw = {
            "height": {"start": start_height, "stop": height}
        }
        cls._make_calls_with_delay(f, fixkw, chkw, time_ms, cls.mult_fps)

    @staticmethod
    def change_width_proportionally(id, time_ms, width, from_modified=False):
        cls._make_calls_with_delay(
            sprite.change_width_proportionally,
            {"id": id,
             "from_modified": from_modified
             },

            {"width":
                 {"start": sprite.get_sprite_width(id), "stop": width}
             },
            time_ms, cls.mult_fps
        )

    @staticmethod
    def change_height_proportionally(id, time_ms, height, from_modified=False):
        cls._make_calls_with_delay(
            sprite.change_height_proportionally,
            {"id": id,
             "from_modified": from_modified
             },

            {"height":
                 {"start": sprite.get_sprite_height(id), "stop": height}
             },
            time_ms, cls.mult_fps
        )

    @staticmethod
    def change_sprite_size_proc(id, time_ms, width, height):
        startw = sprite.get_sprite_width_proc(id)
        startw = startw if startw is not None else 100

        starth = sprite.get_sprite_height_proc(id)
        starth = starth if starth is not None else 100

        cls._make_calls_with_delay(
            sprite.change_sprite_size_proc,
            {"id": id},

            {"width":
                 {"start": startw, "stop": width},
             "height":
                 {"start": starth, "stop": height}
             },
            time_ms, cls.mult_fps
        )

    @staticmethod
    def change_sprite_width_proc(id, time_ms, width):
        startw = sprite.get_sprite_width_proc(id)
        startw = startw if startw is not None else 100

        cls._make_calls_with_delay(
            sprite.change_sprite_width_proc,
            {"id": id},

            {"width":{"start": startw, "stop": width}},
            time_ms, cls.mult_fps
        )

    @staticmethod
    def change_sprite_height_proc(id, time_ms, height):
        starth = sprite.get_sprite_height_proc(id)
        starth = starth if starth is not None else 100

        cls._make_calls_with_delay(
            sprite.change_sprite_height_proc,
            {"id": id},

            {"height":
                 {"start": starth, "stop": height}
             },
            time_ms, cls.mult_fps
        )

    @staticmethod
    def set_sprite_angle(id, time_ms, angle):
        cls._make_calls_with_delay(
            sprite.set_sprite_angle,
            {"id": id},

            {"angle":
                 {"start": sprite.get_sprite_angle(id), "stop": angle}
             },
            time_ms, cls.mult_fps
        )

    @staticmethod
    def move_sprite_to(id, time_ms, x, y):
        start_x, start_y = sprite.get_sprite_pos(id)
        cls._make_calls_with_delay(
            sprite.move_sprite_to,
            {"id": id},

            {"x": {"start": start_x, "stop": x},
             "y": {"start": start_y, "stop": y}
             },
            time_ms, cls.mult_fps
        )

    @staticmethod
    def move_sprite_by(id, time_ms, dx, dy):
        start_x, start_y = sprite.get_sprite_pos(id)
        cls._make_calls_with_delay(
            sprite.move_sprite_to,
            {"id": id},

            {"x": {"start": start_x, "stop": start_x+dx},
             "y": {"start": start_y, "stop": start_y+dy}
             },
            time_ms, cls.mult_fps
        )

    @staticmethod
    def set_left_to(id, time_ms, left):
        cls._make_calls_with_delay(
            sprite.set_left_to,
            {"id": id},

            {"left": {"start": sprite.get_left(id), "stop": left}
             },
            time_ms, cls.mult_fps
        )

    @staticmethod
    def set_right_to(id, time_ms, right):
        cls._make_calls_with_delay(
            sprite.set_right_to,
            {"id": id},

            {"right": {"start": sprite.get_right(id), "stop": right}
             },
            time_ms, cls.mult_fps
        )

    @staticmethod
    def set_top_to(id, time_ms, top):
        cls._make_calls_with_delay(
            sprite.set_top_to,
            {"id": id},

            {"top": {"start": sprite.get_top(id), "stop": top}
             },
            time_ms, cls.mult_fps
        )

    @staticmethod
    def set_bottom_to(id, time_ms, bottom):
        cls._make_calls_with_delay(
            sprite.set_bottom_to,
            {"id": id},

            {"bottom": {"start": sprite.get_bottom(id), "stop": bottom}
             },
            time_ms, cls.mult_fps
        )

    @staticmethod
    def set_centerx_to(id, time_ms, centerx):
        cls._make_calls_with_delay(
            sprite.set_centerx_to,
            {"id": id},

            {"centerx": {"start": sprite.get_centerx(id), "stop": centerx}
             },
            time_ms, cls.mult_fps
        )

    @staticmethod
    def set_centery_to(id, time_ms, centery):
        cls._make_calls_with_delay(
            sprite.set_centery_to,
            {"id": id},

            {"centery": {"start": sprite.get_centery(id), "stop": centery}
             },
            time_ms, cls.mult_fps
        )

    @staticmethod
    def move_sprite_at_angle(id, time_ms, angle, distance):
        start_x, start_y = sprite.get_sprite_pos(id)
        x, y = sprite.calc_point_by_angle_and_distance(id, angle, distance)
        cls._make_calls_with_delay(
            sprite.move_sprite_to,
            {"id": id},

            {"x": {"start": start_x, "stop": x},
             "y": {"start": start_y, "stop": y}
             },
            time_ms, cls.mult_fps
        )

    @staticmethod
    def move_sprite_to_angle(id, time_ms, distance):
        start_x, start_y = sprite.get_sprite_pos(id)
        angle = sprite.get_sprite_final_angle(id)
        x, y = sprite.calc_point_by_angle_and_distance(id, angle, distance)
        cls._make_calls_with_delay(
            sprite.move_sprite_to,
            {"id": id},

            {"x": {"start": start_x, "stop": x},
             "y": {"start": start_y, "stop": y}
             },
            time_ms, cls.mult_fps
        )

    @staticmethod
    def move_sprite_to_point(id, time_ms, x, y, distance):
        start_x, start_y = sprite.get_sprite_pos(id)
        angle = sprite.calc_angle_by_point(id, [x, y])
        if angle is None:
            return

        x, y = sprite.calc_point_by_angle_and_distance(id, angle, distance)
        cls._make_calls_with_delay(
            sprite.move_sprite_to,
            {"id": id},

            {"x": {"start": start_x, "stop": x},
             "y": {"start": start_y, "stop": y}
             },
            time_ms, cls.mult_fps
        )

    @staticmethod
    def rotate_to_angle(id, time_ms, angle_to_look_to):
        angle_modif = sprite.calc_angle_modification_by_angle(id, angle_to_look_to)

        cls._make_calls_with_delay(
            sprite.set_sprite_angle,
            {"id": id},

            {"angle":
                 {"start": sprite.get_sprite_angle(id), "stop": angle_modif}
             },
            time_ms, cls.mult_fps
        )

    @staticmethod
    def rotate_to_point(id, time_ms, x, y):
        angle_to_look_to = sprite.calc_angle_by_point(id, [x, y])
        if angle_to_look_to is None:
            return

        angle_modif = sprite.calc_angle_modification_by_angle(id, angle_to_look_to)

        cls._make_calls_with_delay(
            sprite.set_sprite_angle,
            {"id": id},

            {"angle":
                 {"start": sprite.get_sprite_angle(id), "stop": angle_modif}
             },
            time_ms, cls.mult_fps
        )
cls = wrap_sprite_actions