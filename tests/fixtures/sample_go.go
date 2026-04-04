package main

import (
	"context"
	"fmt"
	"sync"
	"time"
)

type Result struct {
	Value string
	Err   error
}

func fetchAll(ctx context.Context, urls []string) []Result {
	var wg sync.WaitGroup
	results := make([]Result, len(urls))

	for i, url := range urls {
		wg.Add(1)
		go func(idx int, u string) {
			defer wg.Done()
			select {
			case <-ctx.Done():
				results[idx] = Result{Err: ctx.Err()}
			case <-time.After(2 * time.Second):
				results[idx] = Result{Value: fmt.Sprintf("fetched %s", u)}
			}
		}(i, url)
	}

	wg.Wait()
	return results
}
