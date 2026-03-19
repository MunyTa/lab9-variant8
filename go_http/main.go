package main

import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "os"
    "strings"
    "time"
)

type ProcessRequest struct {
    Text    string `json:"text"`
    Option  string `json:"option"`
}

type ProcessResponse struct {
    Result    string    `json:"result"`
    Timestamp string    `json:"timestamp"`
    Status    string    `json:"status"`
}

type ServerStats struct {
    StartTime    time.Time
    RequestCount int
}

var stats ServerStats

func main() {
    stats = ServerStats{
        StartTime: time.Now(),
        RequestCount: 0,
    }

    http.HandleFunc("/api/process", processHandler)
    http.HandleFunc("/api/health", healthHandler)
    http.HandleFunc("/api/stats", statsHandler)
    http.HandleFunc("/", rootHandler)

    port := ":8080"
    if len(os.Args) > 1 {
        port = ":" + os.Args[1]
    }

    fmt.Printf("🚀 HTTP сервер запущен на порту %s\n", port)
    fmt.Printf("📝 Доступные эндпоинты:\n")
    fmt.Printf("   POST /api/process - обработка текста\n")
    fmt.Printf("   GET  /api/health  - проверка здоровья\n")
    fmt.Printf("   GET  /api/stats   - статистика сервера\n")
    fmt.Printf("   GET  /            - приветствие\n")
    fmt.Println(strings.Repeat("-", 50))
    
    log.Fatal(http.ListenAndServe(port, nil))
}

func processHandler(w http.ResponseWriter, r *http.Request) {
    stats.RequestCount++

    if r.Method != http.MethodPost {
        sendError(w, "Only POST method allowed", http.StatusMethodNotAllowed)
        return
    }

    var req ProcessRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        sendError(w, "Invalid JSON format", http.StatusBadRequest)
        return
    }

    if req.Text == "" {
        sendError(w, "Text field is required", http.StatusBadRequest)
        return
    }

    var result string
    switch req.Option {
    case "reverse":
        result = reverseString(req.Text)
    case "uppercase":
        result = strings.ToUpper(req.Text)
    case "lowercase":
        result = strings.ToLower(req.Text)
    case "count":
        result = fmt.Sprintf("Количество символов: %d", len(req.Text))
    case "words":
        words := strings.Fields(req.Text)
        result = fmt.Sprintf("Количество слов: %d", len(words))
    default:
        result = req.Text
    }

    response := ProcessResponse{
        Result:    result,
        Timestamp: time.Now().Format(time.RFC3339),
        Status:    "success",
    }

    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusOK)
    json.NewEncoder(w).Encode(response)
    
    log.Printf("✅ Обработан запрос: option=%s, text=%s", req.Option, req.Text)
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodGet {
        sendError(w, "Only GET method allowed", http.StatusMethodNotAllowed)
        return
    }

    response := map[string]interface{}{
        "status": "healthy",
        "time":   time.Now().Format(time.RFC3339),
        "uptime": time.Since(stats.StartTime).String(),
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}

func statsHandler(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodGet {
        sendError(w, "Only GET method allowed", http.StatusMethodNotAllowed)
        return
    }

    response := map[string]interface{}{
        "start_time":     stats.StartTime.Format(time.RFC3339),
        "uptime":         time.Since(stats.StartTime).String(),
        "request_count":  stats.RequestCount,
        "requests_per_second": float64(stats.RequestCount) / time.Since(stats.StartTime).Seconds(),
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}

func rootHandler(w http.ResponseWriter, r *http.Request) {
    if r.URL.Path != "/" {
        http.NotFound(w, r)
        return
    }

    html := `
    <!DOCTYPE html>
    <html>
    <head>
        <title>Go HTTP Server</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
            h1 { color: #00ADD8; }
            code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>🚀 Go HTTP Server is running!</h1>
        <p>Это HTTP-сервер, созданный для лабораторной работы.</p>
        <h2>Доступные эндпоинты:</h2>
        <ul>
            <li><code>POST /api/process</code> - обработка текста</li>
            <li><code>GET /api/health</code> - проверка здоровья</li>
            <li><code>GET /api/stats</code> - статистика сервера</li>
        </ul>
        <h3>Пример использования /api/process:</h3>
        <pre><code>curl -X POST http://localhost:8080/api/process \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello World", "option": "reverse"}'</code></pre>
    </body>
    </html>
    `
    
    w.Header().Set("Content-Type", "text/html; charset=utf-8")
    w.WriteHeader(http.StatusOK)
    fmt.Fprint(w, html)
}

func sendError(w http.ResponseWriter, message string, statusCode int) {
    response := map[string]interface{}{
        "error":   message,
        "status":  "error",
        "code":    statusCode,
    }
    
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(statusCode)
    json.NewEncoder(w).Encode(response)
    
    log.Printf("❌ Ошибка %d: %s", statusCode, message)
}

func reverseString(s string) string {
    runes := []rune(s)
    for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
        runes[i], runes[j] = runes[j], runes[i]
    }
    return string(runes)
}