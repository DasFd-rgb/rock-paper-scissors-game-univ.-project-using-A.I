# domain 2026111828-choi-min-gyu-project.streamlit.app

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

    #_디자인 설명
    st.write("Teachable Machine 모델을 이용하여 가위, 바위, 보를 인식합니다.")

    #_디자인 모델주소 입력
    model_url = st.text_input(
        "모델 주소",
        placeholder="https://teachablemachine.withgoogle.com/models/xxxxxxxx/"
    )


    if model_url != "":

        # 주소 마지막에 /가 없으면 추가
        if model_url.endswith("/") == False:
            model_url = model_url + "/"


        # 컴퓨터 가위바위보 선택
        computer = random.choice(choice)


        # Teachable Machine에서 제공하는 코드를
        # Streamlit에서 실행하기 위해 HTML 문자열로 작성
        html = """
        <div>
            <h3>가위바위보 이미지 인식</h3>

            <button type="button" onclick="init()">
                카메라 시작
            </button>

            <br><br>

            <div id="webcam-container"></div>

            <br>

            <div id="result"></div>

            <br>

            <div id="label-container"></div>
        </div>


        <!-- TensorFlow.js -->
        <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest/dist/tf.min.js"></script>

        <!-- Teachable Machine 이미지 라이브러리 -->
        <script src="https://cdn.jsdelivr.net/npm/@teachablemachine/image@latest/dist/teachablemachine-image.min.js"></script>


        <script type="text/javascript">

        // Teachable Machine에서 만든 모델 주소
        const URL = "MODEL_URL";


        // 모델과 웹캠에 사용할 변수
        let model;
        let webcam;
        let labelContainer;
        let maxPredictions;


        // 컴퓨터의 가위바위보 선택
        const computer = "COMPUTER";


        // -------------------------------------------------
        // 모델과 카메라 시작
        // -------------------------------------------------

        async function init()
        {
            const modelURL = URL + "model.json";
            const metadataURL = URL + "metadata.json";


            try
            {
                // Teachable Machine 모델 불러오기
                model = await tmImage.load(
                    modelURL,
                    metadataURL
                );


                // 모델의 클래스 개수
                maxPredictions = model.getTotalClasses();


                // 웹캠 만들기
                const flip = true;

                webcam = new tmImage.Webcam(
                    200,
                    200,
                    flip
                );


                // 웹캠 사용 준비
                await webcam.setup();

                // 웹캠 시작
                await webcam.play();


                // 반복 실행 시작
                window.requestAnimationFrame(loop);


                // 웹캠 화면을 HTML에 추가
                document
                    .getElementById("webcam-container")
                    .appendChild(webcam.canvas);


                // 인식 확률을 출력할 공간
                labelContainer =
                    document.getElementById("label-container");


                // 클래스 개수만큼 div 생성
                for(let i = 0; i < maxPredictions; i++)
                {
                    labelContainer.appendChild(
                        document.createElement("div")
                    );
                }
            }

            catch(error)
            {
                document.getElementById("result").innerHTML =
                    "모델 또는 카메라를 불러오지 못했습니다.<br>" + error;
            }
        }


        // -------------------------------------------------
        // 웹캠 화면 반복 실행
        // -------------------------------------------------

        async function loop()
        {
            // 현재 웹캠 화면으로 갱신
            webcam.update();


            // 현재 화면을 AI로 분석
            await predict();


            // 다시 loop 함수 실행
            window.requestAnimationFrame(loop);
        }


        // -------------------------------------------------
        // 이미지 예측
        // -------------------------------------------------

        async function predict()
        {
            // 웹캠의 현재 화면을 모델에 입력
            const prediction =
                await model.predict(webcam.canvas);


            let max = 0;
            let name = "";


            // 가위, 바위, 보 확률 확인
            for(let i = 0; i < maxPredictions; i++)
            {
                let percent =
                    prediction[i].probability * 100;


                // 각 클래스의 확률 출력
                const classPrediction =
                    prediction[i].className +
                    " : " +
                    percent.toFixed(1) +
                    "%";


                labelContainer.childNodes[i].innerHTML =
                    classPrediction;


                // 가장 높은 확률 찾기
                if(prediction[i].probability > max)
                {
                    max = prediction[i].probability;

                    name = prediction[i].className;
                }
            }


            // 영어 클래스 이름으로 학습한 경우
            // 한글로 변경
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


            // -------------------------------------------------
            // 가위바위보 승패 판정
            // -------------------------------------------------

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


            // -------------------------------------------------
            // 결과 출력
            // -------------------------------------------------

            document.getElementById("result").innerHTML =
                "내 선택 : <b>" + name + "</b>" +
                "<br>" +
                "컴퓨터 선택 : <b>" + computer + "</b>" +
                "<br><br>" +
                "게임 결과 : <b>" + gameResult + "</b>";
        }

        </script>
        """


        # HTML 코드 안의 MODEL_URL을
        # 사용자가 입력한 실제 모델 주소로 변경
        html = html.replace(
            "MODEL_URL",
            model_url
        )


        # HTML 코드 안의 COMPUTER를
        # 컴퓨터의 실제 선택으로 변경
        html = html.replace(
            "COMPUTER",
            computer
        )


        #_디자인 HTML 화면 출력
        components.html(
            html,
            height=650
        )


    else:

        #_디자인 안내문
        st.info(
            "Teachable Machine 모델 주소를 입력해주세요."
        )