from PIL import Image
import imageio
import os
import os.path
import re


def create_gif(gif_name, path, duration=0.3):
    '''
    生成gif文件，原始图片仅支持png格式
    gif_name ： 字符串，所生成的 gif 文件名，带 .gif 后缀
    path :      需要合成为 gif 的图片所在路径
    duration :  gif 图像时间间隔
    '''

    frames = []
    pngFiles = os.listdir(path)
    image_list = [os.path.join(path, f) for f in pngFiles]
    mode = re.compile(r'\d+')
    image_list.sort(key=lambda x:int(mode.findall(x)[0]))
    print(image_list)
    for image_name in image_list:
        # 读取 png 图像文件
        # im = Image.open(image_name)
        # w, h = im.size
        # im.thumbnail((w // 2, h // 2))
        # im.save(image_name, 'png')
        frames.append(imageio.imread(image_name))
    # 保存为 gif
    imageio.mimsave(gif_name, frames, 'GIF', duration=duration)

    return


def main():
    gif_name = 'a.gif'
    path = './pic'  # 指定文件路径
    duration = 1
    create_gif(gif_name, path, duration)


if __name__ == "__main__":
    main()
