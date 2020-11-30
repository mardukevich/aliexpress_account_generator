# aliexpress_account_generator
This program registers aliexpress accounts using selenium.
Mail and password are generated automatically and save to files/accounts.txt
# requirements
```
pip3 install selenium http_request_randomizer
```
# Proxies
One account - one ip. For changing ip use proxy,  http_request_randomizer (https://github.com/pgaref/HTTP_Request_Randomizer) is used to get proxy list.
# How to use
```
python3 autoreger.py
```
# P.S.
it's not works well, aliexpress can determine that it's a bot.
if you want create bot's like that, use browser automation studio (BAS), it's better and faster in development. 
