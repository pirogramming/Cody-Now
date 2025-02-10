// 추천 작업 완료 후 upload_history 영역을 숨기고, 추천 섹션을 보이게 전환

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
        elements.codyBtn.style.display = "block";
        elements.loadingDiv.style.display = 'none';

        // 여기서 upload_history 컨테이너를 숨기고, 추천 섹션 컨테이너를 보이게 합니다.
        document.getElementById('upload_history_container').style.display = 'none';
        document.getElementById('recommendation_section_container').style.display = 'block';
    }
}
