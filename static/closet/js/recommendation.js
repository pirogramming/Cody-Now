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
    elements.codyRecommendation.textContent = result.cody_recommendation;
}

function handleCodyError(error, elements) {
    console.error("Error:", error);
    elements.errorSection.style.display = 'block';
    document.getElementById('error-message').textContent = error.message;
} 