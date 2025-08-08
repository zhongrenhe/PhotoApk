from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import os
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS

class PhotoCleaner(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.add_widget(Label(text="起始时间: YYYY-MM-DD HH:MM:SS"))
        self.start_input = TextInput(multiline=False)
        self.add_widget(self.start_input)

        self.add_widget(Label(text="结束时间: YYYY-MM-DD HH:MM:SS"))
        self.end_input = TextInput(multiline=False)
        self.add_widget(self.end_input)

        self.btn = Button(text="查找并删除照片")
        self.btn.bind(on_press=self.clean_photos)
        self.add_widget(self.btn)

        self.result = Label(text="")
        self.add_widget(self.result)

    def get_image_datetime(self, path):
        try:
            image = Image.open(path)
            exif_data = image._getexif()
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id)
                    if tag == "DateTimeOriginal":
                        return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
        except Exception as e:
            print(f"无法读取 {path}：{e}")
        return None

    def clean_photos(self, instance):
        try:
            start_time = datetime.strptime(self.start_input.text, "%Y-%m-%d %H:%M:%S")
            end_time = datetime.strptime(self.end_input.text, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            self.result.text = "时间格式错误"
            return

        folder = "/storage/emulated/0/DCIM/Camera"
        deleted = 0

        if not os.path.exists(folder):
            self.result.text = f"找不到文件夹：{folder}"
            return

        for filename in os.listdir(folder):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                full_path = os.path.join(folder, filename)
                dt = self.get_image_datetime(full_path)
                if dt and start_time <= dt <= end_time:
                    try:
                        os.remove(full_path)
                        deleted += 1
                    except Exception as e:
                        print(f"无法删除 {filename}：{e}")
        self.result.text = f"已删除 {deleted} 张照片"

class PhotoCleanerApp(App):
    def build(self):
        return PhotoCleaner()

if __name__ == '__main__':
    PhotoCleanerApp().run()
