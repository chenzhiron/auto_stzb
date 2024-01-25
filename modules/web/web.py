import pywebio
from pywebio import start_server

from pywebio.output import put_button, use_scope, put_collapse, put_text, put_scope, clear
from pywebio.pin import put_input, put_checkbox, pin_on_change

from modules.web.config import WebConfig

pywebio.config(css_style="""
    * {
        margin: 0 ;
        padding: 0 ;
    }
    .container {padding:0;
    margin:0;
    max-width: 100%;
    }
    .pywebio {
        padding:0;
    }
    .footer{
        display: none;
        }
""")


class WebConfigUI(WebConfig):
    def __init__(self):
        super().__init__()

    def ret_data(self):
        return self.config_data

    def start(self):
        start_server(self.init, port=9091, auto_open_webbrowser=True, debug=True)

    def init(self):
        self.format_com(self.config_data)

    def update_data(self, new_data):
        """更新数据并刷新UI视图。"""
        self.config_data = new_data
        self.refresh_view()

    def refresh_view(self):
        """刷新UI视图以显示最新的数据。"""
        self.clear('st')  # 清除当前视图
        self.init()  # 重新初始化视图

    def format_com(self, data):
        from st import stzb
        aside_elements = [self.components_aside(v) for v in data]
        self.clear('st')
        put_scope('scheduler', stzb.render())
        put_scope('st', [
            put_scope('aside', []).style('width:100px'),
            put_scope('collapse', []).style('width:200px'),
            put_scope('center', []).style('flex:1'),
        ]).style('display:flex;')
        with use_scope('aside'):
            for element in aside_elements:
                element.show()

    def components_aside(self, aside):
        return put_button(aside['name'], onclick=self.components_collapse(aside['children'], aside['name']))

    def components_collapse(self, collapse, title):
        def render():
            collapse_group = [self.cvcomponents_aside(v) for v in collapse]
            for v in collapse:
                self.clear(v['scope'])
            for v in collapse:
                with use_scope(v['scope'], clear=True):
                    put_collapse(title, collapse_group)

        return render

    def cvcomponents_aside(self, aside):
        return put_button(aside['name'], onclick=self.components_collapse_button(aside['children']))

    def components_collapse_button(self, aside):
        def render():
            with use_scope('center', clear=True):
                for index, item in enumerate(aside):
                    input_name = f'item_{index}'
                    if item['value'] is not None and item['show']:
                        if isinstance(item['value'], bool):
                            put_scope(input_name, [
                                put_text(item['explain']),
                                put_checkbox(input_name, [{'label': '', 'value': True}], value=[item['value']])
                            ]).style('display:grid;grid-template-columns:auto auto;')
                            pin_on_change(input_name, self.pin_change_bool(self, item), clear=True)
                        else:
                            put_scope(input_name, [
                                put_text(item['explain']),
                                put_input(input_name, value=str(item['value']), readonly=item['readonly'])
                            ]).style('display:grid;grid-template-columns:auto auto;')
                            pin_on_change(input_name, self.reg_str(self, item), clear=True)
                    else:
                        put_text(item['explain'])

        return render

    @staticmethod
    def pin_change_bool(self, v):
        def render(i):
            if len(i) > 0:
                v['value'] = True
            else:
                v['value'] = False

        return render

    @staticmethod
    def reg_str(self, item):
        def render(v):
            if v is None:
                return None
            item['value'] = v

        return render

    @staticmethod
    def clear(scope_name):
        # 实现清除作用域的静态方法
        clear(scope_name)


ui = WebConfigUI()
