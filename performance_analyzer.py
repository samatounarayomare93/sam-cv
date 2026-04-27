#!/usr/bin/env python
"""
performance_analyzer.py - Analyze and optimize application performance
Usage: python performance_analyzer.py [--profile] [--benchmark] [--memory]
"""

import sys
import time
import psutil
import asyncio
from pathlib import Path
import json
from datetime import datetime

class PerformanceAnalyzer:
    def __init__(self):
        self.metrics = {
            "timestamp": datetime.now().isoformat(),
            "cpu": {},
            "memory": {},
            "disk": {},
            "benchmarks": {}
        }
    
    def get_system_metrics(self):
        """Get current system performance metrics"""
        print("\n📊 SYSTEM PERFORMANCE METRICS")
        print("-" * 60)
        
        # CPU metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        print(f"CPU Usage: {cpu_percent}% ({cpu_count} cores)")
        self.metrics["cpu"]["usage_percent"] = cpu_percent
        self.metrics["cpu"]["core_count"] = cpu_count
        
        # Memory metrics
        memory = psutil.virtual_memory()
        print(f"Memory: {memory.percent}% used ({memory.used / 1024**3:.1f}GB / {memory.total / 1024**3:.1f}GB)")
        self.metrics["memory"]["percent"] = memory.percent
        self.metrics["memory"]["used_gb"] = memory.used / 1024**3
        self.metrics["memory"]["total_gb"] = memory.total / 1024**3
        
        # Disk metrics
        disk = psutil.disk_usage("/")
        print(f"Disk: {disk.percent}% used ({disk.used / 1024**3:.1f}GB / {disk.total / 1024**3:.1f}GB)")
        self.metrics["disk"]["percent"] = disk.percent
        self.metrics["disk"]["used_gb"] = disk.used / 1024**3
        self.metrics["disk"]["total_gb"] = disk.total / 1024**3
        
        return cpu_percent < 80 and memory.percent < 80 and disk.percent < 80
    
    def benchmark_imports(self):
        """Benchmark module import times"""
        print("\n⏱️  MODULE IMPORT BENCHMARKS")
        print("-" * 60)
        
        modules = [
            "core.main_bot",
            "core.telegram_dashboard",
            "core.ai_agent",
            "core.db_client",
            "core.smtp_engine",
            "core.pdf_generator"
        ]
        
        for module in modules:
            try:
                start = time.time()
                __import__(module)
                elapsed = time.time() - start
                status = "✅ Fast" if elapsed < 0.5 else "⚠️  Slow"
                print(f"{status}: {module} ({elapsed*1000:.0f}ms)")
                self.metrics["benchmarks"][module] = {
                    "time_ms": elapsed * 1000,
                    "status": "fast" if elapsed < 0.5 else "slow"
                }
            except Exception as e:
                print(f"❌ Error: {module} ({str(e)})")
    
    def check_memory_leaks(self):
        """Check for potential memory leaks"""
        print("\n🔍 MEMORY LEAK DETECTION")
        print("-" * 60)
        
        # Monitor memory over time
        print("Monitoring memory usage over 10 seconds...")
        memory_samples = []
        
        for i in range(10):
            memory = psutil.virtual_memory().used / 1024**2  # MB
            memory_samples.append(memory)
            time.sleep(1)
            sys.stdout.write(f"\r  Sample {i+1}/10: {memory:.1f}MB")
        
        print("\n")
        
        # Analyze trend
        growth = memory_samples[-1] - memory_samples[0]
        growth_percent = (growth / memory_samples[0] * 100) if memory_samples[0] > 0 else 0
        
        if growth < 10:  # Less than 10MB growth
            print(f"✅ Memory stable (growth: {growth:.1f}MB)")
            self.metrics["memory"]["leak_risk"] = "low"
        elif growth < 50:
            print(f"⚠️  Possible memory leak (growth: {growth:.1f}MB)")
            self.metrics["memory"]["leak_risk"] = "medium"
        else:
            print(f"🔴 Potential memory leak (growth: {growth:.1f}MB)")
            self.metrics["memory"]["leak_risk"] = "high"
    
    def analyze_code_structure(self):
        """Analyze code structure for optimization opportunities"""
        print("\n📐 CODE STRUCTURE ANALYSIS")
        print("-" * 60)
        
        stats = {
            "total_files": 0,
            "total_lines": 0,
            "avg_file_size": 0,
            "largest_file": None,
            "largest_file_size": 0
        }
        
        # Analyze Python files
        py_files = list(Path("core").glob("**/*.py"))
        
        for file in py_files:
            lines = len(file.read_text().split("\n"))
            stats["total_files"] += 1
            stats["total_lines"] += lines
            
            if lines > stats["largest_file_size"]:
                stats["largest_file_size"] = lines
                stats["largest_file"] = str(file)
        
        if stats["total_files"] > 0:
            stats["avg_file_size"] = stats["total_lines"] / stats["total_files"]
        
        print(f"Total Python files: {stats['total_files']}")
        print(f"Total lines of code: {stats['total_lines']}")
        print(f"Average file size: {stats['avg_file_size']:.0f} lines")
        print(f"Largest file: {stats['largest_file']} ({stats['largest_file_size']} lines)")
        
        self.metrics["code_structure"] = stats
        
        # Optimization suggestions
        if stats["largest_file_size"] > 1000:
            print("\n💡 Consider breaking down large files into smaller modules")
    
    def generate_recommendations(self):
        """Generate performance optimization recommendations"""
        print("\n💡 PERFORMANCE OPTIMIZATION RECOMMENDATIONS")
        print("-" * 60)
        
        recommendations = []
        
        if self.metrics["cpu"]["usage_percent"] > 70:
            recommendations.append("High CPU usage - consider increasing batch processing time")
        
        if self.metrics["memory"]["percent"] > 70:
            recommendations.append("High memory usage - implement caching strategies")
        
        if self.metrics["disk"]["percent"] > 80:
            recommendations.append("Low disk space - cleanup old logs and backups")
        
        if not recommendations:
            recommendations.append("System performance is excellent - no urgent optimizations needed")
        
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")
        
        self.metrics["recommendations"] = recommendations
    
    def save_report(self):
        """Save performance analysis report"""
        report_file = Path(f"performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        report_file.write_text(json.dumps(self.metrics, indent=2))
        print(f"\n📊 Report saved: {report_file}")
    
    def run_full_analysis(self):
        """Run complete performance analysis"""
        print("\n" + "="*60)
        print("PERFORMANCE ANALYSIS SUITE")
        print("="*60)
        
        self.get_system_metrics()
        self.benchmark_imports()
        self.check_memory_leaks()
        self.analyze_code_structure()
        self.generate_recommendations()
        self.save_report()
        
        print("\n" + "="*60)
        print("✅ PERFORMANCE ANALYSIS COMPLETE")
        print("="*60)

def main():
    analyzer = PerformanceAnalyzer()
    analyzer.run_full_analysis()
    return 0

if __name__ == "__main__":
    sys.exit(main())
