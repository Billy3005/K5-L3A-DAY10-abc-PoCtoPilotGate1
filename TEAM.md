# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `abc`
- Lớp: `L3A`
- Repo của bàn: [K5-L3A-DAY10-abc-PoCtoPilotGate1](https://github.com/Billy3005/K5-L3A-DAY10-abc-PoCtoPilotGate1)
- Thẻ sự cố đã bốc (S1–S8): `S2`
- Bản chung từ Lab 9 (eval card + PRD v1.1, `docs/lab9/`): bản của Nguyễn Vũ Thành Long (2A202603635)

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Nguyễn Gia Bảo | 2A202603647 | Kỹ sư cổng | Có |
|   2 | Nguyễn Vũ Thành Long | 2A202603635 | Sản phẩm và kinh doanh | |
|   3 | Nguyễn Lê Hải Nam | 2A202603699 | Vận hành và pháp lý | |


Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## NguyenGiaBao-2A202603647

### Phần việc phụ trách

Trưởng nhóm kiêm Kỹ sư cổng: đọc trace, viết và sửa cổng, thêm monitor, chạy các lệnh đo và kiểm tra. Mọi lần đo chính thức của bàn (`eval`, `gate`, `checkpoint`, `grade`, `check_submission`) chạy trên máy này để `runs/journal.jsonl` liền mạch.

- File phụ trách: `lab10/guards.py`, `lab10/monitors.py`.
- Phiếu A: câu 1.3 (offline metric), mục A5 (ký).
- Phiếu B: B0–B2, B7.1–B7.3 (đo baseline, soát lỗi `T-002@55`, cổng phòng ngừa, behavioral test), phần bằng chứng B8.
- Phiếu C: C0, C1, C2, C7, C8 và bản đầu C4–C6, C9 (cả bàn duyệt).

### Đóng góp cụ thể

- Cài đặt repo: remote `upstream`, danh tính Git theo MSSV; phát hiện và sửa lỗi CRLF trên Windows (`core.autocrlf=false`) trước khi ký, để hash tiêu chí và bản chốt khớp trên máy team chấm.
- Câu 1.3: offline metric "tỉ lệ dòng lỗi hãng ghi oan" cho bước `file_carrier_fault`.
- Chạy lệnh ký sau khi cả bàn đồng ý bản cuối (`bad7344`), rồi mới chạy lần đánh giá đầu tiên.
- Vòng 1: 3 cổng G1 (tiền theo tracking DB, ghim chính sách hiệu lực, chặn hoàn trùng), G2 (lỗi hãng có căn cứ, đúng kiện), G3 (quyền của con người: payer, phê duyệt, trần khách/ngày, trần lỗi hãng/ngày); chốt vòng 1 `1695c190`.
- Vòng 2 (thẻ S2): chạy `grade` trước khi sửa; gộp G1+G3 thành một luồng (vá lỗ `modify` bỏ qua G3), hoàn giao trễ luôn `payer=LOGIX`, thêm G3e (`auto_limit_vnd`); 2 monitor `merchant_payer_proposal_rate`, `max_auto_refunds_per_customer_day`; gộp phần của Nam (G4, monitor `unauthorised_merchant_debit_vnd`) lên main mà không đưa lần chốt thứ hai vào lịch sử.
- Điều phối review độc lập với Codex sau mỗi mốc CP1–CP5 và sửa theo các kết luận "duyệt có điều kiện".

Sử dụng AI:
- **Claude Code**: đọc và tóm tắt tài liệu lab; cài `upstream`, danh tính Git, sửa CRLF; soạn câu 1.3; đọc `lab10/agent.py`, viết cổng và monitor; chạy các lệnh đo; soạn nội dung phần Kỹ sư cổng ở Phiếu B, C; gộp phần của Long, Nam lên main; soạn nháp mục cá nhân này (kể cả exit ticket) từ quá trình làm, Bảo đọc lại và xác nhận trước khi nộp.
- **Codex**: điền thông tin nhóm ban đầu trong `TEAM.md`; reviewer độc lập (chỉ đọc) sau mỗi mốc, đối chiếu `RUBRIC.md`, `RULES.md`.
- Ngưỡng, con số trong config và quyết định v1/v2 do bàn tự chọn và thống nhất (RULES.md).

### Bằng chứng

- Commit: `bad7344` (ký tiêu chí) · `9e36680` (cổng vòng 1) · `1afe9ee` (chốt vòng 1, `1695c190`) · `55a5501`, `955d339` (vòng 2) · `3b56740` (gộp phần của Nam).
- Lần chạy (`runs/journal.jsonl`): base `R-base-before-20261118-161138-1eb146` · after vòng 1 `R-base-after-20261118-162743-c78bed` · prepared `R-base-prepared-20261118-164600-8b6380` · S2 trước sửa `R-S2-grade-20261118-170237-8b6380` · S2 cuối `R-S2-grade-20261118-174138-f83220` (PASS-VISIBLE) · bộ nền cuối `R-base-after-20261118-174137-f83220`.
- Phiếu A mục A2 (cột Offline), A5 · Phiếu B mục B0–B2, B7.1–B7.3, B8 · Phiếu C mục C0–C2, C4–C9.

### Exit ticket

Một điều học được: cổng an toàn cũng có chi phí. Cổng vòng 1 chặn hết thiệt hại của S2 nhưng bằng cách chuyển người, làm kho HCM đắt hơn làm tay; tính lại khoản ghi từ nguồn sự thật (DB, chính sách, bảng phê duyệt) vừa chặt hơn vừa rẻ hơn. Một điều còn chưa chắc: cổng dựa hoàn toàn vào tracking DB và bảng `approvals`; nếu chính các bảng đó sai, hoặc bài kiểm tra ẩn có kiểu chỉ dẫn tác động lên bước khác (câu trả lời khách), cổng không thấy.

## NguyenVuThanhLong-2A202603635

### Phần việc phụ trách

Sản phẩm và kinh doanh: mục tiêu, tiêu chí chấp nhận, số liệu kinh doanh và dự thảo quyết định Gate 1.

- Phiếu A: phụ trách chính; phối hợp với Kỹ sư cổng và Vận hành và pháp lý ở các câu liên quan.
- File phụ trách: `config/acceptance_criteria.json` (điền trước khi ký, giữ nguyên sau khi ký); mục `business` trong `config/operating_gates.json`.
- Phiếu B và C: phần kinh doanh, dự thảo quyết định v1/v2 dựa trên bằng chứng để cả nhóm cùng chốt.

### Đóng góp cụ thể

Trong CP4, rà soát số liệu kinh doanh của thẻ S2; ghi C1 và C3.1; thử phạm vi pilot hẹp hơn để so sánh; sau khi code vòng 2 cải thiện chi phí HCM, cập nhật dự thảo C12 về tiếp tục pilot ở phạm vi `all`. Ở CP5, đối chiếu lại quyết định v2 với tiêu chí đã ký và mã grade chính thức, cập nhật bằng chứng run. Dùng Codex hỗ trợ đọc trace/report và soạn nội dung; đã đối chiếu số liệu với Phiếu C và report `lab10.grade` trước khi ghi.

### Bằng chứng

Run chính thức được Phiếu C dẫn (C11, C12): `R-S2-grade-20261118-174138-f83220`; trước đó `R-S2-grade-20261118-173544-641434` (PASS-VISIBLE; integrity, criteria, visible, regression và 6 kiểm tra monitor đạt; test ẩn chưa chạy). Phạm vi thử hẹp: `R-S2-grade-20261118-170947-ab3a59` (chạy trên máy cá nhân của Long, không nằm trong `runs/journal.jsonl` của bàn; chỉ để tham khảo; sau sửa đã chọn lại `all`). Mục Phiếu C phụ trách: C0, C1, C3.1, C12; config: `business.pilot_scope=all`. Đối chiếu tại `templates/form-c-incident.md` và quyết định v2 khớp nhánh “Tiếp tục” trong `decision_rule` đã ký.

### Exit ticket

Một điều học được: quyết định “Tiếp tục” phải dựa đồng thời trên bộ nền, thẻ sự cố và các ngưỡng đã ký; pass_rate tốt chưa đủ nếu chi phí hoặc hàng chờ còn vượt trần. Một điều còn chưa chắc: test ẩn và dữ liệu pilot thật có thể bộc lộ cách injection mới hoặc chi phí đối soát khác mock, nên cần theo dõi trước khi mở rộng.

## NguyenLeHaiNam-2A202603699

### Phần việc phụ trách

Vai **Vận hành và pháp lý**. Câu 1.2 và 1.4 (Phiếu A mục A1–A2); câu 2.4 HAZOP vòng 1 và checklist 9 nhóm việc (Phiếu B mục B4–B5); câu 2.10 cổng người/vận hành/pháp lý, runbook 1–3 và giờ cao điểm (Phiếu B mục B7.5–B7.6); mục `operations` và `legal` trong `config/operating_gates.json`; `submission/submission.json`; gom bài nộp. Vòng 2 (khi có thẻ): mục C3 phần riêng theo thẻ, C11 checklist và runbook 4–5, ba dòng bắt buộc ở C12.

### Đóng góp cụ thể

- Viết mục tiêu nhìn từ chị Oanh (sổ cái khớp 100% với hãng/shop, mọi khoản truy được về đơn/kiện, có nguyên nhân tracking và phê duyệt còn hiệu lực) và chị Hạnh (ca chuyển sang trong 60 phút, có ghi chú giải thích, hàng chờ không vượt 6 ca/giờ, chị giữ quyền đứng tên duyệt).
- Thiết kế telemetry production 3 ô cho ba lệnh ghi ra ngoài (hoàn tiền, ghi lỗi hãng, báo hãng), kèm cửa sổ 15 phút, ngưỡng vàng/đỏ và điểm mù.
- HAZOP `issue_refund`: 5 dòng kỹ thuật (WRONG số ngày khách khai; INVALID phê duyệt A-0031 hết hạn; INCOMPLETE kiện trễ; PERTURBED `payer=MERCHANT` do ghi chú đặt hàng; INCAPABLE `fail_open` khi LLM 429) và 4 dòng ngoài kỹ thuật (người duyệt, ngân sách, dữ liệu gửi bên thứ ba, phạm vi pilot).
- Đặt cổng `operations`: PIC `NV-TUNG`, người duyệt `NV-HANH`, 1 người trực, 6 ca/giờ, chờ tối đa 60 phút, 5 điều kiện dừng, kiểm mẫu 10%, bật ghi chú giải thích; cổng `legal`: chặn 2 trường dữ liệu cá nhân gửi hãng, chỉ ghi lỗi hãng khi tracking có nguyên nhân.
- Viết runbook 1–3 và mục giờ cao điểm; điền checklist 9 nhóm việc với PIC có tên từng dòng; điền `submission/submission.json`.

### Bằng chứng

- `config/operating_gates.json` → `operations`, `legal`.
- `templates/form-a-criteria.md` → A1 (câu 1.2), A2 cột telemetry (câu 1.4).
- `templates/form-b-evaluation-gates.md` → B4, B5, B7.5, B7.6.
- `submission/submission.json`.
- Vòng 2 (thẻ S2): `templates/form-c-incident.md` → C0 (nhật ký), C1 (mốc prepared), C3.1 (mức kiểm soát của con người), C10 (risk register), C11 (checklist + runbook 4–5), C12 (quyết định v2 + ba dòng bắt buộc).
- Mã lần chạy vòng 2 (chính thức, `runs/journal.jsonl` của bàn): tự kiểm tra cuối `R-S2-grade-20261118-174138-f83220` (1 integrity ✅, 3 visible ✅, 5 regression ✅, 6 monitor ✅). Các lần chạy …3c261f, …88a387 chạy trên máy cá nhân của Nam (nhánh `NguyenNam1`, `NguyenNam2`), chỉ để tham khảo.
- Phần của Nam được gộp lên main ở commit `b978a2b` (Phiếu B) và `3b56740` (G4, monitor `unauthorised_merchant_debit_vnd`, Phiếu C).
- `submission/submission.json` đã điền `incident: S2`, quyết định v1/v2 và ba dòng bắt buộc (chép từ Phiếu C mục C12); lệnh gom bài chính thức chạy trên máy chạy đo của bàn.

### Exit ticket

Một điều học được: cổng phải so với nguồn sự thật (tracking, bảng phê duyệt), không so với lời khách; cổng pháp lý bảo vệ người nhận quà — người không có kênh nào để đồng ý. Một điều còn chưa chắc: 1 người trực có đủ cho 14 ca/giờ của ngày sale không; cần số thật từ pilot mới biết có phải xếp 2 người cố định.
