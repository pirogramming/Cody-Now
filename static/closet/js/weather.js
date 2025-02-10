function success(position) {
  const lat = position.coords.latitude;
  const lon = position.coords.longitude;
  section_fetchWeatherData(lat, lon);
}

function error() {
  console.log("위치 정보를 불러올 수 없어 서울 날씨를 표시합니다.");
  section_fetchWeatherData("37.5665", "126.9780");
}

function section_fetchWeatherData(lat, lon) {
  const weatherElement = document.getElementById("weather");

  console.log(`🌍 요청 URL: /api/weather/?lat=${lat}&lon=${lon}`);

  fetch(`/api/weather/?lat=${lat}&lon=${lon}`)
    .then((response) => {
      console.log("📡 응답 상태 코드:", response.status);
      return response.json();
    })
    .then((data) => {
      console.log("📩 API 응답 데이터:", data);

      if (!data.weather || !data.weather.main) {
        console.error("❌ 응답 데이터에 weather 정보가 없음:", data);
        weatherElement.innerHTML = `<p>날씨 정보를 불러올 수 없습니다. (데이터 오류)</p>`;
        return;
      }

      console.log("✅ 날씨 데이터 정상 수신");
      displayWeather(data);
    })
    .catch((error) => {
      console.error("❌ 네트워크 또는 서버 오류:", error);
      weatherElement.innerHTML = `<p>날씨 정보를 불러올 수 없습니다. (네트워크 오류)</p>`;
    });
}

function displayWeather(data) {
  console.log(data);
  const weatherElement = document.getElementById("weather");
  const temperature = data.weather.main.temp;
  const humidity = data.weather.main.humidity;
  const windSpeed = data.weather.wind.speed;
  const weatherDescription = data.weather.weather[0].description;
  const iconCode = data.weather.weather[0].icon;
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
