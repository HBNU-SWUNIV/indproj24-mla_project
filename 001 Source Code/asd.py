from PIL import Image, ImageFilter

# 이미지 불러오기
img_path = "pattern_out/pattern_5.png"
image = Image.open(img_path)

# 언샤프 마스크 적용 (선명도 증가)
unsharp_image = image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

# 가우시안 블러 적용 (과도한 선명도 보완)
gaussian_image = unsharp_image.filter(ImageFilter.GaussianBlur(radius=1))  # 블러 강도 조절 가능

# 최종 결과 이미지 저장
gaussian_image.save("output_highres_image_boosted.jpg")
gaussian_image.show()  # 결과 이미지 표시
