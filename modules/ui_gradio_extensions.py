# based on https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/v1.6.0/modules/ui_gradio_extensions.py

import os
import gradio as gr

GradioTemplateResponseOriginal = gr.routes.templates.TemplateResponse

modules_path = os.path.dirname(os.path.realpath(__file__))
script_path = os.path.dirname(modules_path)


def webpath(fn):
    if fn.startswith(script_path):
        web_path = os.path.relpath(fn, script_path).replace('\\', '/')
    else:
        web_path = os.path.abspath(fn)

    return f'file={web_path}?{os.path.getmtime(fn)}'


def javascript_html():
    script_js_path = webpath('javascript/script.js')
    context_menus_js_path = webpath('javascript/contextMenus.js')
    head = f'<script type="text/javascript" src="{script_js_path}"></script>\n'
    head += f'<script type="text/javascript" src="{context_menus_js_path}"></script>\n'
    return head


def css_html():
    style_css_path = webpath('css/style.css')
    head = f'<link rel="stylesheet" property="stylesheet" href="{style_css_path}">'
    return head


def reload_javascript():
    js = javascript_html()
    css = css_html()

    def template_response(*args, **kwargs):
        res = GradioTemplateResponseOriginal(*args, **kwargs)
        res.body = res.body.replace(b'</head>', f'{js}</head>'.encode("utf8"))
        res.body = res.body.replace(b'</body>', f'{css}</body>'.encode("utf8"))
        res.init_headers()
        return res

    gr.routes.templates.TemplateResponse = template_response

# [TST] 2023-09-05 17:02:40
    notificationSoundPath = os.path.join(script_path, "notification.mp3")
    print("notificationSoundPath", notificationSoundPath)
    if os.path.exists(notificationSoundPath):
        print("notification.mp3 found")
        audio_notification = gr.Audio(interactive=False, value=notificationSoundPath, elem_id="audio_notification", visible=False)
# [TST] 2023-09-05 17:02:40




