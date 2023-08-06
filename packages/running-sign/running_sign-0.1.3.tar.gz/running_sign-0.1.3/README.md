# Running_Sign

Small tool to show dynamic indicator when program is running.

## Function

#### running_sign_rotation(interval= 0, msg_pre="", msg_post="", sign = ["\\", "|", "/", "-", "|", "/", "-"])

generator to show rotating indicator.
	parameter:
	***interval***: number, seconds of interval time between every frame of indicator.
	***msg_pre***: string, content will show before indicator.
	***msg_post***: string, conent will show after indicator.
	***sign: list***, symbols which will be showed sequentially.  



#### running_sign_progress(interval=0, msg_pre = "", msg_post="", sign=".",  max_num = 120)

generator to show progress bar.
	parameter：
    ***interval***: number, seconds of interval time between every frame of indicator.
    ***msg_pre***: string, content will show before indicator.
    ***msg_post***: string, conent will show after indicator.
    ***sign: string***, symbols which will be showed in progress way.
    ***max_num***: number, max numbers of sign in one bar progress.



#### running_sign(interval=0, msg_pre="", msg_post="", sign=None, max_num=120)

funtion, as entrance of two above function.
    ***parameter***: refer to parameters in above function. If sign != None, will call ***running_sign_progress***, otherwise will call ***running_sign_progress***.
    ***return***: generator.



#### running_pct(msg_pre="", msg_post="", sign="■", pct=50, scale=1)

function, show progress bar.
    parameter:
    ***msg_pre***: string, content will show before indicator.
    ***msg_post***: string, conent will show after indicator.
    ***sign: string***, symbols which will be showed in progress way.
    ***pct***: number, length of progress bar.
    ***scale***: number, scale of progress bar, default = 1 while the length of progress bar is 100 which means 100 signs.



# Example

```python
rs = running_sign_rotation(1)
for i in range(10):
    next(rs)
```

