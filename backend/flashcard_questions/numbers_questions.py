"""
Numbers questions for system design metrics and scale.

Covers latency (RAM, SSD, network), throughput (Kafka, web servers),
storage (YouTube scale), QPS, capacity, bandwidth, database performance,
cache hit ratios, and availability numbers.
"""

from typing import List
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flashcard_types import NumbersQuestion

NUMBERS_QUESTIONS: List[NumbersQuestion] = [
    {
        "id": "numbers-1",
        "category": "Latency",
        "question": "What is the typical latency for a RAM access?",
        "answer": "100 nanoseconds (ns)",
        "context": "This is 1,500x faster than SSD random read (150 μs)"
    },
    {
        "id": "numbers-2",
        "category": "Latency",
        "question": "What is the typical latency for an SSD random read?",
        "answer": "150 microseconds (μs)",
        "context": "This is 1,500x slower than RAM but 100x faster than HDD"
    },
    {
        "id": "numbers-3",
        "category": "Latency",
        "question": "What is the typical latency for network within same datacenter?",
        "answer": "0.5 milliseconds (ms)",
        "context": "Baseline for microservice communication"
    },
    {
        "id": "numbers-4",
        "category": "Latency",
        "question": "What is the typical latency for network between US coasts (SF to NYC)?",
        "answer": "40 milliseconds (ms)",
        "context": "Important for multi-region deployments"
    },
    {
        "id": "numbers-5",
        "category": "Throughput",
        "question": "How much data can Kafka handle per second per partition?",
        "answer": "~10 MB/s per partition",
        "context": "Use multiple partitions for higher throughput"
    },
    {
        "id": "numbers-6",
        "category": "Throughput",
        "question": "How many requests can a typical web server handle per second?",
        "answer": "~1,000-10,000 requests/second",
        "context": "Depends on request complexity and server specs"
    },
    {
        "id": "numbers-7",
        "category": "Storage",
        "question": "How much storage does YouTube handle?",
        "answer": "~1 exabyte (1,000 petabytes)",
        "context": "Reference for large-scale video storage systems"
    },
    {
        "id": "numbers-8",
        "category": "Scale",
        "question": "How many tweets are sent per day?",
        "answer": "~500 million tweets/day",
        "context": "~6,000 tweets/second average, 10,000+ peak"
    },
    {
        "id": "numbers-9",
        "category": "Scale",
        "question": "How many Google searches per day?",
        "answer": "~8 billion searches/day",
        "context": "~90,000 searches/second average"
    },
    {
        "id": "numbers-10",
        "category": "QPS",
        "question": "What is a typical read:write ratio for social media?",
        "answer": "100:1 (read-heavy)",
        "context": "Optimize for read performance with caching and replicas"
    },
    {
        "id": "numbers-11",
        "category": "Capacity",
        "question": "How many connections can a typical load balancer handle?",
        "answer": "~50,000-100,000 concurrent connections",
        "context": "Modern load balancers like HAProxy, NGINX"
    },
    {
        "id": "numbers-12",
        "category": "Bandwidth",
        "question": "What is typical internet bandwidth per user?",
        "answer": "~100 Mbps (home), ~1 Gbps (datacenter)",
        "context": "Use for calculating video streaming bitrates"
    },
    {
        "id": "numbers-13",
        "category": "Database",
        "question": "How many queries per second can MySQL handle?",
        "answer": "~10,000 simple queries/second",
        "context": "With proper indexing and hardware"
    },
    {
        "id": "numbers-14",
        "category": "Cache",
        "question": "What is a good cache hit ratio?",
        "answer": "80-90%",
        "context": "Below 70% suggests cache is not effective"
    },
    {
        "id": "numbers-15",
        "category": "Availability",
        "question": "How much downtime does 99.99% availability allow per year?",
        "answer": "52 minutes per year",
        "context": "Also called 'four nines' availability"
    }
]
