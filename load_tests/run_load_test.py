import asyncio
import argparse
import sys
from .load_runner import LoadRunner
from .generate_report import generate_load_excel_report

def main():
    parser = argparse.ArgumentParser(description="CiviFix API Baseline/Load Test Runner")
    parser.add_argument("--users", type=int, default=100, help="Number of concurrent virtual users")
    parser.add_argument("--duration", type=int, default=60, help="Test duration in seconds")
    parser.add_argument("--output", type=str, default="CiviFix_LoadTest_Execution_Report.xlsx", help="Excel report output filename")
    
    args = parser.parse_args()
    
    # Run the async load tester
    runner = LoadRunner(concurrency=args.users, duration_sec=args.duration)
    
    try:
        results = asyncio.run(runner.run())
        # Generate the Excel report
        generate_load_excel_report(results, args.output)
    except KeyboardInterrupt:
        print("\n[WARN] Load test interrupted by user.")
        sys.exit(1)
        
if __name__ == "__main__":
    main()
