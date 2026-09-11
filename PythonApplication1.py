import streamlit as st
import random
import base64
from io import BytesIO
from PIL import Image
import streamlit.components.v1 as components


st.title("가위바위보 프로그램")

# 가위, 바위, 보
choice = ["가위", "바위", "보"]


# 승패를 확인하는 함수
def game(user, computer):
    if user == computer:
        return "무승부"

    if user == "가위" and computer == "보":
        return "승리"

    if user == "바위" and computer == "가위":
        return "승리"

    if user == "보" and computer == "바위":
        return "승리"

    return "패배"


tab1, tab2 = st.tabs(["기본 가위바위보", "이미지 가위바위보"])


# -------------------------------------------------
# 기본 가위바위보
# -------------------------------------------------
with tab1:

    st.write("가위, 바위, 보 중 하나를 선택하세요.")

    col1, col2, col3 = st.columns(3)

    user = ""

    if col1.button("가위"):
        user = "가위"

    if col2.button("바위"):
        user = "바위"

    if col3.button("보"):
        user = "보"


    if user != "":

        computer = random.choice(choice)

        result = game(user, computer)

        st.write("내가 낸 것 :", user)
        st.write("컴퓨터가 낸 것 :", computer)

        if result == "승리":
            st.success("이겼습니다.")

        elif result == "패배":
            st.error("졌습니다.")

        else:
            st.warning("비겼습니다.")



# -------------------------------------------------
# Teachable Machine 이미지 인식
# -------------------------------------------------
with tab2:

    st.write("Teachable Machine에서 만든 모델 주소를 입력하세요.")

    model_url = st.text_input(
        "모델 주소",
        placeholder="https://teachablemachine.withgoogle.com/models/xxxxxxxx/"
    )


    menu = st.radio(
        "이미지 입력 방법",
        ["카메라", "파일 업로드"]
    )


    image_file = None


    if menu == "카메라":

        image_file = st.camera_input(
            "가위, 바위, 보 사진을 찍으세요."
        )

    else:

        image_file = st.file_uploader(
            "사진을 선택하세요.",
            type=["jpg", "jpeg", "png"]
        )


    if model_url != "" and image_file is not None:

        # 주소 마지막에 / 가 없으면 추가
        if model_url.endswith("/") == False:
            model_url = model_url + "/"


        # 이미지 읽기
        img = Image.open(image_file)

        st.image(
            img,
            caption="입력한 이미지",
            width=300
        )


        # 이미지를 HTML에서 사용할 수 있도록 변환
        buffer = BytesIO()

        img.save(buffer, format="PNG")

        img_data = base64.b64encode(
            buffer.getvalue()
        ).decode()


        img_data = "data:image/png;base64," + img_data


        # 컴퓨터는 랜덤으로 선택
        computer = random.choice(choice)


        # Teachable Machine 모델을 실행하는 HTML
        html = """
        <div>

            <p id="message">
                이미지를 확인하고 있습니다.
            </p>

            <img
                id="image"
                src="IMAGE_DATA"
                width="224"
                height="224"
                style="display:none;"
            >

            <div id="result"></div>

        </div>


        <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.20.0/dist/tf.min.js"></script>

        <script src="https://cdn.jsdelivr.net/npm/@teachablemachine/image@0.8.5/dist/teachablemachine-image.min.js"></script>


        <script>

        const url = "MODEL_URL";

        const computer = "COMPUTER";


        async function start()
        {
            try
            {
                const modelURL = url + "model.json";
                const metadataURL = url + "metadata.json";

                const model = await tmImage.load(
                    modelURL,
                    metadataURL
                );


                const image = document.getElementById("image");

                const prediction = await model.predict(image);


                let max = 0;
                let name = "";

                let text = "";


                for(let i = 0; i < prediction.length; i++)
                {
                    let percent = prediction[i].probability * 100;

                    text += prediction[i].className;
                    text += " : ";
                    text += percent.toFixed(1);
                    text += "%<br>";


                    if(prediction[i].probability > max)
                    {
                        max = prediction[i].probability;
                        name = prediction[i].className;
                    }
                }


                // 영어로 학습한 경우 한글로 변경
                if(name.toLowerCase() == "scissors")
                {
                    name = "가위";
                }

                if(name.toLowerCase() == "rock")
                {
                    name = "바위";
                }

                if(name.toLowerCase() == "paper")
                {
                    name = "보";
                }


                let gameResult = "";


                if(name == computer)
                {
                    gameResult = "무승부";
                }

                else if(name == "가위" && computer == "보")
                {
                    gameResult = "승리";
                }

                else if(name == "바위" && computer == "가위")
                {
                    gameResult = "승리";
                }

                else if(name == "보" && computer == "바위")
                {
                    gameResult = "승리";
                }

                else
                {
                    gameResult = "패배";
                }


                document.getElementById("message").innerHTML =
                    "인식 결과 : <b>" + name + "</b>";


                document.getElementById("result").innerHTML =
                    "<br>" +
                    text +
                    "<hr>" +
                    "내 선택 : " + name +
                    "<br>" +
                    "컴퓨터 선택 : " + computer +
                    "<br><br>" +
                    "<b>게임 결과 : " + gameResult + "</b>";

            }

            catch(error)
            {
                document.getElementById("message").innerHTML =
                    "모델을 불러오지 못했습니다.<br>" + error;
            }
        }


        const image = document.getElementById("image");


        image.onload = function()
        {
            start();
        };


        </script>
        """


        html = html.replace(
            "IMAGE_DATA",
            img_data
        )

        html = html.replace(
            "MODEL_URL",
            model_url
        )

        html = html.replace(
            "COMPUTER",
            computer
        )


        components.html(
            html,
            height=350
        )


    else:

        st.info(
            "모델 주소와 이미지를 입력해주세요."
        )