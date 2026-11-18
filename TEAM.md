# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `abc`
- Lớp: `L3A`
- Repo của bàn: [K5-L3A-DAY10-abc-PoCtoPilotGate1](https://github.com/Billy3005/K5-L3A-DAY10-abc-PoCtoPilotGate1)
- Thẻ sự cố đã bốc (S1–S8):

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

## NguyenLeHaiNam-2A202603699

### Phần việc phụ trách

Vai **Vận hành và pháp lý**. Câu 1.2 và 1.4 (Phiếu A mục A1–A2); câu 2.4 HAZOP vòng 1 và checklist 9 nhóm việc (Phiếu B mục B4–B5); câu 2.10 cổng người/vận hành/pháp lý, runbook 1–3 và giờ cao điểm (Phiếu B mục B7.5–B7.6); mục `operations` và `legal` trong `config/operating_gates.json`; `submission/submission.json`; gom bài nộp. Vòng 2 (khi có thẻ): mục C3 phần riêng theo thẻ, C11 checklist và runbook 4–5, ba dòng bắt buộc ở C12.
## NguyenGiaBao-2A202603647

### Phần việc phụ trách

Trưởng nhóm kiêm Kỹ sư cổng: đọc trace, viết và sửa cổng, thêm monitor, chạy các lệnh đo và kiểm tra.

- File phụ trách: `lab10/guards.py`, `lab10/monitors.py`.
- Phiếu B: phần kỹ thuật (đo baseline, soát lỗi, cổng phòng ngừa, behavioral test và kiểm tra regression).
- Phiếu C: phần sửa cổng, monitor và kiểm tra kết quả ba mốc.
- Phối hợp thiết kế offline metric ở Phiếu A và cung cấp bằng chứng cho quyết định v1/v2.

### Đóng góp cụ thể

- Viết mục tiêu nhìn từ chị Oanh (sổ cái khớp 100% với hãng/shop, mọi khoản truy được về đơn/kiện, có nguyên nhân tracking và phê duyệt còn hiệu lực) và chị Hạnh (ca chuyển sang trong 60 phút, có ghi chú giải thích, hàng chờ không vượt 6 ca/giờ, chị giữ quyền đứng tên duyệt).
- Thiết kế telemetry production 3 ô cho ba lệnh ghi ra ngoài (hoàn tiền, ghi lỗi hãng, báo hãng), kèm cửa sổ 15 phút, ngưỡng vàng/đỏ và điểm mù.
- HAZOP `issue_refund`: 5 dòng kỹ thuật (WRONG số ngày khách khai; INVALID phê duyệt A-0031 hết hạn; INCOMPLETE kiện trễ; PERTURBED `payer=MERCHANT` do ghi chú đặt hàng; INCAPABLE `fail_open` khi LLM 429) và 4 dòng ngoài kỹ thuật (người duyệt, ngân sách, dữ liệu gửi bên thứ ba, phạm vi pilot).
- Đặt cổng `operations`: PIC `NV-TUNG`, người duyệt `NV-HANH`, 1 người trực, 6 ca/giờ, chờ tối đa 60 phút, 5 điều kiện dừng, kiểm mẫu 10%, bật ghi chú giải thích; cổng `legal`: chặn 2 trường dữ liệu cá nhân gửi hãng, chỉ ghi lỗi hãng khi tracking có nguyên nhân.
- Viết runbook 1–3 và mục giờ cao điểm; điền checklist 9 nhóm việc với PIC có tên từng dòng; điền `submission/submission.json`.

Sử dụng AI: đã dùng Codex hỗ trợ điền thông tin nhóm, thành viên và phân công trong `TEAM.md`.

### Bằng chứng

- `config/operating_gates.json` → `operations`, `legal`.
- `templates/form-a-criteria.md` → A1 (câu 1.2), A2 cột telemetry (câu 1.4).
- `templates/form-b-evaluation-gates.md` → B4, B5, B7.5, B7.6.
- `submission/submission.json`.
- Vòng 2 (thẻ S2): `templates/form-c-incident.md` → C0 (nhật ký), C1 (mốc prepared), C3.1 (mức kiểm soát của con người), C10 (risk register), C11 (checklist + runbook 4–5), C12 (quyết định v2 + ba dòng bắt buộc).
- Mã lần chạy vòng 2: base `R-S2-before-20261118-171517-3c261f` · prepared `R-S2-prepared-20261118-171517-3c261f` · after `R-S2-after-20261118-170604-3c261f` · tự kiểm tra `R-S2-grade-20261118-171517-3c261f` (1 integrity ✅, 3 visible ✅, 5 regression ✅, 6 monitor ✅).
- `submission/submission.json` đã điền `incident: S2`, quyết định v1/v2 và ba dòng bắt buộc; `check_submission --collect` báo `ĐỦ THÀNH PHẦN`.

### Exit ticket

Một điều học được: cổng phải so với nguồn sự thật (tracking, bảng phê duyệt), không so với lời khách; cổng pháp lý bảo vệ người nhận quà — người không có kênh nào để đồng ý. Một điều còn chưa chắc: 1 người trực có đủ cho 14 ca/giờ của ngày sale không; cần số thật từ pilot mới biết có phải xếp 2 người cố định.

Một điều học được, một điều còn chưa chắc.

## NguyenVuThanhLong-2A202603635

### Phần việc phụ trách

Sản phẩm và kinh doanh: mục tiêu, tiêu chí chấp nhận, số liệu kinh doanh và dự thảo quyết định Gate 1.

- Phiếu A: phụ trách chính; phối hợp với Kỹ sư cổng và Vận hành và pháp lý ở các câu liên quan.
- File phụ trách: `config/acceptance_criteria.json` (điền trước khi ký, giữ nguyên sau khi ký); mục `business` trong `config/operating_gates.json`.
- Phiếu B và C: phần kinh doanh, dự thảo quyết định v1/v2 dựa trên bằng chứng để cả nhóm cùng chốt.

### Đóng góp cụ thể

Thành viên tự bổ sung đóng góp và việc sử dụng AI (nếu có).

### Bằng chứng

Thành viên tự bổ sung mã commit, mã lần chạy và mục phiếu liên quan.

### Exit ticket

Thành viên tự ghi một điều học được, một điều còn chưa chắc.

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
- Mã lần chạy vòng 2: base `R-S2-before-20261118-171517-3c261f` · prepared `R-S2-prepared-20261118-171517-3c261f` · after `R-S2-after-20261118-170604-3c261f` · tự kiểm tra `R-S2-grade-20261118-171517-3c261f` (1 integrity ✅, 3 visible ✅, 5 regression ✅, 6 monitor ✅).
- `submission/submission.json` đã điền `incident: S2`, quyết định v1/v2 và ba dòng bắt buộc; `check_submission --collect` báo `ĐỦ THÀNH PHẦN`.

### Exit ticket

Một điều học được: cổng phải so với nguồn sự thật (tracking, bảng phê duyệt), không so với lời khách; cổng pháp lý bảo vệ người nhận quà — người không có kênh nào để đồng ý. Một điều còn chưa chắc: 1 người trực có đủ cho 14 ca/giờ của ngày sale không; cần số thật từ pilot mới biết có phải xếp 2 người cố định.

