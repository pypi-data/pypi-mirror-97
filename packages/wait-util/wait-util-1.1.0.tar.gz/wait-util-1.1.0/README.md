# changelist
* 1.1.0,  add wait_for
* 1.0.0,  first release

# feedback
* send email to dvdface@gmail.com
* visit https://github.com/dvdface/waitutil

# how to install
`pip install wait-util`

# known issues

None

# how to use
1. **install package**
   
   run `pip install wait-util` to install wait package<br/>

2. **use wait_until_change/wait_until_no_change**
    ```
    from wait import wait_until_change, wait_until_no_change

    def demo():
      return 1

    wait_until_change(demo, interval=1, timeout=5)

    wait_until_no_change(demo, interval=1, timeout=5)
    ```
3. **use wait_for_true/wait_for_false**
    ```
    from wait import wait_for_true, wait_for_false

    def demo():
      return True

    wait_for_true(demo, interval=1, timeout=5)

    wait_for_false(demo, interval=1, timeout=5)
    ```
4. **use wait_for**
    from wait import wait_for

    def func():
        import random
        return random.randint(0, 1)

    wait_for(func, 0)
    ```

# how to contribute
1. **visit https://github.com/dvdface/waitutil**
2. **submit your contribute**
