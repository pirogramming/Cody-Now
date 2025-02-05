//추천 관련
let isGeneratingCody = false;

document.getElementById("get-cody").onclick = async function() {
    if (!analysisResult || isGeneratingCody) {
        console.log("분석 결과가 없거나 이미 코디 생성 중입니다.");
        return;
    }

    const elements = {
        codyBtn: document.getElementById('get-cody'),
        loadingDiv: document.getElementById('cody-loading'),
        errorSection: document.getElementById('error-section'),
        codyResult: document.getElementById("cody-result"),
        codyRecommendation: document.getElementById("cody-recommendation")
    };

    try {
        await generateCodyRecommendation(elements);
    } catch (error) {
        handleCodyError(error, elements);
    }
};

async function generateCodyRecommendation(elements) {
    isGeneratingCody = true;
    updateUIForCodyGeneration(elements);

    try {
        const response = await fetch(genCodyUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({
                data: analysisResult
            })
        });

        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || `HTTP error! status: ${response.status}`);
        }

        if (result.cody_recommendation) {
            updateUIWithCodyResult(elements, result);
        }
    } finally {
        // 로딩 상태 초기화
        isGeneratingCody = false;
        elements.codyBtn.disabled = false;
        elements.loadingDiv.style.display = 'none';
    }
}

function updateUIForCodyGeneration(elements) {
    elements.codyBtn.disabled = true;
    elements.loadingDiv.style.display = 'block';
    elements.errorSection.style.display = 'none';
}

function updateUIWithCodyResult(elements, result) {
    elements.codyResult.style.display = "block";
    displayRecommendation(result);
}

function handleCodyError(error, elements) {
    console.error("Error:", error);
    elements.errorSection.style.display = 'block';
    document.getElementById('error-message').textContent = error.message;
}

function displayRecommendation(data) {
    const recommendationSection = document.querySelector('.recommendation-section');
    const recommendationContent = document.querySelector('#recommendation-content');
    
    if (recommendationSection && recommendationContent) {
        // 원본 텍스트를 표시할 pre 태그 생성
        const originalTextPre = document.createElement('pre');
        originalTextPre.textContent = data.original_text;
        originalTextPre.style.whiteSpace = 'pre-wrap';
        originalTextPre.style.backgroundColor = '#f5f5f5';
        originalTextPre.style.padding = '1rem';
        originalTextPre.style.marginBottom = '2rem';
        
        // HTML 문자열을 파싱하여 실제 HTML 요소로 변환
        const parser = new DOMParser();
        const htmlDoc = parser.parseFromString(data.cody_recommendation, 'text/html');
        
        // 컨텐츠 삽입
        recommendationContent.innerHTML = ''; // 기존 내용 초기화
        recommendationContent.appendChild(originalTextPre);
        recommendationContent.innerHTML += htmlDoc.body.innerHTML;
        
        // 섹션 표시
        recommendationSection.style.display = 'block';
        
        // 링크들을 새 탭에서 열리도록 설정
        const links = recommendationContent.getElementsByTagName('a');
        Array.from(links).forEach(link => {
            link.setAttribute('target', '_blank');
            link.setAttribute('rel', 'noopener noreferrer');
        });
        
        // 이미지 로딩 에러 처리
        const images = recommendationContent.getElementsByTagName('img');
        Array.from(images).forEach(img => {
            img.onerror = function() {
                this.style.display = 'none';
            };
        });
    }
} 