import os
import numpy as np
from PIL import Image, ImageFilter

output_dir = "pattern_out"
tiles = []

for filename in sorted(os.listdir(output_dir)):
    if filename.endswith(".png"):
        base_name = os.path.splitext(filename)[0]
        if base_name[-1] in '0123456789':  # 숫자로 끝나는 파일만 필터링
            tile = Image.open(os.path.join(output_dir, filename))
            tiles.append((base_name, tile))

if not tiles:
    print("No tiles found in the specified folder. Please check the files.")
else:
    tile_width, tile_height = tiles[0][1].size

    stacked_images = np.zeros((len(tiles), tile_height, tile_width, 3), dtype=np.uint8)

    # 5번을 기준으로 주변 이미지 처리
    for idx, (base_name, tile) in enumerate(tiles):
        tile_array = np.array(tile, dtype=np.uint8)
        
        if base_name[-1] == '5':  # '5'로 끝나는 경우는 기준 이미지로 설정
            # '5'로 끝나는 이미지는 그대로 사용
            stacked_images[idx] = tile_array
        elif base_name[-1] in '1246789':  # '5'를 제외한 다른 번호들
            # '5'를 기준으로 좌우 이동하거나 회전하여 배치
            if base_name[-1] in '1' or base_name[-1] in '4' or base_name[-1] in '7':  # 왼쪽
                tile_array = np.roll(tile_array, 0, axis=1)  # 왼쪽으로 이동
            elif base_name[-1] in '3' or base_name[-1] in '6' or base_name[-1] in '9':  # 오른쪽
                tile_array = np.roll(tile_array, 0, axis=1)  # 오른쪽으로 이동
            stacked_images[idx] = tile_array

    # 중간값 계산
    final_image_array = np.median(stacked_images, axis=0).astype(np.uint8)

    final_image = Image.fromarray(final_image_array)

    # 언샤프 마스크 적용
    unsharp_image = final_image.filter(ImageFilter.UnsharpMask(radius=2, percent=110, threshold=3))

    # 최종 결과 이미지 저장
    unsharp_image.save("output_highres_image.jpg")
    unsharp_image.show()  # 결과 이미지 표시
