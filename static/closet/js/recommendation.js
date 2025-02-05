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
        errorSection: document.getElementById('error-section')
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
            displayRecommendation(result);
        }
    } catch (error) {
        throw error;
    } finally {
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

function handleCodyError(error, elements) {
    console.error("Error:", error);
    elements.errorSection.style.display = 'block';
    document.getElementById('error-message').textContent = error.message;
}

function displayRecommendation(data) {
    const recommendationSection = document.querySelector('.recommendation-section');
    const recommendationContent = document.querySelector('#recommendation-content');
    
    if (recommendationSection && recommendationContent) {
        recommendationContent.innerHTML = data.cody_recommendation;
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