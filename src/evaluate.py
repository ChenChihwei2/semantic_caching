precision_at_k = correct_in_topk / total
recall_at_k = correct_in_topk / total_relevant
hit_rate = hits / total
avg_similarity = sum(similarities) / len(similarities)
avg_latency = (end_time - start_time)


metrics = {
    "Precision@3": precision_at_3,
    "Recall@3": recall_at_3,
    "HitRate": hit_rate,
    "AvgSimilarity": avg_sim,
    "AvgLatency_ms": avg_latency
}
json.dump(metrics, open("results/metrics_summary.json","w"), indent=2)
