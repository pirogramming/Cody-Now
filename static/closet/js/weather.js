function success(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    fetchWeatherData(lat, lon);
}

function error() {
    console.log("위치 정보를 불러올 수 없어 서울 날씨를 표시합니다.");
    fetchWeatherData("37.5665", "126.9780");
}

function fetchWeatherData(lat, lon) {
    const weatherElement = document.getElementById("weather");
    
    fetch(weatherApiUrl + `?lat=${lat}&lon=${lon}`)
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
                onerror="this.onerror=null; this.src='/static/closet/images/weather-default.png'"
                style="width: 50px; height: 50px; vertical-align: middle;">
            <span>
                온도: ${temperature}°C | 습도: ${humidity}% | 바람: ${windSpeed} m/s<br>
                날씨: ${weatherDescription}
            </span>
        </div>
    `;
}

// 페이지 로드 시 날씨 정보 가져오기
navigator.geolocation.getCurrentPosition(success, error); 