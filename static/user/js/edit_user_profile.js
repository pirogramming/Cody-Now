let currentStep = 1;
const totalSteps = 3;

const formData = {
    gender: "{{ user.gender }}",
    nickname: "{{ user.nickname }}",
    age: "{{ user.age }}",
    height: "{{ user.height }}",
    weight: "{{ user.weight }}",
    style: "{{ user.style }}"
};

function updateProgress() {
    const progress = ((currentStep - 1) / (totalSteps - 1)) * 100;
    document.getElementById('progress-status').style.width = `${progress}%`;
}

function showStep(step) {
    document.querySelectorAll('.step').forEach(el => el.style.display = 'none');
    document.getElementById(`step${step}`).style.display = 'block';
    
    document.getElementById('prevBtn').style.display = step === 1 ? 'none' : 'block';
    document.getElementById('nextBtn').textContent = step === totalSteps ? '완료' : '다음';
    
    updateProgress();
}

function validateStep(step) {
    switch(step) {
        case 1:
            return formData.gender != null;
        case 2:
            return formData.nickname && formData.age;
        case 3:
            return formData.height && formData.weight && formData.style;
        default:
            return false;
    }
}

function setupEventListeners() {
    // 버튼 이벤트 리스너
    document.querySelectorAll('.gender-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.gender-btn').forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
            formData.gender = btn.dataset.value;
        });
    });

    document.querySelectorAll('.style-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.style-btn').forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
            formData.style = btn.dataset.value;
        });
    });

    // 입력 필드 이벤트 리스너
    ['nickname', 'age', 'height', 'weight'].forEach(field => {
        document.getElementById(field)?.addEventListener('input', (e) => {
            formData[field] = e.target.value;
        });
    });

    // 네비게이션 버튼 이벤트 리스너
    document.getElementById('prevBtn').addEventListener('click', () => {
        if (currentStep > 1) {
            currentStep--;
            showStep(currentStep);
        }
    });

    document.getElementById('nextBtn').addEventListener('click', () => {
        if (validateStep(currentStep)) {
            if (currentStep < totalSteps) {
                currentStep++;
                showStep(currentStep);
            } else {
                submitForm();
            }
        } else {
            alert('모든 필수 항목을 입력해주세요.');
        }
    });
}

// 초기화
document.addEventListener('DOMContentLoaded', () => {
    // 성별 버튼 초기 상태 설정
    if (formData.gender) {
        const genderBtn = document.querySelector(`.gender-btn[data-value="${formData.gender}"]`);
        if (genderBtn) genderBtn.classList.add('selected');
    }

    // 스타일 버튼 초기 상태 설정
    if (formData.style) {
        const styleBtn = document.querySelector(`.style-btn[data-value="${formData.style}"]`);
        if (styleBtn) styleBtn.classList.add('selected');
    }

    setupEventListeners();
    showStep(1);
});

function submitForm() {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    fetch('{% url "user:edit_profile" %}', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '{% url "closet:dashboard" %}';
        } else {
            console.error('Error:', data.errors);
            alert('프로필 수정에 실패했습니다. 다시 시도해주세요.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('서버 통신 중 오류가 발생했습니다.');
    });
}