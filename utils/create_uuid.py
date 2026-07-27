import random
import string

def create_uuid():
    """
    Generating UUIDs for artist profiles
    #### Example:
    ```python
       print(create_uuid())
    ```
    """
    letters = string.ascii_letters
    uuid = ''.join(random.choice(letters) for _ in range(25))
    return uuid