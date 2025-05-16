package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"path/filepath"
	"strings"
)

type SaveData struct {
	Translations []struct {
		DetectedSourceLanguage string `json:"detected_source_language"`
		Text                   string `json:"text"`
	} `json:"translations"`
}

func main() {

	keyFilePath := "key"
	xmlFilePath := "test.xml"
	sourcePath := "source"

	APIkey := readFile(keyFilePath)

	entries, err := os.ReadDir(sourcePath)
	if err != nil {
		fmt.Println("Error reading directory:", err)
		return
	}
	for _, entry := range entries {
		fmt.Println(entry.Name())
		fmt.Println(filepath.Join(sourcePath, entry.Name()))
	}
		
	xmlBytes := readFile(xmlFilePath)

	xmlContent := string(xmlBytes) // read from file
	form := fmt.Sprintf("text=%s&tag_handling=xml&target_lang=ET", url.QueryEscape(xmlContent))
	reader := strings.NewReader(form)

	url := "https://api-free.deepl.com/v2/translate"
	req, err := http.NewRequest("POST", url, reader)
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

	var result SaveData

	err = json.Unmarshal(body, &result)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}

	writeXMLFile("translated.xml", result.Translations[0].Text)
	fmt.Println(result.Translations[0].Text)
}

func writeXMLFile(filePath string, data string) {
	file, err := os.Create(filePath)
	if err != nil {
		fmt.Println("Error creating file:", err)
		return
	}
	defer file.Close()

	writer := bufio.NewWriter(file)
	_, err = writer.WriteString(data)
	if err != nil {
		fmt.Println("Error writing to file:", err)
		return
	}

	writer.Flush()
}

func readFile(filePath string) []byte {
	file, err := os.Open(filePath)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return nil
	}
	defer file.Close()

	data, err := io.ReadAll(file)
	if err != nil {
		fmt.Println("Error reading file:", err)
		return nil
	}

	return data
}
