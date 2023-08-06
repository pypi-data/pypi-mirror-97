## Main
THIS IS FOR EDUCATIONAL PURPOSES ONLY OR IF YOU HAVE CONSENT TO USE THAT SITES INFO!
## Install
https://pypi.org/project/WebProcessor/0.1.2/

```pip install WebProcessor```

## Required
GeckoDriver
- This will be installed automatically on first run

## Uses
```python
from driver.WebProcessor.WebProcessor import WebProcessor
from driver.WebProcessor.WebFilter import WebFilter

wb = WebProcessor(show_window=False,req_user_input=True)
wb.load()
wb.load_page("https://github.com/TheBlockNinja/WebProcessor")

wf = WebFilter()
if not wf.load_filter("test_filter.json"):
    wf.add_filter_data(wf.filter_tag,"link")
    wf.add_filter_data(wf.filter_attribute,"href")
    wf.add_filter_data(wf.filter_contains,"png")
    wf.save_filter("test_filter.json")

data = wf.filter_elements(wb)
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


