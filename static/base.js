function handleImageUpload(event) {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = function(e) {
        const img = new Image();
        img.src = e.target.result;

        img.onload = function() {
            EXIF.getData(img, function() {
                const orientation = EXIF.getTag(this, "Orientation");
                const canvas = document.createElement("canvas");
                const ctx = canvas.getContext("2d");

                let width = img.width;
                let height = img.height;

                // 회전 적용
                if (orientation === 6) { // 90도 회전
                    canvas.width = height;
                    canvas.height = width;
                    ctx.rotate(90 * Math.PI / 180);
                    ctx.drawImage(img, 0, -height);
                } else if (orientation === 8) { // -90도 회전
                    canvas.width = height;
                    canvas.height = width;
                    ctx.rotate(-90 * Math.PI / 180);
                    ctx.drawImage(img, -width, 0);
                } else if (orientation === 3) { // 180도 회전
                    canvas.width = width;
                    canvas.height = height;
                    ctx.rotate(180 * Math.PI / 180);
                    ctx.drawImage(img, -width, -height);
                } else { // 회전이 필요 없을 경우
                    canvas.width = width;
                    canvas.height = height;
                    ctx.drawImage(img, 0, 0);
                }

                document.getElementById("preview-img").src = canvas.toDataURL("image/jpeg");
            });
        };
    };

    reader.readAsDataURL(file);
}

document.getElementById("id_image").addEventListener("change", handleImageUpload);
