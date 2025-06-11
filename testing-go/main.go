package main

import (
	"fmt"
	"sync"
	"time"
)

func worker(id int) {
	fmt.Printf("Worker %d starting\n", id)

	time.Sleep(time.Second)
	fmt.Printf("Worker %d done\n", id)
}

func main() {

	var wg sync.WaitGroup

	semaphore := make(chan struct{}, 2) // Limit to 2 concurrent workers

	for i := 1; i <= 5; i++ {
		wg.Add(1)

		go func(id int) {
			semaphore <- struct{}{} // Acquire a token
			defer wg.Done()
			worker(i)
			<-semaphore // Release the token
		}(i)
	}
	wg.Wait()


}
