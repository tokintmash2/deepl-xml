package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
)

type data struct {
	Text        string `json:"text"`
	TagHandling string `json:"tag_handling"`
}

func main() {

	textToTranslate := strings.NewReader(`text=hello&tag_handling=xml&target_lang=ET`)

	keyFile, err := os.Open("key")
	if err != nil {
		fmt.Println("Error:", err)
	}
	// fmt.Println("API Key:", keyFile)
	defer keyFile.Close()

	APIkey, err := io.ReadAll(keyFile)
	if err != nil {
		fmt.Println("Error:", err)
	}
	// fmt.Println("API Key:", string(APIkey))

	url := "https://api-free.deepl.com/v2/translate"
	req, err := http.NewRequest("POST", url, textToTranslate)
	if err != nil {
		fmt.Println("Error:", err)
	}

	req.Header.Add("Authorization", "DeepL-Auth-Key "+string(APIkey))
	req.Header.Add("Content-Type", "application/x-www-form-urlencoded")

	res, err := http.DefaultClient.Do(req)
	if err != nil {
		fmt.Println("Error:", err)
	}

	defer res.Body.Close()

	body, readErr := io.ReadAll(res.Body)
	if readErr != nil {
		fmt.Print(err.Error())
	}
	fmt.Println(string(body))
}
