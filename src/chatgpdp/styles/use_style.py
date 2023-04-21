import os


class Style:
    @staticmethod
    def get_style(style_name):
        base_path = os.path.join(os.path.dirname(__file__))
        try:
            with open(f"{base_path}/{style_name}", "r") as f:
                return f.read()
        except FileNotFoundError as e:
            print(e)
            return ""
