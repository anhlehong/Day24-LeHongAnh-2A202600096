"""
Lab 24 — Full Evaluation & Guardrail System Demo
Author: Lê Hồng Anh — MSSV: 2A202600096

Streamlit app to demonstrate all 4 phases of the lab.
Run: streamlit run streamlit_demo.py
"""
import streamlit as st
import pandas as pd
import json
import re
import time
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

# ──────────────────────────────────────────────────────────────
# Page Config
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Lab 24 — Lê Hồng Anh",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ Lab 24 — Full Evaluation & Guardrail System")
st.markdown("**Lê Hồng Anh** — MSSV: **2A202600096**")
st.markdown("---")

# Sidebar navigation
page = st.sidebar.radio(
    "📑 Chọn Phase để demo",
    [
        "🏠 Tổng quan",
        "📊 Phase A — RAGAS Evaluation",
        "⚖️ Phase B — LLM-as-Judge",
        "🔒 Phase C — Guardrails (Live Demo)",
        "📐 Phase D — Blueprint",
    ],
)

# ──────────────────────────────────────────────────────────────
# HOME PAGE
# ──────────────────────────────────────────────────────────────
if page == "🏠 Tổng quan":
    st.header("Tổng quan hệ thống")
    st.markdown("""
    Hệ thống **Evaluation & Guardrail** cho RAG pipeline gồm 4 phase:

    | Phase | Nội dung | Điểm |
    |-------|----------|------|
    | **A** | RAGAS Evaluation — đo chất lượng RAG | 30 |
    | **B** | LLM-as-Judge — chấm output bằng LLM | 25 |
    | **C** | Guardrails — PII, Topic, Adversarial, Llama Guard | 35 |
    | **D** | Blueprint — SLO, Architecture, Playbook, Cost | 10 |
    """)

    st.subheader("Kiến trúc hệ thống")
    st.code("""
User Input
  ↓
[L1] Input Guards (parallel)
  ├─ PII Redaction (Presidio + VN regex)
  ├─ Topic Validator (embedding similarity)
  └─ Injection Detection
  ↓
[L2] RAG Pipeline
  ↓
[L3] Output Guard (Llama Guard 3)
  ↓
[L4] Audit Log (async)
  ↓
Response
    """, language="text")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Faithfulness", "0.69")
    col2.metric("Answer Relevancy", "0.74")
    col3.metric("Cohen's Kappa", "0.65")
    col4.metric("PII Detection", "90%")

# ──────────────────────────────────────────────────────────────
# PHASE A — RAGAS
# ──────────────────────────────────────────────────────────────
elif page == "📊 Phase A — RAGAS Evaluation":
    st.header("Phase A — RAGAS Evaluation (30 pts)")

    # Load summary
    with open(PROJECT_ROOT / "phase-a" / "ragas_summary.json") as f:
        summary = json.load(f)

    st.subheader("1. Kết quả RAGAS Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Faithfulness", f"{summary['faithfulness']:.2f}")
    col2.metric("Answer Relevancy", f"{summary['answer_relevancy']:.2f}")
    col3.metric("Context Precision", f"{summary['context_precision']:.2f}")
    col4.metric("Context Recall", f"{summary['context_recall']:.2f}")

    st.info(f"💰 Tổng chi phí API: ${summary.get('total_api_cost_usd', 0.0134):.4f}")

    # Load test set
    st.subheader("2. Test Set Distribution")
    testset_df = pd.read_csv(PROJECT_ROOT / "phase-a" / "testset_v1.csv")
    dist = testset_df["evolution_type"].value_counts()
    st.bar_chart(dist)
    st.caption(f"Tổng: {len(testset_df)} câu hỏi — Simple: {dist.get('simple',0)}, Multi-context: {dist.get('multi_context',0)}, Reasoning: {dist.get('reasoning',0)}")

    # Load results
    st.subheader("3. RAGAS Results (chi tiết)")
    results_df = pd.read_csv(PROJECT_ROOT / "phase-a" / "ragas_results.csv")
    st.dataframe(results_df[["question", "answer", "ground_truth", "evolution_type"]].head(10), use_container_width=True)

    # Failure analysis
    st.subheader("4. Failure Cluster Analysis")
    with open(PROJECT_ROOT / "phase-a" / "failure_analysis.md") as f:
        st.markdown(f.read())

# ──────────────────────────────────────────────────────────────
# PHASE B — LLM-as-Judge
# ──────────────────────────────────────────────────────────────
elif page == "⚖️ Phase B — LLM-as-Judge":
    st.header("Phase B — LLM-as-Judge (25 pts)")

    # Kappa
    with open(PROJECT_ROOT / "phase-b" / "kappa_analysis.json") as f:
        kappa = json.load(f)

    col1, col2, col3 = st.columns(3)
    col1.metric("Cohen's Kappa", f"{kappa['cohen_kappa']:.2f}")
    col2.metric("Agreement %", f"{kappa['agreement_pct']:.0%}")
    col3.metric("Human Labels", kappa['human_labels_count'])

    # Absolute scores
    st.subheader("1. Absolute Scoring (4 dimensions)")
    abs_df = pd.read_csv(PROJECT_ROOT / "phase-b" / "absolute_scores.csv")
    avg_scores = abs_df[["accuracy", "relevance", "conciseness", "helpfulness"]].mean()
    st.bar_chart(avg_scores)
    st.dataframe(abs_df.head(10), use_container_width=True)

    # Pairwise
    st.subheader("2. Pairwise Comparison (Swap-and-Average)")
    pw_df = pd.read_csv(PROJECT_ROOT / "phase-b" / "pairwise_results.csv")
    st.dataframe(pw_df, use_container_width=True)
    st.markdown("""
    **Swap-and-average**: Mỗi cặp được đánh giá 2 lần (đổi vị trí A↔B), giảm **position bias**.
    """)

    # Bias report
    st.subheader("3. Bias Report")
    with open(PROJECT_ROOT / "phase-b" / "judge_bias_report.md") as f:
        st.markdown(f.read())

# ──────────────────────────────────────────────────────────────
# PHASE C — Guardrails (LIVE DEMO)
# ──────────────────────────────────────────────────────────────
elif page == "🔒 Phase C — Guardrails (Live Demo)":
    st.header("Phase C — Guardrails (35 pts)")

    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 PII Detection (Live)",
        "📋 PII Test Results",
        "🛡️ Adversarial Tests",
        "⏱️ Latency Benchmark",
    ])

    # ── TAB 1: Live PII Demo ──
    with tab1:
        st.subheader("Live PII Detection & Redaction")
        st.markdown("Nhập text chứa thông tin cá nhân (PII) — hệ thống sẽ phát hiện và che dấu.")

        # Pre-built examples
        examples = {
            "Chọn ví dụ...": "",
            "🇻🇳 CCCD + SĐT": "Tôi là Nguyễn Văn A, CCCD 012345678901, SĐT 0987654321",
            "🇬🇧 Email + Phone": "Contact John at john.doe@gmail.com or +84912345678",
            "🧾 Tax code": "Mã số thuế: 0123456789-001, email: info@company.vn",
            "🔒 Không có PII": "Lãi suất tiết kiệm hiện tại là bao nhiêu?",
        }
        selected_example = st.selectbox("Chọn ví dụ hoặc tự nhập:", list(examples.keys()))

        user_input = st.text_area(
            "Nhập text:",
            value=examples[selected_example],
            height=100,
            placeholder="Nhập text chứa PII để test...",
        )

        if st.button("🔍 Phát hiện & Che dấu PII", type="primary"):
            if user_input.strip():
                start = time.perf_counter()

                # VN regex patterns
                VN_PII = {
                    "cccd": r"\b\d{12}\b",
                    "phone_vn": r"(\+84|0)\d{9,10}",
                    "tax_code": r"\b\d{10}(-\d{3})?\b",
                    "email": r"\b[\w.-]+@[\w.-]+\.\w+\b",
                }

                output = user_input
                pii_found = []

                for name, pattern in VN_PII.items():
                    matches = re.findall(pattern, output)
                    if matches:
                        pii_found.append((name, len(matches) if isinstance(matches[0], str) else len(matches)))
                        output = re.sub(pattern, f"**[{name.upper()}]**", output)

                latency_ms = (time.perf_counter() - start) * 1000

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Input gốc:**")
                    st.warning(user_input)
                with col2:
                    st.markdown("**Output đã redact:**")
                    st.success(output)

                if pii_found:
                    st.error(f"⚠️ Phát hiện PII: {', '.join([f'{name} ({count})' for name, count in pii_found])}")
                else:
                    st.info("✅ Không phát hiện PII — text an toàn.")

                st.caption(f"⏱️ Latency: {latency_ms:.3f} ms")
            else:
                st.warning("Vui lòng nhập text.")

    # ── TAB 2: PII Test Results ──
    with tab2:
        st.subheader("Kết quả PII Test (10 test cases)")
        pii_df = pd.read_csv(PROJECT_ROOT / "phase-c" / "pii_test_results.csv")
        st.dataframe(pii_df, use_container_width=True)

        detected = pii_df[pii_df["pii_found"] != "none"].shape[0]
        total_with_pii = pii_df[pii_df["input"].str.strip().str.len() > 0].shape[0]
        st.metric("Detection Rate", f"{detected}/{total_with_pii}")

    # ── TAB 3: Adversarial ──
    with tab3:
        st.subheader("Adversarial Attack Results (20 attacks)")
        adv_df = pd.read_csv(PROJECT_ROOT / "phase-c" / "adversarial_test_results.csv")
        st.dataframe(adv_df, use_container_width=True)

        blocked = adv_df[adv_df["blocked"].astype(str).str.lower() == "true"].shape[0]
        total = len(adv_df)
        st.metric("Block Rate", f"{blocked}/{total} ({blocked/total:.0%})")

        # Breakdown by attack type
        st.subheader("Breakdown theo loại tấn công")
        breakdown = adv_df.groupby("attack_type")["blocked"].apply(
            lambda x: x.astype(str).str.lower().eq("true").sum()
        ).reset_index(name="blocked_count")
        breakdown["total"] = adv_df.groupby("attack_type").size().values
        st.dataframe(breakdown, use_container_width=True)

    # ── TAB 4: Latency ──
    with tab4:
        st.subheader("Latency Benchmark")
        with open(PROJECT_ROOT / "phase-c" / "latency_summary.json") as f:
            lat = json.load(f)

        col1, col2, col3 = st.columns(3)
        col1.metric("L1 (Input Guards) P95", f"{lat['L1_P95']:.0f} ms")
        col2.metric("L2 (RAG Pipeline) P95", f"{lat['L2_P95']:.0f} ms")
        col3.metric("L3 (Llama Guard) P95", f"{lat['L3_P95']:.0f} ms")

        bench_df = pd.read_csv(PROJECT_ROOT / "phase-c" / "latency_benchmark.csv")
        st.line_chart(bench_df["latency_ms"], use_container_width=True)
        st.caption("Latency (ms) cho 100 queries benchmark")

# ──────────────────────────────────────────────────────────────
# PHASE D — Blueprint
# ──────────────────────────────────────────────────────────────
elif page == "📐 Phase D — Blueprint":
    st.header("Phase D — Production Blueprint (10 pts)")

    with open(PROJECT_ROOT / "phase-d" / "blueprint.md") as f:
        st.markdown(f.read())

# ──────────────────────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("Lab 24 — Lê Hồng Anh (2A202600096) | Full Evaluation & Guardrail System")
