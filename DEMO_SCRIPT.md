# 🎬 Script Demo Video — Lab 24

**Người thực hiện:** Lê Hồng Anh — MSSV: 2A202600096  
**Thời lượng khuyến nghị:** 5–7 phút  
**Công cụ:** Quay màn hình (OBS / ShareX / Win+G) + mic

---

## Cách chạy demo

```bash
pip install streamlit pandas numpy
cd e:\work\vinuni\week_6\Day24-LeHongAnh-2A202600096
streamlit run streamlit_demo.py
```

---

## PHẦN 0: Giới thiệu (~30 giây)

**Nói:**
> "Xin chào, em là Lê Hồng Anh, MSSV 2A202600096. Hôm nay em sẽ demo Lab 24 — Full Evaluation & Guardrail System cho RAG pipeline. Hệ thống gồm 4 phase: RAGAS Evaluation, LLM-as-Judge, Guardrails, và Production Blueprint."

**Thao tác:** Mở Streamlit app, đang ở trang **Tổng quan**. Chỉ vào kiến trúc hệ thống và 4 metrics chính.

---

## PHẦN 1: Phase A — RAGAS Evaluation (~1 phút)

**Thao tác:** Click vào **"📊 Phase A — RAGAS Evaluation"** trong sidebar.

**Nói:**
> "Phase A: em sử dụng RAGAS framework để đánh giá chất lượng RAG pipeline."
>
> "Em tạo test set gồm 50 câu hỏi, phân bố: 50% simple, 25% multi-context, 25% reasoning. Các câu hỏi về banking và compliance."
>
> "Kết quả 4 RAGAS metrics: Faithfulness 0.69, Answer Relevancy 0.74, Context Precision 0.62, Context Recall 0.68. Chi phí API chỉ khoảng $0.02."

**Thao tác:** Scroll xuống biểu đồ distribution, rồi bảng results.

> "Em cũng phân tích failure clusters — 3 nhóm chính: multi-hop reasoning failures do top-k quá thấp, off-topic retrievals do embedding model chưa fine-tune, và simple question failures do chunk boundaries cắt ngang câu."

---

## PHẦN 2: Phase B — LLM-as-Judge (~1 phút)

**Thao tác:** Click vào **"⚖️ Phase B — LLM-as-Judge"** trong sidebar.

**Nói:**
> "Phase B: em dùng LLM làm judge để chấm điểm output."
>
> "Đầu tiên là Absolute Scoring — mỗi câu trả lời được chấm 4 chiều: accuracy, relevance, conciseness, helpfulness, thang 1-5."

**Thao tác:** Chỉ vào biểu đồ bar chart average scores.

> "Tiếp theo là Pairwise Comparison với kỹ thuật swap-and-average. Mỗi cặp câu trả lời được đánh giá 2 lần, đổi vị trí A và B, để giảm position bias."
>
> "Cohen's Kappa so với human labels là 0.65 — mức substantial agreement, đủ để deploy production."

**Thao tác:** Scroll xuống Bias Report.

> "Em phát hiện 2 loại bias: position bias — A thắng 57% khi đứng đầu, và length bias — câu dài hơn thắng 73%. Mitigation bằng swap-and-average và thêm brevity criterion trong rubric."

---

## PHẦN 3: Phase C — Guardrails (LIVE DEMO) (~2 phút) ⭐

**Đây là phần quan trọng nhất — demo live!**

**Thao tác:** Click vào **"🔒 Phase C — Guardrails (Live Demo)"** trong sidebar.

### 3.1 — PII Detection Live

**Nói:**
> "Bây giờ em demo live PII detection. Hệ thống dùng regex pattern cho tiếng Việt và Presidio NER cho tiếng Anh."

**Thao tác:** 
1. Chọn ví dụ **"🇻🇳 CCCD + SĐT"** → Click **"Phát hiện & Che dấu PII"**

> "Ví dụ 1: Input có CCCD và số điện thoại Việt Nam. Hệ thống phát hiện và thay bằng [CCCD] và [PHONE_VN]."

2. Chọn ví dụ **"🇬🇧 Email + Phone"** → Click button

> "Ví dụ 2: Email và số điện thoại quốc tế. Hệ thống phát hiện email pattern."

3. Tự nhập: `Tôi là Lê Hồng Anh, CCCD 012345678901, email anh@gmail.com` → Click button

> "Ví dụ 3: em tự nhập text — hệ thống detect cả CCCD và email."

4. Chọn ví dụ **"🔒 Không có PII"** → Click button

> "Ví dụ 4: text bình thường — không có PII, hệ thống confirm an toàn."

### 3.2 — Test Results

**Thao tác:** Click tab **"📋 PII Test Results"**

> "Đây là kết quả test 10 test cases, bao gồm cả edge cases như empty string, text rất dài, và multiple PII types."

### 3.3 — Adversarial Tests

**Thao tác:** Click tab **"🛡️ Adversarial Tests"**

> "Em test 20 adversarial attacks gồm 5 loại: DAN jailbreak, roleplay, split injection, encoding, và indirect. Block rate đạt 55% — DAN attacks bị chặn hiệu quả nhất."

### 3.4 — Latency

**Thao tác:** Click tab **"⏱️ Latency Benchmark"**

> "Latency benchmark: Input guards P95 khoảng 3.8s, RAG pipeline P95 khoảng 19s (bao gồm API call), Llama Guard P95 chỉ 45ms."

---

## PHẦN 4: Phase D — Blueprint (~1 phút)

**Thao tác:** Click vào **"📐 Phase D — Blueprint"** trong sidebar.

**Nói:**
> "Phase D: em thiết kế production blueprint gồm:"
>
> "1. SLO Definition — 8 metrics với target và alert threshold. Ví dụ Faithfulness target ≥ 0.85, alert khi < 0.80 trong 30 phút."
>
> "2. Architecture diagram — 4 layers: Input Guards, RAG Pipeline, Output Guard, Audit Log."
>
> "3. Alert playbook — 4 incident types với response steps cụ thể."
>
> "4. Cost analysis — khoảng $46/tháng ở mức hiện tại, scale 10x lên khoảng $480/tháng."

---

## PHẦN 5: Kết luận (~30 giây)

**Thao tác:** Quay lại trang **Tổng quan**.

**Nói:**
> "Tóm lại, Lab 24 em đã xây dựng được:
> - Phase A: RAGAS evaluation với 50 test questions và failure analysis
> - Phase B: LLM-as-Judge với swap-and-average bias mitigation, Cohen's Kappa 0.65
> - Phase C: Guardrails defense-in-depth với PII redaction, topic validation, adversarial defense
> - Phase D: Production blueprint với SLOs, alert playbook, và cost analysis
>
> 3 bài học chính: Đánh giá trước khi guard, bias là systematic cần mitigation, và layer defenses vì không có guardrail nào hoàn hảo.
>
> Cảm ơn thầy/cô đã xem. Em là Lê Hồng Anh, MSSV 2A202600096."

---

## ✅ Checklist trước khi quay

- [ ] Streamlit app chạy OK (`streamlit run streamlit_demo.py`)
- [ ] Tất cả 4 phase hiển thị đúng data
- [ ] PII live demo hoạt động
- [ ] Mic hoạt động, âm thanh rõ
- [ ] Cửa sổ full screen, font đủ lớn
- [ ] Video 5-7 phút (không quá dài)
