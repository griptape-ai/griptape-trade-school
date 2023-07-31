## Header

These are some fancy code annotation ../assets/examples.

### Codeblcoks

Some `code` goes here.

### Plain codeblock

A plain codeblock:
```
Some code here
def myFunc():
    # Content
    print("foo")
```

### Code for a specific language

``` py
# This is python code
class foo():
    def hello(self, input):
        print(input)

me=foo()
me.hello("Howdy")
```

``` bash
# bash
echo "This should be a bash script"
alias ll='ls -latr'
```

### Code With a title

``` py title="app.py"

print("sweet")
```

### Code with line numbers
``` py linenums="1"

print("foo")
print("foo2")

```

### Code with line hilighted
``` py linenums="1" hl_lines="3 4"

is_chatting = True

while is_chatting:
    result = input("What's up?")
    if result == "q":
        is_chatting=False
    else:
        print(result)


```

:rocket: