window.onload = async function () {
    const urlParams = new URLSearchParams(window.location.search);
    const outfitId = urlParams.get("id");

    if (outfitId) {
        try {
            let response = await fetch(`/api/outfit/${outfitId}/`);
            let data = await response.json();

            if (data.image_url) {
                document.getElementById("preview-image").src = data.image_url;
                document.getElementById("preview-image").style.display = "block";
                document.getElementById("image-preview-icon").style.display = "none";
            }

            if (data.analysis_result) {
                document.getElementById("result").textContent = JSON.stringify(data.analysis_result, null, 2);
                document.getElementById("result-section").style.display = "block";
            }

            if (data.cody_recommendation) {
                document.getElementById("cody-recommendation").textContent = data.cody_recommendation;
                document.getElementById("cody-result").style.display = "block";
            }
        } catch (error) {
            console.error("데이터를 불러오는 중 오류 발생:", error);
        }
    }
};
let isUploading = false;
let isGeneratingCody = false;
let analysisResult = null;

// 폼 제출 이벤트 핸들러를 하나로 통합
document.querySelector("form").onsubmit = async function(event) {
    event.preventDefault();
    if (isUploading) return;
    
    const fileSelectButton = document.getElementById("file-input-container");
    const uploadButton = document.getElementById("upload-btn");
    const loadingDiv = document.getElementById("loading");
    const resultSection = document.getElementById("result-section");
    const resultText = document.getElementById("result");
    const uploadControls = document.getElementById("upload-controls");
    const errorSection = document.getElementById("error-section");
    const errorMessage = document.getElementById("error-message");
    const errorTrace = document.querySelector('.error-trace');
    const getCodyButton = document.getElementById("get-cody");
    
    try {
        isUploading = true;
        uploadButton.disabled = true;
        loadingDiv.style.display = "block";
        errorSection.style.display = "none";
        fileSelectButton.style.display = "none";  // 파일 선택 버튼 숨김
        
        let formData = new FormData(this);
        let response = await fetch("", {
            method: "POST",
            body: formData
        });
        let result = await response.json();
        
        if (!response.ok) {
            errorSection.style.display = "block";
            errorMessage.textContent = result.error || '알 수 없는 오류가 발생했습니다.';
            if (result.error_details) {
                errorTrace.textContent = result.error_details;
                document.getElementById('error-details').style.display = 'none';
            }
            fileSelectButton.style.display = "block"; // 오류 시 파일 선택 버튼 다시 보이기
            return;
        }
        
        // 분석 결과 업데이트 (코디 추천에 사용)
        analysisResult = result;
        
        // 결과 UI 업데이트
        resultText.textContent = JSON.stringify(result, null, 2);
        resultSection.style.display = "block";
        uploadControls.classList.add("hidden");
        getCodyButton.style.display = "block";
    } catch (error) {
        console.error("Error:", error);
        errorSection.style.display = "block";
        errorMessage.textContent = error.message || "AI 분석 중 오류가 발생했습니다. 다시 시도해주세요.";
        fileSelectButton.style.display = "block";
    } finally {
        isUploading = false;
        uploadButton.disabled = false;
        loadingDiv.style.display = "none";
    }
};

function previewImage(input) {
    const previewIcon = document.getElementById("image-preview-icon");
    const previewImage = document.getElementById("preview-image");
    const previewContainer = document.getElementById("preview-container");
    const uploadButton = document.getElementById("upload-btn");
    const fileSelectButton = document.getElementById("file-input-container");
    const uploadControls = document.getElementById("upload-controls");

    // 파일 선택이 취소되면 원래 상태로 복구
    if (!input.files || input.files.length === 0) {
        console.log("파일 선택이 취소됨.");
        previewIcon.style.display = "inline-block";
        previewImage.style.display = "none";
        uploadButton.style.display = "none";
        fileSelectButton.style.display = "block";
        previewContainer.style.display = "flex";
        previewContainer.style.flexDirection = "column";  
        previewContainer.style.alignItems = "center";
        uploadControls.style.display = "flex";
        uploadControls.style.flexDirection = "column";
        return;
    }
    console.log("파일이 선택되었습니다:", input.files[0]);
    const reader = new FileReader();
    reader.onload = function (e) {
        previewContainer.style.display = "flex";
        previewContainer.style.flexDirection = "row"; // 가로 정렬
        uploadControls.style.display = "flex";
        uploadControls.style.flexDirection = "column";
        previewIcon.style.display = "none";
        previewImage.src = e.target.result;
        previewImage.style.display = "block";
        fileSelectButton.style.display = "block";
        uploadButton.style.display = "inline-block";
    };
    reader.readAsDataURL(input.files[0]);
}

document.getElementById("get-cody").onclick = async function() {
    if (!analysisResult || isGeneratingCody) {
        console.log("분석 결과가 없거나 이미 코디 생성 중입니다.");
        return;
    }

    const codyBtn = document.getElementById('get-cody');
    const loadingDiv = document.getElementById('cody-loading');
    const errorSection = document.getElementById('error-section');
    
    try {
        isGeneratingCody = true;
        codyBtn.disabled = true;
        loadingDiv.style.display = 'block';
        errorSection.style.display = 'none';

        // 위치 정보 가져오기
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

        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || `HTTP error! status: ${response.status}`);
        }

        if (result.cody_recommendation) {
            document.getElementById("cody-result").style.display = "block";
            document.getElementById("cody-recommendation").textContent = result.cody_recommendation;
        }

    } catch (error) {
        console.error("Error:", error);
        errorSection.style.display = 'block';
        document.getElementById('error-message').textContent = error.message;
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
    fetchWeatherData("37.5665", "126.9780");
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


// 검색기록 섹션