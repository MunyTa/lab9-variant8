#!/usr/bin/env python
"""
Главное приложение для лабораторной работы №9
Интеграция Go + Rust + Python
"""

import argparse
import sys
from pathlib import Path
from orchestrator import IntegrationDemo

def main():
    parser = argparse.ArgumentParser(description="Lab 9: Go + Rust + Python Integration")
    
    parser.add_argument(
        "--go-binary",
        type=Path,
        default=Path("../go_http/http_server.exe"),
        help="Path to Go HTTP server binary"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8081,
        help="Port for Go server"
    )
    
    parser.add_argument(
        "--image",
        type=Path,
        default=Path("test_image.jpg"),
        help="Path to test image for image processing"
    )
    
    args = parser.parse_args()
    
    if not args.go_binary.exists():
        print(f"❌ Go бинарь не найден: {args.go_binary}")
        print("Сначала скомпилируйте: cd go_http && go build -o http_server.exe")
        return 1
    
    try:
        demo = IntegrationDemo(args.go_binary, args.port)
        demo.run_demo(args.image)
    except KeyboardInterrupt:
        print("\n👋 Программа остановлена пользователем")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())