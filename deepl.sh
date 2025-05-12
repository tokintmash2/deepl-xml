curl -X POST 'https://api-free.deepl.com/v2/translate' \
--header 'Authorization: DeepL-Auth-Key a57ff645-14a2-4baf-9a76-9f2127927223:fx' \
--header 'Content-Type: application/json' \
--data '{
  "text": [
    "Hello, world!"
  ],
  "target_lang": "DE"
}'