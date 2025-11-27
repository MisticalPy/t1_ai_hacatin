{% extends 'base.html' %}

{% block optional_head %}
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.14/codemirror.min.css" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.14/theme/dracula.min.css" />

    <style>
        .editor-wrapper {
            width: 1006px;
            height: 289px;
            margin: 12px auto;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.25);
            border-radius: 4px;
            overflow: hidden;
            background: white;
            cursor: text;
        }
        .CodeMirror { height: 100% !important; }

        .CodeMirror {
            background-color: #F7FAFC !important;
            border: 1px solid #DFE7F0 !important;
            height: 100% !important;
        }
        .CodeMirror-gutters {
            background-color: #4ec4ff !important;
            border-right: 1px solid #DFE7F0 !important;
        }
        .CodeMirror-linenumber {
            color: #ffffff !important;
        }
    </style>
{% endblock %}

{% block content %}
<main class="second_main">
<div class="second_base">

    <div class="filters-header">
        <span class="filters-header__pill">{{task.difficulty}}</span>
    </div>

    <div class="second_textarea">
        <p>
            <span>{{task.title}}</span><br>{{task.description}}
        </p>
        <p>
            <span>Входные и выходные данные</span>
            {% for tc in testcases %}
            <br>Входные данные: {{ tc.input_data }} -> Выходные данные: {{ tc.output_data }}
            {% endfor %}
        </p>
    </div>

    <div class="ide_sec">
        <div class="editor-wrapper" id="editorWrapper">
            <textarea id="editorTextarea" placeholder="# Напиши Python код здесь"></textarea>
        </div>
    </div>

    <div class="ide_buttons">
        <div style="width: 230px; height: 100%;"></div>
        <div style="height: 62px; width: 230px;">
            <button class="button_enter_ide" id="button_enter_ide">Продолжить</button>
        </div>
    </div>

</div>
</main>

<!-- CodeMirror -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.14/codemirror.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.14/mode/python/python.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.14/addon/edit/matchbrackets.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.14/addon/edit/closebrackets.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.14/addon/display/placeholder.min.js"></script>

<script>
    // === CodeMirror init ===
    const STORAGE_KEY = 'python_editor_autosave_v1';
    const DEFAULT_CODE = "# Пример Python\nprint('Hello, world!')\n";

    const textarea = document.getElementById('editorTextarea');
    const editor = CodeMirror.fromTextArea(textarea, {
        mode: 'python',
        lineNumbers: true,
        indentUnit: 4,
        tabSize: 4,
        indentWithTabs: false,
        matchBrackets: true,
        autoCloseBrackets: true,
        theme: 'default',
        lineWrapping: true,
        viewportMargin: Infinity,
        placeholder: "# Ваш Python код..."
    });

    const wrapper = document.getElementById('editorWrapper');
    wrapper.style.width = '1006px';
    wrapper.style.height = '289px';

    editor.setOption("extraKeys", {
        "Tab": function(cm) {
            if (cm.somethingSelected()) cm.indentSelection("add");
            else cm.replaceSelection(" ".repeat(4), "end");
        }
    });

    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved !== null) {
        editor.setValue(saved);
    } else {
        editor.setValue(DEFAULT_CODE);
    }

    let saveTimeout = null;
    editor.on('change', () => {
        if (saveTimeout) clearTimeout(saveTimeout);
        saveTimeout = setTimeout(() => {
            try { localStorage.setItem(STORAGE_KEY, editor.getValue()); }
            catch (e) { console.warn('Autosave failed', e);
            }
        }, 500);
    });

    // === getCookie для CSRF ===
    const getCookie = (name) =>
        document.cookie
            .split('; ')
            .find(row => row.startsWith(name + '='))
            ?.split('=')[1] || null;

    // === Обработка кнопки: лог + POST на текущий URL ===
    const runBtn = document.getElementById("button_enter_ide");
    if (runBtn) {
        runBtn.addEventListener("click", async () => {
            const code = editor.getValue();
            const url = window.location.href;  // текущий URL

            console.clear();
            console.log("=== Код из редактора ===");
            console.log(code);

            try {
                const response = await fetch(url, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCookie("csrftoken"),
                    },
                    body: JSON.stringify({
                        code: code
                    })
                });

                const data = await response.json().catch(() => null);
                console.log("=== Ответ от Django ===");
                console.log(data ?? response.status);
            } catch (e) {
                console.error("Ошибка при отправке кода:", e);
            }
        });
    }
</script>
{% endblock %}
