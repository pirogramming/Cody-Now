

let isUploading = false;
let isGeneratingCody = false;
let analysisResult = null;



document.querySelector("form").onsubmit = async function(event) {
    event.preventDefault();
    
    if (isUploading) return;
    
    const uploadBtn = document.getElementById('upload-btn');
    const loadingDiv = document.getElementById('loading');
    const errorSection = document.getElementById('error-section');
    const errorMessage = document.getElementById('error-message');
    const errorTrace = document.querySelector('.error-trace');
    try {
        isUploading = true;
        uploadBtn.disabled = true;
        loadingDiv.style.display = 'block';
        errorSection.style.display = 'none';

        let formData = new FormData(this);
        let response = await fetch("", {
            method: "POST",
            body: formData
        });

        let result = await response.json();
        
        if (!response.ok) {
            errorSection.style.display = 'block';
            errorMessage.textContent = result.error || '알 수 없는 오류가 발생했습니다.';
            if (result.error_details) {
                errorTrace.textContent = result.error_details;
                document.getElementById('error-details').style.display = 'none';
            }
            return;
        }

        analysisResult = result;
        document.getElementById("result").textContent = JSON.stringify(result, null, 2);
        
        if (result.data) {
            document.getElementById("upload-controls").classList.add("hidden");
            document.getElementById("result-section").classList.add("visible");
            document.getElementById("get-cody").style.display = "block";
        }
    } catch (error) {
        console.error("Error:", error);
        errorSection.style.display = 'block';
        errorMessage.textContent = error.message || '알 수 없는 오류가 발생했습니다.';
    } finally {
        isUploading = false;
        uploadBtn.disabled = false;
        loadingDiv.style.display = 'none';
    }
};


//0203 서정 수정 시작
//ai 결과 보기 버튼 누르기 전 ui
function previewImage(input) {
const previewIcon = document.getElementById("image-preview-icon"); // 업로드 아이콘
const previewImage = document.getElementById("preview-image"); // 미리보기 이미지
const previewContainer = document.getElementById("preview-container"); // 컨테이너
const uploadButton = document.getElementById("upload-btn"); // AI 결과 버튼
const fileSelectButton = document.getElementById("file-input-container"); // 파일 선택 버튼
const uploadControls = document.getElementById("upload-controls"); // 업로드 컨트롤 영역

// ✅ 사용자가 "파일 선택" 버튼을 누르고 아무 파일도 선택하지 않으면 → 원래 상태로 되돌리기
if (!input.files || input.files.length === 0) {
    console.log("파일 선택이 취소됨.");

    // 🔄 원래 UI 상태로 복구
    previewIcon.style.display = "inline-block"; // 업로드 아이콘 다시 표시
    previewImage.style.display = "none"; // 미리보기 숨김
    uploadButton.style.display = "none"; // AI 결과 버튼 숨김
    fileSelectButton.style.display = "block"; // 파일 선택 버튼 유지

    // 컨테이너 레이아웃을 초기 상태로 변경 (세로 정렬)
    previewContainer.style.display = "flex";
    previewContainer.style.flexDirection = "column";  
    previewContainer.style.alignItems = "center";

    // 업로드 컨트롤도 원래 상태로 변경 (세로 정렬)
    uploadControls.style.display = "flex";
    uploadControls.style.flexDirection = "column";

    return; // ✅ 여기서 종료 → 아래 코드 실행 안 함
}

// ✅ 파일이 선택된 경우 (정상적으로 업로드된 경우)
console.log("파일이 선택되었습니다:", input.files[0]);
const reader = new FileReader();

reader.onload = function (e) {
    previewContainer.style.display = "flex";
    previewContainer.style.flexDirection = "row"; // ✅ 가로 정렬 적용
    uploadControls.style.display = "flex"; // ✅ flex 컨테이너 유지
    uploadControls.style.flexDirection = "column"; // ✅ 업로드 컨트롤은 세로 정렬

    previewIcon.style.display = "none"; // 업로드 아이콘 숨기기
    previewImage.src = e.target.result;
    previewImage.style.display = "block"; // 미리보기 이미지 표시
    fileSelectButton.style.display = "block"; // 파일 선택 버튼 유지
    uploadButton.style.display = "inline-block"; // AI 결과 버튼 표시
};

reader.readAsDataURL(input.files[0]); // 파일 읽기
}

//ai 결과 보기 버튼 누른 후
document.querySelector("form").onsubmit = async function(event) {
event.preventDefault(); // 기본 폼 제출 방지
const fileSelectButton = document.getElementById("file-input-container"); // 파일 선택 버튼
const uploadButton = document.getElementById("upload-btn"); // AI 결과 버튼
const loadingDiv = document.getElementById("loading"); // 로딩 메시지
const resultSection = document.getElementById("result-section"); // 결과 표시 영역
const resultText = document.getElementById("result"); // 결과 텍스트
const uploadControls = document.getElementById("upload-controls"); // 사진과 분석 결과
const errorDiv = document.getElementById("error-message"); // 오류 메시지 표시 영역
try {
    // 🔄 버튼 숨기고 로딩 화면 표시
    uploadButton.style.display = "none";
    loadingDiv.style.display = "block";
    fileSelectButton.style.display = "none";
    // 🔹 폼 데이터 가져오기
    let formData = new FormData(this);
    let response = await fetch("", {
        method: "POST",
        body: formData
    });

    // 🔹 서버 응답 확인
    let result = await response.json();

    if (response.status === 400 && result.error) {
        // ❌ 오류 발생 시 오류 메시지 표시 & 파일 선택 버튼 보이게
        errorDiv.textContent = result.error;
        errorDiv.style.display = "block";
        fileSelectButton.style.display = "block"; // 파일 선택 버튼 다시 보이기
        return; // 🚨 여기서 함수 종료
    }

    // ✅ 결과가 있으면 UI 업데이트
    resultSection.style.display = "block";
    resultText.textContent = JSON.stringify(result, null, 2); // 결과 표시
    uploadControls.style.flexdirection = "row";
}  catch (error) {
    console.error("Error:", error);
    // ❌ 네트워크 오류 등 예외 상황에서도 파일 선택 버튼 다시 표시
    fileSelectButton.style.display = "block";
    errorDiv.textContent = "AI 분석 중 오류가 발생했습니다. 다시 시도해주세요.";
    errorDiv.style.display = "block";
} finally {
    loadingDiv.style.display = "none"; // 로딩 화면 숨김
}
};



//0203 서정 수정 끝끝

document.getElementById("get-cody").onclick = async function() {
    if (!analysisResult || isGeneratingCody) return;

    const codyBtn = document.getElementById('get-cody');
    const loadingDiv = document.getElementById('cody-loading');
    
    try {
        isGeneratingCody = true;
        codyBtn.disabled = true;
        loadingDiv.style.display = 'block';

        const position = await new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(resolve, reject);
        });

        const response = await fetch("{% url 'closet:gen_cody' %}", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({
                data: analysisResult.data,
                location: {
                    lat: position.coords.latitude,
                    lon: position.coords.longitude
                }
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        
        if (result.cody_recommendation) {
            document.getElementById("cody-result").style.display = "block";
            if (Array.isArray(result.cody_recommendation)) {
                document.getElementById("cody-recommendation").textContent = 
                    result.cody_recommendation.join('\n');
            } else {
                document.getElementById("cody-recommendation").textContent = 
                    result.cody_recommendation;
            }
        } else if (result.error) {
            throw new Error(result.error);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("코디 추천 중 오류가 발생했습니다: " + error.message);
        document.getElementById("cody-result").style.display = "block";
        document.getElementById("cody-recommendation").textContent = 
            "코디 추천 중 오류가 발생했습니다: " + error.message;
    } finally {
        isGeneratingCody = false;
        codyBtn.disabled = false;
        loadingDiv.style.display = 'none';
    }
};

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function success(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    
    fetchWeatherData(lat, lon);
}

function error() {
    const weatherElement = document.getElementById("weather");
    console.log("위치 정보를 불러올 수 없어 서울 날씨를 표시합니다.");
    fetchWeatherData("37.5665", "126.9780");  // 서울 좌표
}

function fetchWeatherData(lat, lon) {
    fetch(`/api/weather/?lat=${lat}&lon=${lon}`)
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                console.error("Error:", data.error);
                weatherElement.innerHTML = `<p>날씨 정보를 불러올 수 없습니다.</p>`;
            } else {
                displayWeather(data);
            }
        })
        .catch((error) => {
            console.error("날씨 데이터를 불러오는 데 실패했습니다.", error);
            weatherElement.innerHTML = `<p>날씨 정보를 불러올 수 없습니다.</p>`;
        });
}

function displayWeather(data) {
    const weatherElement = document.getElementById("weather");
    const temperature = data.main.temp;
    const humidity = data.main.humidity;
    const windSpeed = data.wind.speed;
    const weatherDescription = data.weather[0].description;
    const iconCode = data.weather[0].icon;
    const iconUrl = `https://openweathermap.org/img/wn/${iconCode}@2x.png`;

    weatherElement.innerHTML = `
        <div class="weather-info">
            <img src="${iconUrl}" 
                 alt="${weatherDescription}" 
                 onerror="this.onerror=null; this.src='{% static 'closet/images/weather-default.png' %}'"
                 style="width: 50px; height: 50px; vertical-align: middle;">
            <span>
                온도: ${temperature}°C | 습도: ${humidity}% | 바람: ${windSpeed} m/s<br>
                날씨: ${weatherDescription}
            </span>
        </div>
    `;
}

function toggleErrorDetails() {
    const details = document.getElementById('error-details');
    details.style.display = details.style.display === 'none' ? 'block' : 'none';
}

navigator.geolocation.getCurrentPosition(success, error);