// === ЭЛЕМЕНТЫ И СОСТОЯНИЕ ===
const buttonMic = document.getElementById('neiroButton');
const buttonEnterN = document.getElementById('button_enter_n');

const getCookie = (name) =>
    document.cookie
        .split('; ')
        .find(row => row.startsWith(name + '='))?.split('=')[1] || null;

let isRecording = false;
let mediaRecorder = null;
let chunks = [];
let stream = null;


// ================================
// === ОЗВУЧКА ТЕКСТА (TTS) ===
// ================================
function voiceoverText(message) {
    if (!message) return;

    const synth = window.speechSynthesis;
    let voices = synth.getVoices();
    const langName = "Милена";

    const speak = () => {
        voices = synth.getVoices();
        let voice = voices.find(v => v.name === langName) || voices[0];

        const utter = new SpeechSynthesisUtterance(message);
        utter.voice = voice;
        utter.rate = 1;
        utter.pitch = 0.6;
        utter.volume = 1;

        // 🔒 БЛОКИРУЕМ КНОПКУ НА ВРЕМЯ ОЗВУЧКИ
        buttonMic.classList.add("neiro_micro_disabled");
        buttonMic.disabled = true;

        utter.onend = () => {
            // 🔓 РАЗБЛОКИРУЕМ КНОПКУ ПОСЛЕ ОЗВУЧКИ (если не финальный стоп)
            if (!buttonMic.classList.contains("neiro_micro_disabled_permanent")) {
                buttonMic.classList.remove("neiro_micro_disabled");
                buttonMic.disabled = false;
            }
        };

        utter.onerror = () => {
            if (!buttonMic.classList.contains("neiro_micro_disabled_permanent")) {
                buttonMic.classList.remove("neiro_micro_disabled");
                buttonMic.disabled = false;
            }
        };

        synth.speak(utter);
    };

    if (!voices.length) {
        synth.onvoiceschanged = () => {
            speak();
        };
    } else {
        speak();
    }
}


// ==================================
// === ОБРАБОТКА ОТВЕТА СЕРВЕРА ===
// ==================================
function handleServerResponse(json) {
    if (!json) {
        console.error("Пустой ответ от сервера");
        return;
    }

    if (json.status !== "ok") {
        console.error("Ошибка от сервера:", json.error || json);
        return;
    }

    const message = json.data?.message || "";

    if (json.data?.is_stop) {
        console.log("Диалог завершён — отключаем микрофон и показываем кнопку продолжить");

        // ❗ Перманентно блокируем микрофон
        buttonMic.classList.add("neiro_micro_disabled", "neiro_micro_disabled_permanent");
        buttonMic.disabled = true;

        // добавляем кнопку "Продолжить"
        buttonEnterN.classList.add("button_enter_neiro_add");
    } else {
        // Озвучиваем текст
        voiceoverText(message);
    }
}


// =====================================
// === ОТПРАВКА АУДИО НА СЕРВЕР ===
// =====================================
async function uploadAudio(form) {
    try {
        const response = await fetch(window.location.pathname, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: form,
        });

        const json = await response.json();
        console.log("Сервер ответил на аудио:", json);
        handleServerResponse(json);
    } catch (err) {
        console.error("Ошибка загрузки файла:", err);
    }
}


// ================================
// === ФУНКЦИЯ ЗАПУСКА ЗАПИСИ ===
// ================================
async function startRecording() {
    console.log("🔴 Начинаем запись...");

    try {
        stream = await navigator.mediaDevices.getUserMedia({ audio: true });

        mediaRecorder = new MediaRecorder(stream);

        chunks = [];
        mediaRecorder.ondataavailable = (e) => {
            if (e.data.size > 0) {
                chunks.push(e.data);
            }
        };

        mediaRecorder.start();
        console.log("🎙 Запись пошла");
    } catch (err) {
        console.error("Ошибка доступа к микрофону:", err);
        alert("Не удалось получить доступ к микрофону");
    }
}


// ======================================
// === ФУНКЦИЯ ОСТАНОВКИ И ОТПРАВКИ ===
// ======================================
async function stopRecording() {
    console.log("🛑 Останавливаем запись...");

    if (!mediaRecorder) {
        console.error("mediaRecorder не найден — запись не запущена");
        return;
    }

    return new Promise((resolve) => {
        mediaRecorder.onstop = async () => {
            console.log("📦 Формируем аудио-файл...");

            const blob = new Blob(chunks, { type: "audio/webm" });

            if (stream) {
                stream.getTracks().forEach(t => t.stop());
            }

            const form = new FormData();
            form.append("file", blob, `record_${Date.now()}.webm`);

            console.log("📤 Отправляем на сервер...");
            await uploadAudio(form);

            resolve();
        };

        mediaRecorder.stop();
    });
}


// ================================
// === TOGGLE КНОПКИ + АУДИО ===
// ================================
async function toggleButtonMic() {
    // Если кнопка заблокирована (пока озвучка) — выходим
    if (buttonMic.disabled) {
        console.log("Кнопка заблокирована на время озвучки");
        return;
    }

    isRecording = !isRecording;

    if (isRecording) {
        console.log('сюда пихаем начало записи');

        await startRecording();

        buttonMic.classList.add('btn-squeezing-state');
        setTimeout(() => {
            buttonMic.classList.remove('btn-squeezing-state');
            buttonMic.classList.add('btn-active-state');
        }, 100);
    } else {
        console.log('сюда пихаем отправку на сервак');

        await stopRecording();

        buttonMic.classList.add('btn-squeezing-state');
        setTimeout(() => {
            buttonMic.classList.remove('btn-squeezing-state');
            buttonMic.classList.remove('btn-active-state');
        }, 100);
    }
}

buttonMic.addEventListener('click', () => {
    toggleButtonMic();
});

document.getElementById('button_enter_n').addEventListener('click', function () {
    let url = window.location.href;
    let newUrl = url.replace(/questions\/?$/, "");
    window.location.href = newUrl;  // редирект
});
const neiro_eyes = document.getElementById("neiro_eyes")
const eyelid = document.getElementById("eyelid")
// Это засунуть в функцию которая озвучивает текст в начало
neiro_eyes.classList.add("neiro_eyes_movement");
eyelid.classList.add("eyelid_blink");




// Это засунуть в первое нажатие кнопки записи когда запись начинается
neiro_eyes.classList.remove("neiro_eyes_movement");
eyelid.classList.remove("eyelid_blink");