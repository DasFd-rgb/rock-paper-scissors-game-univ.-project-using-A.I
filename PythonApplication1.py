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

    # 내가 만든 Teachable Machine 모델 주소
    # 본인의 실제 모델 주소로 바꾸기
    model_url = "https://teachablemachine.withgoogle.com/models/KJha1lZTS/"

    st.write("사용 중인 모델 :", model_url)

    html = """
    <div style="color:white; font-family:sans-serif;">

        <h3 style="color:white;">
            가위바위보 이미지 인식
        </h3>

        <p id="status" style="color:white;">
            모델과 카메라를 불러오는 중입니다...
        </p>


        <!-- 웹캠 화면 -->
        <div id="webcam-container"></div>

        <br>

        <!-- 화면 캡처 버튼 -->
        <button
            type="button"
            onclick="captureImage()"
            style="
                padding:8px 20px;
                font-size:15px;
                cursor:pointer;
            "
        >
            화면 캡처
        </button>

        <br><br>


        <!-- 캡처한 화면 -->
        <canvas
            id="capture-canvas"
            width="200"
            height="200"
            style="
                display:none;
                border:1px solid white;
            "
        >
        </canvas>


        <br>


        <!-- 결과 출력 -->
        <div
            id="camera-result"
            style="
                color:white;
                font-size:17px;
                line-height:1.7;
            "
        >
        </div>


        <hr style="margin-top:30px; margin-bottom:30px;">


        <!-- 파일 업로드 -->
        <h3 style="color:white;">
            이미지 파일 업로드
        </h3>

        <input
            type="file"
            id="file-input"
            accept="image/png, image/jpeg"
            style="color:white;"
        >


        <br><br>


        <!-- 업로드한 사진 표시 -->
        <img
            id="upload-image"
            width="250"
            style="
                display:none;
                border:1px solid white;
            "
        >


        <br>


        <!-- 업로드 결과 -->
        <div
            id="upload-result"
            style="
                color:white;
                font-size:17px;
                line-height:1.7;
                margin-top:15px;
            "
        >
        </div>

    </div>


    <!-- TensorFlow.js -->
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.20.0/dist/tf.min.js"></script>


    <!-- Teachable Machine -->
    <script src="https://cdn.jsdelivr.net/npm/@teachablemachine/image@0.8.5/dist/teachablemachine-image.min.js"></script>


    <script type="text/javascript">

    // -------------------------------------------------
    // 변수
    // -------------------------------------------------

    const URL = "MODEL_URL";

    let model;
    let webcam;
    let modelReady = false;


    // -------------------------------------------------
    // 프로그램 시작
    // -------------------------------------------------

    async function init()
    {
        try
        {
            const modelURL = URL + "model.json";

            const metadataURL = URL + "metadata.json";


            // Teachable Machine 모델 불러오기
            model = await tmImage.load(
                modelURL,
                metadataURL
            );


            modelReady = true;


            // 웹캠 생성
            const flip = true;

            webcam = new tmImage.Webcam(
                200,
                200,
                flip
            );


            // 카메라 사용 권한 요청
            await webcam.setup();

            // 카메라 실행
            await webcam.play();


            // 웹캠 화면 추가
            document
                .getElementById("webcam-container")
                .appendChild(webcam.canvas);


            document.getElementById("status").innerHTML =
                "카메라가 준비되었습니다. 화면 캡처 버튼을 눌러주세요.";


            // 웹캠 화면 계속 갱신
            window.requestAnimationFrame(loop);
        }

        catch(error)
        {
            document.getElementById("status").innerHTML =
                "모델 또는 카메라를 불러오지 못했습니다.<br>" +
                error;
        }
    }


    // -------------------------------------------------
    // 웹캠 화면 갱신
    // -------------------------------------------------

    async function loop()
    {
        webcam.update();

        window.requestAnimationFrame(loop);
    }


    // -------------------------------------------------
    // 컴퓨터 가위바위보 랜덤 선택
    // -------------------------------------------------

    function computerChoice()
    {
        const choice = [
            "가위",
            "바위",
            "보"
        ];


        const num = Math.floor(
            Math.random() * 3
        );


        return choice[num];
    }


    // -------------------------------------------------
    // 가장 확률이 높은 가위바위보 찾기
    // -------------------------------------------------

    async function predict(image)
    {
        const prediction =
            await model.predict(image);


        let max = 0;

        let name = "";

        let probabilityText = "";


        for(let i = 0; i < prediction.length; i++)
        {
            let percent =
                prediction[i].probability * 100;


            probabilityText +=
                prediction[i].className +
                " : " +
                percent.toFixed(1) +
                "%<br>";


            if(prediction[i].probability > max)
            {
                max = prediction[i].probability;

                name = prediction[i].className;
            }
        }


        // 영어로 학습했을 경우
        if(name.toLowerCase() == "scissors")
        {
            name = "가위";
        }

        else if(name.toLowerCase() == "rock")
        {
            name = "바위";
        }

        else if(name.toLowerCase() == "paper")
        {
            name = "보";
        }


        return {
            name: name,
            probability: probabilityText
        };
    }


    // -------------------------------------------------
    // 승패 판정
    // -------------------------------------------------

    function game(user, computer)
    {
        if(user == computer)
        {
            return "무승부";
        }

        else if(
            user == "가위" &&
            computer == "보"
        )
        {
            return "승리";
        }

        else if(
            user == "바위" &&
            computer == "가위"
        )
        {
            return "승리";
        }

        else if(
            user == "보" &&
            computer == "바위"
        )
        {
            return "승리";
        }

        else
        {
            return "패배";
        }
    }


    // -------------------------------------------------
    // 웹캠 화면 캡처
    // -------------------------------------------------

    async function captureImage()
    {
        if(modelReady == false)
        {
            return;
        }


        const canvas =
            document.getElementById("capture-canvas");


        const context =
            canvas.getContext("2d");


        // 현재 웹캠 화면을 canvas에 복사
        context.drawImage(
            webcam.canvas,
            0,
            0,
            200,
            200
        );


        // 캡처 이미지 표시
        canvas.style.display = "block";


        // 캡처된 이미지를 AI 모델로 분석
        const result =
            await predict(canvas);


        // 캡처할 때마다 컴퓨터 선택 변경
        const computer =
            computerChoice();


        const gameResult =
            game(result.name, computer);


        document.getElementById(
            "camera-result"
        ).innerHTML =

            "<br>" +

            "<b>AI 분석 결과</b><br>" +

            result.probability +

            "<br>" +

            "내 선택 : <b>" +
            result.name +
            "</b><br>" +

            "컴퓨터 선택 : <b>" +
            computer +
            "</b><br><br>" +

            "게임 결과 : <b>" +
            gameResult +
            "</b>";
    }


    // -------------------------------------------------
    // 이미지 파일 업로드
    // -------------------------------------------------

    document
        .getElementById("file-input")
        .addEventListener(
            "change",

            function(event)
            {
                const file =
                    event.target.files[0];


                if(file == null)
                {
                    return;
                }


                const reader =
                    new FileReader();


                reader.onload =
                    function(e)
                    {
                        const image =
                            document.getElementById(
                                "upload-image"
                            );


                        image.src =
                            e.target.result;


                        image.style.display =
                            "block";


                        image.onload =
                            async function()
                            {
                                if(modelReady == false)
                                {
                                    return;
                                }


                                // 업로드 이미지 분석
                                const result =
                                    await predict(image);


                                // 사진을 새로 업로드할 때마다
                                // 컴퓨터 선택도 새로 생성
                                const computer =
                                    computerChoice();


                                const gameResult =
                                    game(
                                        result.name,
                                        computer
                                    );


                                document.getElementById(
                                    "upload-result"
                                ).innerHTML =

                                    "<b>AI 분석 결과</b><br>" +

                                    result.probability +

                                    "<br>" +

                                    "내 선택 : <b>" +
                                    result.name +
                                    "</b><br>" +

                                    "컴퓨터 선택 : <b>" +
                                    computer +
                                    "</b><br><br>" +

                                    "게임 결과 : <b>" +
                                    gameResult +
                                    "</b>";
                            };
                    };


                reader.readAsDataURL(file);
            }
        );


    // -------------------------------------------------
    // 페이지가 실행되면 자동으로 카메라 시작
    // -------------------------------------------------

    init();

    </script>
    """


    # 모델 주소 넣기
    html = html.replace(
        "MODEL_URL",
        model_url
    )


    #_디자인 HTML 출력
    components.html(
        html,
        height=1000,
        scrolling=True
    )