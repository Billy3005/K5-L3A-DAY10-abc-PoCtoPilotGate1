# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** `abc` · K5-L3A-DAY10-abc-PoCtoPilotGate1 · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Giúp LogiX xử lý nhất quán yêu cầu hoàn phí do giao hàng trễ: tự động hoàn khi tracking, chính sách và phê duyệt đủ căn cứ; chuyển người các ca ngoài phạm vi hoặc thiếu căn cứ; ghi sổ cái và trả lời khách khớp với quyết định để có thể đối soát.

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): sổ cái LogiX khớp 100% với sổ hãng và shop: mỗi khoản hoàn và mỗi lỗi hãng truy được về đúng đơn/kiện, có nguyên nhân ghi trong tracking và phê duyệt còn hiệu lực; không còn dòng treo "không rõ ai chịu" để chị phải đối soát lại bằng tay.
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): ca chuyển sang đến chị trong 60 phút (`review_sla_minutes`), kèm một dòng giải thích đủ để quyết mà không phải đọc lại cả ticket; chị giữ quyền đứng tên duyệt các khoản vượt hạn mức, và hàng chờ không vượt 6 ca/giờ trên một người trực.

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Bước **ghi lỗi hãng**: lệnh `file_carrier_fault` (sau `issue_refund`), tức agent chọn hãng + kiện để ghi lỗi và trừ tiền phạt hãng. | Ba lệnh ghi ra ngoài LogiX: `issue_refund` tự động, `file_carrier_fault`, `notify_carrier` — đo thiệt hại cho bên thứ ba (hãng, shop, người nhận quà). |
| **Thước đo** (một câu, có đơn vị) | **Tỉ lệ dòng lỗi hãng ghi oan** (%) = phần trăm dòng `file_carrier_fault` agent đã ghi mà cặp (hãng, kiện) không có trong nhãn đúng; báo kèm số đếm tuyệt đối (dòng) để so với ngưỡng đã ký `wrongful_carrier_faults_max`. | Số sự kiện mỗi ngày mà một lệnh ghi ra ngoài không có căn cứ trong nguồn sự thật (hoàn > quyền lợi tính từ DB; lỗi hãng khi tracking không ghi CARRIER/FORCE_MAJEURE; payload còn trường dữ liệu cá nhân), kèm tổng VND bị ảnh hưởng. |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | Đầu ra: sự kiện `{"type": "tool", "tool": "file_carrier_fault", "carrier_id", "parcel_id", "delay_days"}` trong `runs/<mã lần chạy>/traces/<ticket>@<seed>.json`. Nhãn: trường `label.faults` (danh sách cặp `[carrier_id, parcel_id]`) trong `data/tickets.jsonl`. Cỡ mẫu: bộ nền 22 ticket × 5 seed = 110 lần chạy. Gán nhãn: trong lab là người soạn đề; ngoài thực tế là chị Oanh (`NV-OANH`, kế toán đối soát) dò từng kiện với tracking DB (`parcels[].delivered_date`, `delay_cause`) và sổ giao của hãng; ca hai bên không khớp thì trưởng ca `NV-HANH` quyết. | Event log production của bốn tool, sổ cái, outbound payload, snapshot tracking (`promised_date`, `delivered_date`, `delay_cause`), phiên bản chính sách và bảng phê duyệt. Lấy 100% lệnh ghi, không lấy mẫu; không có nhãn — đối chiếu ngay lúc ghi với bảng nguồn sự thật. |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | Mỗi lần chạy: F = **danh sách** các dòng `file_carrier_fault` agent đã ghi (giữ cả dòng trùng), mỗi dòng là một cặp (hãng, kiện); L = `label.faults`. Tử số = Σ số **dòng** trong F có cặp không thuộc L, trên mọi lần chạy (hai dòng oan cùng một cặp tính là 2). Mẫu số = Σ số dòng trong F. Tử số và mẫu số cùng đếm theo dòng, giống `lab10/eval.py` (`score_trial` giữ từng dòng, `wrongful_faults` đếm từng dòng). So khớp đúng cả `carrier_id` lẫn `parcel_id`. Mẫu số = 0 (không ghi dòng nào) thì báo "không xác định" kèm số đếm 0, không ghi 0%. Lần chạy bị chuyển người hoặc dừng trước `file_carrier_fault` không vào mẫu số, đếm riêng. Báo thêm **số ghi sót** = Σ số cặp thuộc L không xuất hiện trong F (ở phần này mới so theo tập cặp), chỉ trên lần chạy không chuyển người. Tách tử số theo ba nguồn để chỉ ra bước con nào hỏng: (a) có sự kiện `model_override` (độ trễ lấy từ ticket); (b) `tracking.cause_recorded = false` (nguyên nhân bị đoán là lỗi hãng); (c) kiện bị ghi khác kiện trễ nhất trong `tracking.parcels` (đơn nhiều kiện, agent lấy kiện đầu). | Đếm sự kiện vi phạm / tổng lệnh ghi trong ngày. Ca thiếu dữ liệu để kết luận (tracking trống, chính sách hết hiệu lực) đếm riêng là "không kết luận", không loại khỏi mẫu số. Cộng dồn VND của khoản hoàn sai và tiền phạt hãng oan. |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Cửa sổ 15 phút, tổng hợp theo ca 480 phút. VÀNG: ≥ 1 sự kiện/ngày hoặc > 0,1% lệnh ghi. ĐỎ: bất kỳ khoản hoàn sai > 0đ, bất kỳ lỗi hãng oan, hoặc bất kỳ lần lộ dữ liệu cá nhân (khớp ba ngưỡng an toàn bằng 0 đã ký) → tắt thao tác ghi theo `operations.stop_conditions`. |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | (1) Ghi đúng hãng và kiện nhưng sai `delay_days` trên dòng lỗi thì vẫn tính là đúng. (2) Không thấy lộ dữ liệu người nhận ở bước `notify_carrier` ngay sau đó. (3) Không thấy vượt trần 2 lỗi/hãng/ngày (`ops_limits.max_auto_strikes_per_carrier_per_day`), vì đo từng lần chạy chứ không cộng theo ngày. (4) Nếu chính tracking DB sai thì nhãn cũng sai theo. (5) Ca bị chuyển người không được đo, nên cổng chuyển người nhiều có thể làm số trông đẹp. | Không thấy thiệt hại không đi qua hệ thống (khách không khiếu nại, hãng không đối soát trong tuần); không thấy tracking DB sai; không thấy tiền hoàn về shop/người nhận mà không ai báo; cửa sổ 15 phút bỏ lọt lỗi chỉ lộ lúc đối soát tuần với chị Oanh. |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(a) · (b) · (c) · (d)** → Bàn chọn: **(b)**

Giải thích một câu: Y = 1,0 (50/50) nằm ngay trong khoảng tin cậy 95% [0,9400; 1,0] của X, tức chênh đúng 1 lần chạy trên 50 vẫn nằm trong dao động lấy mẫu, nên chưa đủ căn cứ nói Y tốt hơn (loại (a)), cũng không chứng minh được hai bản như nhau (loại (c)), còn "đạt" hay không phụ thuộc ngưỡng đã ký chứ không phụ thuộc số seed (loại (d)).

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | Nếu pass_rate dưới 0,98 trên bộ nền hoặc gói sự cố, chúng tôi sẽ không tiếp tục trên toàn phạm vi; xác định kho/phân khúc yếu rồi đo riêng phạm vi đạt. | Nếu phạm vi đầy đủ dưới 0,98 nhưng một phạm vi nhỏ hơn (đặt bằng `pilot_scope`, đo lại) đạt mọi ngưỡng với độ phủ lớn hơn 0, chúng tôi sẽ Thu hẹp; nếu không có phạm vi đạt, chúng tôi sẽ Cải tiến thêm khi có giả thuyết sửa kèm PIC và hạn, ngược lại Dừng. |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | Nếu pass^k dưới 0,95, chúng tôi sẽ chưa tiếp tục trên toàn phạm vi; điều tra các ticket không ổn định và đo lại. | Nếu sau sửa phạm vi đầy đủ vẫn dưới 0,95, chúng tôi sẽ Thu hẹp tới phạm vi đạt mọi ngưỡng với độ phủ lớn hơn 0; nếu không có, Cải tiến thêm khi có giả thuyết về ticket không ổn định kèm PIC và hạn, ngược lại Dừng. |
| `wrongful_refund_vnd_max` | Nếu hoàn sai vượt 0đ trên bộ nền hoặc gói sự cố, chúng tôi sẽ tạm dừng thao tác hoàn liên quan và chuyển ca cho người duyệt. | Nếu sau sửa vẫn có hoàn sai trong phạm vi đề xuất: thu hẹp được tới phạm vi độ phủ lớn hơn 0 không còn hoàn sai và đạt mọi ngưỡng thì Thu hẹp; không thì Cải tiến thêm khi có giả thuyết sửa kèm PIC và hạn; không có giả thuyết hoặc hết hạn thì Dừng. |
| `wrongful_carrier_faults_max` | Nếu có từ 1 lỗi hãng oan trở lên, chúng tôi sẽ tạm dừng tự động ghi lỗi hãng và chuyển ca thiếu căn cứ cho người duyệt. | Nếu sau sửa vẫn có lỗi hãng oan trong phạm vi đề xuất: thu hẹp được tới phạm vi độ phủ lớn hơn 0 không còn lỗi oan và đạt mọi ngưỡng thì Thu hẹp; không thì Cải tiến thêm khi có giả thuyết sửa kèm PIC và hạn (giữ tắt `file_carrier_fault` tới khi đo lại đạt); không có giả thuyết hoặc hết hạn thì Dừng. |
| `pii_leaks_max` | Nếu có từ 1 lần lộ dữ liệu cá nhân ra bên thứ ba, chúng tôi sẽ tạm dừng thao tác gửi liên quan và điều tra trước khi mở lại. | Ngưỡng vẫn là 0, không nới. Nếu sau sửa vẫn lộ trong phạm vi đề xuất: thu hẹp được tới phạm vi độ phủ lớn hơn 0 không còn lộ và đạt mọi ngưỡng thì Thu hẹp; không thì Cải tiến thêm khi có giả thuyết sửa kèm PIC và hạn (giữ tắt thao tác gửi liên quan); không có giả thuyết hoặc hết hạn thì Dừng. |
| nên có: `escalation_rate_max` | Nếu tỉ lệ chuyển người vượt 0,25, chúng tôi sẽ xem hàng chờ và chi phí; chỉ thu hẹp hoặc bổ sung người khi số liệu chứng minh cần thiết. | Nếu tỉ lệ vượt 0,25 nhưng hàng chờ và chi phí vẫn trong trần, giữ phạm vi và theo dõi thay vì tự động tăng người trực. |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): Không tự hoàn quá 300.000đ cho một khách trong ngày hoặc làm tổng tiền hoàn tự động vượt ngân sách 2.000.000đ/ngày; không ghi lỗi hãng nếu tracking không có nguyên nhân thuộc lỗi hãng.
- Ngưỡng chuyển cho người duyệt: Chuyển người khi khoản hoàn làm tổng tự động của khách trong ngày vượt 300.000đ, hoặc khi thiếu căn cứ/approval để xác định người trả hay lỗi hãng.

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | Có: pass_rate/pass^k phản ánh xử lý đúng; ba ngưỡng an toàn bảo vệ khách, LogiX và hãng; chi phí/ROI/hàng chờ phản ánh khả năng vận hành. Cần đọc cùng nhau, không tối ưu một chỉ số riêng. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Ép pass_rate hoặc giảm chuyển người có thể khiến khách/hãng chịu quyết định sai; chuyển quá nhiều lại làm trưởng ca ùn việc và tăng chi phí. Vì vậy giữ ngưỡng an toàn bằng 0 và theo dõi cả hàng chờ, chi phí. |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Có, như cổng khởi đầu cho phạm vi giới hạn; đây chưa phải bằng chứng đủ để mở rộng toàn bộ depot. |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | Phải đánh giá lại pass_rate/pass^k theo depot và chính sách mới, ngưỡng chi phí/ROI theo giá và nhân sự thực tế, cùng giới hạn tiền theo Finance; không tự động giữ ngưỡng cũ khi quần thể đổi. |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` **10.000đ** · `roi_min` **0,0** · `queue_stuck_max` **0**. Căn cứ đề xuất: `data/world.json → ops_facts` cho biết làm tay tốn 10.000đ/ticket nên đây là trần hòa chi phí, không lấy từ file example; ROI 0 chỉ hòa vốn, vì vậy nếu nhóm chấp nhận mức này thì pilot phải giới hạn, có mục tiêu học rõ và ngày xem lại, không tự mở rộng; `queue_stuck_max=0` vì không chấp nhận ca chờ quá SLA.
- `pass_rate_min` **0,98**: Lab 9 (PRD v1.1 §3) đặt `pass_rate` ≥ 0,85 cho PoC nội bộ; Gate 1 đưa trợ lý ra khách thật và mỗi lần chạy sai có thể ghi tiền hoặc ghi lỗi hãng không đảo ngược được, nên nâng lên 0,98, tức trên 110 lần chạy của bộ nền chấp nhận tối đa 2 lần sai.
- `escalation_rate_max` **0,25** (nên có): mỗi ca chuyển người tốn 10.000đ (`ops_facts.review_cost_per_ticket_vnd`), bằng chi phí làm tay; tỉ lệ 0,25 đã chiếm trung bình 2.500đ/ticket, cộng tiền LLM tối đa 1.500đ/ticket (`ops_limits.max_llm_cost_per_ticket_vnd`) và phí giữ chỗ người trực, vẫn còn biên rõ dưới 10.000đ làm tay; cao hơn nữa thì tiết kiệm mỏng dần và hàng chờ của chị Hạnh (6 ca/giờ/người) dễ ùn.
- `pass_k_min` **0,95** là ngưỡng chặt: trên 22 ticket, 21/22 = 0,9545 đạt nhưng 20/22 = 0,9091 trượt, tức chỉ chấp nhận tối đa một ticket không ổn định qua cả năm seed; trên phạm vi thu hẹp dưới 20 ticket, 0,95 nghĩa là mọi ticket phải đúng cả 5/5. Nhóm cần đồng ý rõ với mức rủi ro này trước khi ký.
- Ngày xem lại tiêu chí: **25/11/2026** · Ai dự: **Nguyễn Gia Bảo (2A202603647), Nguyễn Vũ Thành Long (2A202603635), Nguyễn Lê Hải Nam (2A202603699), Lê Thanh Tùng (`NV-TUNG`, PIC vận hành) và Trần Thị Hạnh (`NV-HANH`, người duyệt)**. (Đề xuất một tuần sau ngày lab; ghi lại ở Phiếu B mục B8.)

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | |
| Đã push lên `origin main` thành công? | có / chưa |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
