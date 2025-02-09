let currentStep = 1;
const totalSteps = 3;
const formData = { ...window.INITIAL_DATA };  // 초기 데이터 복사
let hasAttemptedNext = false; // 다음 버튼 클릭 시도 여부

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
    updateNextButtonState();
}

function showError(elementId, show) {
    const errorElement = document.getElementById(elementId);
    if (show && hasAttemptedNext) {
        errorElement.classList.add('visible');
    } else {
        errorElement.classList.remove('visible');
    }
}

function validateStep(step) {
    switch(step) {
        case 1:
            const genderValid = formData.gender && ['M', 'F'].includes(formData.gender);
            if (!genderValid && hasAttemptedNext) {
                const errorElement = document.getElementById('gender-error');
                errorElement.classList.add('visible');
                document.querySelectorAll('.gender-btn').forEach(btn => {
                    btn.classList.add('required-field');
                });
            }
            return genderValid;
            
        case 2:
            const nicknameValid = formData.nickname?.trim() !== '';
            const ageValid = formData.age && Number(formData.age) > 0;
            
            showError('nickname-error', !nicknameValid);
            showError('age-error', !ageValid);
            
            return nicknameValid && ageValid;
            
        case 3:
            const heightValid = formData.height && Number(formData.height) > 0;
            const weightValid = formData.weight && Number(formData.weight) > 0;
            const styleValid = formData.style != null;
            
            showError('height-error', !heightValid);
            showError('weight-error', !weightValid);
            showError('style-error', !styleValid);
            
            return heightValid && weightValid && styleValid;
            
        default:
            return false;
    }
}

function setupEventListeners() {
    // 성별 버튼 이벤트 리스너
    document.querySelectorAll('.gender-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.gender-btn').forEach(b => {
                b.classList.remove('selected');
                b.classList.remove('required-field'); // 에러 스타일 제거
            });
            btn.classList.add('selected');
            formData.gender = btn.dataset.value;
            
            // 에러 메시지 숨기기
            const errorElement = document.getElementById('gender-error');
            errorElement.classList.remove('visible');
            
            // 다음 버튼 활성화
            const nextBtn = document.getElementById('nextBtn');
            nextBtn.disabled = false;
            nextBtn.classList.add('active');
        });
    });

    document.querySelectorAll('.style-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.style-btn').forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
            formData.style = btn.dataset.value;
            showError('style-error', false); // 선택 시 에러 메시지 숨김
            updateNextButtonState();
        });
    });

    // 입력 필드 이벤트 리스너
    ['nickname', 'age', 'height', 'weight'].forEach(field => {
        const element = document.getElementById(field);
        if (element) {
            element.addEventListener('input', (e) => {
                formData[field] = e.target.value;
                if (hasAttemptedNext) {
                    validateStep(currentStep); // 입력 시 유효성 검사
                }
                updateNextButtonState();
            });
        }
    });

    // 프로필 이미지 미리보기
    document.getElementById('profile-image')?.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            if (file.size > 5 * 1024 * 1024) {  // 5MB 제한
                alert('파일 크기는 5MB를 초과할 수 없습니다.');
                e.target.value = '';  // 파일 선택 초기화
                return;
            }
            const reader = new FileReader();
            reader.onload = function(e) {
                const preview = document.getElementById('profile-preview');
                preview.src = e.target.result;
                formData.profile_image = file;
            };
            reader.readAsDataURL(file);
        }
    });

    // 네비게이션 버튼 이벤트 리스너
    document.getElementById('prevBtn').addEventListener('click', () => {
        if (currentStep > 1) {
            currentStep--;
            showStep(currentStep);
        }
    });

    document.getElementById('nextBtn').addEventListener('click', () => {
        hasAttemptedNext = true;
        const isValid = validateStep(currentStep);
        
        if (!isValid) {
            // 유효성 검사 실패 시
            const nextBtn = document.getElementById('nextBtn');
            nextBtn.classList.remove('active');
            nextBtn.disabled = true;
            
            // 1단계에서 성별 미선택 시 버튼 강조 및 에러 메시지 표시
            if (currentStep === 1) {
                document.querySelectorAll('.gender-btn').forEach(btn => {
                    btn.classList.add('required-field');
                });
                const errorElement = document.getElementById('gender-error');
                errorElement.classList.add('visible');
            }
            return; // 다음 단계로 진행하지 않음
        }
        
        // 유효성 검사 통과 시
        if (currentStep < totalSteps) {
            currentStep++;
            hasAttemptedNext = false;
            showStep(currentStep);
        } else {
            submitForm();
        }
    });
}

function updateNextButtonState() {
    const nextBtn = document.getElementById('nextBtn');
    const isValid = validateStep(currentStep);
    
    if (isValid) {
        nextBtn.classList.add('active');
        nextBtn.disabled = false;
    } else {
        nextBtn.classList.remove('active');
        nextBtn.disabled = true;
    }
}

// 초기화
document.addEventListener('DOMContentLoaded', () => {
    // 성별 버튼 초기 상태 설정
    if (formData.gender && ['M', 'F'].includes(formData.gender)) {
        const genderBtn = document.querySelector(`.gender-btn[data-value="${formData.gender}"]`);
        if (genderBtn) {
            genderBtn.classList.add('selected');
            const nextBtn = document.getElementById('nextBtn');
            nextBtn.disabled = false;
            nextBtn.classList.add('active');
        }
    } else {
        // 유효한 성별 값이 없는 경우 초기화
        formData.gender = null;
        const nextBtn = document.getElementById('nextBtn');
        nextBtn.disabled = true;
        nextBtn.classList.remove('active');
    }

    // 스타일 버튼 초기 상태 설정
    if (formData.style) {
        const styleBtn = document.querySelector(`.style-btn[data-value="${formData.style}"]`);
        if (styleBtn) styleBtn.classList.add('selected');
    }

    setupEventListeners();
    showStep(1);
    updateNextButtonState();
});

function submitForm() {
    const form = new FormData();
    
    // 프로필 이미지 처리
    const profileImageInput = document.getElementById('profile-image');
    if (profileImageInput.files.length > 0) {
        form.append('profile_image', profileImageInput.files[0]);
    }
    
    // 나머지 데이터 처리
    Object.keys(formData).forEach(key => {
        if (key !== 'profile_image' && formData[key] !== null && formData[key] !== undefined) {
            form.append(key, formData[key].toString());
        }
    });

    fetch(window.URLS.userProfile, {
        method: 'POST',
        headers: {
            'X-CSRFToken': window.CSRF_TOKEN
        },
        body: form
    })
    .then(async response => {
        const data = await response.json();
        if (data.success) {
            window.location.href = window.URLS.dashboard;
        } else {
            throw new Error(data.errors || '프로필 수정에 실패했습니다.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('프로필 수정 중 오류가 발생했습니다: ' + error.message);
    });
}