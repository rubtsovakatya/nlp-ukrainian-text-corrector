import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Коректор українського тексту",
    layout="centered"
)

st.markdown("""
<style>
    .stApp {
        background:
            radial-gradient(
                circle at top right,
                rgba(70, 110, 220, 0.08),
                transparent 45%
            );
    }

    .block-container {
        max-width: 850px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    h1 {
        font-weight: 700;
        letter-spacing: -0.8px;
    }

    div[data-testid="stForm"] {
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
    }

    div[data-testid="stFormSubmitButton"] button {
        border-radius: 10px;
        min-height: 3rem;
        font-weight: 600;
    }

    div[data-testid="stTextArea"] textarea,
    div[data-testid="stTextInput"] input {
        border-radius: 10px;
    }

    .eyebrow {
        color: #6484d8;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)


st.markdown(
    '<div class="eyebrow">AI TEXT ASSISTANT</div>',
    unsafe_allow_html=True
)

st.title("Коректор українського тексту")

st.write(
    "Автоматичне виправлення орфографічних, "
    "граматичних і пунктуаційних помилок "
    "за допомогою мовної моделі."
)

st.divider()


SYSTEM_PROMPT = """
Ти — редактор українських текстів.

Виправляй орфографічні, граматичні та пунктуаційні помилки.
Зберігай початковий зміст і стиль тексту.
Повертай лише виправлений текст без пояснень і вступів.
Якщо помилок немає, повертай текст без змін.
"""


if "corrected_text" not in st.session_state:
    st.session_state.corrected_text = None


with st.form("correction_form"):

    st.subheader("Перевірка тексту")

    user_text = st.text_area(
        "Вхідний текст",
        height=180,
        max_chars=4000,
        placeholder="Введіть текст українською мовою..."
    )

    api_key = st.text_input(
        "Groq API-ключ",
        type="password",
        placeholder="Введіть API-ключ"
    )

    st.caption(
        "Ключ використовується для звернення до Groq API "
        "і не записується у вихідний код."
    )

    submitted = st.form_submit_button(
        "Виправити текст",
        type="primary",
        use_container_width=True
    )


if submitted:

    st.session_state.corrected_text = None

    if not api_key.strip():
        st.warning("Введіть API-ключ.")

    elif not user_text.strip():
        st.warning("Введіть текст для перевірки.")

    else:
        try:
            client = Groq(api_key=api_key.strip())

            with st.spinner("Аналізуємо текст..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT
                        },
                        {
                            "role": "user",
                            "content": user_text
                        }
                    ],
                    temperature=0,
                    max_completion_tokens=1024
                )

            st.session_state.corrected_text = (
                response.choices[0].message.content or ""
            )

        except Exception:
            st.error(
                "Не вдалося виконати запит. "
                "Перевірте API-ключ та підключення."
            )


if st.session_state.corrected_text is not None:

    st.divider()
    st.subheader("Результат")

    with st.container(border=True):
        st.text_area(
            "Виправлений текст",
            value=st.session_state.corrected_text,
            height=180
        )

    st.caption(
        "Перевірте результат перед використанням."
    )


st.divider()
st.caption("NLP Project | Groq API | GPT-OSS 20B")
