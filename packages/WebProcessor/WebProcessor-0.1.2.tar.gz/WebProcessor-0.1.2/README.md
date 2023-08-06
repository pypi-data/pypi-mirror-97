## Main
THIS IS FOR EDUCATIONAL PURPOSES ONLY OR IF YOU HAVE CONSENT TO USE THAT SITES INFO!
## Install
```pip install WebProcessor```

## Required
GeckoDriver
- This will be installed automaticly on first run

## Functions


## Uses
```python
from driver.WebProcessor.WebProcessor import WebProcessor

wb = WebProcessor(show_window=False)
wb.load()
wb.load_page("https://github.com/TheBlockNinja/WebProcessor")

filter_elements = {
    "1_tag" : "link",
    "2_attribute" : "href",
    "3_contains" : "png"
}

data = wb.filter_elements(filter_elements)
print(data)

for i in range(len(data)):
    wb.download_img(file_name="test_"+str(i)+".png", direct=True,url=data[i])
wb.stop()
```

download_img
- If direct is False, it will take a screenshot of the webpage that is currently loaded
```python
for i in range(len(data)):
    wb.load_page(data[i])
    wb.download_img(file_name="test_"+str(i)+".png")
wb.stop()
```


